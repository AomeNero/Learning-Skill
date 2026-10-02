# Learning Skill 体检报告 v2——skill-doctor 实测版

> **日期**：2026-10-02 ｜ **对象**：`skills/learning`（8e2a015 深度重写版，158 行）+ 生态（visualize、agents）｜ **基准**：`/skill-doctor` 真实运行输出 + 《Skill 编写最佳实践.md》官方清单
>
> **方法**：`/skill-doctor` 经 `claude -p`（`MSYS_NO_PATHCONV=1`，规避 Git Bash 路径转换）真实运行，取得实测数据——这是与 v1 报告（纯人工核对）的本质区别。原始输出关键行见附录。

---

## 一、skill-doctor 实测数据

### learning 本体

| 指标 | 实测 | 解读 |
|------|------|------|
| **context** | **~90 tokens** | description 在系统提示中的每回合常驻成本。对比：browser-act ~300、skill-creator ~110、graphify ~120、git-commit ~30——90 属**中等偏优**。263 字符 description 换来触发词 + 让位条款的精确触发，性价比成立 |
| **7d tokens** | 2.5M | 近 7 天归因 token——全部来自本开发周期（7 次使用均为 today），是开发用量不是运行负担 |
| **uses** | 7× | 触发频次健康（近 7 天每天量级） |
| **加载状态** | userSettings 正常加载 | doctor **零报错**：无加载失败、无命名违规、无 frontmatter 异常 |

### 生态

| 对象 | context | 7d tokens | uses | 状态 |
|------|---------|-----------|-----|------|
| `visualize` | ~50 | 2.7M | 2× | ✓ 轻量正常 |
| `browser-act` | ~300 | 8.6M | 3× | ✓ 正常（协同技能，按需触发） |

**doctor 视角结论**：learning 及其直接生态无任何异常项。

## 二、官方清单复核（158 行重写版）

重写未引入新问题，全部项维持或改善：

| 检查项 | v1 判定 | 本次 | 说明 |
|--------|---------|------|------|
| name/description 合规 | ✓ | ✓ | frontmatter 未动 |
| SKILL.md ≤500 行 | ✓（263） | ✓（**158**） | 余量 68% |
| 术语一致 | ⚠→✓ | ✓ | "检索练习"单一术语，无"考核"残留 |
| 渐进披露 / 一层引用 | ✓ | ✓ | 4 链接全存在 |
| 无 Windows 路径 / 无时效信息 | ✓ | ✓ | |
| 工作流清晰步骤 | ✓ | ✓✓ | **新增优势：首尾结构**——开头五步执行地图（触发即读）、结尾红线清单 + 收尾三查（黄金位承载绝对约束），正利用 LLM 首尾注意力优势 |
| 反馈循环 | ⚠→✓ | ✓ | 产出即自检（check-lesson.py 13 项）已入流程 |
| 测试 | ✗ | 部分 ✓ | 冒烟全链路已过（v1 复查记录）；真实学习会话仍待首次进行 |

## 三、上轮修复验证（v1 全部发现项）

| v1 编号 | 修复 | 验证 |
|---------|------|------|
| C-1 内联指令缺口 | KaTeX 相对外链 + cp 指令 | ✓ 冒烟通过；红线清单 Never 明令"不读入上下文" |
| M-1 术语混用 | 全仓统一"检索练习" | ✓ 本次 grep 复核零残留 |
| M-2 零验证 | 冒烟全链路 + （待真实会话） | ✓ 可自动化部分完成 |
| M-3 无自检 | check-lesson.py + 流程闭环 | ✓ 模板自检 3 项报错属预期（占位符设计如此） |
| L-1 布局文档定位 | 移 docs/ | ✓ |
| L-2 katex 版本记录 | assets/katex/README.md | ✓ |

## 四、发现与建议

**无 CRITICAL / HIGH / MEDIUM 问题。** LOW 与观察项：

- **L-4（观察）**：description 263 字符的 context 成本（~90 tokens/回合）可再压缩，但触发精度优先于 token 经济——**不建议动**。当前让位条款（/eli5、graphify）是触发边界的价值来源。
- **E-1（环境建议，非技能问题）**：doctor 报告 11 个技能加载后从未调用（每回合占系统提示）与 4 个闲置插件（drawio 69 天、claude-hud 49 天、rust-analyzer-lsp 29 天、mattpocock-skills 24 天）。其中 **`diagram-design` 在未用列表**——若日后禁用它，learning 的"正式图示"场景走已有的"缺技能内联回退"分支，技能设计已兼容，无阻断。
- **待办延续**：真实学习会话端到端验收（v1 M-2 尾项）仍是唯一未闭环项——所有机制已就绪，建议近期开一场真实会话。

## 五、结论

**learning 技能处于健康状态**：doctor 实测零异常、官方清单全绿、v1 修复全部落地、重写版结构利用首尾注意力优势。技能侧无待修项；剩余动作是使用侧的（真实会话验收 + 可选的环境清理）。

---

## 附录：/skill-doctor 原始输出（learning 相关行）

```
  skill          source        context  7d tokens  uses  last used
  learning       userSettings    ~90       2.5m      7×   today
  visualize      userSettings    ~50       2.7m      2×   today
  browser-act    userSettings   ~300       8.6m      3×   today

  context = this skill's one-line listing in the system prompt, included every turn
  7d tokens = tokens attributed to the skill over the last 7 days of sessions

11 skills loaded but never invoked. Each one adds to the system prompt every turn.
Plugins not used recently: drawio (69d), claude-hud (49d), rust-analyzer-lsp (29d), mattpocock-skills (24d)
```

> 复现方法：`MSYS_NO_PATHCONV=1 claude -p "/skill-doctor"`（Git Bash 下必须禁用路径转换，否则 `/skill-doctor` 被展开为 `C:/Program Files/Git/skill-doctor`）
