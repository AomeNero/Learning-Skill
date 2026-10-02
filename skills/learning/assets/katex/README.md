# KaTeX 资产

版本 **0.16.22**（来源 jsdelivr `katex@0.16.22/dist`，2026-10 落位）。

| 文件 | 说明 |
|------|------|
| `katex.embed.css` | 官方 katex.min.css + 20 个 woff2 字体全部 base64 内嵌（359KB）——单文件无字体路径依赖 |
| `katex.min.js` | 渲染引擎（277KB） |
| `auto-render.min.js` | `$…$` / `$$…$$` 自动扫描渲染（3.5KB） |

用法见 template.html / question-template.html 的外链块：公式课程用 Bash 把三件**复制**到工作区 `lessons/src/katex/`（整个工作区一份，勿读入上下文）。

**升级/重建**：下载新版 dist 的 katex.min.css 与两个 js；再下载全部 woff2（CSS 内 `url(fonts/KaTeX_*.woff2)` 引用的 20 个），把每个 @font-face 的 `src` 整段替换为 `url(data:font/woff2;base64,…) format("woff2")`。升级后跑一次 check-lesson.py 冒烟。
