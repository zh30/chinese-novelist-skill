import tempfile
import unittest
from pathlib import Path

from scripts.check_chapter_wordcount import check_chapter, extract_content_from_chapter


class CheckChapterWordcountTests(unittest.TestCase):
    def test_extracts_only_body_between_body_and_review_sections(self):
        content = """# 第01章：测试

## 本章任务卡
- **章节功能**：推进冲突

## 正文
这里是正文内容。
第二段正文继续推进。

## 章节复盘
- **本章摘要**：不应该计入正文
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "第01章-测试.md"
            path.write_text(content, encoding="utf-8")

            extracted = extract_content_from_chapter(path)

        self.assertEqual(extracted.strip(), "这里是正文内容。\n第二段正文继续推进。")

    def test_check_chapter_counts_only_body_chinese_characters(self):
        content = """# 第01章：测试

## 本章任务卡
- **章节功能**：推进冲突
- **结尾钩子**：有人敲门

## 正文
这是正文。
这里还有第二句。

## 章节复盘
- **新增信息 / 伏笔**：门外的人是谁
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "第01章-测试.md"
            path.write_text(content, encoding="utf-8")

            result = check_chapter(str(path), min_words=5)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["word_count"], 11)


if __name__ == "__main__":
    unittest.main()
