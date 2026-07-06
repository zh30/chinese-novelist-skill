#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短故事质量检查脚本
检查短故事正文是否满足 6000 字、结构完整、完稿复盘和非未完待续等红灯项。
"""

import sys
from pathlib import Path

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import count_chinese_words, setup_windows_encoding

setup_windows_encoding()


CLIMAX_TERMS = [
    '高潮', '最终', '最后一次', '终于', '选择', '决定', '摊牌',
    '真相大白', '冲突爆发', '对峙',
]

RESOLUTION_TERMS = [
    '收束', '解决', '结束', '天亮以后', '后来', '重新', '答案',
    '闭合', '归于', '尘埃落定',
]

TO_BE_CONTINUED_TERMS = [
    '未完待续', '待续', '下回', '下一章', '后续再说',
    '故事才刚刚开始', '危险才刚刚开始', '真正的危险才刚刚开始',
]


def _extract_section(content: str, heading: str) -> str:
    """提取指定二级标题下的内容。"""
    lines = content.split('\n')
    section_start = None
    section_end = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == heading:
            section_start = i + 1
            continue
        if section_start is not None and stripped.startswith('## '):
            section_end = i
            break

    if section_start is None:
        return ''

    return '\n'.join(lines[section_start:section_end]).strip()


def _has_heading(content: str, heading: str) -> bool:
    return any(line.strip() == heading for line in content.split('\n'))


def _make_check(passed: bool, message: str) -> dict:
    return {'passed': passed, 'message': message}


def check_short_story(file_path: str, min_words: int = 6000) -> dict:
    """检查单篇短故事的硬性质量项。"""
    path = Path(file_path)

    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'word_count': 0,
            'status': 'error',
            'message': f'文件不存在：{file_path}',
            'checks': {},
        }

    content = path.read_text(encoding='utf-8')
    body = _extract_section(content, '## 正文')
    word_count = count_chinese_words(body)

    has_body = bool(body.strip())
    has_review = _has_heading(content, '## 完稿复盘')
    has_climax = any(term in body for term in CLIMAX_TERMS)
    has_resolution = any(term in body for term in RESOLUTION_TERMS)
    to_be_continued_matches = [term for term in TO_BE_CONTINUED_TERMS if term in body or term in content]

    checks = {
        'body_section': _make_check(
            has_body,
            '找到 ## 正文 区块' if has_body else '缺少 ## 正文 区块或正文为空',
        ),
        'word_count': _make_check(
            word_count >= min_words,
            f'字数：{word_count}，最低要求：{min_words}',
        ),
        'completion_review': _make_check(
            has_review,
            '找到 ## 完稿复盘' if has_review else '缺少 ## 完稿复盘',
        ),
        'plot_completion': _make_check(
            has_climax and has_resolution,
            '检测到高潮与收束信号' if has_climax and has_resolution else '缺少高潮或收束信号',
        ),
        'no_to_be_continued': _make_check(
            not to_be_continued_matches,
            '未发现未完待续信号' if not to_be_continued_matches else f'发现未完待续信号：{", ".join(to_be_continued_matches)}',
        ),
    }

    status = 'pass' if all(check['passed'] for check in checks.values()) else 'fail'

    return {
        'file': str(path),
        'exists': True,
        'word_count': word_count,
        'status': status,
        'message': '短故事检查通过' if status == 'pass' else '短故事检查未通过',
        'checks': checks,
    }


def check_all_short_stories(directory: str, min_words: int = 6000) -> list:
    """检查目录下所有 Markdown 短故事文件。"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误：目录不存在 - {directory}')
        return []

    short_story_files = sorted(path for path in dir_path.glob('*.md') if path.is_file())
    return [check_short_story(str(path), min_words=min_words) for path in short_story_files]


def print_results(results: list):
    """打印短故事检查结果。"""
    if not results:
        print('没有找到短故事文件')
        return

    passed = sum(1 for result in results if result['status'] == 'pass')
    failed = sum(1 for result in results if result['status'] == 'fail')
    errors = sum(1 for result in results if result['status'] == 'error')

    print('\n' + '=' * 60)
    print('短故事质量检查报告')
    print('=' * 60)

    for result in results:
        icon = '✅' if result['status'] == 'pass' else '⚠️ ' if result['status'] == 'fail' else '❌'
        print(f'\n{icon} {Path(result["file"]).name}')
        print(f'   {result["message"]}')
        print(f'   正文字数：{result["word_count"]}')
        for check_name, check in result.get('checks', {}).items():
            check_icon = '✓' if check['passed'] else '✗'
            print(f'   {check_icon} {check_name}: {check["message"]}')

    print('\n' + '-' * 60)
    print(f'总计：{len(results)} 篇 | {passed} 篇通过 | {failed} 篇未通过 | {errors} 个错误')
    print('-' * 60)


def main():
    """主函数"""
    min_words = 6000

    if len(sys.argv) < 2:
        print('用法：')
        print('  检查单篇短故事：python scripts/check_short_story.py <短故事文件路径> [最小字数]')
        print('  批量检查短故事：python scripts/check_short_story.py --all <目录路径> [最小字数]')
        print('')
        print('示例：')
        print('  python scripts/check_short_story.py short-stories/故事标题.md')
        print('  python scripts/check_short_story.py short-stories/故事标题.md 6000')
        print('  python scripts/check_short_story.py --all short-stories')
        return

    if sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print('错误：使用 --all 时需要指定目录路径')
            return
        directory = sys.argv[2]
        min_words = int(sys.argv[3]) if len(sys.argv) > 3 else 6000
        results = check_all_short_stories(directory, min_words=min_words)
        print_results(results)
    else:
        file_path = sys.argv[1]
        min_words = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
        result = check_short_story(file_path, min_words=min_words)
        print_results([result])


if __name__ == '__main__':
    main()
