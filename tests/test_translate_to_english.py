import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.translate_to_english import build_translation_prompt, translate_novel


class BuildTranslationPromptTests(unittest.TestCase):
    def test_prompt_requires_adaptive_translation(self):
        prompt = build_translation_prompt(
            {
                "title": "测试小说",
                "author": "测试作者",
                "genre": "悬疑",
                "synopsis": "一个关于失踪灯塔的故事。",
                "characters": "林舟：灯塔管理员。",
                "worldbuilding": "海边小镇。",
            },
            "林舟推开灯塔的门。",
            "灯塔",
        )

        self.assertIn("意译翻译", prompt)
        self.assertIn("adaptive translation", prompt)
        self.assertIn("Do not translate word-for-word", prompt)

    def test_prompt_embeds_professional_translation_stages(self):
        prompt = build_translation_prompt(
            {
                "title": "测试小说",
                "author": "测试作者",
                "genre": "悬疑",
                "synopsis": "一个关于失踪灯塔的故事。",
                "characters": "",
                "worldbuilding": "",
            },
            "林舟推开灯塔的门。",
            "灯塔",
        )

        required = [
            "翻译简报",
            "术语表",
            "风格表",
            "译者自检",
            "双语修订",
            "单语润色",
        ]

        for phrase in required:
            self.assertIn(phrase, prompt)

    def test_prompt_requires_plain_translated_markdown_format(self):
        prompt = build_translation_prompt(
            {
                "title": "测试小说",
                "author": "测试作者",
                "genre": "悬疑",
                "synopsis": "一个关于失踪灯塔的故事。",
                "characters": "",
                "worldbuilding": "",
            },
            "林舟推开灯塔的门。",
            "灯塔",
            chapter_number=1,
        )

        self.assertIn("Chapter 1: ", prompt)
        self.assertIn("first line", prompt)
        self.assertIn("blank line", prompt)
        self.assertIn("body text", prompt)
        self.assertIn("no Markdown headings", prompt)
        self.assertNotIn("## Title", prompt)
        self.assertNotIn("## Body", prompt)


