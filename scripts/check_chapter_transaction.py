#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节事务验收脚本

验收一章是否真正完成。作者模式：正文、隔离盲读复述、感知包、复盘、仪表盘。
工厂模式：可启用字数下限，盲读改为抽检。结果只证明事务完整性，不证明文学质量。
"""

from __future__ import annotations

import re
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


AUTHOR_MODE = 'author'
FACTORY_MODE = 'factory'
FACTORY_DEFAULT_MIN = 3000
FACTORY_FAST_MIN = 2500
SOFT_WORD_CEILING = 8000
WEAK_RESTATEMENT_RE = re.compile(r'^(变化|推进|升级)+$')
ABSTRACT_ONLY_RE = re.compile(r'^(真相|爱情|尊严|命运|希望|恐惧)+$')

REVIEW_FIELDS = {
    '摘要': ['三句以内摘要', '本章摘要', '摘要'],
    '选择与代价': ['最重要的选择与后果', '选择与代价', '选择与后果'],
    '状态回写': ['下一章必然由什么结果引发', '状态回写', '关系变化的可观察证据'],
}

BLIND_READ_FIELDS = {
    '盲读人物印象': ['我以为自己在读一个怎样的人'],
    '盲读走神': ['走神起点'],
    '盲读缺口': ['我最想知道而文本没给的'],
    '不可逆变化': ['不可逆变化（读者复述）', '不可逆变化'],
}

PERCEPTION_REQUIRED = (
    '进门第一眼',
    '以为对方要什么',
    '绝不会说出口的半句',
)


def _make_check(passed: bool, message: str) -> dict:
    return {'passed': passed, 'message': message}


def detect_writing_mode(dashboard_text: str) -> str:
    """从仪表盘读取写作模式；缺省为作者。

    识别：
    - 表格 ``| 写作模式 | 工厂 |``（未填的 ``作者 / 工厂`` 仍算作者）
    - 字段 ``- **写作模式**：工厂`` 或 ``写作模式：工厂``
    """
    if not dashboard_text:
        return AUTHOR_MODE
    table = re.search(r'\|\s*写作模式\s*\|\s*([^|]+)\|', dashboard_text)
    if table:
        value = table.group(1).strip()
        if value == '工厂':
            return FACTORY_MODE
    if re.search(r'写作模式\*{0,2}\s*[：:]\s*工厂', dashboard_text):
        return FACTORY_MODE
    return AUTHOR_MODE


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


def _chinese_len(value: str) -> int:
    return len(re.findall(r'[\u4e00-\u9fff]', value or ''))


def _is_weak_restatement(value: str) -> bool:
    if is_placeholder(value):
        return True
    stripped = value.strip()
    if stripped == '复述不出':
        return True
    compact = re.sub(r'[\s，。、；：,.！？!?]+', '', stripped)
    if WEAK_RESTATEMENT_RE.fullmatch(compact):
        return True
    if _chinese_len(stripped) < 8:
        return True
    return False


def _check_blind_read(workspace: Path | None, required: bool) -> dict:
    checks = {}
    if workspace is None:
        if required:
            checks['blind_read_file'] = _make_check(False, '缺少章节工作台，无法读取 blind-read.md')
        return checks

    path = workspace / 'blind-read.md'
    if not path.exists():
        if required:
            checks['blind_read_file'] = _make_check(False, '缺少 workspace/chapters/第N章*/blind-read.md')
        return checks

    text = path.read_text(encoding='utf-8')
    checks['blind_read_file'] = _make_check(True, f'盲读：{path}')
    for key, labels in BLIND_READ_FIELDS.items():
        value = extract_labeled_value(text, labels)
        if key == '不可逆变化':
            if _is_weak_restatement(value):
                checks['irreversible_change'] = _make_check(
                    False,
                    '不可逆变化（读者复述）为空、占位、复述不出，或只含变化/推进/升级',
                )
            else:
                checks['irreversible_change'] = _make_check(True, '不可逆变化已由读者复述')
        elif is_placeholder(value):
            checks[key] = _make_check(False, f'缺少非空字段：{labels[0]}')
        else:
            checks[key] = _make_check(True, f'{labels[0]}已填写')
    return checks


def _check_perception(workspace: Path | None, required: bool) -> dict:
    checks = {}
    if not required:
        return checks
    if workspace is None:
        checks['perception_file'] = _make_check(False, '缺少章节工作台，无法读取 perception.md')
        return checks

    path = workspace / 'perception.md'
    if not path.exists():
        checks['perception_file'] = _make_check(False, '缺少 workspace/chapters/第N章*/perception.md')
        return checks

    text = path.read_text(encoding='utf-8')
    checks['perception_file'] = _make_check(True, f'感知包：{path}')
    for label in PERCEPTION_REQUIRED:
        value = extract_labeled_value(text, [label])
        compact = re.sub(r'[\s，。、；：,.]+', '', value or '')
        if is_placeholder(value) or ABSTRACT_ONLY_RE.fullmatch(compact):
            checks[f'感知-{label}'] = _make_check(False, f'感知包缺少可拍摄内容：{label}')
        else:
            checks[f'感知-{label}'] = _make_check(True, f'{label}已填写')
    return checks


def check_chapter_transaction(
    novel_dir,
    chapter,
    min_words: int | None = None,
    mode: str | None = None,
    factory: bool = False,
) -> dict:
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
            'mode': FACTORY_MODE if factory else AUTHOR_MODE,
            'checks': {},
        }

    chapter_file = Path(chapter) if Path(str(chapter)).is_file() else _find_chapter_file(novel_path, chapter_num)
    if chapter_file:
        chapter_num = parse_chapter_number(chapter_file.name) or chapter_num

    workspace = find_chapter_workspace(novel_path, chapter_num)
    review_path = (workspace / 'review.md') if workspace else None
    dashboard_path = find_progress_dashboard(novel_path)
    dashboard_text = dashboard_path.read_text(encoding='utf-8') if dashboard_path.exists() else ''

    resolved_mode = FACTORY_MODE if factory else (mode or detect_writing_mode(dashboard_text))
    enforce_min = resolved_mode == FACTORY_MODE
    word_floor = FACTORY_DEFAULT_MIN if min_words is None else min_words
    require_blind = resolved_mode == AUTHOR_MODE
    require_perception = resolved_mode == AUTHOR_MODE

    checks = {}
    word_count = 0

    if not chapter_file or not chapter_file.exists():
        checks['manuscript'] = _make_check(False, f'未找到第{chapter_num}章正文')
    else:
        body = extract_text_from_chapter(chapter_file)
        word_count = count_chinese_words(body)
        checks['manuscript'] = _make_check(True, f'正文：{chapter_file.name}')
        if enforce_min:
            checks['word_count'] = _make_check(
                word_count >= word_floor,
                f'字数：{word_count}，最低要求：{word_floor}',
            )
        else:
            note = f'字数：{word_count}'
            if word_count > SOFT_WORD_CEILING:
                note += f'（超过软上限 {SOFT_WORD_CEILING}，不失败）'
            checks['word_count_report'] = _make_check(True, note)

    if not review_path or not review_path.exists():
        checks['review_file'] = _make_check(False, '缺少 workspace/chapters/第N章*/review.md')
        review_text = ''
    else:
        checks['review_file'] = _make_check(True, f'复盘：{review_path}')
        review_text = review_path.read_text(encoding='utf-8')

    for key, labels in REVIEW_FIELDS.items():
        checks[key] = _review_field_check(review_text, labels)

    if require_blind and review_text:
        has_pointer = '盲读指出' in review_text and '正文改动' in review_text
        checks['review_blind_followup'] = _make_check(
            has_pointer,
            '复盘已引用盲读指出与正文改动' if has_pointer else '复盘缺少「盲读指出 / 正文改动」',
        )

    checks.update(_check_blind_read(workspace, required=require_blind))
    checks.update(_check_perception(workspace, required=require_perception))

    if not dashboard_path.exists():
        checks['dashboard'] = _make_check(False, f'缺少 {dashboard_path.name}')
        checks['rolling_summary'] = _make_check(False, '仪表盘不存在，无法核对滚动前情摘要')
    else:
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
        'mode': resolved_mode,
        'message': '章节事务验收通过' if status == 'pass' else '章节事务验收未通过',
        'word_count': word_count,
        'checks': checks,
    }


def check_all_chapter_transactions(
    novel_dir,
    min_words: int | None = None,
    factory: bool = False,
) -> list:
    """验收目录下全部已发现章节。"""
    novel_path = Path(novel_dir)
    if not novel_path.exists():
        print(f'错误：目录不存在 - {novel_dir}')
        return []

    chapter_files = find_chapter_files(novel_path)
    if not chapter_files:
        return [check_chapter_transaction(novel_path, 1, min_words=min_words, factory=factory)]
    return [
        check_chapter_transaction(novel_path, path, min_words=min_words, factory=factory)
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
    print('说明：本脚本只验证正文、盲读复述、感知包、复盘和仪表盘回写是否落盘，不判断文学质量。')

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
        print(f'   模式：{result.get("mode", AUTHOR_MODE)}')
        for name, check in result.get('checks', {}).items():
            mark = 'Y' if check['passed'] else 'N'
            print(f'   [{mark}] {name}: {check["message"]}')

    print('\n' + '-' * 60)
    print(f'总计：{len(results)} 章 | {passed} 通过 | {failed} 未通过 | {errors} 错误')
    print('-' * 60)


def main() -> int:
    if len(sys.argv) < 2:
        print('用法：')
        print('  python3 scripts/check_chapter_transaction.py <小说目录> <章节号>')
        print('  python3 scripts/check_chapter_transaction.py <小说目录> --all')
        print('  python3 scripts/check_chapter_transaction.py <小说目录> --factory <章节号>')
        print('  python3 scripts/check_chapter_transaction.py <小说目录> --fast <章节号>')
        print('')
        print('示例：')
        print('  python3 scripts/check_chapter_transaction.py novels/书名 1')
        print('  python3 scripts/check_chapter_transaction.py novels/书名 --all')
        print('  python3 scripts/check_chapter_transaction.py novels/书名 --factory 3')
        return 2

    novel_dir = sys.argv[1]
    args = sys.argv[2:]
    factory = '--factory' in args or '--fast' in args
    fast = '--fast' in args
    args = [arg for arg in args if arg not in ('--factory', '--fast')]
    min_words = FACTORY_FAST_MIN if fast else (FACTORY_DEFAULT_MIN if factory else None)

    if args and args[0] == '--all':
        if len(args) > 1 and args[1].isdigit():
            min_words = int(args[1])
            factory = True
        results = check_all_chapter_transactions(novel_dir, min_words=min_words, factory=factory)
    else:
        if not args:
            print('错误：请提供章节号，或使用 --all')
            return 2
        chapter = args[0]
        if len(args) > 1 and args[1].isdigit():
            min_words = int(args[1])
            factory = True
        results = [check_chapter_transaction(novel_dir, chapter, min_words=min_words, factory=factory)]

    print_results(results)
    if any(result['status'] != 'pass' for result in results):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
