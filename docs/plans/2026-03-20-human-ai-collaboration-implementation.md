# Human-AI Collaboration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add human-AI collaboration system to SKILL.md and create standalone template.

**Architecture:**
1. Update SKILL.md - add human-AI collaboration section
2. Create `references/08-人机协作.md` template

**Tech Stack:** Plain Markdown files.

---

## Task 1: Update SKILL.md - Add Human-AI Collaboration Section

**Files:**
- Modify: `SKILL.md`

**Step 1: Find insertion point**

Consider adding after "## 叙事节奏曲线" or in a logical workflow position.

**Step 2: Insert the new section**

```markdown
## 人机协作

当用户以人机混合方式写作时，按以下指南执行：

### 协作分工

| 内容类型 | 人类写 | AI 写 | 说明 |
|----------|--------|--------|------|
| 核心设定 | ✅ | | 人物性格、核心冲突、底线 |
| 关键情节 | ✅ | | 重大转折、结局设计 |
| 对白风格 | ✅ | | 人物语言特点 |
| 具体场景 | | ✅ | 场景描写、环境渲染 |
| 过渡衔接 | | ✅ | 章节之间的过渡 |
| 扩写 | | ✅ | 已有大纲的详细内容展开 |
| 修改 | ✅ | | 明确指出问题所在 |

### 上下文传递

每次让 AI 继续写之前，必须传递上下文：

```markdown
## 当前进度
- 章节：第X章
- 当前场景：...
- 主要人物：...
- 上文关键事件：...

## 写作要求
- 继续写：...（具体说明要写什么）
- 风格参考：...（文风要求）
- 注意：...（特别注意事项）
```

### 交接协议

人类修改完一段后，告诉 AI：

```markdown
## 人类修改记录
- 修改位置：第X章 第Y段
- 修改原因：...
- 继续要求：...

## 上一段结尾
"..."（引用上段结尾，让 AI 接上）
```

**详细模板：** [references/08-人机协作.md](references/08-人机协作.md)
```

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: add human-AI collaboration section to SKILL.md

Add ## 人机协作 section with:
- Collaboration division (what humans vs AI should write)
- Context passing mechanism
- Handoff protocol for human modifications
- Reference to 08-人机协作.md template

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Create 08-人机协作.md Template

**Files:**
- Create: `references/08-人机协作.md`

**Step 1: Write the template**

```markdown
# 人机协作

> 本文件用于人机混合写作时的上下文传递和风格参考。

## 协作分工

### 人类负责

- [ ] 核心设定（人物性格、核心冲突、底线）
- [ ] 关键情节（重大转折、结局设计）
- [ ] 对白风格定义（人物语言特点）
- [ ] 修改（明确指出问题所在）

### AI 负责

- [ ] 具体场景描写
- [ ] 环境渲染
- [ ] 过渡衔接
- [ ] 大纲扩写

## 上下文传递

当需要 AI 继续写作时，填写以下内容：

```markdown
## 当前进度
- 章节：第X章
- 当前场景：
- 主要人物：
- 上文关键事件：

## 写作要求
- 继续写：
- 风格参考：
- 注意：
```

## 风格参考

### 角色对白风格

| 角色 | 对白特点 | 示例 |
|------|----------|------|
| 主角 | ... | "..." |
| 配角A | ... | "..." |

### 场景描写风格

| 场景类型 | 描写要点 | 示例 |
|----------|----------|------|
| 室内 | ... | "..." |
| 户外 | ... | "..." |
| 战斗 | ... | "..." |

## 交接记录

当人类修改完一段后，记录：

```markdown
## 人类修改记录
- 修改位置：第X章 第Y段
- 修改原因：
- 继续要求：

## 上一段结尾
"..."
```

### 修改历史

| 日期 | 位置 | 修改内容 | 后续要求 |
|------|------|----------|----------|
| ... | ... | ... | ... |
```

**Step 2: Commit**

```bash
git add references/08-人机协作.md
git commit -m "feat: add human-AI collaboration template

Add references/08-人机协作.md:
- Collaboration division (human vs AI responsibilities)
- Context passing template
- Style reference (character dialogue, scene descriptions)
- Handoff record template with history

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Update SKILL.md - add 人机协作 section | ⬜ |
| 2 | Create references/08-人机协作.md | ⬜ |
