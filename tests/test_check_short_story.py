import tempfile
import unittest
from pathlib import Path

from scripts.check_short_story import check_all_short_stories, check_short_story


BLIND = """
## 盲读

- **我以为自己在读一个怎样的人**：一个守在车站、最后把录音公开的人
- **走神起点**：无
- **我最想知道而文本没给的**：录音里的原话
- **不可逆变化（读者复述）**：她选择公开录音，母亲的名字被写回档案
- **听起来像作者、不像人物的句子**：「她选择公开录音」
- **是否还想翻下一页**：想
- **一句话总判**：她用公开录音结束了隐瞒
"""


class CheckShortStoryTests(unittest.TestCase):
    def test_complete_short_story_passes_all_required_checks(self):
        content = """# 短故事：雨夜

## 短故事任务卡
- **字数目标**：习惯参考 6000 字

## 正文
雨下了一夜，林青一直守在旧车站门口。
她第一次行动失败后，终于在候车室里发现真相。
高潮到来时，她选择公开录音，哪怕会失去工作。
天亮以后，案件收束，母亲的名字也被重新写回档案。
""" + BLIND + """
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
        self.assertTrue(result["checks"]["blind_read"]["passed"])
        self.assertTrue(result["checks"]["irreversible_change"]["passed"])
        self.assertTrue(result["checks"]["quote_作者腔"]["passed"])
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
        self.assertFalse(result["checks"]["completion_review"]["passed"])
        self.assertFalse(result["checks"]["blind_read"]["passed"])
        self.assertFalse(result["checks"]["no_to_be_continued"]["passed"])

    def test_check_all_short_stories_checks_markdown_files_in_directory(self):
        complete = """# 短故事：甲

## 正文
开端里主角遇到问题。中段他失败一次。
高潮时他做出选择。最后冲突解决，故事收束。
""" + BLIND.replace('她选择公开录音', '他做出选择').replace('母亲的名字被写回档案', '故事收束') + """
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

    def test_default_does_not_fail_under_6000_words(self):
        content = """# 短故事：雨夜

## 短故事任务卡
- **字数目标**：习惯参考 6000

## 正文
雨下了一夜，林青一直守在旧车站门口。
她第一次行动失败后，终于在候车室里发现真相。
高潮到来时，她选择公开录音，哪怕会失去工作。
天亮以后，案件收束，母亲的名字也被重新写回档案。
""" + BLIND + """
## 完稿复盘
- **主角变化**：从逃避到承担
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "雨夜.md"
            path.write_text(content, encoding="utf-8")
            default = check_short_story(str(path))
            strict = check_short_story(str(path), min_words=6000, strict=True)

        self.assertEqual(default["status"], "pass")
        self.assertTrue(default["checks"]["word_count"]["passed"])
        self.assertLess(default["word_count"], 6000)
        self.assertEqual(strict["status"], "fail")
        self.assertFalse(strict["checks"]["word_count"]["passed"])

    def test_keyword_climax_without_blind_read_fails(self):
        content = """# 短故事：雨夜

## 正文
她终于做出选择。后来故事收束，一切结束。

## 完稿复盘
- **主角变化**：从逃避到承担
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "雨夜.md"
            path.write_text(content, encoding="utf-8")
            result = check_short_story(str(path), min_words=10)

        self.assertEqual(result["status"], "fail")
        self.assertFalse(result["checks"]["blind_read"]["passed"])
        self.assertNotIn("plot_completion", result["checks"])

    def test_quote_missing_from_body_fails(self):
        content = """# 短故事：雨夜

## 正文
雨下了一夜，林青一直守在旧车站门口。她选择公开录音。
""" + BLIND.replace('「她选择公开录音」', '「她在天台跳了下去」') + """
## 完稿复盘
- **主角变化**：从逃避到承担
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "雨夜.md"
            path.write_text(content, encoding="utf-8")
            result = check_short_story(str(path), min_words=10)

        self.assertEqual(result["status"], "fail")
        self.assertFalse(result["checks"]["quote_作者腔"]["passed"])

    def test_restatement_copied_from_task_card_fails(self):
        content = """# 短故事：雨夜

## 短故事任务卡
- **高潮选择与代价**：把缺页航海日志藏进外套并当夜离开母亲

## 正文
雨下了一夜，林青一直守在旧车站门口。她选择公开录音。
""" + BLIND.replace(
            '她选择公开录音，母亲的名字被写回档案',
            '把缺页航海日志藏进外套并当夜离开母亲',
        ) + """
## 完稿复盘
- **主角变化**：从逃避到承担
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "雨夜.md"
            path.write_text(content, encoding="utf-8")
            result = check_short_story(str(path), min_words=10)

        self.assertEqual(result["status"], "fail")
        self.assertFalse(result["checks"]["plan_leak"]["passed"])


if __name__ == "__main__":
    unittest.main()

