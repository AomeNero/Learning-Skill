# -*- coding: utf-8 -*-
"""把 overview_orig.html 本地化：下载全部外部资源，改写引用，输出离线可用的 overview.html"""
import re, os, html as htmllib, tempfile, subprocess
import urllib.request
from urllib.parse import urljoin, urlparse

SRC   = 'overview_orig.html'
OUT   = 'overview.html'
ASSET = 'overview_assets'
BASE  = 'https://code.claude.com'
UA    = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
         'Accept': '*/*', 'Referer': BASE + '/'}

def norm(url):
    """根相对路径 -> 绝对 URL"""
    return BASE + url if url.startswith('/') else url

# 本网络不可达的 CDN -> 内容相同的镜像（本地路径仍按原 URL 存放）
MIRRORS = {
    'https://d4tuoctqmanu0.cloudfront.net/':
        'https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/',
}

def fetch(url):
    """先走 Python；被 TLS 指纹拦截的 CDN 回退到 PowerShell（schannel 栈）"""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception:
        tmp = tempfile.mktemp()
        cmd = ("powershell -NoProfile -Command \"try{[Net.ServicePointManager]::SecurityProtocol="
               "[Net.SecurityProtocolType]::Tls12;Invoke-WebRequest -Uri '" + url +
               "' -UserAgent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0' "
               "-UseBasicParsing -TimeoutSec 90 -OutFile '" + tmp + "'}catch{exit 1}\"")
        r = subprocess.run(cmd, capture_output=True, timeout=100)
        if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
            data = open(tmp, 'rb').read()
            os.remove(tmp)
            return data
        if os.path.exists(tmp):
            os.remove(tmp)
        raise RuntimeError('both fetchers failed for ' + url[:80])

def local_path(url):
    p = urlparse(url)
    path = p.path
    if path.endswith('/'):
        path += 'index'
    if not path or '.' not in os.path.basename(path):
        path += '/index'
    return os.path.join(ASSET, p.netloc, path.lstrip('/')).replace('\\', '/')

def ext_of(path):
    return os.path.splitext(path)[1].lower()

downloaded = {}

def download(url, depth=0):
    url = norm(url).split('#')[0]
    if not url or url.startswith(('data:', 'blob:', 'mailto:', 'javascript:')):
        return None
    if url in downloaded:
        return downloaded[url]
    lp = local_path(url)
    downloaded[url] = lp
    if os.path.exists(lp):                       # 磁盘缓存：上次已下载，直接复用
        print('  cache %s' % lp)
        return lp
    real = url                                   # 不可达 CDN 换镜像源
    for k, v in MIRRORS.items():
        if url.startswith(k):
            real = v + url[len(k):]
            break
    try:
        data = fetch(real)
    except Exception as e:
        print('  MISS', str(e)[:70])
        return None
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    if ext_of(lp) == '.css' and depth < 5:
        css = data.decode('utf-8', errors='replace')
        css = rewrite_css(css, real, depth)      # 相对引用按真实来源解析
        data = css.encode('utf-8')
    with open(lp, 'wb') as f:
        f.write(data)
    print('  ok %6d %s' % (len(data), lp))
    return lp

CSS_URL = re.compile(r'url\(\s*(["\']?)([^"\')]+?)\1\s*\)')
CSS_IMPORT = re.compile(r'@import\s+(?:url\(\s*(["\']?)([^"\')]+?)\1\s*\)|(["\'])([^"\']+?)\3)')

def relp(lp):
    return os.path.relpath(lp, ASSET).replace('\\', '/')

def rewrite_css(css, base_url, depth):
    def sub_import(m):
        u = (m.group(2) or m.group(4)).strip()
        lp = download(urljoin(base_url, u), depth + 1)
        return f'@import "{relp(lp)}"' if lp else m.group(0)
    css = CSS_IMPORT.sub(sub_import, css)
    def sub_url(m):
        u = m.group(2).strip()
        if u.startswith(('data:', 'blob:')):
            return m.group(0)
        lp = download(urljoin(base_url, u), depth + 1)
        return f'url("{relp(lp)}")' if lp else m.group(0)
    return CSS_URL.sub(sub_url, css)

