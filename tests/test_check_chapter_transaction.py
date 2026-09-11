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


BLIND_READ = """# 盲读

- **我以为自己在读一个怎样的人**：一个不敢报警、把父亲日志藏进外套的女儿
- **走神起点**：无
- **我最想知道而文本没给的**：少掉的那一页写了什么
- **不可逆变化（读者复述）**：她没有报警，把日志藏进外套，从此不能回家
- **听起来像作者、不像人物的句子**：无
- **是否还想翻下一页**：想
- **一句话总判**：她用旧钥匙切断了回家的路
"""

PERCEPTION = """# 感知包

- **POV**：她
- **此刻最想保住的**：父亲留下的航海日志
- **进门第一眼**：阁楼铁环上的旧钥匙和一圈灰
- **故意不看的**：母亲放在楼梯口的拖鞋
- **以为对方要什么**：母亲只是想催她吃饭
- **本轮保护策略**：把缺页藏进外套，装成无事发生
- **绝不会说出口的半句**：日志里少的那页可能写着我的名字
- **策略失败时身体先做的**：把钥匙按进掌心直到生疼
"""

REVIEW = """# 章节复盘

- **三句以内摘要**：她用旧钥匙打开阁楼，发现父亲的航海日志少了一页。
- **最重要的选择与后果**：她没有报警，把日志藏进外套，从此不能回家。
- **关系变化的可观察证据**：她拒绝接母亲电话。
- **盲读指出**：少掉的那一页仍未给读者。
- **正文改动**：章末只停在藏日志，不再解释她为什么怕。
- **下一章必然由什么结果引发**：少掉的那一页会把她带到码头仓库。
"""

DASHBOARD = """# 测试小说 创作进度

- **写作模式**：作者

## 滚动前情摘要

### 章节一行摘要

- 第001章：旧钥匙打开阁楼，航海日志少了一页
"""


def _write_novel(
    root: Path,
    name='测试小说',
    complete=True,
    min_words=40,
    blind_read=None,
    perception=None,
    review=None,
    dashboard=None,
    writing_mode='作者',
):
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
        (workspace / 'review.md').write_text(review or REVIEW, encoding='utf-8')
        (workspace / 'blind-read.md').write_text(blind_read or BLIND_READ, encoding='utf-8')
        (workspace / 'perception.md').write_text(perception or PERCEPTION, encoding='utf-8')
        dash = dashboard or DASHBOARD.replace('作者', writing_mode)
        (novel / '99-进度仪表盘.md').write_text(dash, encoding='utf-8')
    else:
        (novel / '99-进度仪表盘.md').write_text('# 测试小说\n\n还没有摘要\n', encoding='utf-8')

    return novel


class CheckChapterTransactionTests(unittest.TestCase):
    def test_complete_transaction_passes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['status'], 'pass')
        self.assertGreaterEqual(result['word_count'], 40)
        self.assertTrue(result['checks']['rolling_summary']['passed'])
        self.assertTrue(result['checks']['摘要']['passed'])
        self.assertTrue(result['checks']['选择与代价']['passed'])
        self.assertTrue(result['checks']['状态回写']['passed'])
        self.assertTrue(result['checks']['irreversible_change']['passed'])
        self.assertTrue(result['checks']['perception_file']['passed'])

    def test_v31_workspace_without_blind_read_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            (novel / 'workspace' / 'chapters' / '第001章-旧钥匙' / 'blind-read.md').unlink()
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['blind_read_file']['passed'])

    def test_restatement_cannot_restate_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(
                Path(tmpdir),
                blind_read=BLIND_READ.replace(
                    '她没有报警，把日志藏进外套，从此不能回家',
                    '复述不出',
                ),
            )
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['irreversible_change']['passed'])

    def test_empty_and_upgrade_only_restatement_fail(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(
                Path(tmpdir),
                blind_read=BLIND_READ.replace(
                    '她没有报警，把日志藏进外套，从此不能回家',
                    '___',
                ),
            )
            empty = check_chapter_transaction(novel, 1)
            (novel / 'workspace' / 'chapters' / '第001章-旧钥匙' / 'blind-read.md').write_text(
                BLIND_READ.replace('她没有报警，把日志藏进外套，从此不能回家', '推进升级'),
                encoding='utf-8',
            )
            weak = check_chapter_transaction(novel, 1)

        self.assertEqual(empty['status'], 'fail')
        self.assertFalse(empty['checks']['irreversible_change']['passed'])
        self.assertEqual(weak['status'], 'fail')
        self.assertFalse(weak['checks']['irreversible_change']['passed'])

    def test_short_author_chapter_about_900_chars_passes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir), min_words=900)
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['status'], 'pass')
        self.assertGreaterEqual(result['word_count'], 900)
        self.assertLess(result['word_count'], 3000)
        self.assertIn('word_count_report', result['checks'])
        self.assertTrue(result['checks']['word_count_report']['passed'])
        self.assertNotIn('word_count', result['checks'])

    def test_missing_perception_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            (novel / 'workspace' / 'chapters' / '第001章-旧钥匙' / 'perception.md').unlink()
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['perception_file']['passed'])

    def test_placeholder_perception_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(
                Path(tmpdir),
                perception=PERCEPTION.replace('阁楼铁环上的旧钥匙和一圈灰', '真相'),
            )
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['感知-进门第一眼']['passed'])

    def test_factory_short_chapter_fails_min_words(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir), min_words=40, writing_mode='工厂')
            result = check_chapter_transaction(novel, 1, factory=True, min_words=3000)

        self.assertEqual(result['status'], 'fail')
        self.assertEqual(result['mode'], 'factory')
        self.assertFalse(result['checks']['word_count']['passed'])

    def test_dashboard_bold_factory_without_factory_flag(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir), min_words=40, writing_mode='工厂')
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['mode'], 'factory')
        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['word_count']['passed'])

    def test_dashboard_table_factory_without_factory_flag(self):
        table = """# 测试小说 创作进度

| 项目 | 状态 |
|------|------|
| 写作模式 | 工厂 |

## 滚动前情摘要

### 章节一行摘要

- 第001章：旧钥匙打开阁楼，航海日志少了一页
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir), min_words=40, dashboard=table)
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['mode'], 'factory')
        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['word_count']['passed'])

    def test_dashboard_unfilled_template_stays_author(self):
        table = """# 测试小说 创作进度

| 项目 | 状态 |
|------|------|
| 写作模式 | 作者 / 工厂 |

## 滚动前情摘要

### 章节一行摘要

- 第001章：旧钥匙打开阁楼，航海日志少了一页
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir), min_words=900, dashboard=table)
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['mode'], 'author')
        self.assertEqual(result['status'], 'pass')

    def test_missing_review_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir), complete=False)
            result = check_chapter_transaction(novel, 1)

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
            result = check_chapter_transaction(novel, 1)

        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['checks']['摘要']['passed'])
        self.assertFalse(result['checks']['选择与代价']['passed'])
        self.assertFalse(result['checks']['状态回写']['passed'])

    def test_accepts_chapter_file_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            chapter = novel / 'manuscript' / 'zh' / '第001章-旧钥匙.md'
            result = check_chapter_transaction(novel, chapter)

        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['chapter'], 1)

    def test_check_all_finds_existing_chapters(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_novel(Path(tmpdir))
            results = check_all_chapter_transactions(novel)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
