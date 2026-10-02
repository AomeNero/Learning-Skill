# template.html 布局分析

> 文件：`skills/learning/assets/template.html`（课程）+ `question-template.html`（配套练习页，见文末）
> 课程模型：**一门课程 = 一个小节**——每个 HTML 文件承载且仅承载一个小节，编号即小节顺序；练习不在课程内，由配对 `-question.html` 承担
> 设计语言：DESIGN.md（Claude 设计系统）——奶油画布 + 衬线标题 + 珊瑚点睛 + 深墨代码面
> 依赖：**KaTeX 相对外链（公式课程）**——`assets/katex/` 三件复制到工作区 `lessons/src/katex/` 一份共享，课程经 `src/katex/…` 相对路径引入；TeX 源码保留在 HTML，资产缺失时原样显示；无外部网络资源

---

## 一、整体骨架：三栏课程布局（外框 1408px）

```
┌──────────────────────────────────────────────────────────────┐
│ site-header  64px · sticky · 奶油底 · hairline 下边线          │
│ 书本标（开卷两页）+ "Learning Docs" 词标（无主导航）              │
├───────────┬──────────────────────────────┬────────────────────┤
│ .sidebar  │  .content (flex-1, min-w-0)  │  .toc              │
│ 288px     │   └─ .content-inner          │  240px             │
│ sticky    │       max-width: 816px 居中  │  sticky            │
│ 计划小节导航 │                              │  本节大纲（锚点定位） │
├───────────┴──────────────────────────────┴────────────────────┤
│ site-footer  深墨 #181715 · 64px 内边距 · 仅一行版权             │
└──────────────────────────────────────────────────────────────┘
```

**尺寸公式**（CSS 变量集中在 `:root`）：

| 变量 | 值 | 作用 |
|------|-----|------|
| `--shell-max` | `88rem` = 1408px | 外框 = 288 + 816 + 240 + 64（边距） |
| `--sidebar-w` | `18rem` = 288px | 左栏：计划小节导航 |
| `--content-max` | `816px` | 中列（DESIGN.md 规范值） |
| `--toc-w` | `15rem` = 240px | 右栏：本节大纲 |
| `--header-h` | `64px` | 顶栏（top-nav 规范高度） |

> 关键依赖：**外框必须随中列目标宽度增长**——外框不足时中列会被压缩，改 816px "无效果"。三条栏的 sticky 偏移全部引用 `--header-h`，换顶栏高度不用改布局代码。

## 二、设计令牌（全部来自 DESIGN.md）

**色彩**：画布 `#faf9f5`（暖奶油，非纯白）· 墨色 `#141413` · 正文 `#3d3d3a` · 辅文 `#6c6a64` · hairline `#e6dfd8` · 奶油卡 `#efe9de` · 深墨面 `#181715`（代码窗/页脚）· 珊瑚 `#cc785c`

**珊瑚纪律**（全页仅 3 处）：左栏当前小节的编号 · `badge-coral`「推荐」徽章 · 正文文字链接。其余强调一律用奶油色阶。

**字体**（系统栈，无下载）：

| 用途 | 栈 | 规格 |
|------|-----|------|
| 衬线标题 | Tiempos → Garamond → Georgia → 思源宋/SimSun | h1 48/1.1/−1px · h2 28/−0.3px · h3 21/−0.2px，**全部 weight 400** |
| 无衬线正文 | Inter → Segoe UI → 微软雅黑 | 正文 16/1.55；标签 500 |
| 代码 | JetBrains Mono → Cascadia → Consolas | 14/1.6 |

**圆角**：按钮/页签 8px · 卡片 12px · 徽章 pill。**间距**：4px 基数（16/24/32/48）。

## 三、区域明细

### 顶栏 `.site-header`
- sticky 吸顶 + hairline 下边线；词标（书本 SVG 标——开卷两页 + 衬线 19px 字标）
- 仅品牌词标，无主导航——课程是独立复习单元，跨节导航由左栏承担

### 左侧栏 `.sidebar`——全部计划小节导航（三态）
- sticky + `calc(100vh − header-h)` 独立滚动
- 顶部：caption「课程主题」+ 衬线主题名（hairline 下边线收口）
- 小节列表 `.section-nav`（平铺不分组，mono 编号 + 标题）三态：
  - **已发布**：可点击相对链接（同目录 `000N-xxx.html`），灰字 hover 墨字 + 浅奶油底
  - **当前小节**：`.active` 静态高亮——`surface-card` 底 + **编号染珊瑚**（全页唯一珊瑚标记位）
  - **未发布**：`.planned` 置灰占位不可点（`muted-soft`，default 光标）
- **快照语义**：左栏是制作时点的课程地图，新课程发布后不回填旧文件

