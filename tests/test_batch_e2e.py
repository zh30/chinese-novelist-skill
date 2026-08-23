import tempfile
import unittest
from pathlib import Path

from scripts.check_chapter_transaction import check_chapter_transaction
from scripts.check_cross_book_similarity import check_cross_book_similarity


MANIFEST = """# 批量任务清单

### B001 北港
- **类型**：长篇
- **状态**：连载中第 1 章
- **宪章差异**：题材海运账本；主角策略藏证；结局代价失去回家权

### B002 南园
- **类型**：长篇
- **状态**：策划
- **宪章差异**：题材育苗房；主角策略清点缺口；结局代价失去晋升
"""


def _write_complete_chapter(novel: Path, title='旧账', body=None):
    manuscript = novel / 'manuscript' / 'zh'
    workspace = novel / 'workspace' / 'chapters' / f'第001章-{title}'
    manuscript.mkdir(parents=True, exist_ok=True)
    workspace.mkdir(parents=True, exist_ok=True)
    text = body or ('她把账本藏进油布，转身离开北港栈桥。' * 8)
    (manuscript / f'第001章-{title}.md').write_text(f'第001章：{title}\n\n{text}\n', encoding='utf-8')
    (workspace / 'review.md').write_text(
        """# 章节复盘

- **三句以内摘要**：账本被藏进油布，她不能再走原路回家。
- **最重要的选择与后果**：她拒绝把账本交给工头。
- **下一章必然由什么结果引发**：油布会在潮水里露出一角。
""",
        encoding='utf-8',
    )
    (novel / '99-进度仪表盘.md').write_text(
        f"""# {novel.name}

## 滚动前情摘要

- 第001章：账本进油布，回家权被切断
""",
        encoding='utf-8',
    )


class BatchProductionE2ETests(unittest.TestCase):
    def test_manifest_transaction_and_similarity_fixture(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            novels = root / 'novels'
            north = novels / '北港'
            south = novels / '南园'
            (novels).mkdir()
            (novels / '00-批量任务清单.md').write_text(MANIFEST, encoding='utf-8')

            _write_complete_chapter(north, title='油布', body='她把账本藏进油布，潮水拍打北港栈桥。' * 8)
            (north / '01-人物档案.md').write_text('## 主角：周石\n\n- **姓名**：周石\n', encoding='utf-8')

            incomplete = south / 'manuscript' / 'zh'
            incomplete.mkdir(parents=True)
            (incomplete / '第001章-缺苗.md').write_text('第001章：缺苗\n\n只有一句开头。\n', encoding='utf-8')
            (south / '99-进度仪表盘.md').write_text('# 南园\n\n还没写摘要\n', encoding='utf-8')
            (south / '01-人物档案.md').write_text('## 主角：苏晚\n\n- **姓名**：苏晚\n', encoding='utf-8')

            passed = check_chapter_transaction(north, 1, min_words=40)
            failed = check_chapter_transaction(south, 1, min_words=40)
            similarity = check_cross_book_similarity(novels)

            self.assertTrue((novels / '00-批量任务清单.md').exists())
            self.assertIn('宪章差异', (novels / '00-批量任务清单.md').read_text(encoding='utf-8'))
            self.assertEqual(passed['status'], 'pass')
            self.assertEqual(failed['status'], 'fail')
            self.assertFalse(failed['checks']['review_file']['passed'])
            self.assertEqual(len(similarity['books']), 2)
            self.assertEqual(len(similarity['pairs']), 1)
            self.assertEqual(similarity['pairs'][0]['shared_names'], [])


if __name__ == '__main__':
    unittest.main()
