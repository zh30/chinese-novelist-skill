# Writing Modes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add dual-mode writing loop to SKILL.md: draft mode (fast output) vs polish mode (full quality checks).

**Architecture:** Insert new "写作模式选择" section and draft mode steps into SKILL.md. Rename existing Chapter Loop to "精修模式".

**Tech Stack:** Plain Markdown edits only.

---

## Task 1: Add 写作模式选择 Section

**Files:**
- Modify: `SKILL.md`

**Step 1: Read SKILL.md to find insertion point**

Read the file to find where "Default Working Mode" ends and where "Chapter Loop" begins.

**Step 2: Find the location**

The new section should be inserted between:
- End of "Default Working Mode" section
- Start of "Chapter Loop" section

**Step 3: Insert the following content:**

```markdown
## 写作模式选择

根据当前阶段选择合适的写作模式：

| 阶段 | 推荐模式 | 核心目标 |
|------|----------|----------|
| 第一遍起草 | 草稿模式 | 快速输出，不打断创作流 |
| 修改某一章 | 精修模式 | 逐项检查，打磨质量 |
| 写完所有章节后通读 | 精修模式 | 整体检查前后一致性 |

**判断规则：**
- 用户说"起草"、"初稿"、"先写"、"快速输出" → 草稿模式
- 用户说"修改"、"打磨"、"精修"、"检查质量" → 精修模式
- 不明确时默认精修模式
```

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "feat: add writing mode selection guidance to SKILL.md

Add dual-mode concept: draft mode (fast output) vs polish mode (full checks).
Include decision rules for mode selection.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Rename Chapter Loop to 精修模式

**Files:**
- Modify: `SKILL.md`

**Step 1: Find the "## Chapter Loop" header**

Read SKILL.md to find the line containing "## Chapter Loop".

**Step 2: Rename it**

Change `## Chapter Loop` to `## 精修模式`.

**Step 3: Add a brief intro sentence**

After the renamed header, add:

```markdown
精修模式适用于草稿完成后的质量打磨。每个步骤都必须执行。
```

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "feat: rename Chapter Loop to 精修模式

Mark existing chapter loop as polish mode for quality refinement.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 3: Add 草稿模式 Section

**Files:**
- Modify: `SKILL.md`

**Step 1: Read SKILL.md to find insertion point**

Find where to insert the draft mode section. It should be placed either:
- Right before "## 精修模式" (newly renamed Chapter Loop)
- Or in the "写作模式选择" section

**Step 2: Insert the following content before "## 精修模式":**

```markdown
## 草稿模式

草稿模式适用于第一遍快速写作。核心原则：**写出来比写对更重要**。

### 什么时候用
- 用户说"起草第X章"、"先写个初稿"、"快速输出"
- 项目处于初期阶段，需要快速堆字数

### 步骤（简化版）

1. **直接开始写** — 不读大纲、不拆场景、不查参考文档
2. **写完后字数检查** — 运行 `python3 scripts/check_chapter_wordcount.py <章节文件路径>`
3. **标记完成** — 写入章节摘要，进入下一章草稿

### 注意事项
- 草稿阶段不要停下来修改错别字或不通顺的句子——标注出来，写完再统一改
- 不要回头重读上一章——写完就是写完了
- 字数达标（≥3000字）即表示草稿完成
```

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: add draft mode (草稿模式) to SKILL.md

Add simplified draft mode with 3 steps: write directly, check word count, mark done.
Designed for fast output without interrupting creative flow.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Add 写作模式选择 section | ⬜ |
| 2 | Rename Chapter Loop to 精修模式 | ⬜ |
| 3 | Add 草稿模式 section | ⬜ |
