# 文件索引与导航

> 快速找到你需要的文档

---

## 📖 入门必读（3 个文件）

| 优先级 | 文件名 | 用途 | 阅读时间 |
|--------|--------|------|---------|
| ⭐⭐⭐ | [README.md](README.md) | 项目总览，所有功能介绍 | 10 分钟 |
| ⭐⭐⭐ | [QUICK_START.md](QUICK_START.md) | 5 分钟上手指记 | 5 分钟 |
| ⭐⭐⭐ | [SKILL.md](SKILL.md) | 主技能文件，完整工作流 | 30 分钟 |

**推荐顺序**：QUICK_START → README → SKILL

---

## 🧭 v3 创作核心

| 文件名 | 什么时候读取 | 核心用途 |
|--------|-------------|---------|
| [creative-compass.md](references/creative-compass.md) | 新项目、重大转向、故事失去生命力 | 三向故事发现、创作宪章、人物压力、因果脊柱、意象与独创性审计 |
| [editorial-revision.md](references/editorial-revision.md) | 修改、重写、去 AI 味、完稿 | 体验→结构→人物→场景→语言→连续性分层修订与伟大作品门控 |
| [quality-checklist.md](references/quality-checklist.md) | 章节交付与终稿门控 | 用正文证据判断，不使用可互相抵消的总分 |

## 📂 核心模板文件

### 大纲模板

| 文件名 | 适用场景 | 字段数 | 填写时间 |
|--------|---------|--------|---------|
| [outline-template-v1-minimal.md](references/outline-template-v1-minimal.md) | **默认推荐**，快速启动 | 创作宪章 + 12 个短区块 | 10-20 分钟 |
| [outline-template.md](references/outline-template.md) | 复杂项目，需要详细规划 | 50+ 个 | 30 分钟 + |

**建议**：先用极简版，写了几章后再根据需要补充标准版。

---

### 人物档案

| 文件名 | 适用场景 | 特点 |
|--------|---------|------|
| [character-template-v2.md](references/character-template-v2.md) | **默认推荐**，人物压力系统 | 公开追求、保护策略、自我谎言、矛盾、有限信息与可观察关系证据 |
| [character-template.md](references/character-template.md) | 静态档案，v1 版本 | 基础字段，静态描述 |

**v3 人物模板核心改进**：
- 从"填空表格"变成"驱动引擎"
- 用保护策略和压力解释选择，而非固定性格词
- 用可观察证据记录关系，不用信任百分比
- 允许人物做出惊人但回看合理的选择

---

### 其他模板

| 文件名 | 用途 |
|--------|------|
| [chapter-template.md](references/chapter-template.md) | 干净章节正文模板，仅用于 `manuscript/zh` |
| [chapter-workspace-template.md](references/chapter-workspace-template.md) | 章节任务卡、场景拆分、沙盘、复盘和修改记录 |
| [progress-dashboard-template.md](references/progress-dashboard-template.md) | 进度仪表盘，AI 自动维护 |
| [story-bible-template.md](references/story-bible-template.md) | 世界观与伏笔台账（复杂项目） |

### 短故事模板

| 文件名 | 适用场景 | 硬标准 |
|--------|---------|--------|
| [short-story-template.md](references/short-story-template.md) | 写一篇完整短故事 / 短篇故事 | 写入 `short-stories/YYYYMMDD-<标题>.md`，正文不少于 6000 字，剧情必须闭合 |

### 翻译流程

| 文件名 | 适用场景 | 核心用途 |
|--------|---------|----------|
| [translation-workflow.md](references/translation-workflow.md) | 当前 AI 意译翻译 | 默认输出到 `manuscript/en`，包含翻译简报、术语表、风格表、样章校准、双语修订、单语润色和终检 |

---

## 🎭 角色沙盘模式（v2.4 重点）

| 文件名 | 用途 | 重点内容 |
|--------|------|---------|
| [14-角色沙盘模式.md](references/14-角色沙盘模式.md) | 每章角色沙盘 | 一个角色一个运行时文件、有限信息发言、导演裁决、沙盘回写 |

**什么时候读**：
- 每章写作前想先校验“角色自己会不会这么做”
- 群像、悬疑、权谋、言情拉扯、反派行动章
- 人物越来越像工具人、行动只服务大纲

