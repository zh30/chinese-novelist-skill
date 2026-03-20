# Quality Standards Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace abstract Quality Bar with concrete quality checklist in SKILL.md.

**Architecture:** Replace the existing "## Quality Bar" section with detailed "## 质量检查清单" including check items and quantitative indicators.

**Tech Stack:** Plain Markdown edits only.

---

## Task 1: Replace Quality Bar with 质量检查清单

**Files:**
- Modify: `SKILL.md`

**Step 1: Read SKILL.md to find Quality Bar section**

Read SKILL.md to find the "## Quality Bar" section and understand its current location and content.

**Step 2: Find and replace the section**

Find the `## Quality Bar` section and replace its content with the new quality checklist.

The new section should have the following content:

```markdown
## 质量检查清单

每章交付前，按以下清单自检。每项都有具体检查项和量化指标。

### 1. 变化原则
**原规则：** 本章发生了不能删除的变化

**检查项：**
- [ ] 主角做出了明确选择（不是被动接受）
- [ ] 关系状态发生了可感知的变化
- [ ] 世界状态（如果适用）发生了明确改变

**量化指标：**
- 至少有 1 个"选择"事件（主角主动决定做/不做某事）
- 至少有 1 个"状态变化"可被描述

---

### 2. 悬念原则
**原规则：** 回应、升级或偏转至少一条已有悬念

**检查项：**
- [ ] 本章提到了上章留下的悬念/问题
- [ ] 本章结尾留下了新的悬念/问题
- [ ] 至少有 1 条悬念被推进（不论是否解决）

**量化指标：**
- 章节内悬念提及次数 ≥ 1
- 新增悬念数 ≥ 1

---

### 3. 钩子原则
**原规则：** 结尾钩子强度与全书位置匹配

**检查项：**
- [ ] 结尾不是"顺嘴说完"，而是有"突然停下"的感觉
- [ ] 结尾留下了具体的问题/危险/悬念
- [ ] 结尾的紧张程度与章节在全书的位置匹配（前段轻，后段重）

**量化指标：**
- 结尾段落包含"悬念触发词"（突然、没想到、这时、结果...）
- 结尾句不是完整句式（以...、留下...、不知道...）

---

### 4. 展示原则
**原规则：** 人物通过动作、选择、对白被展示，而不是只被描述

**检查项：**
- [ ] 主要角色的情绪通过外在行为展示（不是"他很生气"）
- [ ] 对话中有人物动作/反应穿插（不只是"说"）
- [ ] 没有大段的"他说"+"她说"连续对话

**量化指标：**
- "他说"/"她说"等对话标签占比 < 30% 的对话段落
- 含有动作描写的对话段落 ≥ 50%

---

### 5. 文风原则
**原规则：** 避免空泛形容词堆砌、抽象情绪总结、整段均匀句式和过度书面腔

**检查项：**
- [ ] 没有连续 3 句以上的"他很X"、"她是Y"句式
- [ ] 没有大段情绪总结（如"他感到前所未有的孤独和绝望"）
- [ ] 句子长度有变化（不是每句都一样长）
- [ ] 没有过多的四字词/成语堆砌

**量化指标：**
- 连续相同句式不超过 3 句
- 单段"很X/很Y"形容词不超过 2 个
- 句长标准差 > 5（有一定变化）

---

### 6. 场景原则
**原规则：** 每个章节至少包含若干有任务的场景

**检查项：**
- [ ] 每个场景有明确的"任务"（不是"他们聊了聊天"）
- [ ] 场景之间有进展/转折/信息差
- [ ] 没有连续的场景只在同一个地点做同样的事

**量化指标：**
- 有明确任务的场景 ≥ 3 个
- 场景间有"信息差"或"状态变化"

---

**提示：** 量化指标是辅助验证，不是强制要求。如果字数达标但量化指标不合格，说明内容可能有水分。
```

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "refactor: replace Quality Bar with detailed 质量检查清单

Transform abstract quality rules into concrete checklist with:
- Specific check items per rule
- Quantitative indicators as auxiliary verification
- 6 rules: 变化/悬念/钩子/展示/文风/场景

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Replace Quality Bar with 质量检查清单 in SKILL.md | ⬜ |
