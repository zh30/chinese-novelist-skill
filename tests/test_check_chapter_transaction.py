import tempfile
import unittest
from pathlib import Path

from scripts.check_chapter_transaction import (
    check_all_chapter_transactions,
    check_chapter_transaction,
)


BODY_SENTENCE = '她把旧钥匙按进掌心，决定今晚不再回家。'


def _enough_body(min_words=40):
    return BODY_SENTENCE * ((min_words // 16) + 2)


def _write_novel(root: Path, name='测试小说', complete=True, min_words=40):
    novel = root / name
    manuscript = novel / 'manuscript' / 'zh'
    workspace = novel / 'workspace' / 'chapters' / '第001章-旧钥匙'
    manuscript.mkdir(parents=True)
    workspace.mkdir(parents=True)

    (manuscript / '第001章-旧钥匙.md').write_text(
        f'第001章：旧钥匙\n\n{_enough_body(min_words)}\n',
        encoding='utf-8',
    )

    if complete:
        (workspace / 'review.md').write_text(
            """# 章节复盘

- **三句以内摘要**：她用旧钥匙打开阁楼，发现父亲的航海日志少了一页。
- **最重要的选择与后果**：她没有报警，把日志藏进外套，从此不能回家。
- **关系变化的可观察证据**：她拒绝接母亲电话。
- **下一章必然由什么结果引发**：少掉的那一页会把她带到码头仓库。
""",
            encoding='utf-8',
        )
        (novel / '99-进度仪表盘.md').write_text(
            """# 测试小说 创作进度

## 滚动前情摘要

### 章节一行摘要

- 第001章：旧钥匙打开阁楼，航海日志少了一页
""",
            encoding='utf-8',
        )
    else:
        (novel / '99-进度仪表盘.md').write_text('# 测试小说\n\n还没有摘要\n', encoding='utf-8')

    return novel


class CheckChapterTransactionTests(unittest.TestCase):
    def test_complete_transaction_passes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            result = check_chapter_transaction(novel, 1, min_words=40)

        self.assertEqual(result['status'], 'pass')
        self.assertGreaterEqual(result['word_count'], 40)
        self.assertTrue(result['checks']['rolling_summary']['passed'])
        self.assertTrue(result['checks']['摘要']['passed'])
        self.assertTrue(result['checks']['选择与代价']['passed'])
        self.assertTrue(result['checks']['状态回写']['passed'])

    def test_missing_review_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir), complete=False)
            result = check_chapter_transaction(novel, 1, min_words=40)

        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['review_file']['passed'])
        self.assertFalse(result['checks']['rolling_summary']['passed'])

    def test_placeholder_review_fields_fail(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            review = novel / 'workspace' / 'chapters' / '第001章-旧钥匙' / 'review.md'
            review.write_text(
                """# 章节复盘

- **三句以内摘要**：___
- **最重要的选择与后果**：
- **下一章必然由什么结果引发**：待填
""",
                encoding='utf-8',
            )
            result = check_chapter_transaction(novel, 1, min_words=40)

        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['摘要']['passed'])
        self.assertFalse(result['checks']['选择与代价']['passed'])
        self.assertFalse(result['checks']['状态回写']['passed'])

    def test_accepts_chapter_file_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            chapter = novel / 'manuscript' / 'zh' / '第001章-旧钥匙.md'
            result = check_chapter_transaction(novel, chapter, min_words=40)

        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['chapter'], 1)

    def test_check_all_finds_existing_chapters(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            results = check_all_chapter_transactions(novel, min_words=40)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
