# Changelog

## v3.0.0 (2026-07-31)

### Creative System Rewrite

- 将 `SKILL.md` 从 1100+ 行压缩为渐进式路由入口，详细方法按任务加载，减少上下文拥堵和重复规则。
- 新增 `creative-compass.md`：三向故事发现、读者契约、主题问题、中央矛盾、人物压力、因果脊柱、风格宪章和独创性审计。
- 新增 `editorial-revision.md`：体验、结构、人物、场景、语言、结局和连续性分层修订。
- 重写大纲、人物、章节工作台、短故事、语言和质量模板，移除信任百分比、机械钩子、固定感官配额与可互相抵消的总分。
- 新增“伟大作品门控”：按正文证据报告独特性、必然性、人物复杂度、结构惊奇、语言准确度、情感余震和整体完成度。
- 将 `check_ai_style.py`、`check_novel_health.py` 与 `check_short_story.py` 明确标记为启发式 / 机械信号，避免把关键词统计误当文学裁决。
- 新增 skill 结构与创作原则回归测试，并扩展现实写作评测提示。

## v2.6.2 (2026-07-07)

### Short Story Output Boundary Fix

#### 🐛 Bug Fixes
- 修复短故事模式会把 6000 字以上完整正文直接输出到对话的问题。
- `SKILL.md` 现在要求短故事必须先写入命名 Markdown 文件，默认路径为 `short-stories/YYYYMMDD-<标题>.md`。
- 明确文件命名规则：用户给标题则使用用户标题，未给标题则先生成短标题；同名文件追加 `-02`、`-03` 避免覆盖；长篇外传写入 `novels/<书名>/short-stories/YYYYMMDD-<标题>.md`。
- 最终对话只汇报文件路径、标题、正文字数和 `check_short_story.py` 检查结果，不粘贴完整正文。

#### 📚 Documentation & Tests
- 更新 `README.md`、`QUICK_START.md`、`FILE_INDEX.md`、`AGENTS.md`、`CLAUDE.md` 和 `references/short-story-template.md`，统一短故事文件输出规则。
- 更新 `test-prompts.json` 的短故事期望行为。
- 新增文档测试，防止短故事模式退回到“直接在对话里交付全文”。

## v2.6.1 (2026-07-06)

### Release Hardening

#### 🐛 Bug Fixes
- `scripts/check_novel_health.py`: 修复章节未命中任何场景关键词时的 `KeyError: '其他'`，现在稳定归类为 `其他`。
- `scripts/generate_epub.py`: 英文 EPUB 生成时不再把 `00-translation-brief.md`、`04-qa-checklist.md` 等翻译流程文件误识别为书名或作者元数据。
- `SKILL.md` 和 `FILE_INDEX.md`: 修正旧章节模板引用，整体重写流程现在明确从 `chapter-workspace-template.md` 的任务卡和场景拆分开始，再把最终正文写回 `manuscript/zh/`。

#### 🧪 Verification
- 全量单元测试通过：58 tests。
- Python 编译检查通过：`python3 -m py_compile scripts/*.py tests/*.py`。
- Markdown/补丁空白检查通过：`git diff --check`。
- JSON 校验通过：`python3 -m json.tool test-prompts.json >/dev/null`。
- 端到端烟测通过，覆盖中文正文、短故事 6000 字检查、翻译任务包、中文/英文 EPUB、旧章节迁移和所有主要检查脚本。
- 发布包校验通过：使用 `skill-creator` 打包脚本在临时目录生成 `.skill` 包；同时从仓库发布内容中移除 `.claude/` 本地配置并加入忽略规则。

## v2.6.0 (2026-07-06)

### Clean Manuscript Architecture

#### 📖 Workflow
- 新增长篇项目双轨结构：`manuscript/zh/` 保存中文正文唯一事实来源，`workspace/chapters/` 保存任务卡、场景拆分、沙盘裁决、复盘和修改记录。
- 章节正文模板改为干净 Markdown：第一行章数和章标题，空一行后直接正文，不再在章节文件内放 `## 正文`、任务卡或复盘。
- 英文意译翻译任务默认输出到 `manuscript/en/`，保持译文文件内只含章数、章标题和正文。

