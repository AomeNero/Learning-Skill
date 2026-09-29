# -*- coding: utf-8 -*-
"""扫描 overview.html + 所有本地 CSS 的资源引用，缺失的从源 URL 补下载，然后统一改写"""
import re, os, urllib.request
from urllib.parse import urlparse, urljoin

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
MIRRORS = {'https://d4tuoctqmanu0.cloudfront.net/': 'https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/'}
BASE = 'https://code.claude.com'

def to_local(u):
    p = urlparse(u)
    return os.path.join('overview_assets', p.netloc, p.path.lstrip('/')).replace('\\', '/')

def norm(u):
    return BASE + u if u.startswith('/') else u

def fetch(url):
    real = url
    for k, v in MIRRORS.items():
        if url.startswith(k):
            real = v + url[len(k):]
            break
    req = urllib.request.Request(real, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

# 1. 收集所有引用
refs = set()
h = open('overview.html', encoding='utf-8').read()
refs.update(u for u in re.findall(r'(?:href|src|poster)="([^"]+)"', h))
for m in re.finditer(r'srcset="([^"]+)"', h):
    for part in m.group(1).split(','):
        seg = part.strip().split()
        if seg:
            refs.add(seg[0])
for root, _, files in os.walk('overview_assets'):
    for f in files:
        if f.endswith('.css'):
            c = open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
            refs.update(u for u in re.findall(r'url\(\s*(["\']?)([^"\')]+?)\1\s*\)', c) and
                        [m[1] for m in re.findall(r'url\(\s*(["\']?)([^"\')]+?)\1\s*\)', c)])
            refs.update(m[1] for m in re.findall(r'@import\s+(?:url\(\s*(["\']?)([^"\')]+?)\1\s*\)|(["\'])([^"\']+?)\3)', c))

# 过滤：只要 http(s) 绝对 URL
abs_urls = sorted(u for u in refs if u.startswith('http'))
missing = [u for u in abs_urls if not os.path.exists(to_local(u))]
print(f'绝对引用 {len(abs_urls)} 个，本地缺失 {len(missing)} 个')
for u in missing:
    lp = to_local(u)
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    try:
        data = fetch(u)
        open(lp, 'wb').write(data)
        print('  补齐 %6d %s' % (len(data), lp))
    except Exception as e:
        print('  仍失败', str(e)[:60], u[:80])

# 2. 统一改写所有 css 中可本地化的 url
fixed = 0
for root, _, files in os.walk('overview_assets'):
    for f in files:
        if not f.endswith('.css'):
            continue
        fp = os.path.join(root, f)
        c = open(fp, encoding='utf-8', errors='replace').read()

        def rep(m):
            global fixed
            lp = to_local(m.group(2))
            if os.path.exists(lp):
                fixed += 1
                return 'url("%s")' % os.path.relpath(lp, root).replace('\\', '/')
            return m.group(0)

        c2 = re.sub(r'url\(\s*(["\']?)(https?://[^"\')]+?)\1\s*\)', rep, c)
        if c2 != c:
            open(fp, 'w', encoding='utf-8').write(c2)
print('CSS 改写引用数:', fixed)

# 3. 终验
ext = 0
for root, _, files in os.walk('overview_assets'):
    for f in files:
        if f.endswith('.css'):
            c = open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
            for m in re.finditer(r'url\(\s*(["\']?)(https?://[^"\')]+?)\1\s*\)', c):
                if not os.path.exists(to_local(m.group(2))):
                    ext += 1
                    print('  最终残留:', m.group(2)[:80])
print('CSS 最终残留外部 url():', ext)