src = open(SRC, encoding='utf-8').read()
print('== 1. 去掉 script 与脚本预加载 ==')
src = re.sub(r'<script\b[^>]*>.*?</script\s*>', '', src, flags=re.S | re.I)
src = re.sub(r'<script\b[^>]*/>', '', src, flags=re.I)
src = re.sub(r'<link\b[^>]*rel="(?:preload|modulepreload)"[^>]*as="script"[^>]*/?>', '', src, flags=re.I)
src = re.sub(r'<link\b[^>]*rel="(?:preconnect|dns-prefetch)"[^>]*/?>', '', src, flags=re.I)
src = re.sub(r'<link\b[^>]*rel="modulepreload"[^>]*/?>', '', src, flags=re.I)

print('== 2. 收集资源引用 ==')
urls = set()

def add(m):
    u = htmllib.unescape(m.group(1)).strip()
    if u and not u.startswith(('data:', '#', 'mailto:')):
        urls.add(u)
    return m.group(0)

for m in re.finditer(r'<link\b([^>]*)>', src, flags=re.I):
    attrs = m.group(1)
    if re.search(r'rel="[^"]*(stylesheet|preload|icon|apple-touch-icon|manifest)[^"]*"', attrs, re.I):
        href = re.search(r'href="([^"]+)"', attrs)
        if href:
            add(href)
for m in re.finditer(r'<(?:img|source|video|input)\b[^>]*>', src, flags=re.I):
    tag = m.group(0)
    for am in re.finditer(r'(?:src|srcset|poster)="([^"]+)"', tag):
        add(am)
def add_srcset(m):
    for part in m.group(1).split(','):
        seg = part.strip().split()
        u = htmllib.unescape(seg[0]) if seg else ''
        if u and not u.startswith(('data:', '#')):
            urls.add(u)
    return m.group(0)
src = re.sub(r'srcset="([^"]+)"', add_srcset, src, flags=re.I)
style_blocks = []
def collect_style(m):
    style_blocks.append(m)
    return m.group(0)
for m in re.finditer(r'<style\b[^>]*>(.*?)</style\s*>', src, flags=re.S | re.I):
    for um in CSS_URL.finditer(m.group(1)):
        u = htmllib.unescape(um.group(2)).strip()   # HTML 内联样式需反转义
        if not u.startswith(('data:', 'blob:')):
            urls.add(norm(u))

print(f'共 {len(urls)} 个资源待下载')
print('== 3. 下载并改写 ==')
urlmap = {}
for u in sorted(urls):
    lp = download(u)
    if lp:
        rel = os.path.relpath(lp, '.').replace('\\', '/')
        urlmap[u] = rel
        if '&' in u:
            urlmap[u.replace('&', '&amp;')] = rel
        pu = urlparse(norm(u))
        if pu.netloc == 'code.claude.com':
            urlmap[pu.path] = rel
            urlmap[pu.path + (('?' + pu.query) if pu.query else '')] = rel

def sub_href(m):
    raw = m.group(2)
    lp = urlmap.get(raw) or urlmap.get(htmllib.unescape(raw).strip())
    return f'{m.group(1)}="{lp}"' if lp else m.group(0)

src = re.sub(r'(href|src|poster)="([^"]*)"', sub_href, src)
def sub_srcset(m):
    parts = []
    for part in m.group(2).split(','):
        seg = part.strip().split()
        if seg:
            lp = urlmap.get(seg[0]) or urlmap.get(htmllib.unescape(seg[0]))
            if lp:
                seg[0] = lp
        parts.append(' '.join(seg))
    return f'{m.group(1)}="{", ".join(parts)}"'
src = re.sub(r'(srcset)="([^"]*)"', sub_srcset, src)
# 内联 <style> 中的 url() 一并改写
def sub_style(m):
    def rep(um):
        u = htmllib.unescape(um.group(2)).strip()
        lp = urlmap.get(u) or urlmap.get(norm(u))
        return f'url("{os.path.relpath(lp, ".").replace(chr(92), "/")}")' if lp else um.group(0)
    return CSS_URL.sub(rep, m.group(0))
src = re.sub(r'(<style\b[^>]*>)(.*?)(</style\s*>)', lambda m: m.group(1) + sub_style(m) + m.group(3), src, flags=re.S | re.I)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(src)
print(f'== 完成：{len(downloaded)} 个资源已本地化 -> {OUT} ==')
