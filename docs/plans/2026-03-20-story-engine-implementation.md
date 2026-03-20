# Story Engine Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add independent `## 故事引擎` block to outline template with 3 subfields: core mechanism, cost/resources, escalation rules.

**Architecture:** Modify existing `outline-template.md` to insert new block between "项目定位" and "主线冲突". Update `SKILL.md` intake and planning guidance to emphasize story engine extraction.

**Tech Stack:** Plain Markdown edits only.

---

## Task 1: Update outline-template.md

**Files:**
- Modify: `references/outline-template.md`

**Step 1: Read current outline-template.md**

Read the file to understand current structure and find exact insertion point.

**Step 2: Insert story engine block after 项目定位 section**

Insert the following block after the 项目定位 section and before the 主线冲突 section:

```markdown
## 故事引擎

> 这一部分描述故事的核心驱动力。明确"引擎"比描述"主题"更能指导写作——读者追一本书的理由，往往是一个具体的机制，而不是一个抽象的主题。

### 核心机制
用一句话说清楚：这个故事靠什么驱动读者往下看？

**公式：** 主角必须___，每___就___。

**示例：** 「主角必须每破解一个暗号才能多活一天，每多用一次能力就失去一段记忆。」

**检验标准：** 如果说不出"读者为什么追下去"，这个字段就不够具体。

### 代价与资源
每行动一次，主角/世界要失去什么？什么资源是有限的？

**公式：** ___是有限的，每次___就会消耗___。

**示例：** 「每天只有一次解码机会。用尽后会被强制淘汰出游戏。」

### 升级规则
随着故事推进，代价如何递增？紧张感如何升级？

**公式：** 第N阶段，代价变成___。

**示例：** 「前10章代价是记忆，中10章代价是生命，后10章代价是身边人的命运。」

**检验标准：** 代价必须真的变重，不能只是"越来越难"。
```

**Step 3: Verify structure**

Confirm the new block sits correctly between 项目定位 and 主线冲突.

**Step 4: Commit**

```bash
git add references/outline-template.md
git commit -m "feat: add story engine block to outline template

Add independent ## 故事引擎 section with 3 subfields:
- 核心机制: story's core driving mechanism
- 代价与资源: cost/resource constraints
- 升级规则: escalation logic for tension

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Update SKILL.md - Intake Section

**Files:**
- Modify: `SKILL.md:43-52` (Intake section)

**Step 1: Read current intake section in SKILL.md**

Read lines 40-60 to find exact intake text.

**Step 2: Add story engine to intake questions**

Add story engine as a required intake item alongside the existing 6 questions:

Add to the intake list:
```
- 故事引擎（核心机制、代价/资源、升级规则）
```

And modify the surrounding text to explain why:

```markdown
- 故事引擎（核心机制、代价/资源、升级规则）
- 题材 / 子类型
- 一句话 premise 或核心冲突
- 主角身份、最大欲望、致命缺陷
- 目标读者、文风关键词、禁忌
- 叙事视角（第一人称 / 第三人称 / 群像）
- 篇幅目标与交付模式
```

**Step 3: Add explanatory note after the list**

Add:

```markdown
如果用户只给了模糊想法，不要空泛追问；应给出具体备选并推荐更稳的方案。

**关于故事引擎：** 如果用户说不清引擎，用引导问题帮助提炼：
- 「读者追这本书的理由是什么？是主角的成长？还是谜题解开的那一刻爽感？」
- 「主角每赢一次，代价是什么？代价会越来越大吗？」
- 「这个故事到最后，代价会大到什么程度？」
```

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "feat: add story engine to intake questions in SKILL.md

Add story engine extraction to required 7-item intake checklist.
Include guiding questions for helping users articulate their story engine.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 3: Update SKILL.md - 书名生成 Section

**Files:**
- Modify: `SKILL.md:54-96` (书名生成 section)

**Step 1: Read current 书名生成 section**

**Step 2: Add story engine reference before title generation**

The story engine is relevant because titles often reflect the core mechanism. Add a note:

In the 书名生成 section, after the 标题结构参考 table, add:

```markdown
### 生成流程

1. 分析**故事引擎**（核心机制、代价、升级规则）—— 书名往往暗示机制
2. 提取 2-3 个关键词作为标题元素
3. 运用上表中的结构，组合生成 5 个以上候选
4. 评估每个候选的：独特性、画面感、与主题的关联度
5. 精选 3-5 个最佳选项，每项附上一句话说明推荐理由
6. 让用户最终确认书名
```

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: link story engine to title generation in SKILL.md

Add story engine analysis as first step in title generation workflow.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 4: (Optional) Update plot-structures.md

**Files:**
- Modify: `references/plot-structures.md`

**Step 1: Read current plot-structures.md**

**Step 2: Add "识别故事引擎" section**

Add a new section at the end or near the beginning:

```markdown
## 如何识别故事引擎

写大纲之前，先问自己三个问题：

### 1. 核心机制是什么？
「这个故事靠什么让读者翻页？」
- 不是"成长"或"复仇"这种主题
- 而是具体的、可描述的机制
- 例如：「每回答一个谜题就能多活一天」

### 2. 代价是什么？
「每行动一次，要失去什么？」
- 代价必须是读者能感知到的
- 不能是无关痛痒的代价
- 例如：「记忆」、「时间」、「身边人」

### 3. 代价如何升级？
「故事越往后，代价怎么变得更重？」
- 前10章的代价 vs 后10章的代价
- 如果代价不升级，故事会越写越疲
```

**Step 3: Commit (if modified)**

```bash
git add references/plot-structures.md
git commit -m "docs: add story engine identification guide to plot-structures

Add section on how to identify story engine before writing outline.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | File | Status |
|------|------|--------|
| 1 | `references/outline-template.md` | ⬜ |
| 2 | `SKILL.md` (Intake) | ⬜ |
| 3 | `SKILL.md` (书名生成) | ⬜ |
| 4 | `references/plot-structures.md` (optional) | ⬜ |
