# learning (一套个人 AI 学习系统)

一套个人 AI 学习系统，本仓库是面向 **Claude Code** 的中文改造版，兼及 WorkBuddy 等遵循 Agent Skills 开放标准的客户端。

核心理念：**理解 > 记忆**——在脑中构建依赖图（少数核心真理 + 挂在上面的推导事实），而不是堆砌孤立事实。

## 里面有什么

- `skills/learning/` — 教学系统主体：探查（批量判分定位水平边界）→ 规划（依赖图，非阻塞展示）→ 教学（逐节点：动机 → 确立 → 连接，连续讲述）→ 总判（会话末一次性判分 + 判分记录落盘），配跨会话累积的学习工作区
- `skills/visualize/` — 当图确实比字更清楚时，为课程添加一张正确、极简的配图
- `skills/browser-act/` / `skills/diagram-design/` / `skills/obsidian-markdown/` — 协同技能：浏览器操作与页面演示、正式图示绘制、Obsidian Markdown 格式约定
- `agents/researcher.md` — 网络调研员：教学中的事实核实、课前主题摸底，产出带出处的结构化简报
- `agents/diagram-maker.md` — 配图制作者：把 brief 变成 Mermaid/SVG 渲染的 PNG，渲染后必亲眼看图并迭代，保证图不说假话

## 它是怎么教学的

一次完整的教学会话分四个阶段，永远按序全跑，中间不打断你：

1. **探查**——一两轮批量判分题（每轮至多 4 题、全程至多 8 题）测绘你的水平边界：哪里是已经牢固的地板，哪里是知识耗尽的天花板。测绘到此为止，把交互压到最少。
2. **规划**——结合你的边界与目标，画出本次课程的依赖图（无条件真理在根部，推导事实挂在上面，你的目标在汇点），展示给你看，声明"有异议随时喊停"后直接开教。计划就是教学顺序。
3. **教学**——按你的水平连续输出讲述式教程：一个节点一个节点地构建，先给动机（为什么需要它、为什么是现在），再确立，再把依赖边显式讲清。全程零提问零打断；想自己推理时说"让我自己推"切换问答式。
4. **总判**——全部小节讲完后一次性判分：每小节出题，混入上次内容的一两道复习题；当场判分反馈，答错的小节当场补教；每道题与你的回答都落进日志的判分记录，之后据此更新教程。

所有教学状态落在**学习工作区**（一组约定文件，随会话累积）：

- `MISSION.md` —— 你为什么学这个主题；每次教学以它为锚
- `log/<主题>.md` —— 课程日志，实时镜像讲解正文与会话末的判分记录（题面、你的回答、缺口），标注当前进度
- `lessons/` / `reference/` / `GLOSSARY.md` —— HTML 复习单元、速查参考文档、规范术语表
- `learning-records/` —— 学习记录（相当于教学版 ADR），驱动下次会话从你的前沿继续，而不是重头再来

下次会话开场零提问，直接从上次的前沿续接；对上次内容的复习题混在会话末总判里——既是间隔复习，也检验知识是否真的锁住了；答不上来的节点会安排重教。

## 怎么使用

对 Claude Code 说"教我 X"即可，其余交给系统。建议在一个空目录或专用学习目录里开会话（在代码仓库里触发教学时，系统会先与你确认工作区位置，不经确认不会往项目里倾倒文件）。

### 提示词实例

**开始学习：**

- `教我信号与系统` —— 最小启动。系统会先访谈你为什么学（至多 2-3 轮），再用一两轮批量判分题摸底（全程至多 8 题）
- `我想学 Rust，目标是三个月内给团队交付一个命令行工具` —— 带具体目标的启动：访谈更短，教学全程瞄准这个目标
- `我已经会 Python 基础了，教我异步编程` —— 声明既有知识，测绘从这里验证起步，不重教已会的

**会话中：**

