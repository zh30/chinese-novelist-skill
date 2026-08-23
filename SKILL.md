---
name: chinese-novelist-skill
description: "Create, continue, revise, diagnose, finish, and batch-produce original Chinese fiction, including literary novels, genre/web novels, complete short stories, character and plot development, style editing, continuity management, EPUB export, and adaptive English translation. Use for requests such as 写小说、写一本、短故事、短篇故事、完整故事、继续写、下一章、角色沙盘、修改或重写章节、润色、去 AI 味、检查节奏或质量、自动写完整本、批量写、批量生产、自动写多本、导出 EPUB、翻译小说."
compatibility: Requires python3 and filesystem access. No extra Python packages.
metadata: {version: "3.1.0"}
---

# Chinese Novelist

当前版本：3.1.0。详情见 [CHANGELOG.md](CHANGELOG.md)。

## 使命

帮助作者完成具有独特生命的中文小说，而不只是“合格内容”。把伟大视为持续追求，不冒充可由清单保证的结果。每次创作同时守住四件事：

1. **独特性**：故事只能由这些人物、在这个世界、以这种语言发生。
2. **必然性**：事件由人物选择与既有压力引发，不靠作者搬运情节。
3. **复杂性**：人物、对手和主题都保留矛盾；不把小说写成立意说明书。
4. **余震**：结尾兑现事件与情感，并让关键意象或问题在读者心里继续工作。

先遵守用户给出的事实、边界、篇幅和交付要求。信息不足但不妨碍推进时，做少量明确假设；只有会改变作品核心的缺口才询问。

## 核心原则

- **先发现，后规划**：不要把用户的第一句话直接塞进题材模板。
- **先分岔，后收敛**：至少比较 3 个实质不同的方向；选定后保持创作宪章稳定。
- **人物先于机关**：转折优先来自选择、误判、隐瞒、关系和代价。
- **主题保持为问题**：让不同人物以行动回答同一问题，不替读者总结标准答案。
- **风格来自观察**：用视角、细节、句法和意象建立声音，不靠形容词堆砌。
- **场景必须改变压力**：可用悬念、决定、情绪落点或余韵结束，不强制章章反转。
- **写作与审稿分离**：先完整写出一个单元，再切换编辑视角。
- **脚本只是烟雾报警器**：字数和关键词统计只能提示复核位置，不能证明文学质量。
- **拒绝伪完成**：大纲不算正文，口头进度不算落盘，检查通过不等于作品成熟。

## 意图路由

| 用户意图 | 默认动作 | 必读 |
|---|---|---|
| 新建长篇 / 网文 | 策划期：比较方向，建立创作宪章、因果脊柱和首章任务 | [creative-compass.md](references/creative-compass.md)、[outline-template-v1-minimal.md](references/outline-template-v1-minimal.md) |
| 写短故事 / 短篇 | 走短故事旁路，完成全文并落盘 | [short-story-template.md](references/short-story-template.md) |
| 继续写 / 下一章 | 有界冷启动后执行章节事务 | [chapter-workspace-template.md](references/chapter-workspace-template.md) |
| 批量写 / 自动写多本 | 认领清单条目，按原子事务推进 | [batch-production.md](references/batch-production.md) |
| 人物僵硬 / 群像 / 角色沙盘 | 使用有限信息沙盘，允许人物反抗大纲 | [14-角色沙盘模式.md](references/14-角色沙盘模式.md) |
| 修改 / 重写 / 润色 / 去 AI 味 | 先诊断最高杠杆问题，再做单一职责修订 | [editorial-revision.md](references/editorial-revision.md) |
| 完稿 / 质量审计 | 分层通读，完成整书门控 | [editorial-revision.md](references/editorial-revision.md)、[ending-design.md](references/ending-design.md) |
| 字数、事务验收、AI 痕迹、时间线、跨书同质 | 运行对应脚本，把结果作为复核线索 | [quality-checklist.md](references/quality-checklist.md) |
| 翻译 / EPUB | 执行 Translation 或 Export | [translation-workflow.md](references/translation-workflow.md) |

