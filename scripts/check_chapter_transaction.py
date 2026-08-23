#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节事务验收脚本

验收一章是否真正完成：正文存在且达字数、review.md 必填区块非空、
仪表盘滚动前情摘要含本章条目。结果只证明事务完整性，不证明文学质量。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    count_chinese_words,
    extract_labeled_value,
    extract_markdown_section,
    extract_text_from_chapter,
    find_chapter_files,
    find_chapter_workspace,
    find_progress_dashboard,
    is_placeholder,
    parse_chapter_number,
    setup_windows_encoding,
)

setup_windows_encoding()


REVIEW_FIELDS = {
    '摘要': ['三句以内摘要', '本章摘要', '摘要'],
    '选择与代价': ['最重要的选择与后果', '选择与代价', '选择与后果'],
    '状态回写': ['下一章必然由什么结果引发', '状态回写', '关系变化的可观察证据'],
}


def _make_check(passed: bool, message: str) -> dict:
    return {'passed': passed, 'message': message}


def _find_chapter_file(novel_dir: Path, chapter_num: int):
    for path in find_chapter_files(novel_dir):
        if parse_chapter_number(path.name) == chapter_num:
            return path
    return None


def _review_field_check(review_text: str, labels) -> dict:
    value = extract_labeled_value(review_text, labels)
    if is_placeholder(value):
        return _make_check(False, f'缺少非空字段：{labels[0]}')
    return _make_check(True, f'{labels[0]}已填写')


def _dashboard_has_chapter(dashboard_text: str, chapter_num: int) -> bool:
    summary = extract_markdown_section(dashboard_text, '## 滚动前情摘要')
    haystack = summary or dashboard_text
    tokens = (
        f'第{chapter_num:03d}章',
        f'第{chapter_num:02d}章',
        f'第{chapter_num}章',
    )
    return any(token in haystack for token in tokens)


def check_chapter_transaction(novel_dir, chapter, min_words: int = 3000) -> dict:
    """验收指定章节的事务完整性。"""
    novel_path = Path(novel_dir)
    chapter_num = parse_chapter_number(chapter)

    if not novel_path.exists():
        return {
            'novel': str(novel_path),
            'chapter': chapter_num,
            'exists': False,
            'status': 'error',
            'message': f'小说目录不存在：{novel_dir}',
            'word_count': 0,
            'checks': {},
        }

    chapter_file = Path(chapter) if Path(str(chapter)).is_file() else _find_chapter_file(novel_path, chapter_num)
    if chapter_file:
        chapter_num = parse_chapter_number(chapter_file.name) or chapter_num

    workspace = find_chapter_workspace(novel_path, chapter_num)
    review_path = (workspace / 'review.md') if workspace else None
    dashboard_path = find_progress_dashboard(novel_path)

    checks = {}

    if not chapter_file or not chapter_file.exists():
        checks['manuscript'] = _make_check(False, f'未找到第{chapter_num}章正文')
        word_count = 0
    else:
        body = extract_text_from_chapter(chapter_file)
        word_count = count_chinese_words(body)
        checks['manuscript'] = _make_check(True, f'正文：{chapter_file.name}')
        checks['word_count'] = _make_check(
            word_count >= min_words,
            f'字数：{word_count}，最低要求：{min_words}',
        )

    if not review_path or not review_path.exists():
        checks['review_file'] = _make_check(False, '缺少 workspace/chapters/第N章*/review.md')
        review_text = ''
    else:
        checks['review_file'] = _make_check(True, f'复盘：{review_path}')
        review_text = review_path.read_text(encoding='utf-8')

    for key, labels in REVIEW_FIELDS.items():
        checks[key] = _review_field_check(review_text, labels)

    if not dashboard_path.exists():
        checks['dashboard'] = _make_check(False, f'缺少 {dashboard_path.name}')
        checks['rolling_summary'] = _make_check(False, '仪表盘不存在，无法核对滚动前情摘要')
    else:
        dashboard_text = dashboard_path.read_text(encoding='utf-8')
        checks['dashboard'] = _make_check(True, dashboard_path.name)
        has_summary_heading = '## 滚动前情摘要' in dashboard_text
        has_chapter_line = _dashboard_has_chapter(dashboard_text, chapter_num)
        if has_summary_heading and has_chapter_line:
            checks['rolling_summary'] = _make_check(True, f'滚动前情摘要含第{chapter_num}章')
        elif not has_summary_heading:
            checks['rolling_summary'] = _make_check(False, '仪表盘缺少“## 滚动前情摘要”')
        else:
            checks['rolling_summary'] = _make_check(False, f'滚动前情摘要未记录第{chapter_num}章')

    status = 'pass' if all(check['passed'] for check in checks.values()) else 'fail'
    return {
        'novel': str(novel_path),
        'chapter': chapter_num,
        'chapter_file': str(chapter_file) if chapter_file else '',
        'exists': True,
        'status': status,
        'message': '章节事务验收通过' if status == 'pass' else '章节事务验收未通过',
        'word_count': word_count,
        'checks': checks,
    }