### 中列 `.content`
- `flex:1 + min-width:0`（防长代码行撑破三栏的纪律项）
- 页头：eyebrow（课程主题 · 第 N 节）+ 衬线 h1 48px + 18px lead 动机段
- 提示块 `.callout`：奶油卡 + hairline 边框 + pill 标签（本节挂靠 / 一手资源 / 随时问）
- **展示数学 KaTeX（相对外链）**：正文写 LaTeX（行内 `$x$`、独立 `$$…$$`），TeX 源码留在 HTML；head 引 `src/katex/katex.embed.css`、body 末引 `src/katex/katex.min.js` + `auto-render.min.js`（DOMContentLoaded 扫描渲染）。资产由技能 `assets/katex/` 复制到工作区 `lessons/src/katex/` 一份共享（cp 复制，勿读入上下文）；无公式课程删除外链块
- **代码窗 `.code-window`**（签名组件）：深墨卡 12px 圆角 → 窗口圆点 chrome + mono 文件名 → 内层 `#1f1e1b` 代码块 → `$` 提示符灰 / 参数琥珀 / URL 青
- 组件库另有：页签 `.tab-strip` · 特性卡 `.feature-grid` · 平台卡 `.card-grid` · 图片占位 `.ph-img` · 珊瑚徽章 `.badge-coral`——样式齐备，课程按需取用

### 右栏 `.toc`——本节大纲（页内锚点目录）
- sticky 独立滚动；标题同 caption-uppercase 风格（"在此页面"）
- 列出本节全部 h2/h3 锚点，点击快速定位到对应正文（`scroll-margin-top` 避开吸顶顶栏）
- 层级缩进 `.lvl2` 固定 14px；灰字 hover 墨字；无当前行标记——静态页不做假的滚动跟踪

### 页脚 `.site-footer`
- 深墨 `#181715` + 64px 内边距（footer 规范），仅一行版权：`© 2026 AomeNero`（GitHub 链接，奶油白 hover 下划线）

## 四、响应式

| 断点 | 布局 |
|------|------|
| ≥1280px | 三栏齐全：288 + 816 + 240，大纲 sticky 侧栏 |
| 1024–1279px | 隐藏大纲，双栏（侧栏 + 中列），中列 `max-width:816px` 封顶居中 |
| <1024px | 侧栏收起（无 JS 汉堡菜单，直接收起），单栏 |
| <768px | h1 降为 32px/−0.5px |

锚点跳转：`h2/h3/h4 { scroll-margin-top: header-h + 16px }`——无 JS 实现锚点避开吸顶顶栏。

## 五、可复用要点（搭同类页面照抄）

1. **变量集中**：颜色/圆角/间距/尺寸五组令牌全在 `:root`，改一处全局生效
2. **三栏公式**：外框 = 侧栏 + 中列 + 目录 + 2×内容 padding；四者联动，单独改中列必被外框吃掉
3. **`min-width:0` 纪律**：flex 中列必须加，否则 `pre` 长行撑爆布局
4. **双 sticky**：侧栏与目录各自 `top: var(--header-h)` + 独立 `overflow-y`
5. **珊瑚配额**：当前节编号/徽章/链接三种用途封顶，别的地方用奶油色阶
6. **深墨节奏**：代码窗与页脚两个深色块收尾，与奶油画布形成页面呼吸（DESIGN.md 的 pacing 机制）
7. **交互极简**：唯一的 JS 是 KaTeX 数学渲染（相对外链）；页签压平为静态分节；锚点偏移用 `scroll-margin-top`；移动端直接隐藏次级导航

## 六、配套资产

### question-template.html——检索练习页模板

与课程配对产出：`000N-<slug>.html`（课程）+ `000N-<slug>-question.html`（练习页）。单栏窄居中（720px），复用课程页的设计令牌与顶栏词标。结构：eyebrow + 标题 + 题目卡（单选，选中态墨色徽标）+ 珊瑚提交按钮（CTA）+ 作答报告区。内嵌判分脚本：`META`（配对课程基名）与 `QUIZ`（题面、选项、正确下标、解析）为制作时替换的数据；提交后逐题显示判定（teal ✓ / coral ✗ + 正确答案 + 解析，KaTeX 渲染）并生成报告 markdown（可复制/下载），报告格式与 docs/answer.md 的练习记录一致。答案内嵌于脚本数据，源码可见——自测场景可接受。

### katex/——KaTeX 内嵌资产

`katex.embed.css`（样式 + 20 个 base64 woff2 字体，359KB）、`katex.min.js`（277KB）、`auto-render.min.js`（3.5KB）。课程与练习页共用：仅当本节用到公式时，用 Bash 把三件**复制**到工作区 `lessons/src/katex/`（整个工作区一份；勿将资产读入上下文——640KB 远超单次输出上限），模板保留相对外链与渲染调用（`$…$` / `$$…$$` / `\(…\)` / `\[…\]`）；无公式课程删除外链块，资产缺失时 TeX 源码原样显示。
