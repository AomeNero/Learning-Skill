# learning skill 对抗式审查报告

- 日期：2026-09-29
- 对象：`skills/learning/` 全部 5 文件（SKILL.md 290 行 / 27,013 字符 + 4 个格式文件），辅证：`skills/teach/`、`README.md`、`DESIGN.md`、`assets/Template.html`、`agents/`、`~/.claude/skills/` 安装版、本环境已装技能
- 判定基准：工程制品压测（触发正确性 / 内部一致性 / 对抗场景鲁棒性）；不质疑两条教学原则本身，只查"原则→机制"断链
- 方法：3 个并行红队 subagent（trigger-review / consistency-review / redteam-review）+ 主线程逐条复核
- 语境前提：工作区在本仓库内与任意目录都要能跑；受众以作者本人为主，按"会分发给他人"加测陌生用户 / 英文 / 非开发者剧本
- 原始发现 42 条，去重合并后 **28 条**：**CRITICAL ×1 / HIGH ×9 / MEDIUM ×10 / LOW ×8**
- 边界：本报告只评审不改码；每条附修复建议，修复另行执行

---

## 结论速览

| ID | 级别 | 标题 | 位置 |
|----|------|------|------|
| CR-1 | CRITICAL | researcher 子代理引用在主要语境下不可达，准确性核实链路无降级 | SKILL.md:131,169 |
| H-1 | HIGH | description"任何时候……哪怕只是简短解释"使 290 行全文在几乎所有讲解型对话载入 | SKILL.md:3 |
| H-2 | HIGH | teach/learning 共存无排他，本机 /teach 实际运行英文旧版 | teach:4 vs learning:3 |
| H-3 | HIGH | 工作区锚死当前目录，会在用户代码仓库倾倒教学文件；与 graphify 路由重叠 | SKILL.md:98 |
| H-4 | HIGH | 中断恢复无数据源：续接读取清单不含 log，"上次的前沿"无处可读 | SKILL.md:112 |
| H-5 | HIGH | 跨主题请求三条条款互相矛盾，无裁决路径 | MISSION:27 vs SKILL:210 |
| H-6 | HIGH | 阶段 1a 无拒绝降级、无起点难度、无空地板出口 | SKILL.md:148-161 |
| H-7 | HIGH | 判分题选项内 LaTeX 终端不可读，判分测的是源码阅读力 | SKILL.md:281 |
| H-8 | HIGH | 选项构造程序与 AskUserQuestion 4 上限不自洽（1+1+≥2=5>4） | SKILL.md:137,138,142 |
| H-9 | HIGH | DESIGN.md / Template.html 引用在任意目录与分发语境断裂，assets/ 同名歧义 | SKILL.md:259 |
| M-1 | MEDIUM | 使命访谈"动笔 / 不建"双出路并存，"不建"分支致每会话重访谈 | SKILL.md:111 |
| M-2 | MEDIUM | 协同技能表无"技能不可用"回退条款 | SKILL.md:227-235 |
| M-3 | MEDIUM | 配图链路三分：viz/ 悬空、visualize 未登记、illustration 截胡 | SKILL.md:233,252 |
| M-4 | MEDIUM | 知识类"困难是敌人、讲解平顺"与每节点判分密度的哲学-机制冲突 | SKILL.md:93 vs 198 |
| M-5 | MEDIUM | L1 会话落在已有工作区时 GLOSSARY 义务未定义 | SKILL.md:16 |
| M-6 | MEDIUM | 阶段 1a 的定向标准依赖 1b 的产出，顺序含糊 | SKILL.md:152,159,163 |
| M-7 | MEDIUM | 旧 teach 工作区被 learning 续接时 GLOSSARY 缺失无处置 | SKILL.md:111-112 |
| M-8 | MEDIUM | Other 自由文本半对半错无判分规则，检查膨胀为小作文 | SKILL.md:137,138 |
| M-9 | MEDIUM | 英文分发语言断层：description 纯中文、模板中文渗漏、无语言条款 | SKILL.md:3 |
| M-10 | MEDIUM | "VS Code 预览可直接渲染 LaTeX 与 Mermaid"声明失准（README:43 同源） | SKILL.md:247 |
| L-1 | LOW | 与 eli5 触发空间重叠（窗口窄：需"dead-simple picture explainer"意图） | learning:3 |
| L-2 | LOW | "三个阶段绝不缩放形状"对微小主题无成本豁免，researcher 摸底无豁免 | SKILL.md:129,169 |
| L-3 | LOW | 无边界程度词集中："访谈到底"无停止锚 | SKILL.md:111,152,156 |
| L-4 | LOW | 社区偏好记录位置两处说法不一（NOTES.md vs RESOURCES.md） | SKILL.md:223 |
| L-5 | LOW | Obsidian wikilink 约定只在格式文件隐含，SKILL.md 未声明 | LEARNING-RECORD:36,41 |
| L-6 | LOW | lessons 编号无可执行扫描规则（learning-records 有，lessons 没有） | SKILL.md:257 |
| L-7 | LOW | README:20 "quiz 协议写在 teach skill 里"已过期（现位于 learning） | README.md:20 |
| L-8 | LOW | 4 选项上限把多步推理压成识别题（spec 已自觉授权，属有意取舍） | SKILL.md:71 |

