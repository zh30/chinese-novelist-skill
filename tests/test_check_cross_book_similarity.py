import tempfile
import unittest
from pathlib import Path

from scripts.check_cross_book_similarity import (
    check_cross_book_similarity,
    check_multiple_roots,
    load_book_profile,
)


SHARED_OPENING = '雨夜的车站只剩下一盏灯，林青把旧信按进外套内侧。'
DISTINCT_OPENING = '码头仓库的铁门生锈了，陈启用靴尖踢开一只空油桶。'


def _chapter_body(opening, filler):
    return opening + filler * 8


def _write_book(root: Path, name, opening, character, filler):
    novel = root / name
    manuscript = novel / 'manuscript' / 'zh'
    manuscript.mkdir(parents=True)
    (manuscript / '第001章-开篇.md').write_text(
        f'第001章：开篇\n\n{_chapter_body(opening, filler)}\n',
        encoding='utf-8',
    )
    (novel / '01-人物档案.md').write_text(
        f"""# 人物档案

## 主角：{character}

- **姓名**：{character}
- **公开追求**：活过今晚
""",
        encoding='utf-8',
    )
    (novel / '00-大纲.md').write_text(f'# {name}\n\n一句话故事：{character}必须做选择。\n', encoding='utf-8')
    return novel


class CheckCrossBookSimilarityTests(unittest.TestCase):
    def test_similar_books_raise_smoke_alarm(self):
        filler = '她想起月光、雨夜、灯火和旧信，心有余悸地站在巷口听钟声。'
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            left = _write_book(root, '书甲', SHARED_OPENING, '林青', filler)
            right = _write_book(root, '书乙', SHARED_OPENING, '林青', filler)
            result = check_cross_book_similarity(root)

        self.assertEqual(len(result['books']), 2)
        self.assertEqual(result['status'], 'warn')
        pair = result['pairs'][0]
        self.assertIn('林青', pair['shared_names'])
        self.assertIn(pair['severity'], {'medium', 'high'})
        self.assertTrue(pair['warnings'])

    def test_distinct_books_can_pass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_book(root, '灯塔', DISTINCT_OPENING, '陈启', '潮水拍打栈桥，账本被盐粒粘住。')
            _write_book(root, '温室', '育苗房的温度计碎了一地，苏晚把土覆回缺口。', '苏晚', '她数着缺苗的编号，不肯再问经理。')
            result = check_cross_book_similarity(root)

        self.assertEqual(len(result['books']), 2)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['pairs'][0]['shared_names'], [])

    def test_compare_named_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            left = _write_book(root, '北城', SHARED_OPENING, '林青', '雨夜车站的灯火把旧信照湿。')
            right = _write_book(root, '南城', DISTINCT_OPENING, '陈启', '铁门后只有空油桶和潮气。')
            result = check_multiple_roots([left, right])

        self.assertEqual(len(result['books']), 2)
        self.assertEqual(len(result['pairs']), 1)

    def test_single_book_is_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_book(root, '独本', DISTINCT_OPENING, '陈启', '只有一本不能比较。')
            result = check_cross_book_similarity(root)

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['pairs'], [])

    def test_load_profile_extracts_opening_and_names(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            novel = _write_book(Path(tmpdir), '档案', SHARED_OPENING, '林青', '她把旧信折好。')
            profile = load_book_profile(novel)

        self.assertEqual(profile['name'], '档案')
        self.assertIn('林青', profile['names'])
        self.assertTrue(profile['opening'].startswith('雨夜的车站'))


if __name__ == '__main__':
    unittest.main()