不要一次加载所有引用。只读当前动作列出的必读文件；出现具体问题时再读下文“按问题加载”。

## 交付契约

1. 定位当前模式：策划、连载、短故事、批量、修改、收尾、翻译、导出或诊断。
2. 查找已有文件；先读再写，不凭记忆覆盖用户正文。
3. 把可恢复的产物写入文件。正文与工作材料分开。
4. 完成当前最小闭环：策划交付可决定的方向；章节交付正文、复盘和状态；修改交付真实改动；检查交付证据。
5. 最终回复只说明结果、路径、关键判断、验证与仍存在的不确定性，不粘贴已落盘的长篇正文。

## 项目结构

```text
novels/<书名>/
├── 00-大纲.md
├── 01-人物档案.md
├── 02-世界观与伏笔.md
├── 04-角色沙盘/
├── 99-进度仪表盘.md
├── manuscript/zh/第XXX章-标题.md
├── manuscript/en/Chapter-XXX.md
├── workspace/chapters/第XXX章-标题/
└── workspace/audits/卷X-审计.md
```

批量任务清单写在 `novels/00-批量任务清单.md`，格式见 [batch-production.md](references/batch-production.md)。

硬规则：

- `manuscript/zh/` 是中文正文唯一事实来源；章节文件只含首行章数与标题、空行、正文。
- 任务卡、沙盘、检查结果和修改记录只进入 `workspace/chapters/`。
- 旧混合章节用 `python3 scripts/split_chapter_workspace.py novels/书名` 迁移；未经用户明确要求，不移动原文件。
- 世界简单时可暂不建 `02-世界观与伏笔.md`。

## 策划期

### 1. 识别创作野心

写入 `00-大纲.md`：**类型驱动**、**文学驱动**或**融合驱动**。信息不足时默认融合。三种方向没有高低。

### 2. 运行故事发现

按 [creative-compass.md](references/creative-compass.md) 执行：提取最有能量的矛盾；生成 3 个会导向不同人物选择与结局代价的方向；用专属性、压力、可升级性、情感危险、非现成答案比较；推荐 1 个并说明舍弃理由。建立创作宪章、因果脊柱、结局代价和意象系统。

批量生产时，还要把题材、主角策略和结局代价登记到清单，并与已有书目做差异审计。

### 3. 创建最小文件

- `00-大纲.md`：[outline-template-v1-minimal.md](references/outline-template-v1-minimal.md)
- `01-人物档案.md`：[character-template-v2.md](references/character-template-v2.md)
- `99-进度仪表盘.md`：[progress-dashboard-template.md](references/progress-dashboard-template.md)
- 首章工作台：[chapter-workspace-template.md](references/chapter-workspace-template.md)

用户只要求策划则停在此处。明确要求写正文或自动驾驶时继续写首章。

## 连载期章节事务

每章按以下顺序执行；快速模式可压缩记录，不能跳过人物、因果、验收和状态回写。

### 1. 有界冷启动

只读：`99-进度仪表盘.md`（含滚动前情摘要）、`00-大纲.md` 创作宪章区、本章 POV 人物卡、上一章末尾 800 字。禁止默认重读最近 1–3 章全文；仅修改、审计或仪表盘与正文冲突时按需读正文。冲突时以正文为准并修复仪表盘。

### 2. 建立本章压力

写入 `task-card.md`：POV 现在要完成什么；何种压力迫使其暴露保护策略；对手或关系人物要什么；上一章哪个结果导致本章；将产生什么不可逆后果；读者应带走什么问题、决定或余韵。

人物行为不自然或多人冲突复杂时，执行 [14-角色沙盘模式.md](references/14-角色沙盘模式.md)。角色只知道自己应知的信息。

### 3. 设计场景

标准模式在 `scene-plan.md` 写欲望、阻力、策略变化、转折和离场状态。优先写成“因为……所以……但……”。首章读 [opening-design.md](references/opening-design.md)，对白读 [dialogue-writing.md](references/dialogue-writing.md)，场景失效读 [scene-design-v2.md](references/scene-design-v2.md)，结尾读 [ending-design.md](references/ending-design.md)。