#### 🛠 Scripts
- 新增 `scripts/split_chapter_workspace.py`，可把旧根目录混合章节拆分到 `manuscript/zh/` 和 `workspace/chapters/`；默认保留原文件，`--move-originals` 可归档到 `_archive/mixed-chapters/`。
- `scripts/utils.py` 新增统一章节目录发现：中文优先 `manuscript/zh/`，英文优先 `manuscript/en/`，旧根目录和旧 `en/` 保持兼容。
- 字数检查、AI 味检测、小说健康检查、时间线检查、人物一致性、EPUB 导出和翻译任务生成均复用新章节发现逻辑。

#### 📚 Documentation
- `SKILL.md`、`README.md`、`QUICK_START.md`、`FILE_INDEX.md` 更新为 clean manuscript + workspace 结构。
- 新增 [chapter-workspace-template.md](references/chapter-workspace-template.md)，拆分章节任务卡、场景拆分、沙盘、复盘和修改记录。

## v2.5.0 (2026-07-06)

### Short Story Mode

#### 📖 Workflow
- 新增短故事模式：默认仍为长篇小说 / 网文三阶段工作流；用户明确触发“短故事 / 短篇故事 / 写一篇完整故事”时进入短故事旁路。
- 明确短故事硬标准：正文不少于 6000 个中文字符，可分段或换行，但必须完成开端、诱发事件、升级、反转或代价、高潮选择、结局收束。
- 新增 [短故事模板](references/short-story-template.md)：包含短故事任务卡、完整剧情骨架、正文区和完稿复盘。
- 新增 `scripts/check_short_story.py`：检查短故事正文区、6000 字红灯线、完稿复盘、高潮 / 收束信号和“未完待续”风险，支持 `--all short-stories` 批量检查。

#### 📚 Documentation
- `SKILL.md` 新增短故事入口路由、首轮决策、质量红灯项和推荐文件路径。
- `README.md`、`QUICK_START.md`、`FILE_INDEX.md` 新增短故事使用说明、模板导航和检查命令。
- `AGENTS.md`、`CLAUDE.md` 补充短故事维护说明。

## v2.4.0 (2026-06-26)

### Character Sandbox Mode

#### 🎭 Core Architecture Upgrade
- 新增 [角色沙盘模式](references/14-角色沙盘模式.md)：每章写作前先做角色意志校验，再生成任务卡和正文
- 新增 `04-角色沙盘/` 目录约定：一个关键角色一个运行时文件，另设 `00-角色索引.md` 和 `sessions/第XXX章-沙盘记录.md`
- 明确有限信息原则：角色只能看到自己在小说内应当知道的信息，不能读取完整大纲、未来剧情或其他角色内心
- 允许角色反抗大纲：导演按人物一致性、主线、悬念生命周期、原大纲、单章钩子的优先级裁决

#### 📖 Documentation
- README 重排为更直观的操作台结构，突出每章沙盘、文件地图、常用命令和推荐路径
- FILE_INDEX 新增角色沙盘导航、关键词和场景入口
- 进度仪表盘模板新增角色沙盘状态、反抗大纲裁决和回写提醒

#### 🧪 Tests
- 新增文档发现性测试，确保 `SKILL.md`、`README.md`、`FILE_INDEX.md` 都链接角色沙盘参考文档

## v2.3.1 (2026-06-23)

### Darwin Optimization Round - Execution Boundaries

#### 📖 SKILL.md Enhancements
- 新增 **首轮决策树**：将新建、续写、快写、修改、自动驾驶、检查/导出统一到可执行的第一步，避免只追问不交付
- 收敛 **自动驾驶模式**：从“不断写完整本”的强承诺改为按章节事务推进，只有章节文件和 `99-进度仪表盘.md` 都更新才算完成
- 补充自动驾驶暂停条件：上下文不足、运行时间不足、用户打断、文件写入失败、连续失败熔断时必须输出进度简报和恢复点
- 强化 **修改工作流**：新增最小改动原则和固定交付格式（定位、诊断、级别、改动、验证），降低“修改第 X 章”场景中泛泛整章重写的风险

#### 📊 Darwin Evaluation
- **基线评分**：89.0 / 100
- **优化后评分**：93.0 / 100 (+4.0)
- **保留改进**：3 / 3
  - 首轮决策树：89.0 → 91.0
  - 自动驾驶事务边界：91.0 → 92.0
  - 修改交付格式：92.0 → 93.0
