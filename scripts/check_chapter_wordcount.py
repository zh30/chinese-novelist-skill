#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节 / 短故事字数检查脚本
默认报告字数，不因低于习惯值失败。工厂模式使用 --strict-min 才把下限当成失败。
"""

import sys
from pathlib import Path

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, count_chinese_words, find_chapter_files, setup_windows_encoding

setup_windows_encoding()

# Backward compatibility alias for existing tests
extract_content_from_chapter = extract_text_from_chapter


def check_chapter(file_path: str, min_words: int = 3000, strict: bool = False) -> dict:
    """检查单个正文文件的字数。默认只报告；strict=True 时低于 min_words 失败。"""
    path = Path(file_path)

    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'word_count': 0,
            'status': 'error',
            'message': f'文件不存在：{file_path}'
        }

    main_content = extract_text_from_chapter(path)
    word_count = count_chinese_words(main_content)
    under = word_count < min_words
    if strict and under:
        status = 'fail'
        message = f'字数：{word_count} (✗ 不足，需要至少 {min_words} 字)'
    elif under:
        status = 'pass'
        message = f'字数：{word_count}（习惯参考 {min_words}，非验收失败）'
    else:
        status = 'pass'
        message = f'字数：{word_count}'

    return {
        'file': str(path),
        'exists': True,
        'word_count': word_count,
        'status': status,
        'message': message
    }


def check_all_chapters(directory: str, min_words: int = 3000, strict: bool = False) -> list:
    """检查目录下所有符合模式的章节文件"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误：目录不存在 - {directory}')
        return []

    chapter_files = find_chapter_files(dir_path)
    results = []

    for chapter_file in chapter_files:
        result = check_chapter(str(chapter_file), min_words, strict=strict)
        results.append(result)

    return results


def print_results(results: list, min_words: int = 3000):
    """打印检查结果"""
    if not results:
        print('没有找到章节文件')
        return

    total_words = 0
    passed = 0
    failed = 0

    print('\n' + '=' * 60)
    print('章节 / 短故事字数检查报告')
    print('=' * 60)

    for result in results:
        if not result['exists']:
            print(f'\n❌ {result["file"]}')
            print(f'   {result["message"]}')
            continue

        total_words += result['word_count']
        if result['status'] == 'pass':
            passed += 1
            icon = '✅'
        else:
            failed += 1
            icon = '⚠️ '

        print(f'\n{icon} {Path(result["file"]).name}')
        print(f'   {result["message"]}')

    print('\n' + '-' * 60)
    print(f'总计：{len(results)} 个文件 | {passed} 个达标 | {failed} 个不足 | 总字数：{total_words:,}')
    print('-' * 60)

    if failed > 0:
        print(f'\n⚠️  有 {failed} 章低于 strict 下限 {min_words} 字。加长只允许增加新的策略失败，不要重复确认已知信息。')


def _parse_args(argv):
    strict = False
    min_words = 3000
    args = list(argv)
    if '--strict-min' in args:
        idx = args.index('--strict-min')
        if idx + 1 >= len(args) or not args[idx + 1].isdigit():
            print('错误：--strict-min 需要一个整数')
            return None
        min_words = int(args[idx + 1])
        strict = True
        del args[idx:idx + 2]
    return args, min_words, strict


def main():
    """主函数。默认退出码 0；--strict-min 时低于下限返回 1。"""
    parsed = _parse_args(sys.argv[1:])
    if parsed is None:
        return 2
    args, min_words, strict = parsed

    if not args:
        print('用法：')
        print('  python scripts/check_chapter_wordcount.py <文件路径>')
        print('  python scripts/check_chapter_wordcount.py --all <目录路径>')
        print('  python scripts/check_chapter_wordcount.py <文件路径> --strict-min 3000')
        return 2

    if args[0] == '--all':
        if len(args) < 2:
            print('错误：使用 --all 时需要指定目录路径')
            return 2
        if not strict and len(args) > 2 and args[2].isdigit():
            min_words = int(args[2])
        results = check_all_chapters(args[1], min_words=min_words, strict=strict)
        print_results(results, min_words)
    else:
        if not strict and len(args) > 1 and args[1].isdigit():
            min_words = int(args[1])
        results = [check_chapter(args[0], min_words, strict=strict)]
        print_results(results, min_words)

    if any(result['status'] == 'fail' for result in results if result.get('exists')):
        return 1
    if any(not result.get('exists', True) or result.get('status') == 'error' for result in results):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
