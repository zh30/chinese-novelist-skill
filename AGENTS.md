# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

This is a Codex skill for ambitious Chinese fiction: literary, genre/web, and crossover novels. It combines story discovery, a creative constitution, character pressure, causal long-form state, layered editorial revision, and deterministic smoke checks. It also supports complete Chinese short stories of at least 6000 characters.

The skill is loaded from `SKILL.md` - this is the main entry point that defines the novel writing workflow.

## Project Structure

```
├── SKILL.md              # Main skill file - loaded by Codex
├── README.md             # Documentation
├── references/           # 37 reference documents for novel writing
├── scripts/             # Utility scripts
│   ├── utils.py                      # Shared utility functions
│   ├── check_chapter_wordcount.py   # Word count checker (--all supported)
│   ├── check_short_story.py          # Short story quality checker (--all supported)
│   ├── check_ai_style.py            # AI style detection (9 symptoms, --all supported)
│   ├── check_novel_health.py         # Novel health check (rhythm+scene+word count)
│   ├── check_timeline.py             # Timeline consistency checker
│   ├── character_tracker.py          # Character consistency checker
│   ├── generate_epub.py              # EPUB exporter
│   ├── translate_to_english.py       # Current-AI adaptive translation task generator
│   └── split_chapter_workspace.py    # Migration from mixed chapters to clean manuscript/workspace
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
python3 scripts/check_chapter_wordcount.py novels/书名/manuscript/zh/第001章-标题.md

# Single chapter with custom minimum
python3 scripts/check_chapter_wordcount.py novels/书名/manuscript/zh/第001章-标题.md 3500

# All chapters in a directory
python3 scripts/check_chapter_wordcount.py --all novels/书名

```

### AI Style Check
```bash
# Single chapter
python3 scripts/check_ai_style.py novels/书名/manuscript/zh/第001章-标题.md

# All chapters in a directory
python3 scripts/check_ai_style.py --all novels/书名
```

### Short Story Quality Check
```bash
# Single short story
python3 scripts/check_short_story.py short-stories/YYYYMMDD-故事标题.md

# All short stories in a directory
python3 scripts/check_short_story.py --all short-stories
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

# Export English version (prefers manuscript/en/, still supports legacy en/)
python3 scripts/generate_epub.py novels/书名 --lang en
```

### Prepare Current-AI English Translation Tasks
```bash
# Generate adaptive translation tasks for the current AI
python3 scripts/translate_to_english.py novels/书名

# Generate tasks for specific chapters
python3 scripts/translate_to_english.py novels/书名 --chapters 1-10
```

## Writing Workflow

When using this skill, work follows three phases:
1. **策划期** (Planning): Compare genuinely different directions; establish the creative constitution, causal spine, characters, and first chapter task card
2. **连载期** (Serial): Chapter-by-chapter causal writing, independent editorial pass, smoke checks, and state updates
3. **收尾期** (Completion): Reader pass, then separate structure, character, scene, language, ending, and continuity passes

Within **连载期**, two speed modes:
- **标准模式** (default): Full scene breakdown + red-light check
- **快速模式** ("快写"/"初稿"): Skip scene breakdown, word count + basic hook only

Default: Planning for new projects, Serial for existing chapters.

Optional short-story mode:
- Triggered only by explicit requests such as "短故事", "短篇故事", or "写一篇完整故事".
- Does not enter the long-form serial workflow by default.
- Must write the complete story to a named Markdown file, defaulting to `short-stories/YYYYMMDD-<标题>.md`; do not paste the full 6000+ character body into chat unless explicitly requested.
- Must produce a complete plot with at least 6000 Chinese characters.
- May use paragraphs or line breaks instead of chapter structure.

## Key Files for Novel Projects

Create in `novels/<书名>/`:
- `00-大纲.md` - Creative constitution + causal outline using `references/outline-template-v1-minimal.md` (recommended)
- `01-人物档案.md` - Character pressure systems using `references/character-template-v2.md` (recommended)
- `02-世界观与伏笔.md` - Worldbuilding using `references/story-bible-template.md`
- `99-进度仪表盘.md` - Progress dashboard (auto-maintained by AI)
- `manuscript/zh/第XXX章-标题.md` - Clean Chinese manuscript chapters using `references/chapter-template.md`
- `manuscript/en/Chapter-XXX.md` - Clean English translated chapters
- `workspace/chapters/第XXX章-标题/` - Chapter task cards, scene plans, sandbox notes, reviews, revision notes using `references/chapter-workspace-template.md`
- `第XX章-标题.md` - Legacy mixed chapters only; migrate with `scripts/split_chapter_workspace.py`

For short stories, use `short-stories/YYYYMMDD-<标题>.md` with `references/short-story-template.md`.

## Quality Standards

Each chapter must have:
- A concrete reason to exist and an irreversible causal, relational, cognitive, or emotional change
- At least one prior consequence carried forward; suspense threads are advanced only when the story needs them
- An ending effect appropriate to the chapter: suspense, decision, emotional landing, image, or deliberate closure
- Character shown through action/dialogue, not just description
- One or more scenes with active pressure and strategy change; a single-scene chapter needs sustained escalation and a clear reason
- ≥3000 Chinese characters (≥2500 in fast mode)

Automated checks are smoke alarms, not aesthetic judges. Never use keyword scores to claim literary quality or authorship, and never force a hook, reversal, sensory quota, or sentence-length pattern merely to satisfy a metric.

Each short story must have:
- ≥6000 Chinese characters
- Complete beginning, escalation, turn, climax, and resolution
- A closed main conflict, not only a "to be continued" hook
