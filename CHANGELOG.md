# Changelog

## v2.0.0 (2026-04-01)

### Major Release - Complete Overhaul

本次 v1→v2 重大更新，从"功能堆砌"升级为"工程化工作流"。

### 🎯 核心理念

从"只能生成内容"到"防崩盘+去AI味的系统化工具"

### 📦 新增文件（17个）

**第一轮优化 - 轻量级骨架（Week 1-2）：**
- `references/outline-template-v1-minimal.md` - 极简大纲（10字段）
- `references/progress-dashboard-template.md` - 进度仪表盘
- `scripts/check_ai_style.py` - AI味检测脚本

**第二轮优化 - 核心功能升级（Week 3-4）：**
- `references/09-悬念生命周期管理.md` - 悬念追踪+预警
- `references/10-悬念-章节匹配矩阵.md` - 悬念-章节规划
- `references/11-叙事节奏框架.md` - 三层节奏+5种题材模板
- `references/character-template-v2.md` - 人物档案v2（驱动式）
- `references/scene-design-v2.md` - 场景设计工具升级

**第三轮优化 - 体验完善（Week 5-6）：**
- `references/ai-style-examples.md` - AI味改写范例库
- `references/ai-style-by-genre.md` - 按题材AI味清单
- `references/08-人机协作-v2.md` - 快速协作协议
- `references/12-喘息机制.md` - 喘息章设计
- `references/13-钩子映射表.md` - 钩子映射表

**文档完善：**
- `QUICK_START.md` - 5分钟上手指记
- `WORKFLOW_GUIDE.md` - 工作流可视化指南
- `FILE_INDEX.md` - 文件索引与导航
- `OPTIMIZATION_PLAN.md` - 完整优化计划

### 🔧 核心改进

#### 1. 工作流简化
- **6种模式 → 3阶段**：策划期、连载期、收尾期
- **快速/标准模式**：一句话切换，满足效率与质量需求
- **进度仪表盘**：自动维护，一眼看全局

#### 2. AI味自动检测
- **9种症状识别**：空泛形容词、四字成语、解释连接词、时间转折词、情绪标签句、句式均匀、书面化对白、视角混乱、信息倾倒
- **量化报告**：每千字频次、严重程度分级
- **改写范例库**：9种症状都有前后对比

#### 3. 悬念生命周期管理
- **6状态追踪**：活跃/即将过期/已过期/已回收等
- **自动预警**：5章黄灯、10章红灯
- **章节匹配**：悬念强度与章节位置匹配

#### 4. 三层叙事节奏
- **宏观层**：四幕结构+15个关键节点
- **中观层**：黄金三章模式
- **微观层**：单章3次情绪起伏
- **5种题材模板**：悬疑、玄幻升级流、言情、种田、都市现实

#### 5. 人物档案v2（驱动式引擎）
- **欲望-恐惧双引擎**：自觉/不自觉欲望+核心恐惧
- **声音指纹**：3-5句标志性对白作为锚点
- **缺陷-失败映射**：缺陷导致的失败场景必须发生

#### 6. 场景设计v2（可执行工具）
- **任务检查卡**：量化标准、失败信号
- **切入点评分表**：+2/+1/0/-1评分
- **六种过渡技术**：因果链/悬念转移/情绪对比/时间压缩/空间跳转/POV切换
- **场景价值测试**：5个问题判断场景是否该删

#### 7. 人机协作v2
- **快速续写模式**："继续写"→自动提取上下文→开始写作
- **上下文压缩**：2秒内提取关键信息
- **信息丢失防护**：多来源交叉验证

### 📊 改进对比

| 维度 | v0.8.0 | v2.0.0 |
|------|--------|--------|
| 工作流 | 6种模式，复杂 | 3阶段，傻瓜化 |
| 模板 | 100+字段，重 | 10字段起步，轻 |
| 质量检查 | 50+项，繁琐 | 红绿灯3-5项 |
| 悬念管理 | 静态记录 | 动态追踪+预警 |
| AI味防治 | 负面清单 | 改写范例库 |
| 人机协作 | 正式交接 | 一句话续写 |

### 📚 新手指引

- **5分钟上手**：参见 [QUICK_START.md](QUICK_START.md)
- **功能总览**：参见 [README.md](README.md)
- **快速查找**：参见 [FILE_INDEX.md](FILE_INDEX.md)

---

## v0.8.0

- Added 故事引擎 (Story Engine) section with 核心机制, 代价与资源, 升级规则
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
