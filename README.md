# chinese-novelist-skill

> 从一句真正值得写的矛盾，到拥有独特生命的中文小说。
> 核心目标：让人物、世界、因果和语言彼此需要，同时保留长篇创作的工程稳定性。

---

## 一眼看懂

**chinese-novelist-skill** 是一套中文小说创作与编辑系统。它先比较真正不同的故事方向，建立创作宪章、人物压力与因果脊柱，再按章写作、独立修订并维护长篇状态。脚本只负责发现机械风险，不冒充审美裁判。用户明确要求“短故事 / 短篇故事 / 写一篇完整故事”时，也可以切换到短故事模式，创建不少于 6000 字且剧情完整的单篇故事 Markdown 文件。

```text
一句话创意
  -> 三向故事发现
  -> 创作宪章与因果脊柱
  -> 人物压力系统
  -> 干净章节正文
  -> 独立编辑与证据式门控
  -> 回写进度
  -> 完稿导出

短故事请求
  -> 短故事任务卡
  -> 完整剧情骨架
  -> 写入 short-stories/YYYYMMDD-标题.md
  -> 检查并汇报路径
```

### 适合你，如果你正在遇到

| 问题 | skill 里的解法 |
|------|----------------|
| 点子像题材模板，没有“非它不可” | [创作罗盘](references/creative-compass.md) + 独创性审计 |
| 写到十几章后忘了前面埋的线 | 悬念生命周期 + 章节匹配 |
| 人物行为像服务大纲，不像真人 | [角色沙盘模式](references/14-角色沙盘模式.md) |
| AI 写出来有解释腔、空洞情绪、四字堆砌 | 启发式扫描 + 从 POV 和具体经验重建 |
| 每章不知道该推进什么 | 因果任务卡 + 人物压力与不可逆变化 |
| 长篇文件越来越乱 | `manuscript/` 干净正文 + `workspace/` 创作工作台 |
| 只想写一篇完整短故事 | 短故事模式 + 6000 字红灯线 + 剧情闭合检查 |

---

## 5 分钟开始

### 1. 创建一本新小说

```text
使用 chinese-novelist-skill，帮我写一本悬疑小说，20 章。
```

AI 会交付：

| 产物 | 用途 |
|------|------|
| 3 个实质故事方向 | 比较选择、对手答案和结局代价，不只换设定 |
| 创作宪章与极简总纲 | 锁定读者契约、主题问题、因果脊柱与风格边界 |
| 人物初稿 | 建立公开追求、保护策略、自我谎言和声音 |
| 第 1 章任务卡 | 让首章可以立刻开写 |

### 2. 写一篇短故事

```text
使用 chinese-novelist-skill，写一篇悬疑短故事，不少于 6000 字。
```

短故事模式不会进入长篇连载流程。AI 会创建命名 Markdown 文件，默认路径为 `short-stories/YYYYMMDD-<标题>.md`，并只在对话中汇报路径、字数和检查结果。

| 产物 | 用途 |
|------|------|
| 短故事任务卡 | 锁定 premise、主角欲望、冲突和结局类型 |
| 完整剧情骨架 | 保证开端、升级、反转、高潮、收束都存在 |
| ≥6000 字正文 | 写入 Markdown 文件，可分段或换行，但必须是完整故事 |
| 完稿复盘 | 检查字数、主角变化、伏笔 / 意象回收和结尾闭合 |

模板见 [short-story-template.md](references/short-story-template.md)。除非你明确要求“直接在对话里输出全文”，否则完整正文不会粘贴到聊天窗口。

### 3. 继续写下一章

```text
继续写
```

标准模式下，每章默认执行：

1. 读取 `99-进度仪表盘.md`
2. 检查悬念状态
3. 执行角色沙盘
4. 生成本章任务卡
5. 写正文
6. 运行质量检查
7. 回写仪表盘、悬念和角色文件

### 4. 快速出初稿

```text
快写下一章，先出初稿。
```

快速模式会压缩场景拆分，但仍保留最小沙盘：POV 角色深度发言 + 核心人物轻量心跳。