- **验证**：30 个单元测试通过，本地 markdown 链接缺失数 0

## v2.3.0 (2026-05-06)

### Darwin Optimization Round - Character Agent Architecture

#### 🎭 Core Architecture Upgrade
- **引入角色智能体推演机制**：将写作架构从"章节任务驱动"升级为"角色认知驱动"
- **8维角色状态模型**：目标、信息、情绪、压力、关系、资源、时间、选择空间
- **角色状态快照持久化**：在 `99-进度仪表盘.md` 中记录每章后的角色状态，确保长篇连载角色一致性
- **信息差地图**：追踪每个角色知道/不知道的信息，支持戏剧张力和悬念设计

#### 📖 SKILL.md Enhancements
- **连载期写作循环**：在步骤3插入"角色状态推演"，让章节任务从角色认知自然生长
- **新增完整章节**：`## 角色智能体推演`，包含8维推演表、6步流程、详细示例输出
- **进度仪表盘模板扩展**：新增"角色状态快照"表格模板
- **边界条件覆盖**：明确快速模式、单POV、过渡章节可跳过角色推演

#### 📊 Darwin Evaluation
- **优化前评分**：76.7 / 100
  - 整体架构：12.0 / 15.0
  - 实测表现：18.8 / 25.0
- **优化后评分**：90.0 / 100 (+13.3)
  - 整体架构：15.0 / 15.0 (+3.0, +25%)
  - 实测表现：22.5 / 25.0 (+3.8, +20%)
- **主要突破**：
  - 工作流清晰度：12.0 → 13.5 (+1.5)
  - 边界条件覆盖：7.0 → 9.0 (+2.0)
  - 指令具体性：10.5 → 13.5 (+3.0)

#### 🎯 Impact
- 长篇写作时角色一致性显著提升
- 角色行为从认知状态自然生长，减少"作者木偶感"
- 通过角色状态快照解决跨章节角色失真问题
- 信息差地图让戏剧张力更自然

## v2.2.1 (2026-04-27)

### Darwin Optimization Round - Execution Routing

#### 📖 SKILL.md Enhancements
- 新增 **执行入口速查**：将新建小说、继续连载、快速出稿、修改章节、自动写完、完稿发布、质量检查明确分流
- 新增 **首轮输出契约**：要求先定位阶段、只收集阻塞缺口、立刻交付可用产物、少解释流程、维护进度仪表盘
- 强化自动驾驶入口：明确自动补齐缺失项、选定书名、创建/更新项目文件，并立即开始第 1 章或下一章

#### 📊 Evaluation
- Darwin 基线评分：81.3 / 100
- 优化后评分：87.1 / 100
- 主要提升：整体架构 7.5 → 8.4，实测表现 8.0 → 8.7

## v2.2.0 (2026-04-15)

### Documentation & Consistency Round

#### 🔄 Terminology Fixes
- **SKILL.md**: `check_rhythm.py` 引用更新为 `check_novel_health.py`（原脚本已在 v2.1.1 合并）
- **SKILL.md**: `完稿模式` 统一为 `收尾期`，与三阶段工作流对齐
- **CLAUDE.md**: 完全重写，四模式→三阶段，脚本列表从 3 个更新为 7 个，模板推荐更新为 v2 版
- **WORKFLOW_GUIDE.md**: `精修模式`→`修改模式`，版本对比从 v1→v2 更新为 v2.0→v2.1
- **QUICK_START.md**: 修复 `your-repo` 占位 URL

#### 🧪 Test Coverage
- 新增 `test_scripts.py`：覆盖 utils.py、check_ai_style.py、check_novel_health.py 的核心函数
- 测试总数从 18 → 27

#### 📋 v1 Template Deprecation Notices
- 5 个 v1 文件添加废弃提示：character-template.md, scene-design.md, 07-叙事节奏曲线.md, 08-人机协作.md, outline-template.md

## v2.1.1 (2026-04-14)

### Optimization Round - Gap Fixes & Script Upgrades

