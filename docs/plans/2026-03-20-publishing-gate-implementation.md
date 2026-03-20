# Publishing Gate Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add publishing gate system to SKILL.md and create standalone template.

**Architecture:**
1. Update SKILL.md - add publishing gate section after ## Completion
2. Create `references/06-出版门控.md` template

**Tech Stack:** Plain Markdown files.

---

## Task 1: Update SKILL.md - Add Publishing Gate Section

**Files:**
- Modify: `SKILL.md`

**Step 1: Find Completion section**

Read SKILL.md to find where `## Completion` ends and where `## Translation` begins.

**Step 2: Find the location**

The new section should be inserted between:
- End of `## Completion` section
- Start of `## Translation` section

**Step 3: Insert the new section**

```markdown
## 出版门控

在进入出版或发布前，按以下流程做系统性验收：

### 倒序检查法

从结局往前推，验证每章是否服务结局：

**结局要求 → 倒数第3章 → 倒数第2章 → 倒数第1章 → 结局**

- [ ] 结局是否兑现了大纲承诺？
- [ ] 每章的进展是否导向结局？
- [ ] 是否有偏离结局的章节？

### 常见烂尾模式预警

| 烂尾模式 | 描述 | 检查项 |
|----------|------|--------|
| 机械降神 | 结局靠突然出现的力量解决 | [ ] 结局的解决方案是否在前文有铺垫？ |
| 主角光环 | 主角轻易获胜，无代价 | [ ] 主角是否付出了合理的代价？ |
| 支线烂尾 | 支线挖坑不填 | [ ] 每条支线是否都有回收？ |
| 匆忙收场 | 结尾突然，像赶工 | [ ] 结局是否有足够的篇幅？ |
| 开放结局滥用 | 所有问题都没回答 | [ ] 核心问题是否都有答案？ |
| 反派弱化 | 反派结局时突然变弱 | [ ] 反派是否保持了一致性？ |

### 出版分级标准

| 级别 | 要求 |
|------|------|
| 入门级 | 字数达标、无明显错误、主线完整、人物一致 |
| 专业级 | 入门级 + 无逻辑漏洞、伏笔基本回收、节奏良好 |
| 出版级 | 专业级 + 所有伏笔回收、主题清晰、人物有成长弧线 |

**详细检查清单：** [references/06-出版门控.md](references/06-出版门控.md)
```

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "feat: add publishing gate section to SKILL.md

Add ## 出版门控 section with:
- Reverse-order check method (倒序检查法)
- Common bad ending patterns (常见烂尾模式预警)
- Publishing tier standards (出版分级标准)
- Reference to 06-出版门控.md template

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Create 06-出版门控.md Template

**Files:**
- Create: `references/06-出版门控.md`

**Step 1: Write the template**

```markdown
# 出版门控

> 在进入出版或发布前，按此清单做系统性验收。

## 健康检查（每写完5-10章）

- [ ] 主线悬念是否按计划回收？
- [ ] 是否有某条伏笔超过15章未回收（警告）？
- [ ] 人物状态是否前后一致？
- [ ] 是否有逻辑漏洞？

## 结局验收（写完大纲后）

### 倒序检查法

从结局往前推，验证每章是否服务结局：

**结局要求 → 倒数第3章 → 倒数第2章 → 倒数第1章 → 结局**

- [ ] 结局是否兑现了大纲承诺？
- [ ] 每章的进展是否导向结局？
- [ ] 是否有偏离结局的章节？

### 常见烂尾模式预警

检查是否存在以下模式：

| 烂尾模式 | 描述 | 检查项 |
|----------|------|--------|
| 机械降神 | 结局靠突然出现的力量解决 | [ ] 结局的解决方案是否在前文有铺垫？ |
| 主角光环 | 主角轻易获胜，无代价 | [ ] 主角是否付出了合理的代价？ |
| 支线烂尾 | 支线挖坑不填 | [ ] 每条支线是否都有回收？ |
| 匆忙收场 | 结尾突然，像赶工 | [ ] 结局是否有足够的篇幅？ |
| 开放结局滥用 | 所有问题都没回答 | [ ] 核心问题是否都有答案？ |
| 反派弱化 | 反派结局时突然变弱 | [ ] 反派是否保持了一致性？ |

## 出版分级标准

### 入门级（可网络连载）

- [ ] 字数达标（每章 ≥ 3000字）
- [ ] 无明显错别字/病句
- [ ] 主线完整，有开头有结尾
- [ ] 人物基本一致

### 专业级（可付费发布）

入门级 +：
- [ ] 无逻辑漏洞
- [ ] 伏笔基本回收（允许1-2个悬念留作续作）
- [ ] 节奏控制良好（无过长章节）
- [ ] 对话自然，符合人物性格
- [ ] 开篇钩子足够强

### 出版级（可正式出版）

专业级 +：
- [ ] 所有伏笔回收（或明确标记为续作伏笔）
- [ ] 主题表达清晰
- [ ] 人物有成长弧线
- [ ] 结局有余韵
- [ ] 无敏感内容问题

## 倒序检查工作表

填写以下工作表，验证每章是否服务结局：

| 章节 | 主要事件 | 是否服务结局 | 问题 |
|------|----------|--------------|------|
| 结局 | ... | - | - |
| 倒数第1章 | ... | ✅/❌ | ... |
| 倒数第2章 | ... | ✅/❌ | ... |
| ... | ... | ... | ... |

## 最终确认

在发布前，确认以下问题：

- [ ] 结局是否让读者满意？
- [ ] 是否有遗留问题未解决（除续作伏笔外）？
- [ ] 是否需要续作/系列？
- [ ] 读者在评论区可能问哪些问题？（提前准备）
```

**Step 2: Commit**

```bash
git add references/06-出版门控.md
git commit -m "feat: add publishing gate template

Add references/06-出版门控.md template:
- Health check (5-10 chapters)
- Ending verification with reverse-order method
- Common bad ending patterns table
- Publishing tier standards (3 levels)
- Reverse-order check worksheet
- Final confirmation checklist

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Update SKILL.md - add 出版门控 section | ⬜ |
| 2 | Create references/06-出版门控.md | ⬜ |
