import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_FILES = [ROOT / "SKILL.md", ROOT / "README.md"]


class SkillDocsTests(unittest.TestCase):
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

    def test_local_markdown_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

        # Template files contain placeholder links that only resolve at runtime
        # (e.g. progress-dashboard-template.md links to 00-大纲.md which
        # only exists inside novels/ directories)
        TEMPLATE_LINKS = {
            '00-大纲.md', '01-人物档案.md', '02-世界观与伏笔.md',
            '03-悬念追踪表.md', '04-角色沙盘/00-角色索引.md',
        }

        for path in ROOT.rglob("*.md"):
            # Skip historical design docs (their links don't resolve from docs/plans/)
            if 'docs/plans' in str(path):
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