### 4. 写正文

写入 `manuscript/zh/第XXX章-标题.md`。稳定 POV；用少量有判断力的细节；对白让人物争取东西并保护不愿说的东西；让关键意象自然复现。标准长篇不少于 3000 个中文字符，快速初稿不少于 2500。

### 5. 独立编辑

按 [editorial-revision.md](references/editorial-revision.md) 做最少轮次。至少检查必要性、因果、人物选择、专属细节、语言意图和连续性。做一处有胆量的修改。

### 6. 机械检查与回写

```bash
python3 scripts/check_chapter_wordcount.py <章节文件>
python3 scripts/check_ai_style.py <章节文件>
python3 scripts/check_chapter_transaction.py <小说目录> <章节号>
```

逐条查看命中原句：正确表达可以保留。把摘要、选择、代价、状态、伏笔和未解决风险写入 `review.md` 与仪表盘滚动前情摘要。验收失败则补写后重跑，不得把空壳复盘当成完成。

## 短故事模式（可选）

只有用户明确要求“短故事”“短篇故事”“写一篇完整故事”或同义表达时进入，不转成长篇第一章。

1. 读取 [creative-compass.md](references/creative-compass.md) 的故事发现与 [short-story-template.md](references/short-story-template.md)。
2. 选一个能在单篇内完成压力升级、不可逆选择和情感收束的核心。
3. 创建 `short-stories/YYYYMMDD-<标题>.md`；同名时追加 `-02`、`-03`。完整正文、任务卡、骨架和复盘都写入文件。
4. 正文不少于 6000 个中文字符，除非用户给出更高目标。不得在对话中直接输出完整正文；除非用户明确要求聊天全文。
5. 运行 `python3 scripts/check_short_story.py <短故事文件路径>`，再人工复核高潮是否由人物选择触发、主线是否闭合、结尾是否改变了开头意象。
6. 对话只回复文件路径、标题、正文字数、检查状态和仍需说明的风险，不复制全文。

批量短篇时，每篇仍是一个原子事务：完整落盘 + 短故事检查通过后，才更新清单。

## 🤖 自动驾驶模式

“自动写完整本”“全部写完”“autopilot”等明确请求才触发。自动驾驶扩大持续性，不降低质量标准，也不代表一次生成全书。

- 从用户素材推断非核心缺口；核心方向采用故事发现中的推荐项。
- 以“完成一章正文 + 工作台 + 状态回写 + 事务验收”为原子事务；当前轮可继续时进入下一章。
- 每章完成后必须运行 `python3 scripts/check_chapter_transaction.py <小说目录> <章节号>`。失败则补写并重试一次；连续 2 次失败停机，写入恢复点，不得假装通过。
- 每 10 章或卷末写出 `workspace/audits/卷X-审计.md`（因果、人物弧线、承诺），并运行时间线、人物一致性和健康检查作线索。
- 同批多书完本后运行 `python3 scripts/check_cross_book_similarity.py novels`。
- 不用套路表自动填充核心设计。文件写入失败、上下文无法可靠恢复或用户打断时暂停。

## 批量生产

用户要求“批量写”“自动写多本”或一次给出多个 premise 时，读取 [batch-production.md](references/batch-production.md)。

1. 创建或更新 `novels/00-批量任务清单.md`。
2. 为每本书比较方向并登记宪章差异（题材、主角策略、结局代价）。
3. 认领一个未完成条目；并行时一实例只认领一本书。
4. 每次推进只完成一个原子事务：一章长篇或一篇完整短篇，再验收、回写。
5. 失败按批量协议重试；连续失败标记恢复点，改认领下一条或停机。

同一协议可用于会话内连写、外部 CLI 循环或多实例并行。

## 修改与重写

