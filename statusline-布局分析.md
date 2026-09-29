# statusline.html 布局分析

> 来源：`https://code.claude.com/docs/zh-CN/statusline`（Claude Code Docs · 中文版）
> 页面框架：**Mintlify** 文档系统（Next.js + Tailwind CSS）
> 文件大小：1.4 MB（单文件，样式/脚本在线加载）

---

## 一、整体骨架：经典三栏文档布局

```
┌─────────────────────────────────────────────────────────┐
│  <header>  顶栏  h-16 · fixed → lg:sticky · z-30        │
│  logo | 搜索(Ctrl+K) | 导航链接 | 主题切换                │
├──────────┬──────────────────────────────┬───────────────┤
│ <nav>    │  <main>  lg:flex-1           │  <nav.toc>    │
│ 左侧栏    │  max-w-8xl mx-auto           │  右侧目录      │
│ w-[18rem]│   └─ 正文列 max-w-3xl        │  sticky       │
│ sticky   │                              │  "在此页面"    │
│          │  页头(h1+简介)                │  滚动高亮      │
│          │  MDX 正文(prose)              │               │
├──────────┴──────────────────────────────┴───────────────┤
│  <footer.advanced-footer>  border-t · 居中纵向排列        │
└─────────────────────────────────────────────────────────┘
```

## 二、各区域明细

### 1. 顶栏 `<header>`

- 定位：`z-30 fixed lg:sticky top-0 w-full`——移动端固定，桌面端吸顶
- 高度 `h-16`（64px），内部 `flex items-center` + `border-b` 底部细分割线
- 关键机制：`peer` 类——header 作为 peer 兄弟节点，供下方布局感知其存在
- 内容：logo、搜索入口（Ctrl+K）、水平导航链接、主题切换、社交图标（页面共 119 个内联 SVG，多为此类小图标）

### 2. 左侧栏 `<nav>`

- `hidden lg:block`：移动端隐藏（汉堡菜单唤出），`lg` 起显示
- `sticky self-start shrink-0`，宽度 `w-[18rem]`（288px）
- 吸顶偏移用 CSS 变量：`top-[calc(var(--mintlify-slot-header-height)+…)]`——避开顶栏高度
- 本页含 **18 个文档链接**（设置文件和优先级 → … → 自定义快捷键），当前页高亮

### 3. 主内容区 `<main>`

- `lg:flex-1 lg:min-w-0`：flex 弹性占据剩余宽度，`min-w-0` 防止代码块撑破
- 两层宽度控制：外层 `max-w-8xl mx-auto` 居中 → 正文列 `max-w-3xl`（约 768px）
- **页头**：`header.@container/page-header`——h1 标题 + `prose text-lg` 简介段
- **正文容器**：`mdx-content.prose.prose-gray.dark:prose-invert`
  - Tailwind Typography 插件接管全部元素排版
  - `[contain:inline-size]` + `@container/columns-container`：**容器查询**，按内容区宽度（非视口）响应
- 本页正文构成：35 个代码块、2 个表格、h1–h4 四级标题

### 4. 右侧目录 `<nav class="toc">`

- sticky 右栏，标题"在此页面"
- 层级缩进用变量：`pl-[calc(var(--toc-padding-left)+var(--toc-focus-padding,0rem))]`，每级 `--toc-padding-left` 递增 1rem
- 滚动监听高亮：`li[data-active]` 控制当前小节着色
- 本页目录：设置状态行 / 逐步构建状态行 / 状态行如何工作 / 可用数据 / 示例（7 个子节）/ 子代理状态行 / 提示 / 故障排除

### 5. 页脚 `<footer>`

- `advanced-footer`：`flex flex-col items-center mx-auto border-t`
- 简单的居中纵向布局，顶部一条分割线

## 三、响应式策略

| 断点 | 行为 |
|------|------|
| `< lg`（移动/平板） | 根容器 `max-lg:contents`——取消 flex，各区纵向堆叠；侧栏与 TOC 隐藏，正文通栏 |
| `≥ lg` | 三栏 flex：`18rem` 侧栏 + 弹性正文 + TOC 右栏，双 sticky（侧栏、TOC 各自吸顶） |

## 四、暗色模式

- Tailwind `dark:` 变体全量覆盖（`dark:text-gray-400`、`dark:prose-invert`、`dark:border-gray-300/[0.06]` 等）
- `@media (prefers-color-scheme: dark)` 媒体查询 + class 切换双轨实现

## 五、可复用的模板要点

1. **高度联动**：侧栏/TOC 的 `top` 不写死，而是引用 `--mintlify-slot-header-height` 变量——换顶栏高度无需改布局代码
2. **`min-w-0` 纪律**：flex 子项（正文列）必须加，否则长代码行会把三栏撑爆
3. **代码块标配**：每个 `<pre>` 配复制按钮（本页 21 个，`aria-label="复制"`）+ 语言标签
4. **标题锚点**：每个标题带零宽锚点链接（`#设置状态行` 等中文 slug），hover 显示 `#` 图标
5. **TOC 缩进**：用 CSS 变量做层级缩进而非硬编码 padding，配合 focus 态的 `--toc-focus-padding`
6. **双 sticky**：顶栏、左侧栏、右 TOC 三者均 sticky，各自独立滚动区域
7. **正文列宽度**：`max-w-3xl` 是长文阅读的最佳行宽上限，宽屏下靠 `mx-auto` 居中、两侧留白

## 六、本页内容结构（标题树）

```
h1 自定义你的状态行
├─ h2 设置状态行
│   ├─ h3 使用 /statusline 命令
│   ├─ h3 手动配置状态行
│   └─ h3 禁用状态行
├─ h2 逐步构建状态行
├─ h2 状态行如何工作
├─ h2 可用数据
│   ├─ h3 上下文窗口字段
│   ├─ h3 Prompt cache 字段
│   │   └─ h4 最后一次未命中原因
├─ h2 示例
│   ├─ h3 上下文窗口使用情况 / Git 状态与颜色 / 成本和持续时间跟踪
│   ├─ h3 显示多行 / 可点击链接 / 速率限制使用情况
│   └─ h3 缓存昂贵的操作 / Windows 配置
├─ h2 子代理状态行
├─ h2 提示
└─ h2 故障排除
```
