# Revision Workflow Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add revision workflow section to SKILL.md with problem diagnosis, modification levels, and targeted modification guide.

**Architecture:** Insert new `## 修改工作流` section after `## 精修模式` and before `## Export`.

**Tech Stack:** Plain Markdown edits only.

---

## Task 1: Add 修改工作流 Section

**Files:**
- Modify: `SKILL.md`

**Step 1: Read SKILL.md to find insertion point**

Read the file to find where `## Export` begins. The new section should be inserted before `## Export`.

**Step 2: Find the exact line where ## Export appears**

Insert the following content before `## Export`:

```markdown
## 修改工作流

当用户要求修改、重写或打磨某一章时，按以下流程执行：

### 第一步：问题诊断

读取目标章节，对照质量标准，找出具体问题。用一句话描述问题（如"开头300字太拖，没有进冲突"）。

**常用问题诊断清单：**

**开头问题**
- [ ] 开头是否在20%内进入冲突？
- [ ] 是否有"钩子"吸引读者继续看？
- [ ] 是否有过多的背景/设定说明？

**节奏问题**
- [ ] 是否有过多的"summary"（概述）而非"scene"（场景）？
- [ ] 是否在某段停留太久？
- [ ] 每章是否有明确的事件推进？

**对白问题**
- [ ] 对白是否推进了剧情/关系？
- [ ] 对白是否有多余的"解释腔"？
- [ ] 人物说话是否符合性格？

**结尾问题**
- [ ] 结尾是否有钩子？
- [ ] 是否留下了悬念或转折？

**一致性问题**
- [ ] 是否与前文设定冲突？
- [ ] 人物状态是否连贯？

### 第二步：修改分级

根据问题类型和严重程度，判断修改级别：

| 级别 | 问题类型 | 修改范围 | 预计耗时 |
|------|----------|----------|----------|
| 轻度 | 错别字、语句不通顺、标点错误 | 局部修改 | 10-20分钟 |
| 中度 | 某段对话不够自然、某个场景不够具体 | 单场景/单段落 | 30-60分钟 |
| 重度 | 节奏问题、结构问题、开头钩子太弱 | 多场景或全章重写 | 1-3小时 |

### 第三步：针对性修改

根据诊断结果，按问题类型选择参考文档：

- 钩子太弱 → 参考 [hook-techniques.md](references/hook-techniques.md)
- 节奏太慢 → 参考 [chapter-guide.md](references/chapter-guide.md) 的节奏部分
- 对白太水 → 参考 [dialogue-writing.md](references/dialogue-writing.md)
- 场景空洞 → 参考 [scene-design.md](references/scene-design.md) 和 [content-expansion.md](references/content-expansion.md)
- 整体重写 → 从 [chapter-template.md](references/chapter-template.md) 的场景拆分开始

### 第四步：验证

- 重读修改后的段落，确认问题已解决
- 运行字数检查：`python3 scripts/check_chapter_wordcount.py <章节文件路径>`
- 确认字数没有严重缩水（轻度修改不应影响总字数）
```

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: add revision workflow to SKILL.md

Add ## 修改工作流 section with 4-step process:
1. Problem diagnosis (with checklist)
2. Modification level (light/medium/heavy)
3. Targeted modification (reference docs by problem type)
4. Verification (re-read + word count)

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Add 修改工作流 section to SKILL.md | ⬜ |