---

## 项目文件地图

推荐每本小说放在 `novels/<书名>/` 下：

```text
novels/
└── 我的小说/
    ├── manuscript/
    │   ├── zh/
    │   │   ├── 第001章-标题.md
    │   │   └── 第002章-标题.md
    │   └── en/
    │       ├── Chapter-001.md
    │       └── Chapter-002.md
    ├── workspace/
    │   └── chapters/
    │       └── 第001章-标题/
    │           ├── task-card.md
    │           ├── scene-plan.md
    │           ├── sandbox.md
    │           ├── review.md
    │           └── revision-notes.md
    ├── 00-大纲.md
    ├── 01-人物档案.md
    ├── 02-世界观与伏笔.md
    ├── 03-悬念追踪表.md
    ├── 04-角色沙盘/
    │   ├── 00-角色索引.md
    │   ├── C001-主角名.md
    │   ├── C002-反派名.md
    │   └── sessions/
    │       └── 第001章-沙盘记录.md
    └── 99-进度仪表盘.md
```

短故事可以使用轻量目录：

```text
short-stories/
└── 我的短故事.md
```

### 核心文件分工

| 文件 | 谁维护 | 什么时候看 |
|------|--------|------------|
| `00-大纲.md` | 用户 + AI | 新建、章节偏航、收尾 |
| `01-人物档案.md` | 用户 + AI | 人物设计、关系变化 |
| `02-世界观与伏笔.md` | 用户 + AI | 设定、伏笔、隐藏真相 |
| `03-悬念追踪表.md` | AI 为主 | 每章规划和回写 |
| `04-角色沙盘/00-角色索引.md` | AI 为主 | 每章选角 |
| `04-角色沙盘/C001-角色名.md` | AI 为主 | 每章角色状态回写 |
| `04-角色沙盘/sessions/第XXX章-沙盘记录.md` | AI 为主 | 留存每章角色会议和导演裁决 |
| `99-进度仪表盘.md` | AI 自动维护 | 续写恢复、整体追踪 |
| `manuscript/zh/第XXX章-标题.md` | 用户 + AI | 干净中文正文，唯一事实来源 |
| `workspace/chapters/第XXX章-标题/` | AI 为主 | 本章任务卡、场景拆分、沙盘、复盘、修改记录 |

章节正文文件保持极简：

```markdown
第001章：标题

正文第一段。

正文第二段。
```

旧项目如果已经有根目录混合章节，可以运行：

```bash
python3 scripts/split_chapter_workspace.py novels/我的小说
```

确认拆分正确后，可用 `--move-originals` 把旧章节归档到 `_archive/mixed-chapters/`。

---

## 核心能力

### 0. 创作罗盘与伟大作品门控

[创作罗盘](references/creative-compass.md) 不把第一反应直接扩写成大纲。它先比较三个会导向不同人物选择和结局代价的方向，再建立读者契约、主题问题、中央矛盾、人物压力、因果脊柱、意象与风格宪章。

[编辑修订协议](references/editorial-revision.md) 把修订拆成体验、结构、人物、场景、语言、结局和连续性各轮。最终不使用能互相抵消的总分，而是为独特性、必然性、人物复杂度、结构惊奇、语言准确度、情感余震和整体完成度提供正文证据。

### 短故事模式（可选）

当用户明确说“短故事”“短篇故事”“写一篇完整故事”时，skill 进入短故事模式。默认要求正文不少于 6000 个中文字符，可以自然分段或换行，但必须完成完整剧情闭环：开端、诱发事件、升级、反转或代价、高潮选择、结局收束。

短故事不默认创建长篇项目目录，也不运行每章连载循环。必须写入命名 Markdown 文件，默认使用 `short-stories/YYYYMMDD-<标题>.md`，并套用 [short-story-template.md](references/short-story-template.md)。对话中只汇报文件路径、正文字数和检查结果。

### 1. 三阶段工作流

