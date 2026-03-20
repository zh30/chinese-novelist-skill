# Narrative Rhythm Curve Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add narrative rhythm curve system to SKILL.md and create standalone template.

**Architecture:**
1. Update SKILL.md - add narrative rhythm curve section
2. Create `references/07-叙事节奏曲线.md` template

**Tech Stack:** Plain Markdown files.

---

## Task 1: Update SKILL.md - Add Narrative Rhythm Curve Section

**Files:**
- Modify: `SKILL.md`

**Step 1: Find insertion point**

Find a good location. Consider adding after "## 出版门控" or in the Planning Rules section.

**Step 2: Insert the new section**

```markdown
## 叙事节奏曲线

设计全书的紧张程度起伏，确保节奏有峰有谷，避免越写越平。

### 选择曲线类型

根据你的故事类型，选择一种节奏曲线：

**A. 递进型** — 紧张度持续上升
适用：升级流、复仇流、打怪升级

**B. 波浪型** — 紧张度波浪起伏
适用：悬疑、探险、探险解密

**C. 高原型** — 紧张度保持中高水平
适用：都市、职场、情感

**D. 反转型** — 开头紧张，结局更紧张
适用：宫斗、权谋、阴谋

### 关键节点

每个故事必须有这些关键节点：

| 节点 | 位置 | 紧张度 | 必须元素 |
|------|------|--------|----------|
| 开篇钩子 | 第1章 | ★★★☆ | 危机/悬念/目标 |
| 第一个小高潮 | 前10% | ★★★☆ | 小胜利或小失败 |
| 中点转折 | 50% | ★★★★★ | 认知翻转/重大失败 |
| 中段升级 | 60-70% | ★★★★☆ | 代价增大 |
| 倒数第二个高潮 | 85% | ★★★★★ | 终极选择 |
| 结局 | 100% | ★★★★★ | 终极对决/终极选择 |

### 曲线跟踪

每写完5章，对照设计检查紧张度：

- 紧张度低于设计 → 需要加强
- 紧张度高于设计 → 可能太快，需要喘息

**详细模板：** [references/07-叙事节奏曲线.md](references/07-叙事节奏曲线.md)
```

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: add narrative rhythm curve section to SKILL.md

Add ## 叙事节奏曲线 section with:
- Curve type selection (递进/波浪/高原/反转)
- Key node definitions (6 nodes with position/tension/elements)
- Curve tracking method
- Reference to 07-叙事节奏曲线.md template

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Create 07-叙事节奏曲线.md Template

**Files:**
- Create: `references/07-叙事节奏曲线.md`

**Step 1: Write the template**

```markdown
# 叙事节奏曲线

> 设计全书的紧张程度起伏，确保节奏有峰有谷。

## 选择的曲线类型

- [ ] 递进型 — 紧张度持续上升
- [ ] 波浪型 — 紧张度波浪起伏
- [ ] 高原型 — 紧张度保持中高水平
- [ ] 反转型 — 开头紧张，结局更紧张

**曲线图示：**

```
紧张度：
★

★

★

★                              ★
第1章 →                    → 结局
```

## 关键节点规划

| 节点 | 目标章节 | 紧张度目标 | 必须元素 | 状态 |
|------|----------|-----------|----------|------|
| 开篇钩子 | 第1章 | ★★★☆ | | ⬜ |
| 第一个小高潮 | 第X章 | ★★★☆ | | ⬜ |
| 中点转折 | 第X章 | ★★★★★ | | ⬜ |
| 中段升级 | 第X章 | ★★★★☆ | | ⬜ |
| 倒数第二个高潮 | 第X章 | ★★★★★ | | ⬜ |
| 结局 | 终章 | ★★★★★ | | ⬜ |

## 节奏曲线跟踪表

每写完5章，记录实际紧张度，对照设计检查：

| 检查点 | 章节范围 | 设计紧张度 | 实际紧张度 | 差距 | 调整建议 |
|--------|----------|-----------|-----------|------|----------|
| 第1次 | 第1-5章 | ★★★☆ | | | |
| 第2次 | 第6-10章 | | | | |
| 第3次 | 第11-15章 | | | | |
| 第4次 | 第16-20章 | | | | |
| ... | ... | | | | |

## 各阶段紧张度要求

### 第一阶段（前25%）
- 建立紧张承诺
- 设置主要冲突
- 紧张度：★★☆ ~ ★★★☆

### 第二阶段（25%-50%）
- 逐步升级紧张
- 建立节奏：紧张→喘气→紧张
- 紧张度：★★☆ ~ ★★★★☆

### 第三阶段（50%-75%）
- 中点必须最高或次高
- 代价明显增大
- 紧张度：★★★☆ ~ ★★★★★

### 第四阶段（75%-结局）
- 持续高紧张
- 逐步推向终极高潮
- 紧张度：★★★★☆ ~ ★★★★★

## 常见问题处理

| 问题 | 表现 | 解决方案 |
|------|------|----------|
| 中段疲软 | 紧张度持续走低 | 增加新冲突/角色介入 |
| 高潮太早 | 中段就到达顶峰 | 延迟关键揭示/增加阻碍 |
| 结局平 | 最终对决不够紧张 | 增强代价/增加反转 |
| 节奏单调 | 一直同样的紧张度 | 增加喘息场景/支线起伏 |
```

**Step 2: Commit**

```bash
git add references/07-叙事节奏曲线.md
git commit -m "feat: add narrative rhythm curve template

Add references/07-叙事节奏曲线.md:
- Curve type selection with 4 patterns
- Key nodes table (6 nodes with position/tension/elements)
- Rhythm curve tracking table
- Phase-based tension requirements (4 stages)
- Common problems and solutions

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Update SKILL.md - add 叙事节奏曲线 section | ⬜ |
| 2 | Create references/07-叙事节奏曲线.md | ⬜ |