def check_all_chapter_transactions(novel_dir, min_words: int = 3000) -> list:
    """验收目录下全部已发现章节。"""
    novel_path = Path(novel_dir)
    if not novel_path.exists():
        print(f'错误：目录不存在 - {novel_dir}')
        return []

    chapter_files = find_chapter_files(novel_path)
    if not chapter_files:
        return [check_chapter_transaction(novel_path, 1, min_words=min_words)]
    return [
        check_chapter_transaction(novel_path, path, min_words=min_words)
        for path in chapter_files
    ]


def print_results(results: list):
    """打印事务验收结果。"""
    if not results:
        print('没有可验收的章节事务')
        return

    print('\n' + '=' * 60)
    print('章节事务验收报告')
    print('=' * 60)
    print('说明：本脚本只验证正文、复盘必填项和仪表盘回写是否落盘，不判断文学质量。')

    passed = failed = errors = 0
    for result in results:
        if result['status'] == 'pass':
            passed += 1
            icon = 'OK'
        elif result['status'] == 'error':
            errors += 1
            icon = 'ERROR'
        else:
            failed += 1
            icon = 'FAIL'
        print(f'\n[{icon}] 第{result["chapter"]}章  {result["message"]}')
        print(f'   正文字数：{result["word_count"]}')
        for name, check in result.get('checks', {}).items():
            mark = 'Y' if check['passed'] else 'N'
            print(f'   [{mark}] {name}: {check["message"]}')

    print('\n' + '-' * 60)
    print(f'总计：{len(results)} 章 | {passed} 通过 | {failed} 未通过 | {errors} 错误')
    print('-' * 60)


def main():
    if len(sys.argv) < 2:
        print('用法：')
        print('  python3 scripts/check_chapter_transaction.py <小说目录> <章节号> [最小字数]')
        print('  python3 scripts/check_chapter_transaction.py <小说目录> --all [最小字数]')
        print('  python3 scripts/check_chapter_transaction.py <小说目录> --fast <章节号>')
        print('')
        print('示例：')
        print('  python3 scripts/check_chapter_transaction.py novels/书名 1')
        print('  python3 scripts/check_chapter_transaction.py novels/书名 --all')
        print('  python3 scripts/check_chapter_transaction.py novels/书名 --fast 3')
        return 2

    novel_dir = sys.argv[1]
    min_words = 3000
    args = sys.argv[2:]

    if '--fast' in args:
        min_words = 2500
        args = [arg for arg in args if arg != '--fast']

    if args and args[0] == '--all':
        if len(args) > 1 and args[1].isdigit():
            min_words = int(args[1])
        results = check_all_chapter_transactions(novel_dir, min_words=min_words)
    else:
        if not args:
            print('错误：请提供章节号，或使用 --all')
            return 2
        chapter = args[0]
        if len(args) > 1 and args[1].isdigit():
            min_words = int(args[1])
        results = [check_chapter_transaction(novel_dir, chapter, min_words=min_words)]

    print_results(results)
    if any(result['status'] != 'pass' for result in results):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