| 阶段 | 目标 | 触发词 |
|------|------|--------|
| 策划期 | 锁定大纲、人物、首章任务 | “写一本”“从头开始” |
| 连载期 | 按章推进，持续回写状态 | “继续写”“下一章” |
| 收尾期 | 完稿检查、伏笔回收、导出 | “写完了”“导出 epub” |

你不用记复杂模式。大多数时候，只要说“继续写”，skill 会自动定位进度并推进下一章。

### 2. 角色沙盘模式

[角色沙盘模式](references/14-角色沙盘模式.md) 让关键角色以自己的有限认知发言，适合人物行为可疑、多人冲突、群像与重大选择章节。

它解决的是一个长篇常见问题：大纲说角色该去 A，但按这个角色当前的恐惧、误判、资源和关系，他其实更可能去 B。

每章沙盘分 5 步：

| 步骤 | 产物 |
|------|------|
| 选角 | 本章哪些角色深度发言、轻量心跳或冻结 |
| 有限信息 | 角色只看到自己应该知道的事实 |
| 角色发言 | 行动倾向、反抗大纲、关系判断、场景建议 |
| 导演裁决 | 按人物一致性、主线、悬念、原大纲、钩子排序 |
| 回写状态 | 更新角色文件、沙盘记录和进度仪表盘 |

使用原则：

- 人物与大纲冲突、群像或重大选择时优先使用；普通章节可用任务卡中的最小压力检查。
- 一个关键角色一个运行时文件。
- 角色可以反抗大纲，但最终由导演裁决。
- 角色不写正文，只提供行动倾向和一句可能说出口的话。

### 3. 悬念生命周期管理

悬念不是“记一下”，而是有状态：

| 状态 | 含义 | 处理 |
|------|------|------|
| 活跃 | 最近被提及，读者还记得 | 可推进 |
| 即将过期 | 多章未提及 | 本章保温 |
| 已过期 | 太久未出现 | 必须处理 |
| 已回收 | 已回答或兑现 | 归档 |

参考：

- [09-悬念生命周期管理.md](references/09-悬念生命周期管理.md)
- [10-悬念-章节匹配矩阵.md](references/10-悬念-章节匹配矩阵.md)

### 4. 证据式质量门控

每章先守住存在理由、因果变化、人物真实、专属经验、连续性和完整交付。安静章节可以用关系、认知、决定或意象收尾，不强制悬念钩子。

完稿时按 [小说质量门控](references/quality-checklist.md) 给出“正文证据、最强处、最弱处、最高杠杆修改”，不再用总分宣布优秀或伟大。

### 5. AI 痕迹启发式扫描

```bash
python3 scripts/check_ai_style.py novels/我的小说/manuscript/zh/第001章-标题.md
```

支持标记 9 类常见机械症状。结果只决定人工复核优先级，不能判断作者身份或文学质量；命中的正确表达可以保留。

| 严重度 | 症状 |
|--------|------|
| 重度 | 空泛形容词、情绪标签句、视角混乱 |
| 中度 | 四字成语堆砌、解释性连接词、书面化对白、信息倾倒 |
| 轻度 | 时间转折词滥用、句式过于均匀 |

参考：

- [ai-style-examples.md](references/ai-style-examples.md)
- [ai-style-by-genre.md](references/ai-style-by-genre.md)

### 6. 叙事节奏与章节设计

| 层级 | 工具 | 用途 |
|------|------|------|
| 全本 | [11-叙事节奏框架.md](references/11-叙事节奏框架.md) | 四幕结构、关键节点、题材模板 |
| 章节组 | 黄金三章模式 | 铺垫、升级、小高潮 |
| 单章 | [scene-design-v2.md](references/scene-design-v2.md) | 场景任务、价值变化、过渡 |
| 开头 | [opening-design.md](references/opening-design.md) | 首章吸引力 |
| 结尾 | [ending-design.md](references/ending-design.md) | 收束与余味 |

---

## 常用命令

### 测试 skill

```bash
PYTHONPATH=scripts python3 -m unittest discover tests/ -v
```

### 发版前验证

v2.6.2 发布前已通过以下检查：

