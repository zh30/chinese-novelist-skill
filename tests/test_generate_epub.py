import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.generate_epub import (
    convert_markdown_to_xhtml,
    extract_content_from_chapter,
    find_chapters,
    generate_epub,
    parse_outline,
)


class ParseOutlineTests(unittest.TestCase):
    def test_parses_title_and_author_from_outline(self):
        content = """# 射雕英雄传 大纲

## 项目定位

- **作者 / 笔名**：金庸
- **题材 / 子类型**：武侠
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "00-大纲.md"
            path.write_text(content, encoding="utf-8")

            result = parse_outline(path)

        self.assertEqual(result["title"], "射雕英雄传")
        self.assertEqual(result["author"], "金庸")

    def test_handles_missing_outline_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = parse_outline(Path(tmpdir) / "00-大纲.md")

        self.assertEqual(result["title"], "未知书名")
        self.assertEqual(result["author"], "未知作者")

    def test_handles_missing_author_field(self):
        content = """# 测试小说 大纲

## 项目定位

- **题材 / 子类型**：都市
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "00-大纲.md"
            path.write_text(content, encoding="utf-8")

            result = parse_outline(path)

        self.assertEqual(result["title"], "测试小说")
        # 当作者字段为空时，返回空字符串（后续会提示用户输入）
        self.assertEqual(result["author"], "")


class FindChaptersTests(unittest.TestCase):
    def test_finds_chapter_files_in_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # 创建章节文件
            (tmppath / "第01章-开始.md").write_text("# 第01章 开始\n\n## 正文\n第一章内容", encoding="utf-8")
            (tmppath / "第02章-发展.md").write_text("# 第02章 发展\n\n## 正文\n第二章内容", encoding="utf-8")
            (tmppath / "第03章-高潮.md").write_text("# 第03章 高潮\n\n## 正文\n第三章内容", encoding="utf-8")

            chapters = find_chapters(tmppath)

        self.assertEqual(len(chapters), 3)
        self.assertEqual(chapters[0]["title"], "开始")
        self.assertEqual(chapters[1]["title"], "发展")
        self.assertEqual(chapters[2]["title"], "高潮")

    def test_finds_chapter_title_excluding_task_card(self):
        """测试：章节标题应该是真正的章节标题，而不是本章任务卡"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # 创建带有本章任务卡的章节文件
            content = """# 第01章-林墨的抉择

## 本章任务卡
- **章节功能**：
- **承接上章**：

## 场景拆分
1. 场景一

---

## 正文

林墨站在破碎的甲板上，看着远方的星空。他知道，这是最后的机会了。

---

## 章节复盘
- **本章摘要**：
"""
            (tmppath / "第01章-林墨的抉择.md").write_text(content, encoding="utf-8")

            chapters = find_chapters(tmppath)

        self.assertEqual(len(chapters), 1)
        # 标题不应该是"本章任务卡"，应该是从文件名提取或跳过任务卡
        self.assertNotEqual(chapters[0]["title"], "本章任务卡")

    def test_returns_empty_list_when_no_chapters(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            chapters = find_chapters(Path(tmpdir))

        self.assertEqual(chapters, [])


class ExtractContentFromChapterTests(unittest.TestCase):
    def test_extracts_only_body_content(self):
        """测试：只提取 ## 正文 区块的内容，不包含任务卡、摘要、钩子等"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            content = """# 第01章 林墨的抉择

## 本章任务卡
- **章节功能**：
- **承接上章**：

## 场景拆分
1. 场景一

---

## 正文

林墨站在破碎的甲板上，看着远方的星空。他知道，这是最后的机会了。

苏晴紧紧握住他的手："一定要回来。"

---

