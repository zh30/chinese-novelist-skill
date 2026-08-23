#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨书同质化检测

对多本小说两两比较高频 4-gram、成语/意象词、开篇结尾句式和人名。
结果只是烟雾报警器，不能证明抄袭或文学失败。
"""

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    extract_text_from_chapter,
    find_chapter_files,
    find_novel_project_dirs,
    setup_windows_encoding,
)

setup_windows_encoding()


IMAGE_WORDS = {
    '月光', '雨夜', '灯火', '旧信', '车站', '雨巷', '茶香', '风雪',
    '海风', '山影', '城门', '夜色', '梦境', '影子', '玻璃', '钥匙',
    '照片', '烛火', '青石', '巷口', '黄昏', '黎明', '雾气', '钟声',
}

COMMON_IDIOMS = {
    '前所未有', '不以为意', '心如刀绞', '目光如炬', '意味深长',
    '若有所思', '不动声色', '恍然大悟', '怒火中烧', '泪流满面',
    '斩钉截铁', '一针见血', '咄咄逼人', '不寒而栗', '心有余悸',
}

NAME_PATTERNS = [
    re.compile(r'^#{2,3}\s*(?:主角|配角|反派|对手|关键人物)?[：:]\s*([\u4e00-\u9fff]{2,4})\s*$', re.MULTILINE),
    re.compile(r'\*\*姓名\*\*[：:]\s*([\u4e00-\u9fff]{2,4})'),
    re.compile(r'^#{2,3}\s*([\u4e00-\u9fff]{2,4})\s*$', re.MULTILINE),
]

GENERIC_NAME_BLOCKLIST = {
    '主角', '配角', '反派', '对手', '人物', '档案', '关系', '概述',
    '压力', '声音', '世界', '设定', '目录', '创作', '宪章',
}


def _chinese_only(text: str) -> str:
    return ''.join(re.findall(r'[\u4e00-\u9fff]', text))


def _ngrams(text: str, n: int = 4):
    chars = _chinese_only(text)
    if len(chars) < n:
        return []
    return [chars[i:i + n] for i in range(len(chars) - n + 1)]


def _top_ngrams(text: str, n: int = 4, limit: int = 200) -> Counter:
    return Counter(_ngrams(text, n=n)).most_common(limit)


def _jaccard(left, right) -> float:
    left_set = set(left)
    right_set = set(right)
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / len(left_set | right_set)


def _first_last_sentences(text: str):
    parts = [part.strip() for part in re.split(r'[。！？]+', text) if part.strip()]
    if not parts:
        return '', ''
    return parts[0], parts[-1]


def _extract_names(novel_dir: Path) -> set:
    names = set()
    profile = novel_dir / '01-人物档案.md'
    outline = novel_dir / '00-大纲.md'
    for path in (profile, outline):
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        for pattern in NAME_PATTERNS:
            for match in pattern.findall(text):
                if match not in GENERIC_NAME_BLOCKLIST:
                    names.add(match)
    return names


def _collect_book_text(novel_dir: Path) -> str:
    chunks = []
    for path in find_chapter_files(novel_dir):
        chunks.append(extract_text_from_chapter(path))
    return '\n'.join(chunks)


def load_book_profile(novel_dir: Path) -> dict:
    """提取一本小说用于比较的轻量特征。"""
    novel_dir = Path(novel_dir)
    chapters = find_chapter_files(novel_dir)
    text = _collect_book_text(novel_dir)
    first_body = extract_text_from_chapter(chapters[0]) if chapters else ''
    last_body = extract_text_from_chapter(chapters[-1]) if chapters else ''
    opening, _ = _first_last_sentences(first_body)
    _, ending = _first_last_sentences(last_body or first_body)
    four_grams = [gram for gram, _ in _top_ngrams(text, n=4, limit=200)]
    two_grams = [gram for gram, _ in _top_ngrams(text, n=2, limit=80)]
    idioms = {token for token in COMMON_IDIOMS if token in text}
    images = {token for token in IMAGE_WORDS if token in text}
    repeated_four = {gram for gram, count in Counter(_ngrams(text, 4)).items() if count >= 2}
    return {
        'name': novel_dir.name,
        'path': str(novel_dir),
        'word_count': len(_chinese_only(text)),
        'chapter_count': len(chapters),
        'four_grams': four_grams,
        'two_grams': two_grams,
        'idioms': idioms,
        'images': images,
        'repeated_four': repeated_four,
        'opening': opening,
        'ending': ending,
        'names': _extract_names(novel_dir),
    }


def compare_books(left: dict, right: dict) -> dict:
    """比较两本书并给出烟雾报警级别。"""
    shared_four = set(left['four_grams']) & set(right['four_grams'])
    four_jaccard = _jaccard(left['four_grams'], right['four_grams'])
    opening_jaccard = _jaccard(_ngrams(left['opening'], 2), _ngrams(right['opening'], 2))
    ending_jaccard = _jaccard(_ngrams(left['ending'], 2), _ngrams(right['ending'], 2))
    shared_idioms = sorted((left['idioms'] | left['repeated_four']) & (right['idioms'] | right['repeated_four']))
    shared_images = sorted(left['images'] & right['images'])
    shared_names = sorted(left['names'] & right['names'])
    opening_same = bool(left['opening'] and left['opening'] == right['opening'])

    warnings = []
    severity = 'low'
    if opening_same or four_jaccard >= 0.25:
        severity = 'high'
    elif four_jaccard >= 0.12 or opening_jaccard >= 0.4 or len(shared_names) >= 2:
        severity = 'medium'
    elif shared_names or shared_images or four_jaccard >= 0.05:
        severity = 'low'

    if four_jaccard >= 0.12:
        warnings.append(f'高频4-gram重合 {four_jaccard:.2f}（{len(shared_four)} 个）')
    if opening_same:
        warnings.append('开篇首句完全相同')
    elif opening_jaccard >= 0.4:
        warnings.append(f'开篇句式相近 {opening_jaccard:.2f}')
    if ending_jaccard >= 0.4:
        warnings.append(f'结尾句式相近 {ending_jaccard:.2f}')
    if shared_names:
        warnings.append('人名撞车：' + '、'.join(shared_names))
    if len(shared_images) >= 3:
        warnings.append('意象词重合：' + '、'.join(shared_images[:8]))
    if len(shared_idioms) >= 8:
        warnings.append(f'成语/四字块重合 {len(shared_idioms)} 个')

    if severity == 'low' and not warnings:
        status = 'pass'
    else:
        status = 'warn'

    return {
        'left': left['name'],
        'right': right['name'],
        'status': status,
        'severity': severity if warnings else 'none',
        'four_gram_jaccard': round(four_jaccard, 3),
        'opening_jaccard': round(opening_jaccard, 3),
        'ending_jaccard': round(ending_jaccard, 3),
        'shared_four_count': len(shared_four),
        'shared_names': shared_names,
        'shared_images': shared_images,
        'shared_idioms_count': len(shared_idioms),
        'warnings': warnings,
    }


def check_cross_book_similarity(root) -> dict:
    """扫描目录下的小说项目并两两比较。"""
    root_path = Path(root)
    if not root_path.exists():
        return {
            'root': str(root_path),
            'exists': False,
            'status': 'error',
            'message': f'目录不存在：{root}',
            'books': [],
            'pairs': [],
        }

    novel_dirs = find_novel_project_dirs(root_path)
    books = [load_book_profile(path) for path in novel_dirs]
    pairs = []
    for i, left in enumerate(books):
        for right in books[i + 1:]:
            pairs.append(compare_books(left, right))

    if len(books) < 2:
        status = 'error'
        message = '至少需要两本小说才能比较'
    elif any(pair['severity'] == 'high' for pair in pairs):
        status = 'warn'
        message = '发现高重合信号，需人工复核'
    elif any(pair['status'] == 'warn' for pair in pairs):
        status = 'warn'
        message = '发现同质化线索，需人工复核'
    else:
        status = 'pass'
        message = '未发现明显跨书重合信号'

    return {
        'root': str(root_path),
        'exists': True,
        'status': status,
        'message': message,
        'books': [{'name': book['name'], 'chapters': book['chapter_count'], 'words': book['word_count']} for book in books],
        'pairs': pairs,
    }


def print_report(result: dict):
    print('\n' + '=' * 60)
    print('跨书同质化检测报告')
    print('=' * 60)
    print('说明：本脚本只提示重合线索，不判断抄袭、作者身份或文学质量。')
    print(f'\n{result["message"]}')

    if result.get('books'):
        print('\n书目：')
        for book in result['books']:
            print(f'  - {book["name"]}（{book["chapters"]} 章 / {book["words"]} 字）')

    if not result.get('pairs'):
        print('\n没有可比较的书籍对。')
        return

    for pair in result['pairs']:
        print(f'\n[{pair["severity"]}] {pair["left"]} vs {pair["right"]}')
        print(f'   4-gram Jaccard: {pair["four_gram_jaccard"]}')
        print(f'   开篇/结尾句式: {pair["opening_jaccard"]} / {pair["ending_jaccard"]}')
        if pair['shared_names']:
            print(f'   人名：{"、".join(pair["shared_names"])}')
        for warning in pair['warnings']:
            print(f'   ! {warning}')


def _parse_roots(argv):
    if not argv:
        return None
    if len(argv) == 1:
        return argv[0]
    return argv


def check_multiple_roots(roots) -> dict:
    if isinstance(roots, (str, Path)):
        return check_cross_book_similarity(roots)

    novel_dirs = []
    seen = set()
    for root in roots:
        for path in find_novel_project_dirs(Path(root)):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            novel_dirs.append(path)

    profiles = [load_book_profile(path) for path in novel_dirs]
    pairs = []
    for i, left in enumerate(profiles):
        for right in profiles[i + 1:]:
            pairs.append(compare_books(left, right))

    if len(profiles) < 2:
        status, message = 'error', '至少需要两本小说才能比较'
    elif any(pair['severity'] == 'high' for pair in pairs):
        status, message = 'warn', '发现高重合信号，需人工复核'
    elif any(pair['status'] == 'warn' for pair in pairs):
        status, message = 'warn', '发现同质化线索，需人工复核'
    else:
        status, message = 'pass', '未发现明显跨书重合信号'

    return {
        'root': ', '.join(str(item) for item in roots),
        'exists': True,
        'status': status,
        'message': message,
        'books': [{'name': book['name'], 'chapters': book['chapter_count'], 'words': book['word_count']} for book in profiles],
        'pairs': pairs,
    }


def main():
    if len(sys.argv) < 2:
        print('用法：')
        print('  python3 scripts/check_cross_book_similarity.py novels')
        print('  python3 scripts/check_cross_book_similarity.py novels/书A novels/书B')
        return 2

    roots = sys.argv[1:]
    if len(roots) == 1:
        result = check_cross_book_similarity(roots[0])
    else:
        result = check_multiple_roots(roots)

    print_report(result)
    if result['status'] == 'error':
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