```bash
PYTHONPATH=scripts python3 -m unittest discover tests/ -v
python3 -m py_compile scripts/*.py tests/*.py
python3 -m json.tool test-prompts.json >/dev/null
git diff --check
```

发布包应排除 `.git/`、`.claude/`、`__pycache__/`、`*.pyc`、`.DS_Store`、`dist/` 和已有 `.skill` 产物。

### 检查章节字数

```bash
python3 scripts/check_chapter_wordcount.py novels/我的小说/manuscript/zh/第001章-标题.md
python3 scripts/check_chapter_wordcount.py --all novels/我的小说
```

### 检查短故事

```bash
python3 scripts/check_short_story.py short-stories/我的短故事.md
python3 scripts/check_short_story.py --all short-stories
```

### 检查 AI 味

```bash
python3 scripts/check_ai_style.py novels/我的小说/manuscript/zh/第001章-标题.md
python3 scripts/check_ai_style.py --all novels/我的小说
```

### 小说健康检查

```bash
python3 scripts/check_novel_health.py novels/我的小说
```

### 时间线和人物一致性

```bash
python3 scripts/check_timeline.py novels/我的小说
python3 scripts/character_tracker.py novels/我的小说
```

### 导出 EPUB

```bash
python3 scripts/generate_epub.py novels/我的小说 --author "作者名"
```

### 拆分旧混合章节

```bash
python3 scripts/split_chapter_workspace.py novels/我的小说
python3 scripts/split_chapter_workspace.py novels/我的小说 --move-originals
```

---

## 文档导航

### 新手必读

| 文档 | 作用 |
|------|------|
| [QUICK_START.md](QUICK_START.md) | 5 分钟上手 |
| [SKILL.md](SKILL.md) | 主工作流 |
| [FILE_INDEX.md](FILE_INDEX.md) | 全部文件索引 |

### 核心模板

| 文档 | 作用 |
|------|------|
| [outline-template-v1-minimal.md](references/outline-template-v1-minimal.md) | 极简大纲 |
| [character-template-v2.md](references/character-template-v2.md) | 人物驱动引擎 |
| [chapter-template.md](references/chapter-template.md) | 干净章节正文模板 |
| [chapter-workspace-template.md](references/chapter-workspace-template.md) | 章节任务卡、场景拆分、沙盘和复盘 |
| [short-story-template.md](references/short-story-template.md) | 短故事任务卡和完整剧情骨架 |
| [progress-dashboard-template.md](references/progress-dashboard-template.md) | 进度仪表盘 |
| [story-bible-template.md](references/story-bible-template.md) | 世界观与伏笔 |

### 进阶机制

| 文档 | 作用 |
|------|------|
| [14-角色沙盘模式.md](references/14-角色沙盘模式.md) | 每章角色沙盘、角色文件、导演裁决 |
| [09-悬念生命周期管理.md](references/09-悬念生命周期管理.md) | 悬念追踪和过期预警 |
| [11-叙事节奏框架.md](references/11-叙事节奏框架.md) | 三层节奏体系 |
| [12-喘息机制.md](references/12-喘息机制.md) | 喘息章设计 |
| [13-钩子映射表.md](references/13-钩子映射表.md) | 章节位置与钩子类型 |
| [08-人机协作-v2.md](references/08-人机协作-v2.md) | 人机协作和中断恢复 |

---

## 推荐使用路径

### 新手路径

1. 读 [QUICK_START.md](QUICK_START.md)
2. 用一句话创意启动新书
3. 让 AI 生成极简大纲和首章任务卡
4. 每章只说“继续写”
5. 每章完成后运行 `check_ai_style.py`

### 连载路径

1. 维护 `99-进度仪表盘.md`
2. 每章先跑角色沙盘
3. 每章处理至少一条悬念：推进、保温、回收或延后
4. 每 5-10 章运行 `check_novel_health.py`
5. 阶段结束时检查人物弧线和伏笔状态

### 进阶路径

