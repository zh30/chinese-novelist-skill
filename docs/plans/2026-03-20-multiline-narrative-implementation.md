# Multi-Line Narrative Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create standalone multi-line narrative management template and update SKILL.md to reference it.

**Architecture:**
1. Create `references/03-多线管理.md` template file
2. Update `SKILL.md` Required Files section to reference it

**Tech Stack:** Plain Markdown files only.

---

## Task 1: Create 03-多线管理.md Template

**Files:**
- Create: `references/03-多线管理.md`

**Step 1: Write the template file**

Create the file with the following content:

```markdown
# 多线叙事管理

> 本模板适用于群像、多视角或多叙事线的小说。如果你的小说是单线叙事，可以跳过此文件。

## 叙事线总览

| 叙事线 | 核心人物 | 主要目标 | 预计占比 |
|--------|----------|----------|----------|
| 主线 | 主角 | 核心冲突 | 50% |
| 副线A | 配角X | 支线目标1 | 20% |
| 副线B | 配角Y | 支线目标2 | 20% |
| 暗线 | 反派 | 潜伏目标 | 10% |

**占比说明：** 占比是指该线在全书总字数中的比例。可根据实际调整，但单线不宜低于10%（太低会被读者遗忘）。

## 篇幅分配规则

### 主线与副线关系
- 主线贯穿全书，始终是核心驱动力
- 副线在特定阶段成为临时主线（如"复仇线"在复仇阶段）
- 暗线只在关键时刻出现，但必须贯穿全书

### 分配原则
- 主线：每3-5章必须有明显推进
- 副线A/B：每5-8章必须出现一次
- 暗线：每10章至少铺垫一次
- **任何单线连续消失不得超过10章**

## 线状态跟踪

### 状态定义

| 状态 | 含义 |
|------|------|
| 活跃 | 当前章节有该线的戏份 |
| 铺垫 | 该线暂时退居幕后，但仍有时机出现 |
| 悬空 | 该线超过8章没出现，需要尽快安排 |
| 回收 | 该线进入收束阶段，准备交汇 |
| 完成 | 该线已解决，等待交汇 |

### 跟踪表

| 叙事线 | 当前状态 | 最后出现章节 | 备注 |
|--------|----------|--------------|------|
| 主线 | 活跃 | 第X章 | ... |
| 副线A | 铺垫 | 第X章 | ... |
| 副线B | 悬空 | 第X章 | 连续消失8章，需要安排 |
| 暗线 | 活跃 | 第X章 | ... |

**更新频率：** 每次写完新章节后更新此表。

## 视角切换规则

### 视角类型
- **第一人称** — "我看到了..."
- **有限第三人称** — "他看到了..."（只能知道该人物所知）
- **全知第三人称** — 叙述者什么都知道

### 切换时机
- **允许切换：** 新场景开始、同一场景内时间跳跃、POV人物完成任务
- **避免切换：** 冲突进行中、情感高潮点、关键信息刚揭露
- **切换警示：** 单章节内视角切换超过3次需要检查是否必要

### 视角占比参考

| 叙事线 | 推荐视角 | 占比控制 |
|--------|----------|----------|
| 主线 | 有限第三人称 | 该线章节的80%以上 |
| 副线 | 可根据需要选择 | 该线章节的70%以上 |

## 交汇设计

### 交汇节点

在章节规划时，预先标记关键交汇节点：

| 交汇节点 | 涉及叙事线 | 交汇方式 | 章节 |
|----------|-----------|----------|------|
| 第一次交汇 | 主线+副线A | 人物相遇 | 第X章 |
| 第二次交汇 | 主线+副线A+副线B | 目标冲突 | 第X章 |
| 第三次交汇 | 所有线 | 高潮对决 | 终章 |

### 交汇原则
- 交汇前每条线必须有至少一次"准备"（让读者知道这条线要来了）
- 交汇时要有"原来如此"的揭示感
- 交汇点不要超过3条线同时交汇（会乱）

## 健康检查

每写完5-10章，做一次多线健康检查：

### 检查项
- [ ] 每条线是否按计划推进？
- [ ] 是否有某条线超过10章没出现？
- [ ] 视角切换是否混乱？
- [ ] 交汇节点是否按计划执行？
- [ ] 各线目标是否与主线冲突有交集？

### 常见问题处理

| 问题 | 解决方案 |
|------|----------|
| 某条线写太多了 | 砍场景，把篇幅转移给其他线 |
| 某条线消失了 | 安排一次"意外相遇"或"信息传递" |
| 交汇太早 | 延迟交汇，增加铺垫 |
| 交汇太晚 | 提前合并，减少支线章节 |
```

**Step 2: Commit**

```bash
git add references/03-多线管理.md
git commit -m "feat: add multi-line narrative management template

Add standalone 03-多线管理.md for managing multi-POV novels:
- 叙事线总览: line overview with allocation percentages
- 篇幅分配规则: main/sub/hidden line relationships
- 线状态跟踪: state definitions and tracking table
- 视角切换规则: when/how to switch POV
- 交汇设计: convergence nodes and principles
- 健康检查: periodic review checklist

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Update SKILL.md Required Files

**Files:**
- Modify: `SKILL.md`

**Step 1: Find Required Files section**

Read SKILL.md to find the "## Required Files" section.

**Step 2: Add multi-line management reference**

Find the line with `第XX章-标题.md` and add after it:

```markdown
- `03-多线管理.md` → 使用 [references/03-多线管理.md](references/03-多线管理.md)（仅多线叙事小说需要）
```

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: reference multi-line management template in SKILL.md

Add reference to 03-多线管理.md in Required Files section,
noting it's only needed for multi-POV novels.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Create references/03-多线管理.md | ⬜ |
| 2 | Update SKILL.md Required Files | ⬜ |
