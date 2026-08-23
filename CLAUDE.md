# chinese-novelist-skill

Version: 3.1.0. This repository is an Agent Skill for ambitious Chinese fiction.

1. Read `SKILL.md` and follow its intent routing. Do not load every file in `references/` by default.
2. Write recoverable artifacts to disk. `manuscript/zh/` is the only source of truth for Chinese chapter text.
3. Scripts are smoke alarms, not aesthetic judges.

## Commands

```bash
PYTHONPATH=scripts python3 -m unittest discover tests/ -v
python3 scripts/check_chapter_wordcount.py novels/书名/manuscript/zh/第001章-标题.md
python3 scripts/check_chapter_transaction.py novels/书名 1
python3 scripts/check_cross_book_similarity.py novels
```

## Hard rules

- Do not paste completed chapter or 6000+ character short-story bodies into chat unless the user explicitly asks.
- Prefer bounded recovery: dashboard rolling summary + constitution + POV card + last 800 characters of the previous chapter.

See `README.md` for install paths across agents.
