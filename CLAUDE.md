# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skill for Chinese novel/web novel writing. It provides a structured workflow for planning, writing, and maintaining long-form Chinese fiction with consistent characters, plot threads, and writing quality.

## Project Structure

```
├── SKILL.md           # Main skill file - loaded by Claude Code
├── README.md          # Documentation
├── references/        # 16 reference documents for novel writing
├── scripts/           # Utility scripts
│   └── check_chapter_wordcount.py  # Word count checker
└── tests/             # Unit tests
```

## Commands

### Run Tests
```bash
python -m pytest tests/
# or
python tests/test_check_chapter_wordcount.py
```

### Check Chapter Word Count
```bash
# Single chapter
python scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md

# Single chapter with custom minimum
python scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md 3500

# All chapters in a directory
python scripts/check_chapter_wordcount.py --all novels/书名
```

## Writing Workflow

When using this skill, work follows these modes:
1. **策划模式** (Planning): Story outline, characters, worldbuilding
2. **试写模式** (Trial write): First chapter/sample
3. **连载模式** (Serial): Chapter-by-chapter writing
4. **完稿模式** (Complete draft): Full manuscript

Default: Planning for new projects, Serial for existing chapters.

## Key Files for Novel Projects

Create in `novels/<书名>/`:
- `00-大纲.md` - Outline using `references/outline-template.md`
- `01-人物档案.md` - Characters using `references/character-template.md`
- `02-世界观与伏笔.md` - Worldbuilding using `references/story-bible-template.md`
- `第XX章-标题.md` - Chapters using `references/chapter-template.md`

## Quality Standards

Each chapter must have:
- Meaningful change that advances the plot
- At least one plot thread resolved, escalated, or deflected
- Hook strength matching the chapter's position in the book
- Character shown through action/dialogue, not just description
- Multiple scenes with clear tasks (not just summary)
