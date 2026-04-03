# 文件索引与导航

> 快速找到你需要的文档

---

## 📖 入门必读（3个文件）

| 优先级 | 文件名 | 用途 | 阅读时间 |
|--------|--------|------|---------|
| ⭐⭐⭐ | [README.md](README.md) | 项目总览，所有功能介绍 | 10分钟 |
| ⭐⭐⭐ | [QUICK_START.md](QUICK_START.md) | 5分钟上手指记 | 5分钟 |
| ⭐⭐⭐ | [SKILL.md](SKILL.md) | 主技能文件，完整工作流 | 30分钟 |

**推荐顺序**：QUICK_START → README → SKILL

---

## 📂 核心模板文件（4个）

### 大纲模板

| 文件名 | 适用场景 | 字段数 | 填写时间 |
|--------|---------|--------|---------|
| [outline-template-v1-minimal.md](references/outline-template-v1-minimal.md) | **默认推荐**，快速启动 | 10个 | 5分钟 |
| [outline-template.md](references/outline-template.md) | 复杂项目，需要详细规划 | 50+个 | 30分钟+ |

**建议**：先用极简版，写了几章后再根据需要补充标准版。

---

### 人物档案

| 文件名 | 适用场景 | 特点 |
|--------|---------|------|
| [character-template-v2.md](references/character-template-v2.md) | **默认推荐**，驱动式引擎 | 欲望-恐惧双引擎、声音指纹、缺陷-失败映射 |
| [character-template.md](references/character-template.md) | 静态档案，v1版本 | 基础字段，静态描述 |

**v2版核心改进**：
- 从"填空表格"变成"驱动引擎"
- 每个字段都能转化为写作约束
- 包含「声音锚点」保持对白一致性

---

### 其他模板

| 文件名 | 用途 |
|--------|------|
| [chapter-template.md](references/chapter-template.md) | 章节任务卡、场景拆分、复盘 |
| [progress-dashboard-template.md](references/progress-dashboard-template.md) | 进度仪表盘，AI自动维护 |
| [story-bible-template.md](references/story-bible-template.md) | 世界观与伏笔台账（复杂项目） |

---

## 🛠️ 工具脚本（3个）

| 文件名 | 用途 | 使用频率 |
|--------|------|---------|
| [check_chapter_wordcount.py](scripts/check_chapter_wordcount.py) | 字数检查 | 每章必用 |
| [check_ai_style.py](scripts/check_ai_style.py) | **AI味检测**（重点新功能） | 每章必用 |
| [generate_epub.py](scripts/generate_epub.py) | 导出EPUB电子书 | 完稿时用 |

**AI味检测脚本**（v2重点）：
```bash
python scripts/check_ai_style.py novels/我的小说/第01章.md
```

检测9种AI味症状：
- 🔴 重度：空泛形容词、情绪标签句、视角混乱
- 🟡 中度：四字成语、解释连接词、书面化对白
- 🟢 轻度：时间转折词、句式均匀

---

## 📚 改进文档（按轮次分类）

### 第一轮改进（轻量级骨架）

| 文件名 | 用途 | 类别 |
|--------|------|------|
| [outline-template-v1-minimal.md](references/outline-template-v1-minimal.md) | 极简大纲 | 模板 |
| [progress-dashboard-template.md](references/progress-dashboard-template.md) | 进度仪表盘 | 模板 |
| [check_ai_style.py](scripts/check_ai_style.py) | AI味检测 | 工具 |

---

### 第二轮改进（核心功能升级）

