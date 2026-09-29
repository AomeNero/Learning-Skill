# -*- coding: utf-8 -*-
"""补漏：删 googleapis 死链，改写 CSS 残留绝对 URL"""
import re, os
from urllib.parse import urlparse

h = open('overview.html', encoding='utf-8').read()
before = len(h)
h = re.sub(r'<link\b[^>]*fonts\.googleapis\.com[^>]*/?>\s*', '', h, flags=re.I)
print('HTML 删除 googleapis 链接字节:', before - len(h))

def to_local(u):
    p = urlparse(u)
    return os.path.join('overview_assets', p.netloc, p.path.lstrip('/'))

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
                rel = os.path.relpath(lp, root).replace('\\', '/')
                return 'url("%s")' % rel
            return m.group(0)

        c2 = re.sub(r'url\(\s*(["\']?)(https?://[^"\')]+?)\1\s*\)', rep, c)
        if c2 != c:
            open(fp, 'w', encoding='utf-8').write(c2)
print('CSS 修复引用数:', fixed)

open('overview.html', 'w', encoding='utf-8').write(h)

# 复验
h = open('overview.html', encoding='utf-8').read()
res = re.findall(r'<(?:link|img|source|video|input)\b[^>]*?(?:href|src|srcset)="(https?://[^"]+)"', h)
print('HTML 剩余外部资源引用:', [r[:70] for r in res])
ext = 0
for root, _, files in os.walk('overview_assets'):
    for f in files:
        if f.endswith('.css'):
            c = open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
            ext += len(re.findall(r'url\(["\']?https?://', c))
print('CSS 剩余外部 url():', ext)
