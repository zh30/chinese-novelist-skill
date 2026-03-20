# chinese-novelist-skill

一个面向中文小说与网文创作的 Markdown skill。

它不是“随便写个故事”的提示词集合，而是一套更稳定的长篇创作工作流：先锁定设定与大纲，再按章节推进，持续维护人物、伏笔、时间线、文风和结局兑现。

## 为什么用它

- 把模糊脑洞快速落成可执行的大纲
- 让长篇连载不容易写散、写崩、写成模板文
- 强化首章钩子、对白张力、场景拆分和结局收束
- 降低常见 AI 痕迹，例如空泛情绪句、解释腔和四字词堆砌

## 适合谁

- 想从零开始写中文长篇小说或网文的人
- 已经有设定，但缺总纲、人物档案或分章规划的人
- 已经写了几章，想继续续写并保持前后连贯的人
- 想重写某一章，让它更抓人、更像中文小说的人

## 快速开始

安装后，直接在支持 skill 的工具里用自然语言触发即可：

```text
使用 chinese-novelist-skill，帮我策划一部 20 章的悬疑小说。
```

```text
使用 chinese-novelist-skill，继续写 novels/夜雨旧案/ 里的下一章。
```

```text
使用 chinese-novelist-skill，重写第 1 章开头，让钩子更强、对白更自然。
```

如果你的工具支持按 skill 名调用，优先显式写出 `chinese-novelist-skill`。

## 推荐工作流

这个 skill 默认按四种模式工作：

- `策划模式`：先做题材定位、故事引擎、大纲、人物、世界观与伏笔台账
- `试写模式`：在策划完成后，先写首章或样章
- `连载模式`：一章一章推进，持续维护故事状态
- `完稿模式`：在用户明确要求时，连续完成整本初稿

如果你是第一次使用，推荐顺序是：

1. 先做总纲
2. 再生成人物档案和世界观台账
3. 然后试写首章
4. 最后进入逐章连载

不建议一开始就让它直接从第 1 章写到第 30 章。

## 安装

这是一个纯 Markdown skill 项目。安装方式取决于你使用的工具，但基本思路一致：

1. 下载或克隆本仓库
2. 把整个目录放到对应工具的 skill 目录中
3. 让工具重新加载 skill

`Codex`、`Claude Code`、`OpenCode`、`OpenClaw` 等工具的具体路径和加载方式可能不同，请以对应工具文档为准。

## 它会产出什么

推荐的工作目录如下：

```text
novels/
└── 书名/
    ├── 00-大纲.md
    ├── 01-人物档案.md
    ├── 02-世界观与伏笔.md
    ├── 第 01 章 - 章节标题.md
    ├── 第 02 章 - 章节标题.md
    └── ...
```

- `00-大纲.md`：总纲、章节规划、悬念和进度
- `01-人物档案.md`：主角、反派、配角、关系变化
- `02-世界观与伏笔.md`：规则、时间线、势力、伏笔和角色状态
- `第XX章-标题.md`：单章任务卡、正文和章节复盘

## 内置能力

- 开篇与章节推进：[chapter-guide.md](references/chapter-guide.md)、[opening-design.md](references/opening-design.md)、[scene-design.md](references/scene-design.md)、[hook-techniques.md](references/hook-techniques.md)
- 人物、对白与文风：[dialogue-writing.md](references/dialogue-writing.md)、[style-polishing.md](references/style-polishing.md)、[character-template.md](references/character-template.md)
- 长篇连贯与结构规划：[plot-structures.md](references/plot-structures.md)、[consistency.md](references/consistency.md)、[story-bible-template.md](references/story-bible-template.md)、[outline-template.md](references/outline-template.md)
- 扩写与收尾：[content-expansion.md](references/content-expansion.md)、[ending-design.md](references/ending-design.md)、[quality-checklist.md](references/quality-checklist.md)

## 字数检查

仓库内提供了一个简单的字数检查脚本，用来优先统计章节文件里的 `## 正文` 区块。

```bash
python3 scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md
python3 scripts/check_chapter_wordcount.py --all novels/书名
python3 scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md 3500
```

## 导出 EPUB 电子书

当你的小说写到一定篇幅后，可以将其导出为 EPUB 格式的电子书，方便在手机、平板或电子书阅读器上阅读。

