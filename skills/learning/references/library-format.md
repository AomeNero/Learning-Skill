# library/ 原始资料条目格式

`library/` 位于工作区根目录（与 `lessons/` 同级）。存放**网络下载的原始资料全文**——网页、文章、文档、规范、论文的完整 MD 转存。不做摘要压缩；原始内容照存，供教学引用与 Obsidian 全文搜索。

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

（原始资料全文——完整转存网页/文章/文档内容，不做删减或摘要）
```

## YAML 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✓ | 原文标题 |
| `source` | ✓ | 原文 URL；书籍则写 ISBN+页码 |
| `author` | | 原文作者（有则填） |
| `published` | | 原文发布日期（YYYY-MM-DD） |
| `created` | ✓ | 入库日期（YYYY-MM-DD） |
| `description` | | 一句话描述（Obsidian 搜索用） |
| `tags` | | Obsidian 标签数组 |
| `credibility` | ✓ | `A`（一手/官方规范）、`B`（公认专家/权威社区）、`C`（单一来源待交叉印证） |
| `related` | | wikilink 数组，关联到 lessons/ 的课程文件 |

## 规则

- **全文照存**：原始内容完整转存为 Markdown，不删减不摘要——摘要/要点由教学时按需提取，不固化在 library 条目里。
- **文件命名**：`0001-<dash-case-name>.md`，编号扫描现有最大加一。
- **A/B 要求 ≥2 个独立来源交叉印证**；单源标 C——后续有新来源印证时升级。
- **课程引用时带可信度**：如"据 [TCP 握手规范（A）](source-url)"。
- **宁精不滥**：每个知识点只存 1-2 条最优质的原始资料；全部可用来源管在 resources.md。