**小说目录中对应文件**：
```text
04-角色沙盘/
├── 00-角色索引.md
├── C001-角色名.md
└── sessions/
    └── 第XXX章-沙盘记录.md
```

---

## 🛠️ 工具脚本（9 个）

| 文件名 | 用途 | 使用频率 |
|--------|------|---------|
| [check_chapter_wordcount.py](scripts/check_chapter_wordcount.py) | 章节 / 短故事字数检查 | 每章必用；短故事用 `6000` 最小字数 |
| [check_short_story.py](scripts/check_short_story.py) | 短故事硬边界与结构信号（不能替代通读） | 每篇短故事必用 |
| [check_ai_style.py](scripts/check_ai_style.py) | **AI 痕迹启发式扫描**（9 种症状，支持--all 批量） | 每章完成后按需复核 |
| [check_novel_health.py](scripts/check_novel_health.py) | **长篇机械健康信号**（字数 + 关键词场景分布） | 每 5-10 章 |
| [check_timeline.py](scripts/check_timeline.py) | **时间线一致性检查**（季节/天气/时段） | 每 10 章或完稿时 |
| [character_tracker.py](scripts/character_tracker.py) | **人物一致性检查**（禁止用语 + 情绪突变） | 每 10 章或完稿时 |
| [generate_epub.py](scripts/generate_epub.py) | 导出 EPUB 电子书 | 完稿时用 |
| [translate_to_english.py](scripts/translate_to_english.py) | 生成当前 AI 意译翻译任务包 | 按需 |
| [split_chapter_workspace.py](scripts/split_chapter_workspace.py) | 拆分旧混合章节为 `manuscript/zh` 正文和 `workspace/chapters` 工作台 | 旧项目迁移时 |

**AI 痕迹启发式扫描**：
```bash
python scripts/check_ai_style.py novels/我的小说/manuscript/zh/第001章-标题.md
```

检测 9 种机械症状并给出复核优先级。命中不等于错误，低信号也不等于作品成熟；必须结合 POV、人物选择、因果和完整段落人工判断。

---

## 📚 改进文档（按轮次分类）

### 第一轮改进（轻量级骨架）

| 文件名 | 用途 | 类别 |
|--------|------|------|
| [outline-template-v1-minimal.md](references/outline-template-v1-minimal.md) | 极简大纲 | 模板 |
| [progress-dashboard-template.md](references/progress-dashboard-template.md) | 进度仪表盘 | 模板 |
| [check_ai_style.py](scripts/check_ai_style.py) | AI 味检测 | 工具 |

---

### 第二轮改进（核心功能升级）

| 文件名 | 用途 | 重点内容 |
|--------|------|---------|
| [09-悬念生命周期管理.md](references/09-悬念生命周期管理.md) | 悬念追踪 | 状态定义、预警规则、推进方式 |
| [10-悬念 - 章节匹配矩阵.md](references/10-悬念-章节匹配矩阵.md) | 悬念规划 | 章节 - 悬念匹配、强度检查 |
| [11-叙事节奏框架.md](references/11-叙事节奏框架.md) | 节奏设计 | 三层体系、5 种题材模板 |
| [character-template-v2.md](references/character-template-v2.md) | 人物档案 | 驱动式引擎、声音指纹 |
| [scene-design-v2.md](references/scene-design-v2.md) | 场景设计 | 任务检查卡、过渡技术、价值测试 |

---

### 第三轮改进（体验完善）

| 文件名 | 用途 | 重点内容 |
|--------|------|---------|
| [ai-style-examples.md](references/ai-style-examples.md) | **AI 味改写** | 9 种症状的前后对比范例 |
| [ai-style-by-genre.md](references/ai-style-by-genre.md) | **题材专项** | 悬疑/言情/玄幻/都市的 AI 味防治 |
| [08-人机协作-v2.md](references/08-人机协作-v2.md) | 协作协议 | 快速续写、信息提取 |
| [12-喘息机制.md](references/12-喘息机制.md) | 喘息章设计 | 黄金结构、情绪控制 |
| [13-钩子映射表.md](references/13-钩子映射表.md) | 钩子选择 | 关键节点 - 钩子类型映射 |