### 快速开始

```bash
# 一行命令即可导出
python3 scripts/generate_epub.py novels/书名
```

这会在小说目录下自动生成 `书名.epub` 文件。

### 命令行选项

```bash
python3 scripts/generate_epub.py <小说目录> [选项]
```

| 选项 | 说明 | 示例 |
|------|------|------|
| `-o <路径>` | 指定输出文件位置 | `-o ~/Desktop/书名.epub` |
| `--author <作者>` | 覆盖大纲中的作者名 | `--author "金庸"` |

**完整示例：**

```bash
# 导出到桌面
python3 scripts/generate_epub.py novels/我的小说 -o ~/Desktop/我的小说.epub

# 覆盖作者名（如果大纲里没有填作者）
python3 scripts/generate_epub.py novels/我的小说 --author "我的笔名"

# 同时指定作者和输出路径
python3 scripts/generate_epub.py novels/我的小说 --author "金庸" -o output.epub
```

### 前提条件

导出 EPUB 前，请确保小说目录满足以下条件：

1. **大纲文件**：`00-大纲.md` 必须存在
2. **书名格式**：大纲第一行为 `# 书名 大纲`
3. **作者字段**（可选）：大纲「项目定位」部分包含 `- **作者 / 笔名**：xxx`
4. **章节文件**：目录下有以 `第` 开头的 Markdown 文件（如 `第01章-标题.md`）

### 导出内容

生成的 EPUB 包含：

| 内容 | 说明 |
|------|------|
| 封面页 | 显示书名和作者 |
| 目录页 | 可点击跳转至各章节 |
| 章节正文 | 所有 `## 正文` 区块的内容 |

> **注意**：只会导出 `## 正文` 部分，章节任务卡、复盘等不会被包含在 EPUB 中。

## 翻译成英文

当小说完成后，可以将其翻译成适合英文读者阅读的英文版本。翻译功能集成在 skill 中，直接使用 AI 能力完成，无需额外配置 API。

### 工作流程

1. **准备阶段**：读取大纲、人物档案、世界观，构建翻译上下文
2. **术语提取**：分析小说内容，提取角色名、修炼体系、门派术语等，建立统一术语表
3. **并行翻译**：将章节分成多批次，使用多个 subagent 并行翻译
4. **最终校对**：检查术语一致性、人名统一、剧情衔接
5. **保存结果**：英文版保存到 `en/` 目录

### 使用方式

在对话中直接告诉 skill：

```text
使用 chinese-novelist-skill，帮我把这本小说翻译成英文。
```

```text
使用 chinese-novelist-skill，翻译 novels/夜雨旧案/ 的第 1-5 章。
```

### 英文版目录结构

```
novels/
└── 书名/
    ├── 00-大纲.md
    ├── 01-人物档案.md
    ├── 第01章-标题.md
    └── en/                    # 英文版
        ├── Chapter-001.md
        ├── Chapter-002.md
        └── ...
```

### 导出英文版 EPUB

英文版同样可以导出为 EPUB 电子书：

```bash
python3 scripts/generate_epub.py novels/书名 --lang en
```

这会在小说目录下生成 `书名-en.epub` 文件。

### 一致性保障

翻译过程中通过以下机制保证质量：

| 机制 | 作用 |
|------|------|
| 统一术语表 | 强制所有角色名、术语翻译一致 |
| 批次设计 | 相邻章节同批次，保持剧情连贯 |
| 最终校对 | 全局检查人名、术语、风格一致性 |

## 兼容性与版本

- 当前版本：`0.8.0`
- 版本记录：见 [CHANGELOG.md](CHANGELOG.md)
- `SKILL.md` frontmatter 保持最小化，优先兼容只识别 `name` 与 `description` 的 skill loader

## 常见问题

### 为什么不建议直接一次写完整本书？

因为中文长篇最容易在中段失控。先规划、再试写、再连载，通常质量更稳。

### 这个 skill 适合哪些题材？

悬疑、言情、奇幻、仙侠、科幻、都市现实、群像长篇都可以。它更偏长篇叙事流程，而不是某个单一题材。

### 它只适合某一个工具吗？

不是。它尽量保持对主流 skill 工具的兼容性，但具体加载方式仍取决于工具本身。

## 许可证

MIT
