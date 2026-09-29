# Template.html 布局分析

> 文件：`assets/Template.html`（17 KB，单文件）
> 设计语言：DESIGN.md（Claude 设计系统）——奶油画布 + 衬线标题 + 珊瑚点睛 + 深墨代码面
> 依赖：**零**——系统字体栈、无 JS、无外部资源、无图片文件

---

## 一、整体骨架：三栏文档布局（外框 1408px）

```
┌──────────────────────────────────────────────────────────┐
│ site-header  64px · sticky · 奶油底 · hairline 下边线      │
│ 四芒星占位标 + "Learning Docs" 词标 | 主导航               │
├───────────┬──────────────────────────────┬────────────────┤
│ .sidebar  │  .content (flex-1, min-w-0)  │  .toc          │
│ 288px     │   └─ .content-inner          │  240px         │
│ sticky    │       max-width: 816px 居中  │  sticky        │
│ 独立滚动   │                              │  "在此页面"     │
├───────────┴──────────────────────────────┴────────────────┤
│ site-footer  深墨 #181715 · 64px 内边距 · 仅一行版权        │
└──────────────────────────────────────────────────────────┘
```

**尺寸公式**（CSS 变量集中在 `:root`）：

| 变量 | 值 | 作用 |
|------|-----|------|
| `--shell-max` | `88rem` = 1408px | 外框 = 288 + 816 + 240 + 64（边距） |
| `--sidebar-w` | `18rem` = 288px | 左侧栏 |
| `--content-max` | `816px` | 中间列（DESIGN.md 规范值） |
| `--toc-w` | `15rem` = 240px | 右侧目录 |
| `--header-h` | `64px` | 顶栏（top-nav 规范高度） |

> 关键依赖：**外框必须随中列目标宽度增长**——曾因外框 1216px 时中列被压到约 640px，改 816px "无效果"。三条栏的 sticky 偏移全部引用 `--header-h`，换顶栏高度不用改布局代码。

## 二、设计令牌（全部来自 DESIGN.md）

**色彩**：画布 `#faf9f5`（暖奶油，非纯白）· 墨色 `#141413` · 正文 `#3d3d3a` · 辅文 `#6c6a64` · hairline `#e6dfd8` · 奶油卡 `#efe9de` · 深墨面 `#181715`（代码窗/页脚）· 珊瑚 `#cc785c`

**珊瑚纪律**（全页仅 3 处）：TOC 当前行左标记 · `badge-coral`「推荐」徽章 · 正文文字链接。其余强调一律用奶油色阶。

**字体**（系统栈，无下载）：

| 用途 | 栈 | 规格 |
|------|-----|------|
| 衬线标题 | Tiempos → Garamond → Georgia → 思源宋/SimSun | h1 48/1.1/−1px · h2 28/−0.3px · h3 21/−0.2px，**全部 weight 400** |
| 无衬线正文 | Inter → Segoe UI → 微软雅黑 | 正文 16/1.55；标签 500 |
| 代码 | JetBrains Mono → Cascadia → Consolas | 14/1.6 |

**圆角**：按钮/页签 8px · 卡片 12px · 徽章 pill。**间距**：4px 基数（16/24/32/48）。

## 三、区域明细

### 顶栏 `.site-header`
- sticky 吸顶 + hairline 下边线；词标（四芒星 SVG 占位 + 衬线 19px 字标）
- 右侧集群（外部链接/搜索/助手）已按需求**删除**，仅存品牌 + 3 个主导航

### 左侧栏 `.sidebar`
- sticky + `calc(100vh − header-h)` 独立滚动
- 分组标题：12px / 500 / 1.5px 字距全大写（caption-uppercase 规范）
- 链接：14px/500 灰字，hover 浅奶油底；当前页 `surface-card` 底 + 8px 圆角

### 中列 `.content`
- `flex:1 + min-width:0`（防长代码行撑破三栏的纪律项）
- 页头：衬线 h1 48px + 18px lead 段
- 提示块 `.callout`：奶油卡 + hairline 边框 + pill 标签（珊瑚不用在这里）
- **代码窗 `.code-window`**（签名组件）：深墨卡 12px 圆角 → 窗口圆点 chrome + mono 文件名 → 内层 `#1f1e1b` 代码块 → `$` 提示符灰 / 参数琥珀 / URL 青
- 页签 `.tab-strip`：category-tab 规范——未激活透明灰字，激活 `#efe9de` 底
- 特性卡 `.feature-grid`：奶油卡 `#efe9de`，auto-fill ≥14rem 自适应列数，32px 内边距
- 平台卡 `.card-grid`：画布底 + hairline 边 + hairline→灰的 hover，auto-fill ≥13rem
- 图片占位 `.ph-img`：浅奶油底 + 虚线 hairline 框（替代真实截图）

### 右侧目录 `.toc`
- sticky 独立滚动；标题同 caption-uppercase 风格
- 层级缩进 `.lvl2` 固定 14px；当前行：2px 珊瑚左标 + 墨字（全页唯一珊瑚线条）

### 页脚 `.site-footer`
- 深墨 `#181715` + 64px 内边距（footer 规范），仅一行版权：`© 2026 AomeNero`（GitHub 链接，奶油白 hover 下划线）

## 四、响应式

| 断点 | 行为 |
|------|------|
| ≥1280px | 三栏齐全：288 + 816 + 240 精确成立，内容列左右 padding 32px |
| 1024–1279px | 隐藏 TOC，双栏；内容列由 `max-width:816px` 封顶居中 |
| <1024px | 隐藏侧栏（无 JS 汉堡菜单，直接收起）+ 主导航，单栏通栏 |
| <768px | h1 降为 32px/−0.5px |

锚点跳转：`h2/h3/h4 { scroll-margin-top: header-h + 16px }`——无 JS 实现锚点避开吸顶顶栏。

## 五、可复用要点（搭同类页面照抄）

1. **变量集中**：颜色/圆角/间距/尺寸五组令牌全在 `:root`，改一处全局生效
2. **三栏公式**：外框 = 侧栏 + 中列 + 目录 + 2×内容 padding；三者联动，单独改中列必被外框吃掉
3. **`min-width:0` 纪律**：flex 中列必须加，否则 `pre` 长行撑爆布局
4. **双 sticky**：侧栏与 TOC 各自 `top: var(--header-h)` + 独立 `overflow-y`
5. **珊瑚配额**：CTA/徽章/链接/当前位标记四种用途封顶，别的地方用奶油色阶
6. **深墨节奏**：代码窗与页脚两个深色块收尾，与奶油画布形成页面呼吸（DESIGN.md 的 pacing 机制）
7. **无 JS 交互替代**：页签压平为静态分节；锚点偏移用 `scroll-margin-top`；移动端直接隐藏次级导航