1. 用 [character-template-v2.md](references/character-template-v2.md) 打磨人物引擎
2. 用 [14-角色沙盘模式.md](references/14-角色沙盘模式.md) 拆成每个角色一个文件
3. 用 [11-叙事节奏框架.md](references/11-叙事节奏框架.md) 调整全本结构
4. 用 [ai-style-examples.md](references/ai-style-examples.md) 做章节精修

### 短故事路径

1. 明确说“写一篇短故事 / 短篇故事”
2. 使用 [short-story-template.md](references/short-story-template.md) 锁定完整剧情骨架
3. 正文写入 `short-stories/YYYYMMDD-标题.md`，不少于 6000 字
4. 运行 `python3 scripts/check_short_story.py short-stories/YYYYMMDD-标题.md`
5. 检查结尾是否收束主线，而不是停在“未完待续”

---

## 常见问题

### Q: 我必须把所有文件都填满吗？

不用。新项目先填 `00-大纲.md`、`01-人物档案.md` 和 `99-进度仪表盘.md`。角色沙盘可以从主角、反派、关键关系人物开始，其他角色后续再补。

### Q: 角色沙盘会不会拖慢写作？

标准模式会多一步，但它减少的是后期返工。快速模式也只保留最小沙盘：一个 POV 深度发言，加几个核心角色心跳。

### Q: 如果角色反抗大纲怎么办？

这正是沙盘的价值。导演按优先级裁决：人物一致性 > 主线不断 > 悬念生命周期 > 原大纲 > 单章爽点 / 钩子。必要时改大纲，不硬拧角色。

### Q: 适合哪些题材？

悬疑、玄幻、言情、都市、职场、历史、科幻、武侠、恐怖、校园都可用。群像、权谋、悬疑和强关系拉扯题材尤其适合角色沙盘。

### Q: 我只想去 AI 味，不想用完整流程可以吗？

可以。直接运行 `scripts/check_ai_style.py`，再对照 [ai-style-examples.md](references/ai-style-examples.md) 改写。

---

## 安装

```bash
git clone https://github.com/henry/chinese-novelist-skill.git
cd chinese-novelist-skill
PYTHONPATH=scripts python3 -m unittest discover tests/ -v
```

支持作为通用 Markdown skill 使用；安装路径按你的 AI 工具约定放置即可。

---

## 版本

- **v3.0.0**：重构为创作罗盘 + 因果章节事务 + 分层编辑系统；新增独创性审计和伟大作品证据式门控，将自动检查明确降级为启发式信号，移除机械钩子、题材套模和总分崇拜。
- **v2.6.2**：修复短故事模式输出边界：完整正文必须写入 `short-stories/YYYYMMDD-<标题>.md` 等命名 Markdown 文件，对话只汇报路径、字数和检查结果。
- **v2.6.1**：发布加固版本。完成全量 Skill 检测、端到端烟测和临时 `.skill` 打包校验；修复小说健康检查 `其他` 场景回退、英文 EPUB 元数据误读翻译流程文件、章节工作台文档引用等问题；移除 `.claude/` 本地配置发布风险。
- **v2.6.0**：新增 `manuscript/zh` 干净正文和 `workspace/chapters` 章节工作台结构，提供 `scripts/split_chapter_workspace.py` 迁移旧混合章节；英文译文默认写入 `manuscript/en`。
- **v2.5.0**：新增短故事模式，支持不少于 6000 字的完整单篇故事，提供短故事模板、剧情闭合红灯项和 `scripts/check_short_story.py` 检查脚本。
- **v2.4.0**：新增角色沙盘模式，每章写作前进行角色意志校验；支持每个角色独立运行时文件和沙盘记录。
- **v2.3.1**：强化执行入口、自动驾驶边界和修改工作流。
- **v2.3.0**：引入角色状态推演机制。
- **v2.0.0**：三阶段工作流、AI 味检测、悬念生命周期、节奏框架、人物 v2。

详见 [CHANGELOG.md](CHANGELOG.md)。

---

## 许可证

MIT License

> 最后提醒：工作流能守住注意力，不能替你承担作品的危险。先找到非写不可的问题，再让人物用选择和代价回答；脚本只负责提醒你回头看。
