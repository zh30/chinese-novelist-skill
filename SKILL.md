---
name: chinese-novelist
description: Use when the user wants to plan, write, continue, or revise a Chinese novel, web novel, serialized story, chapter outline, character bible, or chapter draft in Chinese.
---

# Chinese Novelist

## Overview

为中文长篇小说和网文创作提供一套可持续执行的工作流：先稳住设定与大纲，再按章节推进，持续维护人物状态、悬念台账和文风质量，避免写到后面失控、注水或前后打架。

## When to Use

- 用户要从零开始写中文小说、网文、长篇故事、连载故事
- 用户已有设定，想补大纲、人物档案、世界观、章节规划
- 用户要续写已有章节，要求前后连贯
- 用户要重写某章，增强钩子、节奏、对白、人物张力或减少 AI 味

## Default Working Mode

先判断用户要的交付深度，再选最轻的有效模式：

1. `策划模式`：只做题材定位、故事引擎、大纲、人物、世界观、伏笔台账
2. `试写模式`：策划完成后，只写首章或样章
3. `连载模式`：按章推进，每次交付 1 章或少量连续章节
4. `完稿模式`：只有在用户明确要求整本初稿时，才连续写完整部长篇

如果用户没有说清楚：
- 新项目默认 `策划模式`
- 已有章节的项目默认 `连载模式`

## Intake

只补问真正缺失的关键信息，优先补齐以下 6 项：

- 题材 / 子类型
- 一句话 premise 或核心冲突
- 主角身份、最大欲望、致命缺陷
- 目标读者、文风关键词、禁忌
- 叙事视角（第一人称 / 第三人称 / 群像）
- 篇幅目标与交付模式

如果用户只给了模糊想法，不要空泛追问；应给出具体备选并推荐更稳的方案。

## Required Files

在 `novels/<书名>/` 内创建或更新：

- `00-大纲.md` → 使用 [outline-template.md](references/outline-template.md)
- `01-人物档案.md` → 使用 [character-template.md](references/character-template.md)
- `02-世界观与伏笔.md` → 使用 [story-bible-template.md](references/story-bible-template.md)
- `第XX章-标题.md` → 使用 [chapter-template.md](references/chapter-template.md)

## Planning Rules

开始批量写章节前，至少锁定以下内容：

- `logline`
- 主线冲突、对抗力量、利害关系
- 主角外部目标与内在成长弧线
- 结局类型与兑现方式
- 采用的结构模板（参见 [plot-structures.md](references/plot-structures.md)）
- 逐章功能分配
- 未回收悬念、伏笔、时间线、关系状态

除非用户明确要求跳过规划，否则不要直接写完全书。即使用户要求“直接开写”，也先产出一页精简总纲再动笔。

## Chapter Loop

每写一章都按这个循环执行：

1. 读取 `00-大纲.md`、最近章节摘要、`02-世界观与伏笔.md`
2. 明确 `本章目标 / 阻碍 / 转折 / 结尾钩子`
3. 先拆 3-6 个场景，再落正文
4. 开头前 20% 必须尽快进入冲突，参考 [chapter-guide.md](references/chapter-guide.md)
   - 如果在写首章，额外参考 [opening-design.md](references/opening-design.md)
5. 对话、扩写、连贯性、结尾钩子分别参考：
   - [dialogue-writing.md](references/dialogue-writing.md)
   - [content-expansion.md](references/content-expansion.md)
   - [consistency.md](references/consistency.md)
   - [hook-techniques.md](references/hook-techniques.md)
   - [scene-design.md](references/scene-design.md)
   - [style-polishing.md](references/style-polishing.md)
6. 长章节交付前，运行：
   - `python scripts/check_chapter_wordcount.py <章节文件路径>`
7. 交付前用 [quality-checklist.md](references/quality-checklist.md) 自查
8. 回写章节摘要、人物状态、伏笔状态与章节进度

## Quality Bar

每章至少满足：

- 本章发生了不能删除的变化
- 回应、升级或偏转至少一条已有悬念
- 结尾钩子强度与全书位置匹配
- 人物通过动作、选择、对白被展示，而不是只被描述
- 避免空泛形容词堆砌、抽象情绪总结、整段均匀句式和过度书面腔
- 每个章节至少包含若干有任务的场景，而不是流水账拼接

## Completion

在 `完稿模式` 收尾时，必须额外检查：

- 主线悬念是否回收
- 主角弧线是否完成
- 设定规则是否前后一致
- 是否存在遗失角色、断裂线索、无兑现伏笔
- 是否需要留下续作钩子；只有用户要时才保留
- 终稿收尾方式参考 [ending-design.md](references/ending-design.md)
