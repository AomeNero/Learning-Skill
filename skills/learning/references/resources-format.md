# resources.md 格式

`resources.md` 位于工作区的 `docs/` 子目录，是本主题策展的可信来源**全清单**（最佳来源的全文已沉淀在 `library/`）。讲解用的知识应取自这里，而不是参数化记忆的猜测。智慧则来自这里列出的社区。

**格式遵循 Obsidian Flavored Markdown**——创建与编辑时参照 `obsidian-markdown` 技能的语法约定（wikilink、tag、callout 等）。

## 模板

```md
---
title: "{主题}——资源清单"
tags:
  - "resources"
  - "{主题slug}"
created: 2026-10-03
---

# {主题} 资源

## 知识

- [书：《力量训练的科学与实践》（Zatsiorsky & Kraemer）](https://example.com)
  关于训练计划与适应的基础文本。用于：周期化、恢复、强度区间的所有问题。
  > 最佳来源全文 → [[0001-zatsiorsky-book|library 条目]]

- [文章："我该练多少？"（Greg Nuckols，Stronger By Science）](https://example.com)
  基于证据的容量地标综述。用于：各肌群的每周组数目标。

## 智慧（社区）

- [r/weightroom](https://reddit.com/r/weightroom)
  高信噪比的 subreddit，严格治理 bro-science。用于：训练计划批评、平台期排障。
- 线下：{健身房名字} 周二力量课
  用于：训练动作的实时教练反馈。

## 缺口

> [!warning] 缺少恢复与睡眠的权威来源——下次摸底优先补。

## 备注

> 学习者拒绝加入社区（2026-10-03 记录，不再反复提议）。
```

## YAML 字段

| 字段 | 说明 |
|------|------|
| `title` | Obsidian 属性面板显示标题 |
| `tags` | Obsidian 标签（`resources` + 主题 slug） |
| `created` | 创建日期 |

## 规则

- **只收高可信来源。** 优先一手来源、公认专家、同行评审的工作、有严格治理的社区。
- **每条都要注释。** 光秃秃的链接三个月后毫无用处。加一行：它覆盖什么、什么时候该用它。
- **最佳来源 wikilink 到 library/。** 全文已转存的条目，在注释末尾加 wikilink 引用（如 `[[0001-xxx|library 条目]]`）。
- **按知识 / 智慧分组。** 呼应 [SKILL.md](../SKILL.md) 中的哲学。一个资源只出现在一个组里也完全可以。
- **缺口用 callout。** `> [!warning]` 显式标出——Obsidian 渲染醒目，驱动未来搜索。
- **社区偏好记在备注节。** 学习者拒绝加入社区时记一行，后续会话不再反复提议。
- **无情修剪。** 五个锋利的来源好过三十个平庸的。
- **创建与编辑时使用 `obsidian-markdown` 技能**——确保 YAML、wikilink、callout 语法正确。
