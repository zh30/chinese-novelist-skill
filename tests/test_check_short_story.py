import tempfile
import unittest
from pathlib import Path

from scripts.check_short_story import check_all_short_stories, check_short_story


class CheckShortStoryTests(unittest.TestCase):
    def test_complete_short_story_passes_all_required_checks(self):
        content = """# 短故事：雨夜

## 短故事任务卡
- **字数目标**：不少于 6000 字

## 正文
雨下了一夜，林青一直守在旧车站门口。
她第一次行动失败后，终于在候车室里发现真相。
高潮到来时，她选择公开录音，哪怕会失去工作。
天亮以后，案件收束，母亲的名字也被重新写回档案。

## 完稿复盘
- **主角变化**：从逃避到承担
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "雨夜.md"
            path.write_text(content, encoding="utf-8")

            result = check_short_story(str(path), min_words=40)

        self.assertEqual(result["status"], "pass")
        self.assertGreaterEqual(result["word_count"], 40)
        self.assertTrue(result["checks"]["body_section"]["passed"])
        self.assertTrue(result["checks"]["completion_review"]["passed"])
        self.assertTrue(result["checks"]["plot_completion"]["passed"])
        self.assertTrue(result["checks"]["no_to_be_continued"]["passed"])

    def test_incomplete_short_story_reports_specific_failures(self):
        content = """# 短故事：断桥

这是一个还没写完的故事。
主角走到桥边，发现真正的危险才刚刚开始。
未完待续。
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "断桥.md"
            path.write_text(content, encoding="utf-8")

            result = check_short_story(str(path), min_words=40)

        self.assertEqual(result["status"], "fail")
        self.assertFalse(result["checks"]["body_section"]["passed"])
        self.assertFalse(result["checks"]["word_count"]["passed"])
        self.assertFalse(result["checks"]["completion_review"]["passed"])
        self.assertFalse(result["checks"]["plot_completion"]["passed"])
        self.assertFalse(result["checks"]["no_to_be_continued"]["passed"])

    def test_check_all_short_stories_checks_markdown_files_in_directory(self):
        complete = """# 短故事：甲

## 正文
开端里主角遇到问题。中段他失败一次。
高潮时他做出选择。最后冲突解决，故事收束。

## 完稿复盘
- **主角变化**：从犹豫到行动
"""
        incomplete = """# 短故事：乙

## 正文
只有一个开头。
未完待续。
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            stories_dir = Path(tmpdir) / "short-stories"
            stories_dir.mkdir()
            (stories_dir / "甲.md").write_text(complete, encoding="utf-8")
            (stories_dir / "乙.md").write_text(incomplete, encoding="utf-8")
            (stories_dir / "notes.txt").write_text("ignore", encoding="utf-8")

            results = check_all_short_stories(str(stories_dir), min_words=10)

        self.assertEqual([Path(result["file"]).name for result in results], ["乙.md", "甲.md"])
        self.assertEqual([result["status"] for result in results], ["fail", "pass"])


if __name__ == "__main__":
    unittest.main()
