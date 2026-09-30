# learn（Claude Code 中文版）

[![video](assets/thumbnail.png)](https://www.youtube.com/watch?v=kzcI5F4tGiU)

一套个人 AI 学习系统，出自视频 [How I Use AI to Learn Things](https://www.youtube.com/watch?v=kzcI5F4tGiU)。原版（[amosblomqvist/learn](https://github.com/amosblomqvist/learn)）是给 [pi](https://github.com/earendil-works/pi) 写的配置；本仓库是面向 **Claude Code** 的中文改造版。

核心理念：**理解 > 记忆**——在脑中构建依赖图（少数核心真理 + 挂在上面的推导事实），而不是堆砌孤立事实。

## 里面有什么

- `skills/learning/` — 教学哲学与流程：探查（判分定位水平边界）→ 规划（依赖图 + 检查点）→ 教学（逐节点：动机 → 确立 → 连接 → 判分检查）
- `skills/visualize/` — 当图确实比字更清楚时，为课程添加一张正确、极简的配图
- `agents/researcher.md` — 网络调研员：事实核实、主题摸底
- `agents/diagram-maker.md` — 配图制作者：渲染后必亲眼看图，保证图不说假话

原版的四个 pi 扩展（quiz / ask-user-question / md-log / visual-tools）按 Claude Code 的内置能力重做：

| 原扩展 | Claude Code 方案 |
|---|---|
| quiz（判分答题） | 内置 `AskUserQuestion` 模拟，协议写在 learning skill 里 |
| ask-user-question（偏好提问） | 直接用内置 `AskUserQuestion` |
| md-log（会话镜像） | 约定式日志：课程同步写入 `log/<主题>.md` |
| visual-tools（图渲染） | 子代理用 `Bash` 跑 mermaid-cli / rsvg-convert + `Read` 看图 |

## 安装

本仓库**就是一个** `.claude` 目录。在你的学习项目根目录：

```bash
git clone <本仓库> .claude
```

然后用 Claude Code 打开该项目——项目级 skills 与 agents 自动加载，直接说"教我 X"即可。

## 依赖

- [Claude Code](https://claude.com/claude-code)
- 配图渲染（可选）：Node.js + `@mermaid-js/mermaid-cli`（Mermaid 图，需本机 Chrome/Edge，puppeteer 找不到浏览器时设 `PUPPETEER_EXECUTABLE_PATH` 指向系统浏览器）、`rsvg-convert` 或 ImageMagick 7（SVG 图，仅类 Unix）。没装也能用：渲染不可用时 maker 返回 `NONE`（附源文件路径），降级为在课程日志里贴 Mermaid/SVG 源码（Obsidian 原生渲染 mermaid 代码块）。

## 说明

- 没有子代理也能跑：主会话直接教学，事实核实降级为自带搜索（researcher 缺席时），只是少了自动配图（两个 maker）
- 课程日志写入 `log/<主题>.md`，配图存放在 `viz/`；用 Obsidian 阅读（LaTeX 与 Mermaid 开箱渲染），或装了对应扩展的 VS Code 预览
