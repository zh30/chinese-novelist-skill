# English Translation Feature Design

## Overview

为中文小说写作技能增加"深度翻译"功能，将小说翻译为适合英文读者的英文版本。

## Requirements Summary

| Item | Choice |
|------|--------|
| Output Format | Markdown files |
| Translation Method | AI-driven (with full context) |
| Directory | `novels/<书名>/en/` |
| Context | Outline + Character Profiles + Worldbuilding |

## Architecture

### Trigger Conditions

用户说以下话时触发翻译模式：
- "翻译成英文"
- "生成英文版"
- "帮我翻译"
- "English translation"
- 其他明确表达翻译需求的语句

### Execution Flow

1. **确认范围**：询问用户要翻译全本还是部分章节
2. **读取上下文**：
   - `00-大纲.md` → 提取书名、作者、类型、简介
   - `01-人物档案.md` → 提取人物信息
   - `02-世界观与伏笔.md` → 提取世界观要点
3. **构建提示词**：将上下文组装为翻译提示词
4. **调用 AI**：逐章翻译
5. **保存结果**：写入 `en/` 目录

### File Structure

```
novels/<书名>/
├── 00-大纲.md
├── 01-人物档案.md
├── 02-世界观与伏笔.md
├── 第01章-标题.md
├── 第02章-标题.md
└── en/
    ├── 00-outline.md      # Outline translation
    ├── 01-characters.md   # Character profiles translation
    ├── 02-worldbuilding.md # Worldbuilding translation
    ├── Chapter-01.md      # Chapter translation
    └── Chapter-02.md
```

### Translation Prompt Design

```
# Translation Task

You are a professional novel translator. Translate the following Chinese novel chapter into fluent English.

## Novel Information
- Title: [书名]
- Author: [作者]
- Genre: [类型]
- Synopsis: [大纲中的简介]

## Characters
[人物档案要点]

## Worldview
[世界观与伏笔要点]

## Translation Requirements
1. Maintain the narrative rhythm and emotional tension
2. Use pinyin for character names (e.g., Zhang Wei)
3. Keep Chinese-specific terms (gongfu, qigong) with pinyin or explanatory translation
4. Preserve chapter structure (## Title, ## Body)
5. Use modern English, avoid stiff literal translations
6. Keep dialogue natural and fluent

## Chapter to Translate
[章节内容]
```

## Integration with Existing Features

### EPUB Export

修改 `generate_epub.py` 支持英文版：
- 新增 `--lang` 参数（默认 `zh-CN`，可选 `en`）
- 读取 `en/` 目录生成英文 EPUB
- 设置正确的语言标识

### Word Count Check

- 英文版使用独立的 word count 检查
- 不与中文版混淆

## Implementation Plan

1. **Update SKILL.md**: Add translation mode documentation
2. **Create translation script**: `scripts/translate_to_english.py`
3. **Update generate_epub.py**: Add `--lang` parameter for English support
4. **Test**: Verify translation quality and file output