---

## CRITICAL

### CR-1 researcher 子代理引用在主要语境下不可达，准确性核实链路无降级
- **定级依据**：SKILL.md:131 是排他指令（"停下来，**先**用 Agent 工具派一个 researcher 子代理快速核实，**再说出口**"），无任何文内降级路径；而 researcher 在两个主要语境下不可达。
- **主线程实证**：① 本仓库直接打开时——`agents/researcher.md` 位于仓库根而非 `.claude/agents/`，仓库无 `.claude/` 目录，本审查会话可用 agent 类型列表中确无 researcher（**作者日常语境现已断链**）；② 只拷 `skills/` 分发时必然缺失。仅 README:30 的官方安装（`git clone <仓库> .claude`）语境下可加载。README:42 有兜底（"没有子代理也能跑"），但写在 README——agent 运行时读不到。
- **失效场景**：教学中遇不确定事实 → `Agent(subagent_type="researcher")` 报未知类型 → 机械 agent 卡死或自行发挥；"准确性压过流畅"这一全 skill 的信任根基在最常用语境下靠运气维持。
- **修复**：在"准确性"段与阶段 2 各加一句降级链："researcher 不可用时改用自带 WebSearch 核实；仍不可用时明示学习者此条未经核实"。可再补探测句："不确定 researcher 是否存在时，以 general-purpose 代行其简报。"
- 来源：consistency-review C-01，主线程独立证实（含本会话直接证据）。

## HIGH

### H-1 description 无边界触发条款，290 行全文被大多数讲解型对话载入
- "任何时候在向用户讲解或教授知识时都要使用（哪怕只是简短解释）"（SKILL.md:3）是无边界触发器：解释报错、答疑、读代码全命中。载入的不是 L1 摘要而是全文 290 行（约 1.5–2 万 token，量级推测），其中约 250 行是 L2 专属死重。附带污染：LaTeX 强制（:279-290）渗入终端闲答；:131 全局命令式的核实条款可能拖慢普通对话（后半句为推测）。
- **失效场景**：用户问"这个 flatMap 是干嘛的"→ 全文载入 → 一句能直答的问题被重构为"第一性原理发现式讲解"。
- **修复**：删除"任何时候"条款，触发锚定显式学习意图（"我想学 X / 教我 X / teach me Y"）；顺带解答不触发，察觉想系统深入时再提议（T-6 重写文本见附）。L1 常态原则若需保留，下沉到 CLAUDE.md/记忆层，不要用 290 行 skill 承载。
- 来源：trigger-review T-1+T-6。

