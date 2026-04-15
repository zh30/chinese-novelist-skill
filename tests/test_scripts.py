import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from utils import extract_text_from_chapter, count_chinese_words, find_chapter_files


class TestUtils(unittest.TestCase):
    def test_count_chinese_words_basic(self):
        text = "这是中文测试"
        self.assertEqual(count_chinese_words(text), 6)

    def test_count_chinese_words_ignores_markdown(self):
        text = "**这是**中文`测试`"
        self.assertEqual(count_chinese_words(text), 6)

    def test_count_chinese_words_ignores_english(self):
        text = "这是hello中文world测试"
        self.assertEqual(count_chinese_words(text), 6)

    def test_extract_text_from_chapter_body_section(self):
        content = """# 第01章-测试

## 本章任务卡
- **章节功能**：推进冲突

## 正文
这是正文内容。
第二段正文。

## 章节复盘
- **本章摘要**：不计入
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "第01章-测试.md"
            path.write_text(content, encoding="utf-8")
            extracted = extract_text_from_chapter(path)
        self.assertIn("这是正文内容", extracted)
        self.assertNotIn("不计入", extracted)

    def test_extract_text_from_chapter_fallback(self):
        content = """# 第01章-测试

这里是正文内容，没有## 正文标记。
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "第01章-测试.md"
            path.write_text(content, encoding="utf-8")
            extracted = extract_text_from_chapter(path)
        self.assertIn("正文内容", extracted)

    def test_find_chapter_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "第01章-开始.md").write_text("# 第01章", encoding="utf-8")
            (Path(tmpdir) / "第02章-发展.md").write_text("# 第02章", encoding="utf-8")
            (Path(tmpdir) / "00-大纲.md").write_text("# 大纲", encoding="utf-8")
            files = find_chapter_files(Path(tmpdir))
        self.assertEqual(len(files), 2)

    def test_find_chapter_files_sorting(self):
        """Chapter files should be sorted by chapter number."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "第10章-后半.md").write_text("第10章", encoding="utf-8")
            (Path(tmpdir) / "第01章-开始.md").write_text("第01章", encoding="utf-8")
            (Path(tmpdir) / "第03章-中间.md").write_text("第03章", encoding="utf-8")
            files = find_chapter_files(Path(tmpdir))
        self.assertEqual(len(files), 3)
        self.assertEqual(files[0].name, "第01章-开始.md")
        self.assertEqual(files[1].name, "第03章-中间.md")
        self.assertEqual(files[2].name, "第10章-后半.md")


class CheckAiStyleTests(unittest.TestCase):
    def test_ai_style_single_file(self):
        from check_ai_style import check_ai_style
        content = """# 第01章-测试

## 正文
他感到前所未有的悲伤。然而她非常开心的笑了。突然，门开了。
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "第01章-测试.md"
            path.write_text(content, encoding="utf-8")
            result = check_ai_style(str(path))
        self.assertTrue(result['exists'])
        self.assertGreater(result['word_count'], 0)
        self.assertIn('check_results', result)
        # Should detect 9 patterns
        self.assertEqual(len(result['check_results']), 9)

    def test_ai_style_nonexistent_file(self):
        from check_ai_style import check_ai_style
        result = check_ai_style("/nonexistent/path/第01章.md")
        self.assertFalse(result['exists'])

    def test_ai_style_detects_emotion_tags(self):
        """Emotion tag detection should catch patterns like '他感到前所未有的悲伤'."""
        from check_ai_style import check_ai_style
        content = """# 第01章-测试

## 正文
他感到前所未有的悲伤。她心中一阵恐惧。
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "第01章-测试.md"
            path.write_text(content, encoding="utf-8")
            result = check_ai_style(str(path))
        self.assertTrue(result['exists'])
        emotion_result = result['check_results'].get('emotion_tags', {})
        self.assertGreater(emotion_result.get('count', 0), 0)


class CheckNovelHealthTests(unittest.TestCase):
    def test_novel_health_basic(self):
        from check_novel_health import check_novel
        with tempfile.TemporaryDirectory() as tmpdir:
            content = """# 第01章-测试

## 正文
他在房间里坐着。她走了进来。他们开始对话。
""" * 10
            (Path(tmpdir) / "第01章-测试.md").write_text(content, encoding="utf-8")
            result = check_novel(Path(tmpdir))
        self.assertEqual(result['total_chapters'], 1)
        self.assertIn('word_score', result)
        self.assertIn('rhythm_score', result)

    def test_novel_health_multiple_chapters(self):
        """Health check should work with multiple chapter files."""
        from check_novel_health import check_novel
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "第01章-开始.md").write_text(
                "# 第01章\n## 正文\n他在房间里坐着看窗外。\n" * 50,
                encoding="utf-8"
            )
            (Path(tmpdir) / "第02章-发展.md").write_text(
                "# 第02章\n## 正文\n她冲到外面街道上跑了。\n" * 50,
                encoding="utf-8"
            )
            result = check_novel(Path(tmpdir))
        self.assertEqual(result['total_chapters'], 2)
        self.assertGreater(result['total_words'], 0)


if __name__ == "__main__":
    unittest.main()