| 文件名 | 用途 | 重点内容 |
|--------|------|---------|
| [09-悬念生命周期管理.md](references/09-悬念生命周期管理.md) | 悬念追踪 | 状态定义、预警规则、推进方式 |
| [10-悬念-章节匹配矩阵.md](references/10-悬念-章节匹配矩阵.md) | 悬念规划 | 章节-悬念匹配、强度检查 |
| [11-叙事节奏框架.md](references/11-叙事节奏框架.md) | 节奏设计 | 三层体系、5种题材模板 |
| [character-template-v2.md](references/character-template-v2.md) | 人物档案 | 驱动式引擎、声音指纹 |
| [scene-design-v2.md](references/scene-design-v2.md) | 场景设计 | 任务检查卡、过渡技术、价值测试 |

---

### 第三轮改进（体验完善）

| 文件名 | 用途 | 重点内容 |
|--------|------|---------|
| [ai-style-examples.md](references/ai-style-examples.md) | **AI味改写** | 9种症状的前后对比范例 |
| [ai-style-by-genre.md](references/ai-style-by-genre.md) | **题材专项** | 悬疑/言情/玄幻/都市的AI味防治 |
| [08-人机协作-v2.md](references/08-人机协作-v2.md) | 协作协议 | 快速续写、信息提取 |
| [12-喘息机制.md](references/12-喘息机制.md) | 喘息章设计 | 黄金结构、情绪控制 |
| [13-钩子映射表.md](references/13-钩子映射表.md) | 钩子选择 | 关键节点-钩子类型映射 |

---

## 🎓 按场景查找文档

### 场景1：刚开始使用

需要解决的问题：
- 不知道怎么开始
- 不了解功能
- 想快速上手

推荐阅读：
1. [QUICK_START.md](QUICK_START.md) - 5分钟上手
2. [README.md](README.md) - 功能总览
3. [SKILL.md](SKILL.md) §三阶段工作流

---

### 场景2：每章写作时

需要解决的问题：
- 怎么继续写
- 质量如何检查
- 怎么管理悬念

相关文档：
1. [SKILL.md](SKILL.md) §连载期
2. [09-悬念生命周期管理.md](references/09-悬念生命周期管理.md) - 悬念规划
3. [check_ai_style.py](scripts/check_ai_style.py) - 质量检测

快速指令：
```text
继续写                    # 自动读取上下文
运行AI味检查              # 检测质量
查看进度仪表盘            # 看当前状态
```

---

### 场景3：去除AI味

需要解决的问题：
- 文本有AI感
- 不知道怎么改
- 需要改写范例

相关文档：
1. [ai-style-examples.md](references/ai-style-examples.md) - 9种症状改写范例
2. [ai-style-by-genre.md](references/ai-style-by-genre.md) - 按题材专项清单

快速查找：
- 空泛形容词堆砌 → ai-style-examples.md §症状1
- 四字成语 → ai-style-examples.md §症状2
- 情绪标签句 → ai-style-examples.md §症状5
- 悬疑类AI味 → ai-style-by-genre.md §悬疑

---

### 场景4：设计节奏

需要解决的问题：
- 不知道怎么安排章节节奏
- 不知道每章应该写什么强度
- 某题材的节奏特点

相关文档：
1. [11-叙事节奏框架.md](references/11-叙事节奏框架.md) - 三层体系+题材模板
2. [13-钩子映射表.md](references/13-钩子映射表.md) - 关键节点-钩子映射
3. [12-喘息机制.md](references/12-喘息机制.md) - 喘息章设计

快速查找：
- 悬疑节奏 → 11-叙事节奏框架.md §悬疑/推理
- 玄幻节奏 → 11-叙事节奏框架.md §玄幻升级流
- 钩子选择 → 13-钩子映射表.md
- 什么时候喘息 → 12-喘息机制.md

---

### 场景5：设计人物

需要解决的问题：
- 人物不够立体
- 人物前后不一致
- 对白没有区分度

相关文档：
1. [character-template-v2.md](references/character-template-v2.md) - 人物驱动引擎
2. [ai-style-by-genre.md](references/ai-style-by-genre.md) §言情 - 人物描写专项

重点阅读：
- 欲望-恐惧双引擎 §核心引擎
- 声音指纹 §声音指纹
- 缺陷-失败映射 §缺陷-失败映射