---

### 第四轮改进（角色沙盘）

| 文件名 | 用途 | 重点内容 |
|--------|------|---------|
| [14-角色沙盘模式.md](references/14-角色沙盘模式.md) | 角色沙盘 | 复杂章节按需运行、角色可反抗大纲、单角色运行时记忆、导演裁决 |

---

## 🎓 按场景查找文档

### 场景 1：刚开始使用

需要解决的问题：
- 不知道怎么开始
- 不了解功能
- 想快速上手

推荐阅读：
1. [QUICK_START.md](QUICK_START.md) - 5 分钟上手
2. [README.md](README.md) - 功能总览
3. [SKILL.md](SKILL.md) §三阶段工作流

---

### 场景 2：写一篇短故事

需要解决的问题：
- 不想开长篇，只要一篇完整短故事
- 需要不少于 6000 字
- 需要可分段或换行，但剧情完整
- 需要生成命名 Markdown 文件，而不是把全文贴在对话中

相关文档：
1. [SKILL.md](SKILL.md) §短故事模式
2. [short-story-template.md](references/short-story-template.md) - 短故事任务卡、完整剧情骨架和 `short-stories/YYYYMMDD-<标题>.md` 命名规则
3. [check_short_story.py](scripts/check_short_story.py) - 检查 6000 字、正文区、完稿复盘和剧情收束

快速指令：
```text
写一篇悬疑短故事，不少于 6000 字
写一个完整短篇故事，可以分段
```

---

### 场景 3：每章写作时

需要解决的问题：
- 怎么继续写
- 质量如何检查
- 怎么管理悬念
- 怎么让人物行为先于大纲自然发生

相关文档：
1. [SKILL.md](SKILL.md) §连载期
2. [14-角色沙盘模式.md](references/14-角色沙盘模式.md) - 每章角色沙盘
3. [09-悬念生命周期管理.md](references/09-悬念生命周期管理.md) - 悬念规划
4. [check_ai_style.py](scripts/check_ai_style.py) - 质量检测

快速指令：
```text
继续写                    # 自动读取上下文
执行角色沙盘              # 先做角色意志校验
运行 AI 味检查              # 检测质量
查看进度仪表盘            # 看当前状态
```

---

### 场景 4：去除 AI 味

需要解决的问题：
- 文本有 AI 感
- 不知道怎么改
- 需要改写范例

相关文档：
1. [ai-style-examples.md](references/ai-style-examples.md) - 9 种症状改写范例
2. [ai-style-by-genre.md](references/ai-style-by-genre.md) - 按题材专项清单

快速查找：
- 空泛形容词堆砌 → ai-style-examples.md §症状 1
- 四字成语 → ai-style-examples.md §症状 2
- 情绪标签句 → ai-style-examples.md §症状 5
- 悬疑类 AI 味 → ai-style-by-genre.md §悬疑

---

### 场景 5：设计节奏

需要解决的问题：
- 不知道怎么安排章节节奏
- 不知道每章应该写什么强度
- 某题材的节奏特点

相关文档：
1. [11-叙事节奏框架.md](references/11-叙事节奏框架.md) - 三层体系 + 题材模板
2. [13-钩子映射表.md](references/13-钩子映射表.md) - 关键节点 - 钩子映射
3. [12-喘息机制.md](references/12-喘息机制.md) - 喘息章设计

快速查找：
- 悬疑节奏 → 11-叙事节奏框架.md §悬疑/推理
- 玄幻节奏 → 11-叙事节奏框架.md §玄幻升级流
- 钩子选择 → 13-钩子映射表.md
- 什么时候喘息 → 12-喘息机制.md

---

### 场景 6：设计人物

需要解决的问题：
- 人物不够立体
- 人物前后不一致
- 对白没有区分度
- 人物行动像作者安排，不像自己选择

相关文档：
1. [character-template-v2.md](references/character-template-v2.md) - 人物驱动引擎
2. [14-角色沙盘模式.md](references/14-角色沙盘模式.md) - 角色运行时记忆和每章发言
3. [ai-style-by-genre.md](references/ai-style-by-genre.md) §言情 - 人物描写专项

