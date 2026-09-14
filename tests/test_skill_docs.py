import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_FILES = [ROOT / "SKILL.md", ROOT / "README.md"]


class SkillDocsTests(unittest.TestCase):
    def test_skill_entrypoint_is_concise_and_has_valid_frontmatter(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(
            len(skill.splitlines()),
            500,
            msg="SKILL.md should remain a concise router; detailed craft belongs in references/",
        )

        parts = skill.split("---", 2)
        self.assertGreaterEqual(len(parts), 3)
        frontmatter_keys = {
            line.split(":", 1)[0].strip()
            for line in parts[1].splitlines()
            if ":" in line and not line.startswith((" ", "\t"))
        }
        self.assertTrue({"name", "description"}.issubset(frontmatter_keys))
        allowed = {
            "name",
            "description",
            "compatibility",
            "license",
            "metadata",
            "allowed-tools",
            "when-to-use",
            "argument-hint",
        }
        self.assertLessEqual(frontmatter_keys, allowed)
        self.assertIn("compatibility", frontmatter_keys)
        self.assertIn("metadata", frontmatter_keys)
        self.assertIn("when-to-use", frontmatter_keys)
        self.assertIn("argument-hint", frontmatter_keys)
        self.assertIn('version: "3.5.0"', parts[1])
        self.assertIn("当前版本：3.5.0", skill)
        self.assertIn("references/harness-grok-antigravity.md", skill)

    def test_great_work_protocol_is_discoverable(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        required_references = {
            "references/creative-compass.md",
            "references/editorial-revision.md",
            "references/quality-checklist.md",
            "references/batch-production.md",
            "references/blind-read.md",
            "references/voice-lock-template.md",
        }

        for reference in required_references:
            self.assertIn(reference, skill)

        required_principles = [
            "独特性",
            "因果脊柱",
            "主题保持为问题",
            "脚本只是烟雾报警器",
            "不强制章章反转",
            "伟大作品门控",
            "有界冷启动",
            "滚动前情摘要",
            "盲读",
            "隔离",
            "感知包",
            "声音锁",
            "作者模式",
            "工厂模式",
            "禁止同上下文填写盲读",
            "check_chapter_transaction.py",
            "check_cross_book_similarity.py",
        ]
        for principle in required_principles:
            self.assertIn(principle, skill)

        self.assertNotIn("结尾句不完整", skill)
        archived = (
            "13-钩子映射表.md",
            "hook-techniques.md",
            "07-叙事节奏曲线.md",
            "05-节奏健康报告.md",
            "06-出版门控.md",
            "content-expansion.md",
        )
        load_section = skill.split("## 按问题加载", 1)[1].split("## 工具", 1)[0]
        for name in archived:
            self.assertNotIn(name, load_section)

    def test_skill_and_readme_reference_opening_and_ending_guides(self):
        required = {"references/opening-design.md", "references/ending-design.md"}

        combined = "\n".join(path.read_text(encoding="utf-8") for path in MARKDOWN_FILES)

        for rel_path in required:
            self.assertIn(rel_path, combined)

    def test_character_sandbox_mode_is_discoverable(self):
        required_reference = "references/14-角色沙盘模式.md"
        required_files = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "FILE_INDEX.md"]

        for path in required_files:
            content = path.read_text(encoding="utf-8")
            self.assertIn(
                required_reference,
                content,
                msg=f"{path.name} should link to {required_reference}",
            )

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("角色沙盘模式", readme)

    def test_short_story_mode_is_discoverable(self):
        required_reference = "references/short-story-template.md"
        required_script = "scripts/check_short_story.py"
        required_files = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "QUICK_START.md",
            ROOT / "FILE_INDEX.md",
        ]

        for path in required_files:
            content = path.read_text(encoding="utf-8")
            self.assertIn(
                required_reference,
                content,
                msg=f"{path.name} should link to {required_reference}",
            )
            self.assertIn(
                required_script,
                content,
                msg=f"{path.name} should link to {required_script}",
            )
            self.assertIn("短故事", content)

    def test_short_story_mode_writes_named_markdown_file(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        short_story_section = skill.split("## 短故事模式（可选）", 1)[1].split("## 🤖 自动驾驶模式", 1)[0]
        prompt_expectations = (ROOT / "test-prompts.json").read_text(encoding="utf-8")

        required_phrases = [
            "short-stories/YYYYMMDD-<标题>.md",
            "不得在对话中直接输出完整正文",
            "对话只回复文件路径",
            "运行 `python3 scripts/check_short_story.py <短故事文件路径>`",
        ]

        for phrase in required_phrases:
            self.assertIn(phrase, short_story_section)

        self.assertIn("short-stories/YYYYMMDD-<标题>.md", prompt_expectations)
        self.assertIn("只在对话中汇报文件路径", prompt_expectations)
        self.assertNotIn("交付短故事任务卡、完整剧情骨架、不少于6000字的完整正文", prompt_expectations)

    def test_translation_mode_uses_current_ai_adaptive_translation(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        translation_section = skill.split("## Translation", 1)[1]

        required_phrases = [
            "当前 AI",
            "意译翻译",
            "不调用独立翻译接口",
            "翻译简报",
            "样章校准",
            "双语修订",
            "单语润色",
            "终检",
            "manuscript/en/Chapter-XXX.md",
            "章数和章标题同在第一行",
            "空一行后直接写正文",
            "scripts/translate_to_english.py",
            "references/translation-workflow.md",
        ]

        for phrase in required_phrases:
            self.assertIn(phrase, translation_section)

        self.assertNotIn("API 环境变量", translation_section)
        self.assertNotIn("指定 AI 提供商", translation_section)
        self.assertNotIn("## Title", translation_section)
        self.assertNotIn("## Body", translation_section)

    def test_batch_production_mode_is_discoverable(self):
        required_reference = "references/batch-production.md"
        required_scripts = [
            "scripts/check_chapter_transaction.py",
            "scripts/check_cross_book_similarity.py",
        ]
        required_files = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "FILE_INDEX.md",
        ]

        for path in required_files:
            content = path.read_text(encoding="utf-8")
            self.assertIn(required_reference, content, msg=f"{path.name} should link to {required_reference}")
            for script in required_scripts:
                self.assertIn(script, content, msg=f"{path.name} should link to {script}")
            self.assertIn("批量", content)

        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("novels/00-批量任务清单.md", skill)
        self.assertIn("上一章末尾 800 字", skill)
        self.assertIn("上一章全文", skill)
        self.assertNotIn("禁止默认重读最近 1–3 章全文", skill)

    def test_clean_manuscript_workspace_structure_is_discoverable(self):
        required_files = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "QUICK_START.md",
            ROOT / "FILE_INDEX.md",
        ]
        required_phrases = [
            "manuscript/zh",
            "workspace/chapters",
            "manuscript/en",
            "scripts/split_chapter_workspace.py",
            "references/chapter-workspace-template.md",
        ]

        for path in required_files:
            content = path.read_text(encoding="utf-8")
            for phrase in required_phrases:
                self.assertIn(phrase, content, msg=f"{path.name} should mention {phrase}")

    def test_grok_and_antigravity_harness_is_discoverable(self):
        required = [
            ROOT / "references" / "harness-grok-antigravity.md",
            ROOT / "GEMINI.md",
            ROOT / ".grok" / "agents" / "blind-reader.md",
            ROOT / ".grok" / "agents" / "chinese-novelist.md",
            ROOT / ".grok" / "commands" / "next-chapter.md",
            ROOT / ".grok" / "commands" / "new-novel.md",
            ROOT / ".grok" / "workflows" / "chinese-novelist-factory.rhai",
            ROOT / ".agents" / "agents" / "blind-reader.md",
            ROOT / ".agents" / "agents" / "chinese-novelist.md",
            ROOT / ".agents" / "workflows" / "next-chapter.md",
            ROOT / ".agents" / "workflows" / "factory-chapter.md",
            ROOT / ".agents" / "skills" / "chinese-novelist-skill" / "SKILL.md",
        ]
        for path in required:
            self.assertTrue(path.is_file(), msg=f"missing harness file: {path.relative_to(ROOT)}")

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        quick = (ROOT / "QUICK_START.md").read_text(encoding="utf-8")
        for text in (readme, quick):
            self.assertIn("~/.grok/skills/chinese-novelist-skill", text)
            self.assertIn("Antigravity", text)
            self.assertNotIn("Grok Build、Hermes、Pi 等无 skill 机制", text)
            self.assertNotIn("无独立 skill 机制的 Agent（Grok Build", text)

        harness = (ROOT / "references" / "harness-grok-antigravity.md").read_text(encoding="utf-8")
        self.assertIn("spawn_subagent", harness)
        self.assertIn("invoke_subagent", harness)
        self.assertIn("blind-reader", harness)
        self.assertIn("chinese-novelist-factory", harness)

        grok_reader = (ROOT / ".grok" / "agents" / "blind-reader.md").read_text(encoding="utf-8")
        agy_reader = (ROOT / ".agents" / "agents" / "blind-reader.md").read_text(encoding="utf-8")
        self.assertIn("read_file", grok_reader)
        self.assertIn("view_file", agy_reader)
        self.assertIn("复述不出", grok_reader)
        self.assertIn("复述不出", agy_reader)

        wrapper = (
            ROOT / ".agents" / "skills" / "chinese-novelist-skill" / "SKILL.md"
        ).read_text(encoding="utf-8")
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../../../SKILL.md", wrapper)
        self.assertIn("when-to-use", wrapper)
        root_desc = root_skill.split("description:", 1)[1].split("when-to-use:", 1)[0].strip()
        wrap_desc = wrapper.split("description:", 1)[1].split("when-to-use:", 1)[0].strip()
        self.assertEqual(root_desc, wrap_desc)

    def test_local_markdown_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

        # Template files contain placeholder links that only resolve at runtime
        # (e.g. progress-dashboard-template.md links to 00-大纲.md which
        # only exists inside novels/ directories)
        TEMPLATE_LINKS = {
            '00-大纲.md', '01-人物档案.md', '02-世界观与伏笔.md',
            '03-悬念追踪表.md', '04-角色沙盘/00-角色索引.md',
            '00-批量任务清单.md',
            '05-声音锁.md',
        }

        for path in ROOT.rglob("*.md"):
            # Skip historical design docs (their links don't resolve from docs/plans/)
            if 'docs/plans' in str(path) or 'docs/legacy' in str(path):
                continue
            content = path.read_text(encoding="utf-8")
            for target in pattern.findall(content):
                if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
                    continue
                # Template placeholder links only resolve at runtime in novels/ directories
                if target in TEMPLATE_LINKS:
                    continue
                if '___' in target or target.startswith('第'):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    msg=f"{path.relative_to(ROOT)} has broken link: {target}",
                )


if __name__ == "__main__":
    unittest.main()
