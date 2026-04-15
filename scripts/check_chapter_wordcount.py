#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节字数检查脚本
检查指定章节文件的字数，低于 3000 字时提示需要扩充
"""

import sys
from pathlib import Path

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, count_chinese_words, find_chapter_files, setup_windows_encoding

setup_windows_encoding()

# Backward compatibility alias for existing tests
extract_content_from_chapter = extract_text_from_chapter


def check_chapter(file_path: str, min_words: int = 3000) -> dict:
    """检查单个章节的字数"""
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

    status = 'pass' if word_count >= min_words else 'fail'
    message = f'字数：{word_count}' + (
        f' (✓ 达标)' if word_count >= min_words else f' (✗ 不足，需要至少 {min_words} 字)'
    )

    return {
        'file': str(path),
        'exists': True,
        'word_count': word_count,
        'status': status,
        'message': message
    }


def check_all_chapters(directory: str, min_words: int = 3000) -> list:
    """检查目录下所有符合模式的章节文件"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误：目录不存在 - {directory}')
        return []

    chapter_files = find_chapter_files(dir_path)
    results = []

    for chapter_file in chapter_files:
        result = check_chapter(str(chapter_file), min_words)
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
    print('章节字数检查报告')
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
    print(f'总计：{len(results)} 章 | {passed} 章达标 | {failed} 章不足 | 总字数：{total_words:,}')
    print('-' * 60)

    if failed > 0:
        print(f'\n⚠️  有 {failed} 章内容不足 {min_words} 字，建议使用扩充技巧：')
        print('   - 添加细节描写（环境、心理、动作）')
        print('   - 增加对话场景')
        print('   - 扩展人物内心活动')
        print('   - 补充背景故事')
        print(f'\n   参考：references/content-expansion.md')


def main():
    """主函数"""
    min_words = 3000

    if len(sys.argv) < 2:
        print('用法：')
        print('  检查单个章节：python scripts/check_chapter_wordcount.py <章节文件路径> [最小字数]')
        print('  检查所有章节：python scripts/check_chapter_wordcount.py --all <目录路径> [最小字数]')
        print('')
        print('示例：')
        print('  python scripts/check_chapter_wordcount.py novels/故事/第01章.md')
        print('  python scripts/check_chapter_wordcount.py novels/故事/第01章.md 3500')
        print('  python scripts/check_chapter_wordcount.py --all novels/故事')
        print('  python scripts/check_chapter_wordcount.py --all novels/故事 3500')
        return

    if sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print('错误：使用 --all 时需要指定目录路径')
            return
        directory = sys.argv[2]
        min_words = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
        results = check_all_chapters(directory, min_words=min_words)
        print_results(results, min_words)
    else:
        file_path = sys.argv[1]
        min_words = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
        result = check_chapter(file_path, min_words)
        print_results([result], min_words)


if __name__ == '__main__':
    main()