重点阅读：
- 欲望 - 恐惧双引擎 §核心引擎
- 声音指纹 §声音指纹
- 缺陷 - 失败映射 §缺陷 - 失败映射
- 角色沙盘模式 §单角色运行时文件模板

---

### 场景 7：设计场景

需要解决的问题：
- 场景没有任务
- 不知道场景怎么过渡
- 场景太长/太短

相关文档：
1. [scene-design-v2.md](references/scene-design-v2.md) - 场景设计工具
2. [scene-design.md](references/scene-design.md) - 基础指南（v1）

重点阅读：
- 场景任务检查卡 §场景任务检查卡
- Scene/Sequel §Scene/Sequel 实用指南
- 六种过渡技术 §六种场景过渡技术
- 场景价值测试 §场景价值测试

---

### 场景 8：协作/交接

需要解决的问题：
- 多人协作
- 人类修改后交给 AI
- 长时间中断后恢复

相关文档：
1. [08-人机协作-v2.md](references/08-人机协作-v2.md) - 快速协作协议

快速模式（默认）：
```text
继续写              # AI 自动提取上下文
```

正式模式（特殊）：
```markdown
## 人类修改记录
- 修改位置：第 X 章 第 Y 段
- 修改原因：___
- 继续要求：___
```

---

## 🔍 按关键词查找

| 关键词 | 相关文档 |
|--------|---------|
| 快速开始 | QUICK_START.md |
| 极简大纲 | outline-template-v1-minimal.md |
| 短故事 / 短篇故事 | short-story-template.md, SKILL.md §短故事模式 |
| 6000 字故事 | short-story-template.md, check_short_story.py |
| 质量检查 | quality-checklist.md, editorial-revision.md, check_ai_style.py |
| AI 味 | ai-style-examples.md, ai-style-by-genre.md |
| 悬念管理 | 09-悬念生命周期管理.md, 10-悬念 - 章节匹配矩阵.md |
| 角色沙盘 | 14-角色沙盘模式.md, progress-dashboard-template.md |
| 角色反抗大纲 | 14-角色沙盘模式.md |
| 节奏设计 | 11-叙事节奏框架.md, 13-钩子映射表.md |
| 人物塑造 | character-template-v2.md, 14-角色沙盘模式.md |
| 场景设计 | scene-design-v2.md |
| 喘息章 | 12-喘息机制.md |
| 钩子技巧 | 13-钩子映射表.md, hook-techniques.md |
| 对白写作 | dialogue-writing.md, ai-style-by-genre.md §言情 |
| 导出 epub | generate_epub.py, README.md §导出 EPUB |

---

## 📊 文档重要性矩阵

```
重要性
 高 │ 创作罗盘   极简大纲   分层编辑   证据门控
     │ (v3)      (v3)       (v3)       (v3)
     │
 中 │ 人物v3    角色沙盘   场景v2    悬念管理
     │ (v3)      (按需)      (启发式)   (按需)
     │
 低 │ 喘息机制  钩子映射   协作v2
     │ (启发式)  (启发式)    (按需)
     └──────────────────────────────→
       高频      中频       低频      使用频率
```

**建议优先掌握**：
1. 创作罗盘与创作宪章（每次新项目）
2. 因果任务卡（每章）
3. 分层编辑协议（修改与完稿）
4. 角色沙盘、悬念和脚本工具（问题出现时按需加载）

---

## 🗂️ 文件组织结构