#### 🐛 Bug Fixes (P0)
- **check_ai_style.py**: 补全缺失的 3 种 AI 味检测（过度书面化对白、视角混乱、信息倾倒），现在完整支持文档声称的 9 种症状
- **check_ai_style.py**: 四字成语检测重构——不再误杀普通四字中文组合，只匹配已知成语列表
- **check_ai_style.py**: 新增 `--all` 批量检测模式，可一次检测整个小说目录
- **quality-checklist.md**: 修正旧版 6 模式术语为三阶段（策划期/连载期/收尾期）

#### 🔧 Script Upgrades (P0)
- **新增 `scripts/utils.py`**: 提取共享函数（extract_text_from_chapter、count_chinese_words、find_chapter_files），消除 4 个脚本的重复实现
- **合并 check_rhythm.py → check_novel_health.py**: 统一字数统计、场景检测、节奏健康检查为单一脚本，场景类型从 4 种扩展到 6 种（新增回忆闪回、情感沉淀）
- **新增 `scripts/character_tracker.py`**: 人物一致性检查——检测禁止用语、情绪突变、声音一致性
- **新增 `scripts/check_timeline.py`**: 时间线一致性检查——检测季节矛盾、时段分散、天气异常

#### 📖 SKILL.md Enhancements (P1)
- **新增收尾期完整流程**: 三步走（绿灯质量检查→完稿润色→出版门控），含版本管理建议和续作钩子决策框架
- **新增多线叙事写作循环**: 线切换时机决策表、POV 转换规则、进度仪表盘多线扩展模板
- **新增中断恢复协议**: 长期中断后恢复流程、续写简报模板、从任意章节恢复、自动驾驶断路器恢复 3 选项
- **新增脚本工具表**: SKILL.md 异常处理表增加多线叙事线偏移处理、脚本失败等新行
- **异常处理表升级**: 长期中断从"读仪表盘 +2 章摘要"升级为完整恢复协议

#### 🏷️ Documentation (P2)
- v1 模板标注废弃：character-template.md、scene-design.md、07-叙事节奏曲线.md、08-人机协作.md、outline-template.md 均添加废弃提示并指向 v2 版本
- FILE_INDEX.md 脚本列表从 3 个更新为 7 个（新增 check_novel_health、check_timeline、character_tracker）
- README.md 修复占位 URL、补充脚本列表

## v2.0.0 (2026-04-01)

### Major Release - Complete Overhaul

本次 v1→v2 重大更新，从"功能堆砌"升级为"工程化工作流"。

### 🎯 核心理念

从"只能生成内容"到"防崩盘 + 去 AI 味的系统化工具"

### 📦 新增文件（17 个）

**第一轮优化 - 轻量级骨架（Week 1-2）：**
- `references/outline-template-v1-minimal.md` - 极简大纲（10 字段）
- `references/progress-dashboard-template.md` - 进度仪表盘
- `scripts/check_ai_style.py` - AI 味检测脚本

**第二轮优化 - 核心功能升级（Week 3-4）：**
- `references/09-悬念生命周期管理.md` - 悬念追踪 + 预警
- `references/10-悬念-章节匹配矩阵.md` - 悬念 - 章节规划
- `references/11-叙事节奏框架.md` - 三层节奏 +5 种题材模板
- `references/character-template-v2.md` - 人物档案 v2（驱动式）
- `references/scene-design-v2.md` - 场景设计工具升级

**第三轮优化 - 体验完善（Week 5-6）：**
- `references/ai-style-examples.md` - AI 味改写范例库
- `references/ai-style-by-genre.md` - 按题材 AI 味清单
- `references/08-人机协作-v2.md` - 快速协作协议
- `references/12-喘息机制.md` - 喘息章设计
- `references/13-钩子映射表.md` - 钩子映射表

**文档完善：**
- `QUICK_START.md` - 5 分钟上手指记
- `WORKFLOW_GUIDE.md` - 工作流可视化指南
- `FILE_INDEX.md` - 文件索引与导航
- `OPTIMIZATION_PLAN.md` - 完整优化计划

### 🔧 核心改进

#### 1. 工作流简化
- **6 种模式 → 3 阶段**：策划期、连载期、收尾期
- **快速/标准模式**：一句话切换，满足效率与质量需求
- **进度仪表盘**：自动维护，一眼看全局