## 章节复盘
- **本章摘要**：林墨决定牺牲自己
- **章节钩子**：老马说的还有一个人能救地球
"""
            (tmppath / "第01章-林墨的抉择.md").write_text(content, encoding="utf-8")

            result = extract_content_from_chapter(tmppath / "第01章-林墨的抉择.md")

        # 验证不包含任务卡、摘要、钩子等内容
        self.assertNotIn("本章任务卡", result)
        self.assertNotIn("章节摘要", result)
        self.assertNotIn("章节钩子", result)
        self.assertNotIn("章节复盘", result)
        # 验证包含正文内容
        self.assertIn("林墨站在破碎的甲板上", result)
        self.assertIn("苏晴紧紧握住他的手", result)

    def test_handles_missing_body_section(self):
        """测试：没有 ## 正文 时的回退行为"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # 旧模板：没有 ## 正文
            content = """# 第01章 开始

这是第一章的内容。
故事从这里开始。

## 本章任务卡
任务内容
"""
            (tmppath / "第01章-开始.md").write_text(content, encoding="utf-8")

            result = extract_content_from_chapter(tmppath / "第01章-开始.md")

        # 应该包含正文内容，但不包含任务卡
        self.assertIn("这是第一章的内容", result)
        self.assertNotIn("本章任务卡", result)


class ConvertMarkdownToXhtmlTests(unittest.TestCase):
    def test_converts_paragraphs(self):
        content = "第一段\n\n第二段"
        result = convert_markdown_to_xhtml(content)

        self.assertIn("<p>第一段</p>", result)
        self.assertIn("<p>第二段</p>", result)

    def test_converts_headings(self):
        content = "# 大标题\n\n## 二级标题\n\n### 三级标题"
        result = convert_markdown_to_xhtml(content)

        self.assertIn("<h1>大标题</h1>", result)
        self.assertIn("<h2>二级标题</h2>", result)
        self.assertIn("<h3>三级标题</h3>", result)

    def test_escapes_html_characters(self):
        content = "<script>alert('xss')</script>"
        result = convert_markdown_to_xhtml(content)

        self.assertIn("&lt;script&gt;", result)


class GenerateEpubTests(unittest.TestCase):
    def test_generates_valid_epub_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # 创建大纲文件
            outline = """# 测试小说 大纲

## 项目定位

- **作者 / 笔名**：测试作者
- **题材 / 子类型**：都市
"""
            (tmppath / "00-大纲.md").write_text(outline, encoding="utf-8")

            # 创建章节文件
            chapter1 = """# 第01章 开始

## 正文
这是第一章的内容。
故事从这里开始。
"""
            (tmppath / "第01章-开始.md").write_text(chapter1, encoding="utf-8")

            chapter2 = """# 第02章 发展

## 正文
这是第二章的内容。
故事继续发展。
"""
            (tmppath / "第02章-发展.md").write_text(chapter2, encoding="utf-8")

            # 生成 EPUB
            output_path = tmppath / "test.epub"
            result = generate_epub(tmppath, output_path)

            self.assertTrue(result)
            self.assertTrue(output_path.exists())

            # 验证 EPUB 结构
            with zipfile.ZipFile(output_path, 'r') as epub:
                names = epub.namelist()
                self.assertIn('mimetype', names)
                self.assertIn('META-INF/container.xml', names)
                self.assertIn('OEBPS/content.opf', names)
                self.assertIn('OEBPS/nav.xhtml', names)
                self.assertIn('OEBPS/title-page.xhtml', names)

                # 验证 mimetype
                mimetype = epub.read('mimetype').decode('utf-8')
                self.assertEqual(mimetype, 'application/epub+zip')

    def test_overrides_author_from_command_line(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # 创建大纲文件
            outline = """# 测试小说 大纲

## 项目定位

- **作者 / 笔名**：大纲作者
"""
            (tmppath / "00-大纲.md").write_text(outline, encoding="utf-8")

            # 创建章节文件
            chapter = """# 第01章 开始

## 正文
内容
"""
            (tmppath / "第01章-开始.md").write_text(chapter, encoding="utf-8")

            # 生成 EPUB 并覆盖作者
            output_path = tmppath / "test.epub"
            result = generate_epub(tmppath, output_path, author_override="命令行作者")

            self.assertTrue(result)

            # 验证作者被覆盖
            with zipfile.ZipFile(output_path, 'r') as epub:
                content_opf = epub.read('OEBPS/content.opf').decode('utf-8')
                self.assertIn("命令行作者", content_opf)
                self.assertNotIn("大纲作者", content_opf)

    def test_fails_for_nonexistent_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = generate_epub(Path(tmpdir) / "nonexistent", Path(tmpdir) / "test.epub")

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