```
chinese-novelist-skill/
│
├── 📄 根目录文档
│   ├── README.md                    ⭐ 项目总览
│   ├── QUICK_START.md               ⭐ 快速上手
│   ├── WORKFLOW_GUIDE.md            ⭐ 工作流可视化
│   ├── FILE_INDEX.md                📍 本文件
│   ├── SKILL.md                     ⭐ 主技能文件
│   └── OPTIMIZATION_PLAN.md         📋 优化计划
│
├── 📁 references/                   📚 参考文档
│   ├── ⭐ 核心模板
│   │   ├── outline-template-v1-minimal.md    ⭐ 极简大纲
│   │   ├── character-template-v2.md          ⭐ 人物v2
│   │   ├── chapter-template.md              干净章节正文模板
│   │   ├── chapter-workspace-template.md    章节工作台模板
│   │   ├── short-story-template.md          短故事模板
│   │   ├── progress-dashboard-template.md   进度仪表盘
│   │   └── story-bible-template.md            世界观
│   │
│   ├── 🔧 v2改进文档（第二轮）
│   │   ├── 09-悬念生命周期管理.md           ⭐ 悬念追踪
│   │   ├── 10-悬念-章节匹配矩阵.md           悬念规划
│   │   ├── 11-叙事节奏框架.md               ⭐ 节奏设计
│   │   └── scene-design-v2.md               场景工具
│   │
│   ├── ✨ v2改进文档（第三轮）
│   │   ├── ai-style-examples.md             ⭐⭐ AI味改写
│   │   ├── ai-style-by-genre.md             ⭐ 题材专项
│   │   ├── 08-人机协作-v2.md                协作协议
│   │   ├── 12-喘息机制.md                   喘息章
│   │   └── 13-钩子映射表.md                 钩子选择
│   │
│   ├── 🎭 v2.4角色沙盘
│   │   └── 14-角色沙盘模式.md               ⭐⭐ 每章角色意志校验
│   │
│   └── 📖 v1原始文档
│       ├── outline-template.md              标准大纲
│       ├── character-template.md            人物v1
│       ├── scene-design.md                  场景v1
│       ├── chapter-guide.md                 章节指南
│       ├── opening-design.md                首章设计
│       ├── hook-techniques.md               钩子技巧
│       ├── dialogue-writing.md              对白写作
│       ├── style-polishing.md               文风打磨
│       ├── plot-structures.md               剧情结构
│       ├── consistency.md                   一致性
│       ├── content-expansion.md             内容扩写
│       ├── ending-design.md                 结局设计
│       └── ...（其他）
│
├── 📁 scripts/                      🛠️ 工具脚本
│   ├── check_chapter_wordcount.py   ⭐ 字数检查
│   ├── check_short_story.py         ⭐ 短故事检查
│   ├── check_ai_style.py            ⭐⭐ AI味检测
│   └── generate_epub.py             EPUB导出
│
├── 📁 novels/                       📝 小说目录
    └── （你的小说项目）

└── 📁 short-stories/                📝 短故事目录（可选）
    └── （你的短故事）
```

---

## 💡 使用建议

### 新手路径

```
第1周：掌握核心
├── QUICK_START.md（5分钟）
├── README.md（10分钟）
└── 实践：写3-5章

第2周：提升质量
├── ai-style-examples.md（30分钟）
├── check_ai_style.py（每次写作使用）
└── 实践：修改已有章节

第3周：掌握进阶
├── 14-角色沙盘模式.md（30分钟）
├── 09-悬念生命周期管理.md（20分钟）
├── 11-叙事节奏框架.md（30分钟）
└── 实践：跑每章沙盘+规划悬念+检查节奏

第4周：精通
├── character-template-v2.md（30分钟）
├── scene-design-v2.md（20分钟）
└── 实践：完整使用所有工具
```

### 遇到问题

1. **不知道从哪里开始** → QUICK_START.md
2. **AI 写的有机器感** → ai-style-examples.md
3. **节奏感觉不对** → 11-叙事节奏框架.md
4. **悬念写到后面忘了** → 09-悬念生命周期管理.md
5. **人物前后不一致** → character-template-v2.md + 14-角色沙盘模式.md
6. **只想写短故事** → short-story-template.md
7. **不知道怎么继续** → 对 AI 说"继续写"（自动读取上下文）

---

## 📝 更新记录

- **2026-07-31**: v3.0.0 引入创作罗盘、分层编辑、独创性审计和伟大作品证据式门控；主入口压缩为渐进式路由
- **2026-07-07**: v2.6.2 修复短故事模式输出边界，完整正文必须写入命名 Markdown 文件
- **2026-07-06**: v2.5 新增短故事模式，不少于 6000 字且剧情完整
- **2026-06-26**: v2.4 新增角色沙盘模式，每章写作前进行角色意志校验
- **2026-04-01**: 完成三轮优化，新增 13 个文件，更新 README 和文档
- **2026-03-20**: v1.0.0 版本发布

---

*如果找不到需要的文档，使用 Ctrl+F 在本页面搜索关键词。*
