# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skill for Chinese novel/web novel writing. It provides a structured workflow for planning, writing, and maintaining long-form Chinese fiction with consistent characters, plot threads, and writing quality.

The skill is loaded from `SKILL.md` - this is the main entry point that defines the novel writing workflow.

## Project Structure

```
├── SKILL.md              # Main skill file - loaded by Claude Code
├── README.md             # Documentation
├── references/           # 35 reference documents for novel writing
├── scripts/             # Utility scripts
│   ├── utils.py                      # Shared utility functions
│   ├── check_chapter_wordcount.py   # Word count checker (--all supported)
│   ├── check_ai_style.py            # AI style detection (9 symptoms, --all supported)
│   ├── check_novel_health.py         # Novel health check (rhythm+scene+word count)
│   ├── check_timeline.py             # Timeline consistency checker
│   ├── character_tracker.py          # Character consistency checker
│   ├── generate_epub.py              # EPUB exporter
│   └── translate_to_english.py       # English translation
├── tests/               # Unit tests
└── docs/                # Design docs and implementation plans
    └── plans/
```

## Commands

### Run Tests
```bash
PYTHONPATH=scripts python3 -m unittest discover tests/ -v
# or run a specific test
PYTHONPATH=scripts python3 -m unittest tests.test_check_chapter_wordcount
```

### Check Chapter Word Count
```bash
# Single chapter (default min: 3000)
python3 scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md

# Single chapter with custom minimum
python3 scripts/check_chapter_wordcount.py novels/书名/第01章-标题.md 3500

# All chapters in a directory
python3 scripts/check_chapter_wordcount.py --all novels/书名
```

### AI Style Check
```bash
# Single chapter
python3 scripts/check_ai_style.py novels/书名/第01章-标题.md

# All chapters in a directory
python3 scripts/check_ai_style.py --all novels/书名
```

### Novel Health Check
```bash
python3 scripts/check_novel_health.py novels/书名
```

### Timeline Consistency Check
```bash
python3 scripts/check_timeline.py novels/书名
```

### Character Consistency Check
```bash
python3 scripts/character_tracker.py novels/书名
```

### Export to EPUB
```bash
# Export Chinese version
python3 scripts/generate_epub.py novels/书名

# Export with custom author
python3 scripts/generate_epub.py novels/书名 --author "作者名"

# Export to custom path
python3 scripts/generate_epub.py novels/书名 -o output.epub

# Export English version (requires en/ directory)
python3 scripts/generate_epub.py novels/书名 --lang en
```

### Translate to English
```bash
# Translate entire novel
python3 scripts/translate_to_english.py novels/书名

# Translate specific chapters
python3 scripts/translate_to_english.py novels/书名 --chapters 1-10
```

## Writing Workflow

When using this skill, work follows three phases:
1. **策划期** (Planning): Outline, characters, first chapter task card
2. **连载期** (Serial): Chapter-by-chapter writing with red-light quality checks
3. **收尾期** (Completion): Final polish, timeline check, publishing gate

Within **连载期**, two speed modes:
- **标准模式** (default): Full scene breakdown + red-light check
- **快速模式** ("快写"/"初稿"): Skip scene breakdown, word count + basic hook only

Default: Planning for new projects, Serial for existing chapters.

## Key Files for Novel Projects

Create in `novels/<书名>/`:
- `00-大纲.md` - Outline using `references/outline-template-v1-minimal.md` (recommended)
- `01-人物档案.md` - Characters using `references/character-template-v2.md` (recommended)
- `02-世界观与伏笔.md` - Worldbuilding using `references/story-bible-template.md`
- `99-进度仪表盘.md` - Progress dashboard (auto-maintained by AI)
- `第XX章-标题.md` - Chapters using `references/chapter-template.md`

## Quality Standards

Each chapter must have:
- Meaningful change that advances the plot
- At least one plot thread resolved, escalated, or deflected
- Hook strength matching the chapter's position in the book
- Character shown through action/dialogue, not just description
- Multiple scenes with clear tasks (not just summary)
- ≥3000 Chinese characters (≥2500 in fast mode)
