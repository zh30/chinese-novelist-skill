# Character Sandbox Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `chinese-novelist-skill` with an every-chapter character sandbox mode that gives each important character an isolated runtime memory and limited-information sandbox output before chapter writing.

**Architecture:** This is a documentation-and-template feature. The main `SKILL.md` becomes the routing layer, `references/14-角色沙盘模式.md` holds the full protocol, `progress-dashboard-template.md` exposes the dashboard summary, and README / FILE_INDEX make the feature discoverable.

**Tech Stack:** Markdown skill files, Python unittest documentation checks, existing local link resolver in `tests/test_skill_docs.py`.

## Global Constraints

- Every chapter must pass character sandbox gating before task-card generation.
- Character memory is persisted as one file per character under `04-角色沙盘/`.
- Character subagents may provide action tendency, one scene suggestion, and one line of dialogue; they must not write prose.
- Character subagents receive limited information only and cannot see complete outlines, future plot, other character interiors, hidden truth, or author intent.
- Director priority order is: character consistency, mainline continuity, suspense lifecycle, original outline schedule, chapter hook.
- README must become more intuitive and visually scannable.

---

### Task 1: Add Documentation Test Coverage

**Files:**
- Modify: `tests/test_skill_docs.py`

**Interfaces:**
- Consumes: existing markdown-link resolver.
- Produces: tests that require the new sandbox reference and README mention.

- [x] **Step 1: Write failing docs tests**

Add assertions that `SKILL.md`, `README.md`, and `FILE_INDEX.md` mention `references/14-角色沙盘模式.md`, and that README contains `角色沙盘模式`.

- [x] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=scripts python3 -m unittest tests.test_skill_docs -v`
Expected: FAIL because the reference does not exist yet.

- [x] **Step 3: Continue after failure**

Leave the failing tests in place for Task 2 and Task 3.

### Task 2: Add Full Character Sandbox Reference

**Files:**
- Create: `references/14-角色沙盘模式.md`

**Interfaces:**
- Consumes: approved design in `docs/superpowers/specs/2026-06-26-character-sandbox-mode-design.md`.
- Produces: canonical protocol referenced by `SKILL.md`, README, and FILE_INDEX.

- [x] **Step 1: Create reference document**

Add sections for purpose, when to use, file structure, role index, single-character runtime file, per-chapter flow, character subagent output, director裁决, writing rules, state writeback, guardrails, fast mode, autopilot mode, and acceptance checklist.

- [x] **Step 2: Run docs test**

Run: `PYTHONPATH=scripts python3 -m unittest tests.test_skill_docs -v`
Expected: still FAIL until `SKILL.md`, README, and FILE_INDEX link the new reference.

### Task 3: Update Core Skill Routing and Workflow

**Files:**
- Modify: `SKILL.md`
- Modify: `references/progress-dashboard-template.md`

**Interfaces:**
- Consumes: `references/14-角色沙盘模式.md`.
- Produces: every-chapter sandbox protocol in the main skill and dashboard.

- [x] **Step 1: Update `SKILL.md` metadata and version**

Set version to `2.4.0`, version date to `2026-06-26`, and describe character sandbox mode.

- [x] **Step 2: Update required files**

Add `04-角色沙盘/` and its files under Required Files.

- [x] **Step 3: Replace role推演 loop language**

Change the serial loop from “角色状态推演” to “角色沙盘模式”, with fast-mode and autopilot downgrade rules.

- [x] **Step 4: Rewrite the role-agent section**

Keep the current 8-dimensional model as conceptual foundation, but define the new per-character-file, limited-information, director-c裁决 protocol and link to `references/14-角色沙盘模式.md`.

- [x] **Step 5: Update dashboard template**

Add `角色沙盘状态`, `本章沙盘裁决`, and quick links to `04-角色沙盘/00-角色索引.md` and latest session record.

### Task 4: Update README and Navigation

**Files:**
- Modify: `README.md`
- Modify: `FILE_INDEX.md`
- Optional modify if needed: `QUICK_START.md`

**Interfaces:**
- Consumes: main skill and reference doc.
- Produces: visually scannable introduction and discoverability.

- [x] **Step 1: Rewrite README opening**

Make the feature list more visual and add a concise “核心工作流” section.

- [x] **Step 2: Add角色沙盘 section**

Explain the mode with a compact diagram, file tree, and three-step chapter flow.

- [x] **Step 3: Update FILE_INDEX**

Add `references/14-角色沙盘模式.md` in advanced/core workflow sections.

- [x] **Step 4: Keep markdown links resolvable**

Do not add placeholder links that fail local tests.

### Task 5: Verify and Commit

**Files:**
- Test: `tests/test_skill_docs.py`
- Test: all tests

**Interfaces:**
- Consumes: all prior tasks.
- Produces: clean working tree ready for review.

- [x] **Step 1: Run docs tests**

Run: `PYTHONPATH=scripts python3 -m unittest tests.test_skill_docs -v`
Expected: PASS.

- [x] **Step 2: Run full test suite**

Run: `PYTHONPATH=scripts python3 -m unittest discover tests/ -v`
Expected: PASS.

- [x] **Step 3: Review diff**

Run: `git diff --stat` and `git diff --check`.
Expected: no whitespace errors and changes limited to docs/tests/templates.

- [x] **Step 4: Commit**

Commit message: `Add character sandbox mode`
