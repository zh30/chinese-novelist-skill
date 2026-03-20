# Changelog

## v0.8.0

- Added 故事引擎 (Story Engine) section with 核心机制, 代价与资源, 升级规则
- Added dual-mode writing loop (草稿模式/精修模式)
- Added 修改工作流 (Revision Workflow) with 4-step process
- Replaced Quality Bar with detailed 质量检查清单 (6 rules with check items and quantitative indicators)
- Added 多线管理 (Multi-line Narrative Management) template
- Added 节奏预警 (Rhythm Alert) system with check_rhythm.py script
- Added 素材积累 (Research Material) phase and template
- Added 出版门控 (Publishing Gate) with 倒序检查 and tiered standards
- Added 叙事节奏曲线 (Narrative Rhythm Curve) design
- Added 人机协作 (Human-AI Collaboration) section and template
- Added 小说体检 (Novel Health Check) system with check_novel_health.py

## v0.3.1

- Added EPUB export and word count check to skill trigger description for natural language activation.
- Added Export section to SKILL.md with usage instructions.

## v0.3.0

- Added EPUB export script (`scripts/generate_epub.py`) to generate EPUB e-books from novel projects.
- Added author/pseudonym field to outline template.
- Added comprehensive tests for the EPUB generation script.

## v0.2.1

- Renamed the skill identifier in `SKILL.md` frontmatter to `chinese-novelist-skill`.
- Added an explicit in-document version block to `SKILL.md`.

## v0.2.0

- Rebuilt `SKILL.md` around a more stable novel-writing workflow and standard skill metadata.
- Added planning/state templates for outline, characters, story bible, opening design, scene design, style polishing, and ending design.
- Strengthened dialogue, structure, consistency, and quality-check references for Chinese long-form fiction.
- Updated the chapter word-count script to count the `## 正文` section preferentially.
- Added tests for the word-count script and local documentation links.
