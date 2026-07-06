# 专业意译翻译流程

本流程用于中文小说 / 网文英译。目标不是逐字搬运，而是在不改变事实、伏笔、人物关系和世界观规则的前提下，让英文读者获得接近原文的叙事效果。

## 调研依据

- ISO 17100 类翻译服务流程把翻译视为受控项目，而不是一次性出稿；核心环节包括初译、译者自检、独立修订、可选审读 / 校对和最终验证。参考：[Translation process under ISO 17100](https://iso17100.com/translation-process/)。
- ATA 的质量控制建议强调接案判断、源文理解、翻译过程中的问题记录和交付前检查。参考：[Quality Control in Translation](https://www.atanet.org/resources/quality-control-translation/)。
- ATA 关于 revision 的说明区分了双语修订和下游单语编辑 / 校对；双语修订需要拿源文对照译文。参考：[Revision and its Kin](https://www.atanet.org/resources/revision-and-its-kin/)。
- ATA 也强调译者是写作者，翻译包含理解、写作、修订和编辑，并且译者应主动提出源文歧义和不一致。参考：[The Translator as an Editor](https://www.atanet.org/translation/the-translator-as-an-editor/)。
- 术语表和风格指南能显著减少术语漂移、口吻漂移和返工，尤其适合 AI 翻译提示词。参考：[Lionbridge style guide and terminology glossary](https://www.lionbridge.com/blog/translation-localization/how-to-create-a-translation-style-guide-and-terminology-glossary/)。
- 文学翻译研究中，专业环境常见多阶段版本演进，尤其是初稿 / 后编辑 / 修订等阶段。参考：[Literary translation as a three-stage process](https://aclanthology.org/2022.eamt-1.13/)。

## 第一性原理

1. **目的决定策略**：译文首先服务目标读者和交付场景。小说英译要让英文读者愿意继续读，而不是让中文读者逐字核对。
2. **意义不可漂移**：事实、因果、人物动机、伏笔、时间线和世界观规则不可擅改。
3. **效果需要重建**：中文里的悬念、压迫感、讽刺、暧昧、节奏和留白，英文中可能要换句法和表达才能成立。
4. **一致性必须外化**：人名、称谓、境界、地名、物品和专有概念必须写入术语表；声音和标点偏好必须写入风格表。
5. **质量来自分工**：同一个 AI 也要切换角色执行：译者、译者自检、双语修订者、英文编辑、项目终检。
6. **可追溯优先**：不确定项写入查询日志，不能靠临场感觉在不同章节反复改口。

## 标准流程

### 0. 接案与翻译简报

确认翻译范围、目标读者、出版 / 自用场景、英文变体、专名处理原则、交付格式和是否需要用户确认样章。

输出：`manuscript/en/00-translation-brief.md`

### 1. 源文通读与风险识别

读取大纲、人物档案、世界观、最近章节和待译章节。标记双关、诗词、称谓、文化负载词、伏笔句、时间线和人物声音。

输出：待补充到 `manuscript/en/03-query-log.md` 的问题清单。

### 2. 术语表与风格表

先建术语表，再翻译正文。风格表明确英文口吻、句长倾向、对白处理、文化词处理、意译边界和不可改写项。

输出：
- `manuscript/en/01-termbase.md`
- `manuscript/en/02-style-sheet.md`

### 3. 样章校准

默认选第 1 章开头 800-1500 个中文字符做样章。当前 AI 给出译文和 3-5 条风格决策，人工模式等待确认；自动模式把样章策略写入风格表后继续。

### 4. 初译

当前 AI 按翻译简报、术语表和风格表逐章意译。允许拆句、合句、调整语序和替换文化表达；禁止新增事件、删伏笔、改人物关系。

输出：`manuscript/en/Chapter-XXX.md`

译文文件格式必须是纯 Markdown 正文：

```markdown
Chapter 1: English Chapter Title

Translated chapter body...
```

第一行只写章数和章标题；空一行后直接写正文。不要写标题标签、正文标签、译者说明、QA 说明或任何额外说明。

### 5. 译者自检

译者角色回看源文和译文，检查漏译、错译、反译、术语漂移、格式错误和情绪效果变弱。

### 6. 双语修订

切换为修订者角色，拿源文对照译文。优先修正意义、事实、伏笔、术语、口吻和格式。发现严重问题时，局部重译。

任务文件：`manuscript/en/_translation_tasks/Chapter-XXX.revise.prompt.md`

### 7. 单语润色

切换为英文小说编辑角色，只读英文稿。目标是消除翻译腔、改善段落流动、对白节奏和可读性。除非英文句子明显事实断裂，否则不回看源文。

任务文件：`manuscript/en/_translation_tasks/Chapter-XXX.edit.prompt.md`

### 8. 终检与交付

检查文件命名、章节顺序、纯译文 Markdown 结构、TBD、译者说明残留、术语一致性和 EPUB 可导出性。

输出：可交付的 `manuscript/en/Chapter-XXX.md` 文件。

## 当前 AI 文件映射

运行：

```bash
python3 scripts/translate_to_english.py novels/书名 --chapters "1-3"
```

会生成：

```text
manuscript/en/
├── 00-translation-brief.md
├── 01-termbase.md
├── 02-style-sheet.md
├── 03-query-log.md
├── 04-qa-checklist.md
└── _translation_tasks/
    ├── Chapter-001.translate.prompt.md
    ├── Chapter-001.revise.prompt.md
    └── Chapter-001.edit.prompt.md
```

当前 AI 应按 `translate -> revise -> edit -> final QA` 的顺序执行，不跳过修订和润色。
