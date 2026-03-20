# Research Material Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add research material phase to workflow with SKILL.md updates and new template.

**Architecture:**
1. Update SKILL.md - add research phase between 策划模式 and 试写模式
2. Create `references/04-素材积累.md` template

**Tech Stack:** Plain Markdown files.

---

## Task 1: Update SKILL.md - Add Research Phase

**Files:**
- Modify: `SKILL.md`

**Step 1: Read SKILL.md to find insertion point**

Find the "Default Working Mode" section and locate where 试写模式 is mentioned. The new section should be inserted after 策划模式 completes but before 试写模式 begins.

**Step 2: Find the relevant text**

Look for the list that includes:
```
1. `策划模式`：只做题材定位...
2. `试写模式`：策划完成后，只写首章或样章
```

**Step 3: Add a new section after the Default Working Mode section**

After the text about "新项目默认策划模式" and "已有章节的项目默认连载模式", add:

```markdown
## 素材积累

在正式写作前，针对所写题材进行资料收集和整理。

**触发条件：**
- 题材涉及专业领域（医疗、法律、历史、职场等）
- 用户不确定是否了解足够的背景知识
- 用户主动要求"做功课"

### 工作流程

**第一步：确定素材范围**
- 根据题材类型，列出需要研究的领域
- 参考 [04-素材积累.md](references/04-素材积累.md) 的题材素材清单

**第二步：收集素材**
- 网络搜索、阅读相关书籍
- 采访相关从业者（如适用）
- 实地考察（如适用）

**第三步：整理素材**
- 按模板结构整理到 `novels/<书名>/04-素材积累.md`
- 标记"必须准确"vs"可以虚构"的内容

**第四步：验证素材**
- 检查关键细节是否准确
- 确保没有常识性错误
- 标注敏感内容（如有）

**原则：**
- 真实细节增加可信度，但不需要成为专家
- 可以虚构的部分要明确标记
- 写完记得更新素材文件
```

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "feat: add research material phase to SKILL.md

Add ## 素材积累 section between 策划模式 and 试写模式:
- Trigger conditions for when to do research
- 4-step workflow (identify scope, collect, organize, verify)
- Reference to 04-素材积累.md template

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Create 04-素材积累.md Template

**Files:**
- Create: `references/04-素材积累.md`

**Step 1: Write the template**

```markdown
# 素材积累

> 本文件用于整理写作所需的领域知识。写完记得更新。

## 素材清单

### 必查项目（根据题材）

- [ ] 领域基础知识（术语、行话、基本规则）
- [ ] 从业者日常（工作流程、挑战、习惯）
- [ ] 常见错误（外行人容易犯的错）
- [ ] 专业细节（能增加真实感的小细节）

### 题材素材清单

**职场/商战**
- [ ] 行业术语和缩写
- [ ] 典型工作日流程
- [ ] 会议/汇报的语言风格
- [ ] 常见职业病/压力源
- [ ] 行业潜规则

**医疗**
- [ ] 医院科室分工
- [ ] 常见诊断流程
- [ ] 医疗术语（患者能理解的）
- [ ] 医患沟通话术
- [ ] 医疗行业的禁忌话题

**历史**
- [ ] 当时日常用语
- [ ] 饮食习惯、服饰、交通
- [ ] 社会阶层和礼仪
- [ ] 货币/物价/工资
- [ ] 常见历史错误（避免穿越）

**悬疑/犯罪**
- [ ] 侦查基本流程
- [ ] 常见取证方法
- [ ] 犯罪心理学基础
- [ ] 法律程序（拘留、审讯、起诉）
- [ ] 警察/法医真实工作状态

**科幻**
- [ ] 科技术语（用普通人能理解的方式解释）
- [ ] 技术现状和局限
- [ ] 逻辑自洽性检查
- [ ] 科学顾问（如需要）

**都市/现实**
- [ ] 当地生活细节（气候、交通、物价）
- [ ] 社区/邻里关系
- [ ] 普通人日常困扰
- [ ] 语言习惯和口头禅

### 自定义领域

根据你的具体题材，列出需要研究的领域：

#### [领域名称]

**必查项：**
- ...

**加分项（增加真实感）：**
- ...

**常见错误：**
- ...
```

**Step 2: Add 整理好的素材 section**

After the 素材清单 section, add:

```markdown
## 整理好的素材

### 术语表

| 术语 | 解释 | 用途 |
|------|------|------|
| ... | ... | ... |

### 场景素材

#### [场景类型]

**真实细节：**
- ...

**可以虚构的部分：**
- ...

#### [场景类型]

**真实细节：**
- ...

**可以虚构的部分：**
- ...
```

**Step 3: Commit**

```bash
git add references/04-素材积累.md
git commit -m "feat: add research material template

Add references/04-素材积累.md template:
- 素材清单: genre-specific checklists (职场/医疗/历史/悬疑/科幻/都市)
- 自定义领域: for custom research topics
- 整理好的素材: 术语表 and 场景素材 sections

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Update SKILL.md - add 素材积累 section | ⬜ |
| 2 | Create references/04-素材积累.md template | ⬜ |
