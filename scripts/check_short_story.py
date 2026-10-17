#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短故事质量检查脚本

检查正文区、完稿复盘、未完待续，以及盲读复述和引文是否对得上正文。
不把「终于 / 后来 / 收束」当作通过条件。6000 字是习惯参考；--strict-min 才把字数当下限失败。
引文对得上不能证明盲读来自另一次隔离调用。
"""

import sys
from pathlib import Path

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_chapter_transaction import assess_blind_read_text
from utils import count_chinese_words, setup_windows_encoding

setup_windows_encoding()


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


def _drop_sections(content: str, headings: set) -> str:
    """去掉指定二级标题及其正文，留下任务卡等计划文本。"""
    kept = []
    skipping = False
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('## '):
            skipping = stripped in headings
            if skipping:
                continue
        if skipping:
            continue
        kept.append(line)
    return '\n'.join(kept)


def _load_blind_read(content: str, path: Path):
    """优先读同目录 blind-read.md；否则读故事文件里的 ## 盲读。"""
    sidecar = path.parent / 'blind-read.md'
    if sidecar.is_file() and sidecar.resolve() != path.resolve():
        return sidecar.read_text(encoding='utf-8'), f'盲读：{sidecar.name}'
    section = _extract_section(content, '## 盲读')
    if section:
        return section, '盲读在故事文件的 ## 盲读'
    return '', ''


def check_short_story(file_path: str, min_words: int = 6000, strict: bool = False) -> dict:
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
    to_be_continued_matches = [term for term in TO_BE_CONTINUED_TERMS if term in body or term in content]
    blind_text, blind_where = _load_blind_read(content, path)
    plan_text = _drop_sections(content, {'## 正文', '## 盲读'})

    checks = {
        'body_section': _make_check(
            has_body,
            '找到 ## 正文 区块' if has_body else '缺少 ## 正文 区块或正文为空',
        ),
        'word_count': _make_check(
            (not strict) or word_count >= min_words,
            f'字数：{word_count}，习惯参考：{min_words}'
            if not strict
            else f'字数：{word_count}，最低要求：{min_words}',
        ),
        'completion_review': _make_check(
            has_review,
            '找到 ## 完稿复盘' if has_review else '缺少 ## 完稿复盘',
        ),
        'no_to_be_continued': _make_check(
            not to_be_continued_matches,
            '未发现未完待续信号' if not to_be_continued_matches else f'发现未完待续信号：{", ".join(to_be_continued_matches)}',
        ),
    }
    if not blind_text:
        checks['blind_read'] = _make_check(False, '缺少同目录 blind-read.md 或 ## 盲读')
    else:
        checks['blind_read'] = _make_check(True, blind_where)
        checks.update(assess_blind_read_text(blind_text, body, plan_text))

    status = 'pass' if all(check['passed'] for check in checks.values()) else 'fail'

    return {
        'file': str(path),
        'exists': True,
        'word_count': word_count,
        'status': status,
        'message': '短故事检查通过' if status == 'pass' else '短故事检查未通过',
        'checks': checks,
    }


def check_all_short_stories(directory: str, min_words: int = 6000, strict: bool = False) -> list:
    """检查目录下所有 Markdown 短故事文件。"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误：目录不存在 - {directory}')
        return []

    short_story_files = sorted(path for path in dir_path.glob('*.md') if path.is_file())
    return [check_short_story(str(path), min_words=min_words, strict=strict) for path in short_story_files]


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
    print('说明：正文、复盘、未完待续和盲读复述是硬项。引文必须在正文里，复述不得只存在于任务卡。字数默认只报告。这不能证明隔离调用已经发生。')

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


def main() -> int:
    """主函数。默认不因字数失败；--strict-min 时低于下限返回 1。"""
    args = list(sys.argv[1:])
    strict = False
    min_words = 6000
    if '--strict-min' in args:
        idx = args.index('--strict-min')
        if idx + 1 >= len(args) or not args[idx + 1].isdigit():
            print('错误：--strict-min 需要一个整数')
            return 2
        min_words = int(args[idx + 1])
        strict = True
        del args[idx:idx + 2]

    if not args:
        print('用法：')
        print('  python scripts/check_short_story.py <短故事文件路径>')
        print('  python scripts/check_short_story.py --all <目录路径>')
        print('  python scripts/check_short_story.py <短故事文件路径> --strict-min 6000')
        return 2

    if args[0] == '--all':
        if len(args) < 2:
            print('错误：使用 --all 时需要指定目录路径')
            return 2
        if not strict and len(args) > 2 and args[2].isdigit():
            min_words = int(args[2])
        results = check_all_short_stories(args[1], min_words=min_words, strict=strict)
    else:
        if not strict and len(args) > 1 and args[1].isdigit():
            min_words = int(args[1])
        results = [check_short_story(args[0], min_words=min_words, strict=strict)]

    print_results(results)
    if any(result['status'] != 'pass' for result in results):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