#### 2. AI 味自动检测
- **9 种症状识别**：空泛形容词、四字成语、解释连接词、时间转折词、情绪标签句、句式均匀、书面化对白、视角混乱、信息倾倒
- **量化报告**：每千字频次、严重程度分级
- **改写范例库**：9 种症状都有前后对比

#### 3. 悬念生命周期管理
- **6 状态追踪**：活跃/即将过期/已过期/已回收等
- **自动预警**：5 章黄灯、10 章红灯
- **章节匹配**：悬念强度与章节位置匹配

#### 4. 三层叙事节奏
- **宏观层**：四幕结构 +15 个关键节点
- **中观层**：黄金三章模式
- **微观层**：单章 3 次情绪起伏
- **5 种题材模板**：悬疑、玄幻升级流、言情、种田、都市现实

#### 5. 人物档案 v2（驱动式引擎）
- **欲望 - 恐惧双引擎**：自觉/不自觉欲望 + 核心恐惧
- **声音指纹**：3-5 句标志性对白作为锚点
- **缺陷 - 失败映射**：缺陷导致的失败场景必须发生

#### 6. 场景设计 v2（可执行工具）
- **任务检查卡**：量化标准、失败信号
- **切入点评分表**：+2/+1/0/-1 评分
- **六种过渡技术**：因果链/悬念转移/情绪对比/时间压缩/空间跳转/POV 切换
- **场景价值测试**：5 个问题判断场景是否该删

#### 7. 人机协作 v2
- **快速续写模式**："继续写"→自动提取上下文→开始写作
- **上下文压缩**：2 秒内提取关键信息
- **信息丢失防护**：多来源交叉验证

### 📊 改进对比

| 维度 | v0.8.0 | v2.0.0 |
|------|--------|--------|
| 工作流 | 6 种模式，复杂 | 3 阶段，傻瓜化 |
| 模板 | 100+ 字段，重 | 10 字段起步，轻 |
| 质量检查 | 50+ 项，繁琐 | 红绿灯 3-5 项 |
| 悬念管理 | 静态记录 | 动态追踪 + 预警 |
| AI 味防治 | 负面清单 | 改写范例库 |
| 人机协作 | 正式交接 | 一句话续写 |

### 📚 新手指引

- **5 分钟上手**：参见 [QUICK_START.md](QUICK_START.md)
- **功能总览**：参见 [README.md](README.md)
- **快速查找**：参见 [FILE_INDEX.md](FILE_INDEX.md)

---

## v0.8.0

- Added 故事引擎 (Story Engine) section with 核心机制，代价与资源，升级规则
- Added dual-mode writing loop (草稿模式/精修模式)
- Added 修改工作流 (Revision Workflow) with 4-step process
- Replaced Quality Bar with detailed 质量检查清单 (6 rules with check items and quantitative indicators)
- Added 多线管理 (Multi-line Narrative Management) template
- Added 节奏预警 (Rhythm Alert) system with check_rhythm.py script
- Added 素材积累 (Research Material) phase and template
- Added 出版门控 (Publishing Gate) with 倒序检查 and tiered standards
- Added 叙事节奏曲线 (Narrative Rhythm Curve) design
- Added 人机协作 (Human-AI Collaboration) section and template
- Added 小说体检 (Novel Health Check) system with check_novel_health.py

## v0.3.1

- Added EPUB export and word count check to skill trigger description for natural language activation.
- Added Export section to SKILL.md with usage instructions.

## v0.3.0

- Added EPUB export script (`scripts/generate_epub.py`) to generate EPUB e-books from novel projects.
- Added author/pseudonym field to outline template.
- Added comprehensive tests for the EPUB generation script.

## v0.2.1

- Renamed the skill identifier in `SKILL.md` frontmatter to `chinese-novelist-skill`.
- Added an explicit in-document version block to `SKILL.md`.

## v0.2.0

- Rebuilt `SKILL.md` around a more stable novel-writing workflow and standard skill metadata.
- Added planning/state templates for outline, characters, story bible, opening design, scene design, style polishing, and ending design.
- Strengthened dialogue, structure, consistency, and quality-check references for Chinese long-form fiction.
- Updated the chapter word-count script to count the `## 正文` section preferentially.
- Added tests for the word-count script and local documentation links.