1. 读取目标文本、相邻章节、创作宪章和用户反馈。
2. 用一句可证伪的话诊断最高杠杆问题。
3. 判定层级：字句、段落、场景、章节、结构。根因在上层时，不先做逐句润色。
4. 只改解决问题所需的最小范围，除非用户要求重写。
5. 执行 [editorial-revision.md](references/editorial-revision.md)。去 AI 味时重建观察、动作和句法。
6. 重读改后文本，运行相关脚本，更新 `revision-notes.md` 和受影响状态。
7. 汇报实际改了什么；不要只给建议却不修改文件。

## 收尾期

按 [editorial-revision.md](references/editorial-revision.md) 分轮处理：读者通读；结构；人物；场景；语言；结局；连续性。

“伟大作品门控”不打总分。对独特性、必然性、人物复杂度、结构惊奇、语言准确度、情感余震和整体完成度，各给出正文证据、最强处、最弱处与下一项最高杠杆修改。

## 按问题加载

- 构思、主题、独创性、创作宪章：[creative-compass.md](references/creative-compass.md)
- 人物深度与声音：[character-template-v2.md](references/character-template-v2.md)、[character-building.md](references/character-building.md)
- 结构选择：[plot-structures.md](references/plot-structures.md)
- 场景与节奏：[scene-design-v2.md](references/scene-design-v2.md)、[11-叙事节奏框架.md](references/11-叙事节奏框架.md)、[12-喘息机制.md](references/12-喘息机制.md)
- 悬念管理：[09-悬念生命周期管理.md](references/09-悬念生命周期管理.md)
- 多线叙事：[03-多线管理.md](references/03-多线管理.md)
- 对白：[dialogue-writing.md](references/dialogue-writing.md)
- 中文文风：[style-polishing.md](references/style-polishing.md)
- 开篇与结局：[opening-design.md](references/opening-design.md)、[ending-design.md](references/ending-design.md)
- 一致性：[consistency.md](references/consistency.md)
- 深度修订与门控：[editorial-revision.md](references/editorial-revision.md)、[quality-checklist.md](references/quality-checklist.md)
- 批量编排与跨书差异：[batch-production.md](references/batch-production.md)

## 工具

| 任务 | 命令 |
|---|---|
| 章节字数 | `python3 scripts/check_chapter_wordcount.py <文件>` |
| 批量章节 | `python3 scripts/check_chapter_wordcount.py --all <小说目录>` |
| 章节事务验收 | `python3 scripts/check_chapter_transaction.py <小说目录> <章节号>` |
| AI 痕迹线索 | `python3 scripts/check_ai_style.py <文件或 --all 目录>` |
| 短故事硬性项 | `python3 scripts/check_short_story.py <文件或 --all 目录>` |
| 长篇机械健康信号 | `python3 scripts/check_novel_health.py <小说目录>` |
| 时间线 | `python3 scripts/check_timeline.py <小说目录>` |
| 人物一致性 | `python3 scripts/character_tracker.py <小说目录>` |
| 跨书同质化 | `python3 scripts/check_cross_book_similarity.py novels` |
| 拆分旧章节 | `python3 scripts/split_chapter_workspace.py <小说目录>` |
| 生成翻译任务 | `python3 scripts/translate_to_english.py <小说目录>` |
| EPUB | `python3 scripts/generate_epub.py <小说目录>` |

## Translation

当用户要求翻译成英文时，读取 [translation-workflow.md](references/translation-workflow.md)，使用当前 AI 执行意译翻译，不调用独立翻译接口。

1. 运行 `python3 scripts/translate_to_english.py <小说目录>` 生成翻译简报、术语表、风格表与任务包。
2. 做样章校准，再逐章初译、译者自检、双语修订、单语润色和终检。
3. 最终译文写入 `manuscript/en/Chapter-XXX.md`；章数和章标题同在第一行，空一行后直接写正文，不保留工作说明。
4. 保留剧情功能、人物声音、潜台词、节奏和文化质感；不得新增事件或改写人物关系。

导出前确认目录和语言：

```bash
python3 scripts/generate_epub.py <小说目录>
python3 scripts/generate_epub.py <小说目录> --lang en
```

优先读取 `manuscript/zh/` 或 `manuscript/en/`，成功后返回生成文件的绝对路径。