- `为什么非得是这样？我自己怎么可能发现这个？` —— 触发发现式讲解：每一步都先给你动机，让知识感觉是被你自己发现的
- `这部分画张图` —— 触发配图链：派 maker 产出经过渲染验证的 PNG，嵌入课程日志
- `这里我没懂，换种讲法` —— 调整当前小节的讲解方式（讲述式 ↔ 问答式）
- `让我自己推` —— 切换到问答式（Socratic）：关键步骤先让你自己推理再揭示；默认是连续讲述不打断
- `别考我了，直接讲吧` —— 拒绝水平测绘：系统会说明测绘的目的并请你确认一次；仍拒绝则按访谈信息估计水平直接开教（会话末总判仍会检验落地）

**跨会话：**

- `继续上次的` / `我们学到哪了` —— 从课程日志标注的前沿续接，开场零提问；对上次内容的复习混在会话末总判里
- `考考我上次学的傅里叶变换` —— 定向复习，检验存储强度
- `我想换个主题，改学线性代数` —— 使命修订：新主题开新工作区，旧工作区原样保留，学习记录收束变更

顺带的提问、答疑、调试不会触发教学系统，按普通对话处理；系统在答疑中察觉你想系统深入时，会主动提议开始学习会话。

## Claude Code安装

前置：已安装并登录 [Claude Code](https://claude.com/claude-code)。

### 方式一：Claude Code 插件（推荐）

在 Claude Code 里执行：

```
/plugin marketplace add AomeNero/Learning-Skill
/plugin install learning-skill@learning-skill
```

装完用 `/plugin` 确认 `learning-skill` 处于已启用状态，然后在任意目录开会话说"教我 X"即可。后续更新在 `/plugin` 界面操作，版本号见仓库 tag。

### 方式二：clone 为 .claude 目录

本仓库**也是一个** `.claude` 目录。在你的学习项目根目录：

```bash
git clone https://github.com/AomeNero/Learning-Skill.git .claude
```

然后用 Claude Code 打开该项目——项目级 skills 与 agents 自动加载，直接说"教我 X"即可。这种方式把技能与学习工作区绑在同一个目录，适合固定地点学习的场景。

## WorkBuddy安装

WorkBuddy 与 Claude Code 共用同一套 SKILL.md 格式，把 `skills/` 下的各技能目录拷入其技能目录即可。

bash / macOS / Linux：

```bash
git clone https://github.com/AomeNero/Learning-Skill.git
mkdir -p .workbuddy/skills && cp -r Learning-Skill/skills/* .workbuddy/skills/
```

Windows PowerShell：

```powershell
git clone https://github.com/AomeNero/Learning-Skill.git
New-Item -ItemType Directory -Force .workbuddy/skills | Out-Null
Copy-Item -Recurse Learning-Skill/skills/* .workbuddy/skills/
```

注：`agents/` 下的两个子代理（researcher、diagram-maker）是 Claude Code 专属机制，WorkBuddy 下自动降级——事实核实改用内置搜索，配图由主线程直接产出源码贴进日志（见下方"说明"）。

## 依赖（可选）

- 配图渲染：Node.js + `@mermaid-js/mermaid-cli`（Mermaid 图，需本机 Chrome/Edge，puppeteer 找不到浏览器时设 `PUPPETEER_EXECUTABLE_PATH` 指向系统浏览器）、`rsvg-convert` 或 ImageMagick 7（SVG 图，仅类 Unix）。不装也能用：渲染不可用时配图降级为在课程日志里贴 Mermaid/SVG 源码（Obsidian 原生渲染 mermaid 代码块）
- 课程日志建议用 [Obsidian](https://obsidian.md) 阅读（LaTeX 与 Mermaid 开箱渲染）；VS Code 预览需装对应扩展

## 说明

- 没有子代理也能跑：主会话直接教学——事实核实降级为自带搜索，配图降级为主线程直接产出 Mermaid/SVG 源码贴进日志（两者都会向学习者声明"未经子代理验证"）
- 涉及数学的内容一律 LaTeX 记号；判分题选项避免复杂记号，保证终端里当场可读
- 教学语言与工作区文件语言始终跟随你使用的语言
