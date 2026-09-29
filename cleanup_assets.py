# -*- coding: utf-8 -*-
"""清理误下载的导航页面；补齐 LM-italic.woff；重写 CSS；终验"""
import re, os, shutil, time, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
KEEP = {'assets.claude.ai', 'cdn.jsdelivr.net', 'code.claude.com',
        'd4tuoctqmanu0.cloudfront.net', 'fonts.cdnfonts.com',
        'mintcdn.com', 'mintlify.b-cdn.net'}

base = 'overview_assets'
removed = 0
for d in os.listdir(base):
    p = os.path.join(base, d)
    if os.path.isdir(p) and d not in KEEP:
        shutil.rmtree(p)
        removed += 1
    elif os.path.isfile(p):
        os.remove(p)
        removed += 1
print('清理目录/文件数:', removed)

# 修正 code.claude.com 下误抓的整页 HTML（保留 css/woff2/favicon）
cc = os.path.join(base, 'code.claude.com')
bad = []
for root, _, files in os.walk(cc):
    for f in files:
        if f.endswith(('.html', '')) and '.' not in f:
            bad.append(os.path.join(root, f))
for b in bad:
    os.remove(b)
print('code.claude.com 下误抓页面:', len(bad))

# 补齐 LM-italic.woff（jsdelivr 偶发断连，重试 5 次）
lp = os.path.join(base, 'cdn.jsdelivr.net/gh/vincentdoerig/latex-css/fonts/LM-italic.woff')
if not os.path.exists(lp):
    url = 'https://cdn.jsdelivr.net/gh/vincentdoerig/latex-css/fonts/LM-italic.woff'
    for i in range(5):
        try:
            req = urllib.request.Request(url, headers=UA)
            data = urllib.request.urlopen(req, timeout=60).read()
            os.makedirs(os.path.dirname(lp), exist_ok=True)
            open(lp, 'wb').write(data)
            print('补齐 LM-italic.woff:', len(data), 'bytes')
            break
        except Exception as e:
            print('retry', i + 1, str(e)[:50])
            time.sleep(2)

# 重写 CSS 中剩余 url()
from urllib.parse import urlparse
def to_local(u):
    p = urlparse(u)
    return os.path.join(base, p.netloc, p.path.lstrip('/')).replace('\\', '/')

fixed = 0
for root, _, files in os.walk(base):
    for f in files:
        if not f.endswith('.css'):
            continue
        fp = os.path.join(root, f)
        c = open(fp, encoding='utf-8', errors='replace').read()

        def rep(m):
            global fixed
            lp2 = to_local(m.group(2))
            if os.path.exists(lp2):
                fixed += 1
                return 'url("%s")' % os.path.relpath(lp2, root).replace('\\', '/')
            return m.group(0)

        c2 = re.sub(r'url\(\s*(["\']?)(https?://[^"\')]+?)\1\s*\)', rep, c)
        if c2 != c:
            open(fp, 'w', encoding='utf-8').write(c2)
print('CSS 改写引用数:', fixed)

# 终验
ext = []
for root, _, files in os.walk(base):
    for f in files:
        if f.endswith('.css'):
            c = open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
            for m in re.finditer(r'url\(\s*(["\']?)(https?://[^"\')]+?)\1\s*\)', c):
                if not os.path.exists(to_local(m.group(2))):
                    ext.append(m.group(2)[:80])
print('CSS 残留外部 url():', len(ext), ext[:3])
total = sum(len(fs) for _, _, fs in os.walk(base))
print('最终资源文件数:', total)
