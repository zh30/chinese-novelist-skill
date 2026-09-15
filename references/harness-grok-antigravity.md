# Grok Build CLI、Gemini Antigravity 与 Pi 适配

> `SKILL.md` 仍是创作协议。本文件只映射宿主能力，不改写作规则。

派出隔离盲读、跑工厂循环、或当前宿主是 Grok Build / Antigravity / Pi 时读取。

## 发现与调用

把本仓库作为 skill 根目录（含 `SKILL.md`、`references/`、`scripts/`）：

| 宿主 | 用户级 | 仓库级（本仓库作工作区时已自带） |
|------|--------|----------------------------------|
| Grok Build CLI | `~/.grok/skills/chinese-novelist-skill` | `.agents/skills/chinese-novelist-skill/` |
| Antigravity / `agy` | `~/.gemini/config/skills/chinese-novelist-skill` 或 `~/.gemini/antigravity-cli/skills/chinese-novelist-skill` | 同上 |
| Pi | `~/.pi/agent/skills/chinese-novelist-skill` 或 `~/.agents/skills/chinese-novelist-skill` | `.agents/skills/`；slash 用 `.pi/prompts/` |

```bash
ln -s /absolute/path/to/chinese-novelist-skill ~/.grok/skills/chinese-novelist-skill
ln -s /absolute/path/to/chinese-novelist-skill ~/.gemini/config/skills/chinese-novelist-skill
ln -s /absolute/path/to/chinese-novelist-skill ~/.pi/agent/skills/chinese-novelist-skill
mkdir -p ~/.grok/agents ~/.gemini/config/agents ~/.pi/agent/prompts ~/.pi/agent/agents
ln -s /absolute/path/to/chinese-novelist-skill/.grok/agents/blind-reader.md ~/.grok/agents/blind-reader.md
ln -s /absolute/path/to/chinese-novelist-skill/.grok/agents/chinese-novelist.md ~/.grok/agents/chinese-novelist.md
ln -s /absolute/path/to/chinese-novelist-skill/.agents/agents/blind-reader.md ~/.gemini/config/agents/blind-reader.md
ln -s /absolute/path/to/chinese-novelist-skill/.agents/agents/chinese-novelist.md ~/.gemini/config/agents/chinese-novelist.md
ln -s /absolute/path/to/chinese-novelist-skill/.pi/prompts/next-chapter.md ~/.pi/agent/prompts/next-chapter.md
ln -s /absolute/path/to/chinese-novelist-skill/.pi/prompts/new-novel.md ~/.pi/agent/prompts/new-novel.md
ln -s /absolute/path/to/chinese-novelist-skill/.pi/prompts/factory-chapter.md ~/.pi/agent/prompts/factory-chapter.md
ln -s /absolute/path/to/chinese-novelist-skill/.pi/agents/blind-reader.md ~/.pi/agent/agents/blind-reader.md
```

Pi 项目 skill 需先信任工作区。强制加载：`pi --skill /absolute/path/to/chinese-novelist-skill`。

Slash：`/chinese-novelist-skill`、`/next-chapter`、`/new-novel`。Pi 另用 `/skill:chinese-novelist-skill`（`enableSkillCommands` 打开时 skill 名也可当 slash）。Grok 工厂另有 `/workflow chinese-novelist-factory`。写作会话可选主 agent `chinese-novelist`（Grok：`/agents`；Antigravity：`agy --agent chinese-novelist`）。

## 盲读派出

写作 agent 禁止自己写 `blind-read.md`。隔离调用只返回填写后的模板；写作 agent 原样落盘。

白名单路径写进 spawn prompt，不要写“读上一章”这种需再搜索的句子。

**Grok Build**：`spawn_subagent`。优先 `subagent_type: blind-reader`（仅 `read_file`）。否则用 `explore`，prompt 写明：只对列出的路径调用 `read_file`；禁止 `grep`、`list_dir`、shell。不要用 `isolation: worktree`——工作树仍含大纲。

**Antigravity**：`invoke_subagent`，优先 `blind-reader`（仅 `view_file`）。否则动态 subagent，prompt 同样只列白名单路径。

**Pi**：默认无内置 subagent。用 `bash` 另起一次 print 会话，关掉会泄漏大纲的上下文：

```bash
pi -p --no-context-files --no-skills --no-prompt-templates --no-extensions "$(cat <<'EOF'
You are a reader who has never seen the outline, character bible, or author's notes.
Use only the read tool on these paths:
- <本章路径>
- <上一章路径，若有>
Do not grep, find, ls, bash, write, or edit.
Fill the 盲读 template from references/blind-read.md (the seven labeled fields).
If you cannot restate the irreversible change, write 复述不出.
Return only the filled template. Do not write files.
EOF
)"
```

若已安装会读取 `.pi/agents/` 的 subagent 包，派出 `blind-reader`（仅 `read`，`contextFiles: false`）。不要用 git worktree 当隔离。

无法隔离则停止交付，请用户另开只读正文的对话。

## 工厂与批量

每个原子事务仍须验收。Grok 的 `/plan` 只能写会话 `plan.md`，小说策划写入 `00-大纲.md`，不要用 plan mode 代替策划期。

| 意图 | Grok Build | Antigravity | Pi |
|------|------------|-------------|-----|
| 一章工厂事务 | `/workflow chinese-novelist-factory` | `/factory-chapter` 或 `/goal` 加批量提示词 | `/factory-chapter` |
| 外部循环 | `grok -p "<批量提示词>" --yolo` | `agy -p "<批量提示词>"` | `pi -p "<批量提示词>"` |
| 无人值守连写 | 每事务一次 workflow / `-p` | `/goal` 也必须按章验收 | 每事务一次 `pi -p`；不要在一次调用里写完多章再验收 |

批量提示词见 [batch-production.md](batch-production.md)「外部循环」。

## 工具对应

| 动作 | Grok Build | Antigravity | Pi |
|------|------------|-------------|-----|
| 读文件 | `read_file` | `view_file` | `read` |
| 写 / 改文件 | `write` / `search_replace` | `replace_file_content` 等写工具 | `write` / `edit` |
| 跑脚本 | `run_terminal_command` | `run_command` | `bash` |
| 隔离子代理 | `spawn_subagent` | `invoke_subagent` | `pi -p --no-context-files --no-skills`（或可选 subagent 包） |

脚本仍用 `python3 scripts/...`。不要把已落盘的长篇或 6000 字以上短故事正文粘贴到对话里。
