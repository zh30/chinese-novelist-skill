# chinese-novelist skill

一个面向中文小说和网文创作的 skill，重点解决三件事：

- 从模糊想法快速落到可执行的大纲
- 在长篇连载里持续维护人物、伏笔、时间线和文风稳定
- 让章节更像“可追更的中文小说”，而不是模板化 AI 文

## 适用场景

- 从零开始写中文长篇 / 网文 / 连载小说
- 已有设定，想补总纲、人物档案、世界观台账
- 已写了几章，想继续续写
- 想重写某章，提高钩子、对白、节奏、悬念强度

## 推荐工作流

### 1. 先确定模式

- `策划模式`：只做大纲和设定
- `试写模式`：大纲 + 样章
- `连载模式`：一章一章推进
- `完稿模式`：整本初稿

默认不建议一上来直接 30-50 章全自动暴写。更稳的顺序是：

1. 先锁定故事引擎
2. 再做章节规划
3. 最后进入章节创作

### 2. 维护四个核心文件

```text
novels/
└── 书名/
    ├── 00-大纲.md
    ├── 01-人物档案.md
    ├── 02-世界观与伏笔.md
    ├── 第01章-章节标题.md
    └── ...
```

### 3. 每章都走闭环

1. 读总纲、人物档案、伏笔台账
2. 明确本章目标、阻碍、转折、钩子
3. 拆 3-6 个场景再写正文
4. 自查质量清单
5. 更新章节摘要、人物状态、伏笔状态

## 这次优化后的重点

- `SKILL.md` 现在使用更标准的 skill frontmatter，触发条件更清晰
- 不再依赖不存在的 `AskUserQuestion` 工具，而是改成兼容普通 agent 对话的问询方式
- 新增 `02-世界观与伏笔.md`，补上长篇连载最容易丢的状态管理层
- 新增场景设计和文风打磨指南，补上“会写完”和“写得像中文小说”之间的差距
- 新增首章设计和结局兑现指南，把开篇命中率与收尾完成度单独拉起来
- 大纲、人物、章节模板重写后，更适合中文长篇连载的节奏
- 质量清单从“泛泛而谈”改成更贴近中文小说的具体检查项

## 内置参考资料

| 文件 | 作用 |
|------|------|
| `references/chapter-guide.md` | 强开头与章节结构 |
| `references/opening-design.md` | 首章设计与追读钩子 |
| `references/hook-techniques.md` | 章节结尾钩子 |
| `references/ending-design.md` | 结局兑现与终章收束 |
| `references/dialogue-writing.md` | 中文对白质量 |
| `references/content-expansion.md` | 合理扩写 |
| `references/consistency.md` | 连贯性维护 |
| `references/scene-design.md` | 场景推进与章节拆场 |
| `references/style-polishing.md` | 去 AI 味与中文文风修整 |
| `references/plot-structures.md` | 结构模板 |
| `references/outline-template.md` | 总纲模板 |
| `references/character-template.md` | 人物档案模板 |
| `references/story-bible-template.md` | 世界观 / 伏笔 / 时间线台账 |
| `references/chapter-template.md` | 单章模板 |
| `references/quality-checklist.md` | 交付前自查 |

## 字数检查

```bash
python scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md
python scripts/check_chapter_wordcount.py --all novels/书名
python scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md 3500
```

## 安装

把这个目录放到你所用 agent 的 skills 目录即可。不同 agent 的安装路径不同，但目录结构保持不变。
