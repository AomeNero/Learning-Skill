# library/ 原始资料条目格式

`library/` 位于工作区根目录（与 `lessons/` 同级）。存放**网络下载的原始资料全文**——网页、文章、文档、规范、论文的完整 MD 转存。不做摘要压缩；原始内容照存，供教学引用与 Obsidian 全文搜索。

**格式遵循 Obsidian Flavored Markdown**——创建条目时参照 `obsidian-markdown` 技能的语法约定（wikilink、callout、tag、embed 等）。

## 模板

```md
---
title: "TCP 三次握手详解"
source: "https://example.com/tcp-handshake"
author: "张三"
published: 2025-06-15
created: 2026-10-03
description: "TCP 建立连接的三步握手过程，含状态迁移图"
tags:
  - "tcp"
  - "网络协议"
credibility: A
related:
  - "[[0002-packets-the-atom]]"
---

## TCP 三次握手详解

（原始资料全文——完整转存，不做删减或摘要）
```

## YAML 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✓ | 原文标题（Obsidian 属性面板显示） |
| `source` | ✓ | 原文 URL；书籍则写 ISBN+页码 |
| `author` | | 原文作者 |
| `published` | | 原文发布日期（YYYY-MM-DD） |
| `created` | ✓ | 入库日期（YYYY-MM-DD） |
| `description` | | 一句话描述（Obsidian 搜索与链接预览用） |
| `tags` | | Obsidian 标签数组（支持嵌套如 `网络/tcp`） |
| `credibility` | ✓ | `A` / `B` / `C`（见分级规则） |
| `related` | | wikilink 数组，关联 lessons/ 的课程文件 |

## 规则

- **全文照存**：原始内容完整转存为 Obsidian Flavored Markdown，不删减不摘要。
- **文件命名**：`0001-<中文标题>.md`，编号扫描现有最大加一。中文标题取原标题；原文非中文取简短中文译名；清理文件名非法字符（`\ / : " ? # | ^ [ ]`）。
- **直写入库**：条目由 researcher 子代理调研时直写（brief 必含 library/ 绝对路径），主会话返回后核实、缺则兜底补写。`agents/researcher.md` 内联了本格式的同步副本——**本文件为正本，改格式两处须同步**。
- **A/B 要求 ≥2 个独立来源交叉印证**；单源标 C——后续有新来源印证时升级。
- **课程引用时带可信度**：如 `> [!quote] 据 [TCP 握手规范（A）](source-url)` 或正文引用 `[[0001-tcp-spec-source|TCP 握手规范（A）]]`。
- **宁精不滥**：每个知识点只存 1-2 条最优质的原始资料。
- **创建条目时使用 `obsidian-markdown` 技能**——确保 wikilink、callout、tag、embed 等 Obsidian 语法正确。