---

### 场景6：设计场景

需要解决的问题：
- 场景没有任务
- 不知道场景怎么过渡
- 场景太长/太短

相关文档：
1. [scene-design-v2.md](references/scene-design-v2.md) - 场景设计工具
2. [scene-design.md](references/scene-design.md) - 基础指南（v1）

重点阅读：
- 场景任务检查卡 §场景任务检查卡
- Scene/Sequel §Scene/Sequel实用指南
- 六种过渡技术 §六种场景过渡技术
- 场景价值测试 §场景价值测试

---

### 场景7：协作/交接

需要解决的问题：
- 多人协作
- 人类修改后交给AI
- 长时间中断后恢复

相关文档：
1. [08-人机协作-v2.md](references/08-人机协作-v2.md) - 快速协作协议

快速模式（默认）：
```text
继续写              # AI自动提取上下文
```

正式模式（特殊）：
```markdown
## 人类修改记录
- 修改位置：第X章 第Y段
- 修改原因：___
- 继续要求：___
```

---

## 🔍 按关键词查找

| 关键词 | 相关文档 |
|--------|---------|
| 快速开始 | QUICK_START.md |
| 极简大纲 | outline-template-v1-minimal.md |
| 质量检查 | check_ai_style.py, SKILL.md §红绿灯 |
| AI味 | ai-style-examples.md, ai-style-by-genre.md |
| 悬念管理 | 09-悬念生命周期管理.md, 10-悬念-章节匹配矩阵.md |
| 节奏设计 | 11-叙事节奏框架.md, 13-钩子映射表.md |
| 人物塑造 | character-template-v2.md |
| 场景设计 | scene-design-v2.md |
| 喘息章 | 12-喘息机制.md |
| 钩子技巧 | 13-钩子映射表.md, hook-techniques.md |
| 对白写作 | dialogue-writing.md, ai-style-by-genre.md §言情 |
| 导出epub | generate_epub.py, README.md §导出EPUB |

---

## 📊 文档重要性矩阵

```
重要性
 高 │ 极简大纲   AI味改写   悬念管理
     │ (v1)      (v2重点)   (v2重点)
     │
 中 │ 人物v2    节奏框架   场景v2
     │ (v2)      (v2)       (v2)
     │
 低 │ 喘息机制  钩子映射   协作v2
     │ (v2)      (v2)       (v2)
     └──────────────────────────────→
       高频      中频       低频      使用频率
```

**建议优先掌握**：
1. 极简大纲（每次新项目）
2. AI味改写（每次质量检查）
3. 悬念管理（每章规划）

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
│   │   ├── chapter-template.md              章节模板
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
│   ├── check_ai_style.py            ⭐⭐ AI味检测
│   └── generate_epub.py             EPUB导出
│
└── 📁 novels/                       📝 小说目录
    └── （你的小说项目）
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
├── 09-悬念生命周期管理.md（20分钟）
├── 11-叙事节奏框架.md（30分钟）
└── 实践：规划悬念+检查节奏

第4周：精通
├── character-template-v2.md（30分钟）
├── scene-design-v2.md（20分钟）
└── 实践：完整使用所有工具
```

### 遇到问题

1. **不知道从哪里开始** → QUICK_START.md
2. **AI写的有机器感** → ai-style-examples.md
3. **节奏感觉不对** → 11-叙事节奏框架.md
4. **悬念写到后面忘了** → 09-悬念生命周期管理.md
5. **人物前后不一致** → character-template-v2.md
6. **不知道怎么继续** → 对AI说"继续写"（自动读取上下文）

---

## 📝 更新记录

- **2026-04-01**: 完成三轮优化，新增13个文件，更新README和文档
- **2026-03-20**: v1.0.0 版本发布

---

*如果找不到需要的文档，使用 Ctrl+F 在本页面搜索关键词。*