class TranslateToEnglishTests(unittest.TestCase):
    def test_translate_novel_prepares_current_ai_task_without_api_keys(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel_dir = Path(tmpdir)
            (novel_dir / "00-大纲.md").write_text(
                """# 测试小说 大纲

**作者 / 笔名**：测试作者
""",
                encoding="utf-8",
            )
            (novel_dir / "第01章-开始.md").write_text(
                """# 第01章 开始

## 正文
这是需要翻译的正文。
""",
                encoding="utf-8",
            )

            with patch.dict("os.environ", {}, clear=True):
                result = translate_novel(novel_dir, chapters="1")

            self.assertTrue(result)
            task_path = novel_dir / "manuscript" / "en" / "_translation_tasks" / "Chapter-001.prompt.md"
            self.assertTrue(task_path.exists())
            task_content = task_path.read_text(encoding="utf-8")
            self.assertIn("当前 AI", task_content)
            self.assertIn("意译翻译", task_content)
            self.assertIn("这是需要翻译的正文。", task_content)
            self.assertFalse((novel_dir / "manuscript" / "en" / "Chapter-001.md").exists())

    def test_translate_novel_prepares_professional_workflow_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel_dir = Path(tmpdir)
            (novel_dir / "00-大纲.md").write_text(
                """# 灯塔来信 大纲

**作者 / 笔名**：测试作者
**题材 / 类型**：悬疑
**一句话简介**：灯塔里藏着一封不该存在的信。
""",
                encoding="utf-8",
            )
            (novel_dir / "01-人物档案.md").write_text(
                "林舟：灯塔管理员。\n沈照：失踪的邮差。\n",
                encoding="utf-8",
            )
            (novel_dir / "02-世界观与伏笔.md").write_text(
                "雾港：潮汐会改变街道入口的海边小镇。\n",
                encoding="utf-8",
            )
            (novel_dir / "第01章-灯塔.md").write_text(
                """# 第01章 灯塔

## 正文
林舟推开灯塔的门，潮声从背后追上来。
""",
                encoding="utf-8",
            )

            result = translate_novel(novel_dir, chapters="1")

            self.assertTrue(result)
            expected_files = [
                "00-translation-brief.md",
                "01-termbase.md",
                "02-style-sheet.md",
                "03-query-log.md",
                "04-qa-checklist.md",
                "_translation_tasks/Chapter-001.translate.prompt.md",
                "_translation_tasks/Chapter-001.revise.prompt.md",
                "_translation_tasks/Chapter-001.edit.prompt.md",
            ]

            for rel_path in expected_files:
                self.assertTrue((novel_dir / "manuscript" / "en" / rel_path).exists(), rel_path)

            brief = (novel_dir / "manuscript" / "en" / "00-translation-brief.md").read_text(encoding="utf-8")
            termbase = (novel_dir / "manuscript" / "en" / "01-termbase.md").read_text(encoding="utf-8")
            style_sheet = (novel_dir / "manuscript" / "en" / "02-style-sheet.md").read_text(encoding="utf-8")
            qa = (novel_dir / "manuscript" / "en" / "04-qa-checklist.md").read_text(encoding="utf-8")
            translate_prompt = (
                novel_dir / "manuscript" / "en" / "_translation_tasks" / "Chapter-001.translate.prompt.md"
            ).read_text(encoding="utf-8")
            revise_prompt = (
                novel_dir / "manuscript" / "en" / "_translation_tasks" / "Chapter-001.revise.prompt.md"
            ).read_text(encoding="utf-8")
            edit_prompt = (
                novel_dir / "manuscript" / "en" / "_translation_tasks" / "Chapter-001.edit.prompt.md"
            ).read_text(encoding="utf-8")

            self.assertIn("翻译目的", brief)
            self.assertIn("目标读者", brief)
            self.assertIn("交付规格", brief)
            self.assertIn("林舟", termbase)
            self.assertIn("中文术语", termbase)
            self.assertIn("意译边界", style_sheet)
            self.assertIn("双语修订", qa)
            self.assertIn("单语润色", qa)
            self.assertIn("终检", qa)
            self.assertIn("术语表", translate_prompt)
            self.assertIn("source against target", revise_prompt)
            self.assertIn("read the English only", edit_prompt)
            self.assertIn("Chapter 1: ", translate_prompt)
            self.assertIn("no Markdown headings", translate_prompt)
            self.assertIn("plain translated Markdown", qa)
            self.assertNotIn("## Title", brief)
            self.assertNotIn("## Body", brief)
            self.assertNotIn("## Title", qa)
            self.assertNotIn("## Body", qa)
            self.assertNotIn("## Title", revise_prompt)
            self.assertNotIn("## Body", revise_prompt)

    def test_translate_novel_reads_clean_manuscript_zh(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel_dir = Path(tmpdir)
            zh_dir = novel_dir / "manuscript" / "zh"
            zh_dir.mkdir(parents=True)
            (novel_dir / "00-大纲.md").write_text(
                """# 干净小说 大纲

**作者 / 笔名**：测试作者
""",
                encoding="utf-8",
            )
            (zh_dir / "第001章-雨夜.md").write_text(
                """第001章：雨夜

雨落在旧站台上。
""",
                encoding="utf-8",
            )

            result = translate_novel(novel_dir, chapters="1")

            self.assertTrue(result)
            task_path = novel_dir / "manuscript" / "en" / "_translation_tasks" / "Chapter-001.translate.prompt.md"
            task_content = task_path.read_text(encoding="utf-8")
            self.assertIn("雨落在旧站台上。", task_content)
            self.assertNotIn("第001章：雨夜\n\n雨落", task_content)

    def test_translation_script_has_no_external_provider_configuration(self):
        script = (Path(__file__).resolve().parent.parent / "scripts" / "translate_to_english.py").read_text(
            encoding="utf-8"
        )

        forbidden = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GEMINI_API_KEY",
            "--provider",
            "translate_with_openai",
            "translate_with_anthropic",
            "translate_with_gemini",
        ]

        for token in forbidden:
            self.assertNotIn(token, script)


if __name__ == "__main__":
    unittest.main()
