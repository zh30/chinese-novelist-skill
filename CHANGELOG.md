# Changelog

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
