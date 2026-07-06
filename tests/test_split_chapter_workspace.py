import tempfile
import unittest
from pathlib import Path

from scripts.split_chapter_workspace import split_chapter_workspace


class SplitChapterWorkspaceTests(unittest.TestCase):
    def test_splits_mixed_chapter_into_manuscript_and_workspace(self):
        content = """# 第001章-雨夜

## 本章任务卡
- **章节功能**：打开冲突

## 场景拆分
1. 旧站台
2. 灯灭

---

## 正文

雨落在旧站台上。

林舟没有抬头。

---

## 章节复盘
- **本章摘要**：林舟收到来信
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            novel_dir = Path(tmpdir)
            source = novel_dir / "第001章-雨夜.md"
            source.write_text(content, encoding="utf-8")

            result = split_chapter_workspace(novel_dir)

            clean_path = novel_dir / "manuscript" / "zh" / "第001章-雨夜.md"
            workspace_dir = novel_dir / "workspace" / "chapters" / "第001章-雨夜"

            self.assertTrue(result["ok"])
            self.assertTrue(source.exists())
            self.assertTrue(clean_path.exists())
            self.assertTrue((workspace_dir / "task-card.md").exists())
            self.assertTrue((workspace_dir / "scene-plan.md").exists())
            self.assertTrue((workspace_dir / "review.md").exists())

            clean = clean_path.read_text(encoding="utf-8")
            task_card = (workspace_dir / "task-card.md").read_text(encoding="utf-8")
            review = (workspace_dir / "review.md").read_text(encoding="utf-8")

        self.assertEqual(clean, "第001章：雨夜\n\n雨落在旧站台上。\n\n林舟没有抬头。\n")
        self.assertIn("打开冲突", task_card)
        self.assertIn("林舟收到来信", review)
        self.assertNotIn("本章任务卡", clean)
        self.assertNotIn("章节复盘", clean)

    def test_move_originals_archives_source_when_requested(self):
        content = """# 第001章-雨夜

## 正文
雨落在旧站台上。
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            novel_dir = Path(tmpdir)
            source = novel_dir / "第001章-雨夜.md"
            source.write_text(content, encoding="utf-8")

            result = split_chapter_workspace(novel_dir, move_originals=True)

            archive = novel_dir / "_archive" / "mixed-chapters" / "第001章-雨夜.md"

            self.assertTrue(result["ok"])
            self.assertFalse(source.exists())
            self.assertTrue(archive.exists())


if __name__ == "__main__":
    unittest.main()