### H-2 teach/learning 共存无排他；本机 /teach 实际运行英文旧版
- 三层问题：① `disable-model-invocation: true` 只挡自动调用，不建立排他——/teach 开启会话后，后续讲解轮次仍满足 learning 的"任何时候教授"，同会话双技能叠加，产物约定冲突（teach: reference/*.html + 工作区 assets 组件 vs learning: reference/*.md + log + GLOSSARY）；② teach 未删除未标废弃，README:44 仍以现存口吻提及；③ **主线程实证**：本机 `~/.claude/skills/teach/` 是英文原版（"Teach the user a new skill or concept..."），与仓库中文版不同源——作者本机敲 /teach 跑的不是仓库版。另：仓库内 teach 与 learning 的 4 个格式文件经 cmp **逐字节相同、零漂移**，但属无主双份拷贝，且已现称谓分叉（格式文件"用户" vs 正文"学习者"），漂移只是时间问题。
- **修复**：teach 二选一——删除，或顶部加废弃声明重定向 learning；格式文件单一事实源（learning 持有，teach 引用）；同步或删除 `~/.claude/skills/teach/` 英文旧版；统一"用户/学习者"称谓。
- 来源：trigger-review T-2+T-8、consistency-review C-03，主线程证实（cmp + 安装版读取）。

### H-3 工作区锚死当前目录：代码仓库倾倒教学文件 + graphify 路由重叠
- SKILL.md:98 "L2 会话把当前目录当作学习工作区"无选址判断。在用户的代码项目里命中 L2 即在项目根创建 MISSION.md、log/、lessons/、GLOSSARY.md、learning-records/。且本环境 graphify 声称覆盖"any question about a codebase"——开发者在代码库问"讲讲这个模块为什么这样设计，我想真正搞懂"时两者同时命中，无仲裁规则。
- **修复**：① 选址条款："非空目录或代码仓库中触发 L2 时，先与学习者确认工作区目录（默认建议独立目录）"；② 让位条款："纯代码库理解问题让位给 graphify 等专用技能"。
- 来源：trigger-review T-3。

### H-4 中断恢复无数据源：续接读取清单不含 log
- 续接指令（:112）读取清单只有 MISSION / learning-records / GLOSSARY / NOTES 四类；而节点进度的唯一载体是 `log/<主题slug>.md`（:250 "每教完一个节点，把该节内容追加进去"），不在清单里。learning-records 又被明文排除承载过程（LEARNING-RECORD-FORMAT:42 "逐会话的活动日志……不算数"）。
- **失效场景**：中断后重开 → 按清单读完 → 无文件含节点进度 → 重教（违反"而非重头再来"）或凭空猜前沿。叠加：log 的 `<主题slug>` 无生成规则，中文主题两次会话可能生成两个 slug，旧进度失联；中断时 log 末尾可能只有题面无反馈，节点是否落地不可判定。
- **修复**：:112 清单加入"log/<主题slug>.md（有则读，前沿 = 最后一个带完整判分反馈的节点）"；写死 slug 规则（dash-case 英文意译，续接以 log/ 既有文件名为准）；补"悬空题面视为未确认节点，重走判分检查"。
- 来源：consistency-review C-02 + redteam-review R-1-1/R-1-2/R-1-3，合并。

### H-5 跨主题请求三条条款互相矛盾，无裁决路径
- 用户在主题 A 工作区中途说"教我 B"：MISSION-FORMAT:27 说一区一使命（应换工作区）；SKILL.md:210 说"用户指定了确切想学的东西则以其为准"（可教）；SKILL.md:17/98 的 L2 触发 + 目录锚定使"换工作区"无可执行指令。教 → 污染工作区（B 的节点写进 A 的 log/GLOSSARY，带偏后续 ZPD 计算）；拒 → 违用户意愿；迁移 → 无路径。"临时插问 vs 换使命"无判别规则。
- **修复**：触发分层加裁决："会话内非使命主题默认按 L1 处理、不落工作区文件；学习者明确要换学习目标时走 MISSION 修订流程（确认 + 学习记录），换使命需新工作区目录。"
- 来源：redteam-review R-2-1 + consistency-review C-06，合并。

### H-6 阶段 1a 边界三缺失：拒绝降级、起点难度、空地板出口
- ① "绝不跳过"（:148）是标题级禁令，全文无用户拒绝豁免——唯一降级条款"讲述式"（:72）文义只覆盖阶段 3 的段落选择。零基础 + 急脾气用户说"别考我了直接讲"→ 两难：继续出题 = 持续违抗直接指令；服从 = 违反禁令。且 1a 无轮数熔断（"要多长有多长。不用赶"，:152）。② 二分搜索无起点定义（:156-157 只写答对后猛跳、答错后收窄）。③ 连续"不知道"降到最基础概念后，"地板为空"无出口条款，agent 受"夹住"要求驱动继续降档。
- **修复**：1a 末尾补三句："首题取该线中等难度；用户明确拒绝测绘时，说明目的并给一次选择，仍拒绝则接受、按访谈信息设保守地板、保留节点级判分作最小检验；连续多题'不知道'且已降至最基础概念时，边界视为定位在零，直接从无条件真理起教。"
- 来源：redteam-review R-3-1/R-3-2 + consistency-review C-09，合并。

### H-7 判分题选项内 LaTeX 终端不可读，判分失真
- :281 要求"判分题的选项和解释"一律 LaTeX，其理由（"日志文件按 LaTeX 渲染"）只覆盖落盘产物，罩不住 AskUserQuestion 实时弹窗。终端里 4 个选项全是 `$\det(A-\lambda I)=0$` 源码——因读不懂源码而答错 → 节点检查误报"不牢"（:198）→ 重教已掌握内容。判分测的是源码阅读力，不是理解。
- **修复**：格式节加裁决："落盘产物一律 LaTeX；判分题**选项**避免矩阵/分式/求和等复杂结构，用单行简单记号或等价文字描述——交互可读性优先；题干可用一句话说明记号含义。"
- 来源：redteam-review R-7-1 + consistency-review C-15，合并。

### H-8 选项构造程序与 AskUserQuestion 4 上限不自洽
- 三条并存无算术裁决：:137 "options 最多 4 个"；:138 "值得时显式加一个'不知道'选项"；:142 构造程序要求"变异成每个干扰项"（≥2）。1 正确 + 1 不知道 + ≥2 干扰 = ≥5 > 4。
- **失效场景**：判分是全 skill 最高频动作——塞 5 选项则工具报错重试；自行砍干扰项则每题砍法不一，"持平构造"程序在 2 干扰项下形同虚设；"值得时"三字无判据。
- **修复**：quiz 协议加死规则："选项恒为 4：1 正确 + 2 干扰 + 1 '不知道'（默认常驻，不按'值得'裁量）；仅二选一辨析题用 3 项。"
- 来源：redteam-review R-8-1。

### H-9 DESIGN.md / Template.html 引用在任意目录与分发语境断裂，assets/ 同名歧义
- :259 "按学习仓库根的 DESIGN.md 设计系统制作……参照 assets/Template.html 的令牌"：本仓库直开时可达；clone 为 .claude 后位于 `./.claude/DESIGN.md`（工作区 = 用户项目根，"学习仓库根"指代不明）；单独分发时彻底不存在。另 assets/ 同名歧义：teach 语境 `./assets/` 是工作区组件目录，learning 语境 `assets/` 是仓库模板目录，在工作区 assets/ 找 Template.html 必然落空。
- **失效场景**：任意目录首课 → agent 三选一：凭同句四个视觉词（奶油画布、衬线标题、深墨代码窗、珊瑚点睛）自造令牌（最可能，跨工作区视觉漂移）/ 拒产课程 / 无中生有创建 DESIGN.md——均无授权。
- **修复**：把课程相关令牌摘要（或 Template.html 全文）复制进 `skills/learning/`（如 `skills/learning/TEMPLATE.html`），SKILL.md 改为引用技能目录内相对路径——所有语境成立；再补缺失分支："缺省时以四个视觉词为种子在工作区自建精简 DESIGN.md，不阻塞课程产出。"
- 来源：consistency-review C-04 + redteam-review R-6-1，合并；主线程证实文件位置。

## MEDIUM

### M-1 使命访谈"动笔 / 不建"双出路并存
- SKILL.md:111 同句并存"说不清为什么就动笔"与"坏的使命比没有使命更糟"（MISSION-FORMAT:29 重复后者）。拒答型用户："动笔"写入反格式占位（违反 MISSION-FORMAT:11 "避免抽象表述"）；"不建"分支 → 每次开会话重判"新工作区"、重走访谈、每次被拒，永远进不了续接态。
- **修复**：定唯一出路："访谈至多 2-3 轮；给不出具体动机就动笔如实记录（'动机暂缺，凭兴趣学习'）——动机空缺本身是有用信息，不许以'坏使命更糟'为由不建文件。"
- 来源：redteam-review R-4-1。

### M-2 协同技能表无"技能不可用"回退条款
- :227-235 "交给对应技能，不要重复造轮子"——分发用户未装 browser-act/diagram-design 时调用报错，无授权内联回退，卡住或违规"造轮子"（恰是表格禁止的）。
- **修复**：表后加一行："目标技能不可用时用基础能力内联回退，不因缺技能阻塞教学。"
- 来源：redteam-review R-6-2。

### M-3 配图链路三分：viz/ 悬空、visualize 未登记、illustration 截胡
- `![说明](../viz/<文件名>.png)`（:252）是 viz/ 在全文唯一出现——工作区清单（:96-107）与产物三层（:237-243）均无 viz/；目录约定实际由 skills/visualize 定义，但 visualize 不在协同技能表（:229-234）。同时自动触发的 illustration（强 IP：小Y/小M、蓝黄红）可能截胡教学配图请求，与 diagram-design 路由及"奶油画布"设计系统冲突。
- **修复**：协同表加"课程配图 | visualize"一行并声明其优先，表下加"教学配图不使用 illustration"；工作区清单补 `./viz/*.png`；图片条款改"能产出图片时才嵌入，否则省略，不留死链"。
- 来源：consistency-review C-05 + trigger-review T-7 + redteam-review R-6-3，合并。

### M-4 知识类"平顺讲解"与每节点判分密度的哲学-机制张力
- :93 知识获取"困难是敌人……别让费解的跳跃挤占工作记忆"；但机制侧判分密度最高：1a 连环测 + 每节点判分"一视同仁"（:198）+ Socratic 步骤可判分即判分（:71）。三策略中只有交错标了"仅限技能练习"，提取练习与间隔未限定——调和全靠读者推断"判分是及格线、合意困难是超出部分"这层未写出的区分。
- **修复**：流利节补分界："节点级判分对所有主题一视同仁（及格线）；合意困难的额外加压仅适用技能类主题。知识类 Socratic 判分题每节点至多一道，测绘集中在 1a 不渗入教学。"
- 来源：consistency-review C-10 + redteam-review R-7-2，合并。

### M-5 L1 落在已有工作区时 GLOSSARY 义务未定义
- :16 L1 "只适用：两条原则 + 准确性核实。不建任何文件"读作排他清单；GLOSSARY-FORMAT:3 "所有讲解……都应遵守它的术语"是全局义务。已有工作区里问 L1 问题：读不读 GLOSSARY？字面冲突无裁决。
- **修复**：:16 补一句："L1 不建文件，但工作区已存在时，术语遵守 GLOSSARY.md。"
- 来源：consistency-review C-07。

### M-6 阶段 1a 的定向标准依赖 1b 产出，顺序含糊
- 1a 沿"课程将依赖的每一条线"（:152）"以与目标的相关性为界"（:159）定向，但目标在 1b（:163）才收集——探查时参照系未定，机械 agent 无法判断测哪些线。
- **修复**：1a 开头补："先按学习者陈述的粗目标定候选依赖线；1b 明确目标后若依赖线变化，回头补测新增线。"
- 来源：consistency-review C-08。

### M-7 旧 teach 工作区续接时 GLOSSARY 缺失无处置
- teach 工作区约定里 GLOSSARY 不是独立文件（只是 reference 的一种）。旧工作区 MISSION.md 存在 → 走续接步骤 2（只读不建）→ GLOSSARY.md 不存在，无初始化指令也无容忍说明，而 learning 又把它定为"一旦建立必须遵守"。
- **修复**：步骤 2 补"GLOSSARY.md 不存在则惰性建立（首个术语立住时创建）"。
- 来源：consistency-review C-11。

### M-8 Other 自由文本半对半错无判分规则
- :138 只有"按内容照常判分"，格式是二元制（✓/✗ + 正确答案 + 简短解释）。半对半错的自由文本：判 ✓ 违反"错误模型必须深挖"精神，判 ✗ 惩罚部分正确且边界测绘失真。spec 精神驱动 agent 追问澄清 → 每题膨胀多轮。
- **修复**：加规则："自由文本按核心断言判分，含实质错误成分即 ✗ 并指出错处；不为部分正确给 ✓；一道题至多一轮澄清。"
- 来源：redteam-review R-8-2。

### M-9 英文分发语言断层
- description 纯中文无英文触发词（显式英文请求靠语义匹配推测仍可触发 75-90%，中文 90%+）；更大问题是分发后整份中文 SKILL 驱动英文用户——quiz 选项、MISSION 模板示例（"十月底跑完半马"）全中文渗漏；全文无语言条款。
- **修复**：description 补英文触发词（teach me / I want to learn / help me understand）；SKILL.md 会话开始加"工作区文件与教学语言始终跟随学习者语言；模板只约定结构不约定语言"。
- 来源：trigger-review T-4 + redteam-review R-5-1，合并。

### M-10 "VS Code 预览可直接渲染 LaTeX 与 Mermaid"声明失准
- :247 及 README:43 声称 VS Code 预览可直接渲染——实测内置 Markdown 预览两者默认都不渲染，均需扩展（Obsidian 开箱成立）。整个"数学一律 LaTeX"规则的辩护（"日志按 LaTeX 渲染"）部分建立在此失准声明上。
- **失效场景**：无 Obsidian 的学习者用 VS Code 打开日志 → 数学与依赖图全显源码——终端不渲染 + 查看器也不渲染 = 最差组合。
- **修复**：改为"Obsidian（开箱渲染）或装了 LaTeX/Mermaid 扩展的 VS Code 预览"。
- 来源：consistency-review C-12，主线程证实 README:43 为同源出处。

## LOW

- **L-1 与 eli5 触发重叠（窗口窄）**：eli5 需"dead-simple picture explainer"意图才自动触发，比 trigger-review 初判的碰撞面窄。"画个图简单讲讲 X"类请求仍可能双命中且输出契约互斥（HTML 大图 artifact vs 对话内发现式讲解）。修复：learning description 加让位句"已输入 /eli5 或要求图画式极简解释时让位"。来源：T-5，主线程复核后降级。
- **L-2 微小主题无成本豁免**："教我什么是变量"级 L2 也要全三阶段 + researcher 摸底 + DAG 检查点。形状不变是明示设计意图，可辩护；但摸底开销对微小主题无豁免。修复：阶段 2 补"主题极小时摸底可省"。来源：C-13。
- **L-3 无边界程度词**："访谈到底"（:111）无停止锚（失控风险最高）；"狠狠提高"（:156）有行为定义可接受；"快速"（:169）可接受。修复："访谈到底"后加"至多 3-5 问，能写出 1-3 句'为什么'即止"。来源：C-14。
- **L-4 社区偏好记录位置不一**：SKILL.md:223 说记 NOTES.md，RESOURCES-FORMAT:32 说记 RESOURCES.md。修复：统一主记录地，另一处改引用。来源：C-16。
- **L-5 wikilink 约定未声明**：[[MISSION.md]] 等 wikilink 只在 LEARNING-RECORD-FORMAT:36,41 隐含；VS Code/GitHub 不识别。修复：SKILL.md 工作区节提一句"文件间交叉引用用 Obsidian wikilink"。来源：C-17。
- **L-6 lessons 编号无扫描规则**：learning-records 有"扫描最大编号加一"，lessons 只有"编号每次递增"（:257）。修复：补"同法扫描 ./lessons/ 最大编号加一"。来源：C-18。
- **L-7 README:20 已过期**："quiz（判分答题）……协议写在 teach skill 里"——quiz 协议现已迁入 learning/SKILL.md。主线程发现（复核 README 时）。
- **L-8 4 选项上限压扁多步推理**：spec 在 :71 已自觉授权"转成选择题呈现"，属有意取舍非疏漏；可接受现状，若改允许多步推理拆串行小题链。来源：R-7-3。

---

## 专项小结：teach/learning 新旧关系

1. **仓库内无漂移**：4 对格式文件 cmp 逐字节相同（主线程复核证实）。
2. **但结构未裁决**：teach 未删未标废弃，双份无主拷贝 + 称谓分叉（用户/学习者）+ RESOURCES-FORMAT:29 引用的"SKILL.md 哲学"章节在两 skill 中内容已不同——语义漂移只是时间问题。
3. **本机安装脱钩**：`~/.claude/skills/teach/` 是英文原版，/teach 实际行为与仓库源不符（主线程读取证实）。
4. **共存冲突实体**：disable-model-invocation 不排他 → 同会话双触发可预期；reference/*.html vs *.md、工作区 assets 组件 vs 自包含单文件、两套判分题构造规则。
5. **修复顺序**：retire teach（删除或废弃重定向）→ 格式文件单一事实源 → 清理本机英文旧版 → learning 头部加旧工作区续接容忍规则。

## 复核记录（主线程对 subagent 发现的修正）

| 项 | 处理 |
|----|------|
| C-01 researcher | **证实并升级确证**：本会话即"仓库直开"语境，可用 agent 列表无 researcher，直接证据成立；维持 CRITICAL |
| T-2 安装版 teach 英文旧版 | **证实**：读取 `~/.claude/skills/teach/SKILL.md` 确认为英文原版 |
| "格式文件已漂移"类论断 | **修正**：仓库内 4 对文件 cmp 逐字节相同、零漂移；漂移风险成立但尚未发生（T-8 的"无主双份"表述为准） |
| T-1 "27,013 字符" | **证实**：wc 实测 290 行 / 27,013 字符 |
| C-12 VS Code 渲染 | **证实**：README:43 为同源出处；内置预览默认不渲染 LaTeX/Mermaid 属实 |
| T-5 eli5 冲突面 | **降级 HIGH 面窄化**：eli5 自动触发需 "dead-simple picture explainer" 意图，重叠窗口比初判窄 → LOW |
| T-9 darwin 重叠 | **不立为发现**：触发词几乎不相交，agent 自评"无需改动"，仅留作 description 写法正反参照 |
| README:20 quiz 位置过期 | **主线程新增** L-7 |

## 总评与修复顺序建议

learning 的教学主线（触发分层 → 三阶段 → 产物三层）内部基本自洽，哲学到机制的推导大体成立，质量高于典型 skill。缺陷集中在三层：

1. **语境假设单一**（CR-1、H-9、M-2、M-3）：几乎所有外部引用（researcher、DESIGN.md、Template.html、visualize、协同技能）都默认"完整 clone 为 .claude"语境，与"任意目录开工作区 + 分发"的声明语境冲突；其中 researcher 连"仓库直开"语境都断，且是排他指令无降级——唯一 CRITICAL。
2. **状态机缺口**（H-4、H-5、M-1、M-7）：过程状态只有一个载体（log）却没接入续接读取链；跨主题、访谈拒答、旧工作区续接三类分叉点没有写死出路，全靠 agent 即兴。
3. **触发与协议边界**（H-1、H-8、H-7、H-6）：description 的"任何时候"条款是最大的单点污染源；quiz 协议（最高频动作）在选项算术与 LaTeX 可读性上与工具现实不自洽。

**建议修复顺序**（先便宜后昂贵、先高频后低频）：
1. CR-1 researcher 降级链（两句话，解除唯一 CRITICAL）
2. H-1 description 重写（一并解决 H-3 的让位半边、M-9 的英文触发词、L-1）
3. H-8 quiz 选项算术死规则 + H-7 选项 LaTeX 裁决（同节顺手改）
4. H-4/H-5/M-1 状态机三缺口（续接清单加 log、跨主题裁决、访谈唯一出路）
5. H-9 设计资产进技能目录 + M-2/M-3 回退条款
6. H-6 1a 三句边界（拒绝降级/起点/空地板）
7. teach retire 专项（H-2 + M-7 + L-7）
8. 其余 MEDIUM/LOW 按条勾销

---

*方法注：三线并行红队（trigger-review / consistency-review / redteam-review）共 42 条原始发现，主线程逐条复核（cmp 字节比对、文件读取、本会话环境实证）后去重合并为 28 条。红队推演均为纸面走线，未发起真实教学会话，未修改任何文件。*
