# learning (一套个人 AI 学习系统)

一套个人 AI 学习系统，本仓库是面向 **Claude Code** 的中文改造版，兼及 WorkBuddy 等遵循 Agent Skills 开放标准的客户端。

核心理念：**理解 > 记忆**——在脑中构建依赖图（少数核心真理 + 挂在上面的推导事实），而不是堆砌孤立事实。

## 里面有什么

- `skills/learning/` — 教学系统主体：目标访谈（零基础默认）→ 规划（依赖图，非阻塞展示）→ 课程静默批量产出（教学全在课程正文，逐节自检）→ 检索练习（≤4 题/节，错题落档）→ 错题驱动续接，配跨会话累积的学习工作区
- `skills/diagram-design/` — 课程配图**首选**：全类型图示（架构/流程/时序/ER 等）产出 SVG
- `skills/visualize/` — 备用配图链：diagram-design 不可用时派 maker 产出经验证的 SVG
- `skills/browser-act/` / `skills/obsidian-markdown/` — 协同技能：浏览器操作与页面演示、Obsidian Markdown 格式约定
- `agents/researcher.md` — 网络调研员：教学中的事实核实、课前主题摸底，产出带出处的结构化简报
- `docs/` — 项目文档：[Skill-指南](docs/Skill-指南.md)（系统全景与流程规格）、[template-布局](docs/template-布局.md)（模板布局分析）
- `agents/diagram-maker.md` — 配图制作者：把 brief 变成 SVG 成品（mermaid 类 CLI 渲染并亲眼看临时 PNG 验证；SVG 类手写并逐项源码审查），课程直接外链引用，不转 PNG

## 它是怎么教学的

一次完整的教学会话分四个阶段，永远按序全跑；教学对象默认零基础，不做水平测绘：

1. **目标访谈**——不判分的追问，把"我想理解 X"追到具体为止；同时访谈你为什么学（至多 2-3 轮），落成使命文档。
2. **规划**——结合你的目标，画出本次课程的依赖图（无条件真理在根部，推导事实挂在上面，你的目标在汇点），展示给你看，声明"有异议随时喊停"后直接开教。计划就是教学顺序。
3. **课程产出（静默批量）**——按依赖图逐节产出：课程 HTML（教学全在课程正文——逐节点给动机、确立、连接，对话不复述），每节把 ≤4 道单选题追加进唯一的 `lessons/question.html`，逐节跑 check-lesson.py 自检；**从产出到一次性汇报绝对零提问零输出**，全部完成后一次性汇报"共 N 节"。
4. **检索练习**——打开 `lessons/question.html`（全部小节的练习集中于此）：按节序阅读课程后回来**凭记忆**作答，全部答完**一次提交**——页面当场判分（按节分块）并生成作答报告，自动弹出"另存为"（文件名预填 answer.md），保存到练习页同级的 lessons/ 目录；已有同名文件确认替换即自动追加（历史不丢，回退复制）。答错只记录不回头——错题驱动下次学习优先重教（重写对应课程节 + 确认题划销）。

所有教学状态落在**学习工作区**（一组约定文件，随会话累积，文件名一律小写英文）。状态管理类文件集中收在 `docs/` 子目录，教学产物留在工作区根：

- `docs/` —— 状态管理文件：`mission.md`（你为什么学这个主题；每次教学以它为锚）、`resources.md`（可信资源清单）
- `lessons/` —— 课程 `000N-*.html` + **练习总页 `question.html`**（所有小节的检索练习集中于此）+ `answer.md`（练习与错题档案；全对也记，驱动下次优先重教未清错题）+ `src/`（配图 SVG 与 katex 共享资产）——**课程即已讲，answer.md 有练习记录即已练**

下次会话开场零提问，直接从上次的前沿续接；`lessons/answer.md` 里未清的错题所涉知识点会融入教学流优先重教，重教后出一道确认题钉住、答对划销——既是间隔复习，也检验知识是否真的锁住了。

## 怎么使用

对 Claude Code 说"教我 X"即可，其余交给系统。建议在一个空目录或专用学习目录里开会话（在代码仓库里触发教学时，系统会先与你确认工作区位置，不经确认不会往项目里倾倒文件）。

### 提示词实例

**开始学习：**

- `教我信号与系统` —— 最小启动。系统会先访谈你为什么学（至多 2-3 轮）与想学到哪，然后直接开教
- `我想学 Rust，目标是三个月内给团队交付一个命令行工具` —— 带具体目标的启动：访谈更短，教学全程瞄准这个目标
- `我已经会 Python 基础了，教我异步编程` —— 声明既有知识，落一条学习记录作起点参考；默认仍是零基础教学，不重新摸底考

**会话中：**

- `为什么非得是这样？我自己怎么可能发现这个？` —— 触发发现式讲解：每一步都先给你动机，让知识感觉是被你自己发现的
- `这部分画张图` —— 触发配图：优先 diagram-design 产 SVG，不可用时派 maker（visualize），外链嵌进本节课程 HTML
- `这里我没懂，换种讲法` —— 当前小节换个讲法重讲；小节末的检索练习会检验是否真的落地
- `我上次错的那道题再讲讲` —— 定向触发错题重教：从 answer.md 调出对应知识点，重教后出确认题划销

**跨会话：**

- `继续上次的` / `我们学到哪了` —— 从 lessons/ 课程与 answer.md 练习档案续接（有课=已讲，档案有记录=已练），开场零提问；answer.md 的未清错题融入教学流优先重教
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

注：`agents/` 下的两个子代理（researcher、diagram-maker）是 Claude Code 专属机制，WorkBuddy 下自动降级——事实核实改用内置搜索，配图由主线程直接手写 SVG 内联进课程 HTML（见下方"说明"）。

## 依赖（可选）

- 配图渲染：Node.js + `@mermaid-js/mermaid-cli`（Mermaid 图，需本机 Chrome/Edge，puppeteer 找不到浏览器时设 `PUPPETEER_EXECUTABLE_PATH` 指向系统浏览器）、`rsvg-convert` 或 ImageMagick 7（SVG 图，仅类 Unix）。不装也能用：渲染不可用时配图降级为内联 SVG 进课程 HTML（mermaid 源码在课程 HTML 中不渲染，改走 SVG 或省略）
- 课程是轻量 HTML，双击浏览器即读；公式课程的 KaTeX 资产在工作区 `lessons/src/katex/` 共享一份（相对路径引入，TeX 源码保留在页面里）；`docs/` 下的 Markdown 文件建议用 [Obsidian](https://obsidian.md) 阅读（LaTeX 开箱渲染）

## 说明

- 没有子代理也能跑：主会话直接教学——事实核实降级为自带搜索，配图降级为主线程手写 SVG 内联进课程（两者都会向学习者声明"未经子代理验证"）
- 涉及数学的内容一律 LaTeX 记号；判分题选项避免复杂记号，保证终端里当场可读
- 教学语言与工作区文件语言始终跟随你使用的语言
