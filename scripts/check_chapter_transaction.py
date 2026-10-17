#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节事务验收脚本

验收一章是否真正完成。作者模式：正文、盲读复述、引文在正文中、
复述不抄计划、禁止句不原样复发、感知包、复盘、仪表盘。
工厂模式：可启用字数下限；第 5、10、15… 章与作者模式同样要求盲读，
其余章缺少盲读时必须标注「未隔离」。
引文和计划片段对得上，只说明盲读文本与正文一致，不能证明换过上下文。
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

QUOTE_FIELDS = (
    ('走神起点', ('走神起点',)),
    ('作者腔', ('听起来像作者、不像人物的句子',)),
)
PLAN_SPAN = 8
FACTORY_SAMPLE_EVERY = 5
VOICE_LOCK_FILENAME = '05-声音锁.md'
PLAN_FILENAMES = ('perception.md', 'task-card.md', 'scene-plan.md')
ABSENT_QUOTE_RE = re.compile(r'^(无|没有|无走神)$')
QUOTE_PATTERNS = (
    re.compile(r'「([^」]+)」'),
    re.compile(r'“([^”]+)”'),
    re.compile(r'"([^"]+)"'),
    re.compile(r'『([^』]+)』'),
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


def _chinese_compact(value: str) -> str:
    return ''.join(re.findall(r'[\u4e00-\u9fff]', value or ''))


def _is_absent_quote(value: str) -> bool:
    compact = re.sub(r'[\s，。、；：,.！？!?「」“”"『』]+', '', value or '')
    return bool(ABSENT_QUOTE_RE.fullmatch(compact))


def _quote_candidates(value: str) -> list:
    found = []
    for pattern in QUOTE_PATTERNS:
        found.extend(pattern.findall(value or ''))
    return [item.strip() for item in found if item.strip()]


def _appears_in_manuscript(quote: str, manuscript: str) -> bool:
    if quote and quote in (manuscript or ''):
        return True
    compact_quote = _chinese_compact(quote)
    if len(compact_quote) < 4:
        return False
    return compact_quote in _chinese_compact(manuscript)


def quote_binding_issue(value: str, manuscript: str) -> str:
    """引文必须是正文里的连续原文，或明确写无。空字符串表示通过。"""
    if _is_absent_quote(value):
        return ''
    candidates = _quote_candidates(value) or [value.strip()]
    saw_quote = False
    for candidate in candidates:
        if _is_absent_quote(candidate):
            continue
        saw_quote = True
        if _chinese_len(candidate) < 4:
            return f'引文过短，无法对上正文：{candidate}'
        if not _appears_in_manuscript(candidate, manuscript):
            return f'引文不在正文中：{candidate}'
    if not saw_quote:
        return ''
    return ''


def plan_only_span(restatement: str, manuscript: str, plan_text: str, n: int = PLAN_SPAN) -> str:
    """返回复述里一段只出现在计划、不出现在正文的连续汉字。没有则返回空串。"""
    rest = _chinese_compact(restatement)
    book = _chinese_compact(manuscript)
    plan = _chinese_compact(plan_text)
    if len(rest) < n or len(plan) < n:
        return ''
    for index in range(len(rest) - n + 1):
        span = rest[index:index + n]
        if span in plan and span not in book:
            return span
    return ''


def _quote_checks(text: str, manuscript: str) -> dict:
    checks = {}
    for key, labels in QUOTE_FIELDS:
        value = extract_labeled_value(text, list(labels))
        if is_placeholder(value):
            checks[f'quote_{key}'] = _make_check(False, f'缺少可核对的引文：{labels[0]}')
            continue
        issue = quote_binding_issue(value, manuscript)
        checks[f'quote_{key}'] = _make_check(
            not issue,
            issue or f'{labels[0]}已对上正文，或标明无',
        )
    return checks


def assess_blind_read_text(text: str, manuscript: str, plan_text: str = '') -> dict:
    """核对盲读字段、引文是否在正文、复述是否抄了计划。不判断文学，也不证明隔离。"""
    checks = {}
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

    checks.update(_quote_checks(text, manuscript))
    if _chinese_len(plan_text) >= PLAN_SPAN:
        restatement = extract_labeled_value(text, BLIND_READ_FIELDS['不可逆变化'])
        span = plan_only_span(restatement, manuscript, plan_text)
        checks['plan_leak'] = _make_check(
            not span,
            f'复述使用了正文里没有的计划用语：{span}' if span else '复述没有只存在于计划中的连续片段',
        )
    return checks


def _collect_plan_text(novel_dir: Path, workspace: Path | None) -> str:
    parts = []
    outline = novel_dir / '00-大纲.md'
    if outline.exists():
        parts.append(outline.read_text(encoding='utf-8'))
    if workspace is not None:
        for name in PLAN_FILENAMES:
            path = workspace / name
            if path.exists():
                parts.append(path.read_text(encoding='utf-8'))
    return '\n'.join(parts)


def _forbidden_sentences(text: str) -> list:
    section = extract_markdown_section(text, '## 本书不准再写的句子')
    sentences = []
    for line in section.splitlines():
        stripped = re.sub(r'^\s*(?:[-*]|\d+[\.、])\s*', '', line.strip())
        stripped = stripped.strip('。；;')
        if _chinese_len(stripped) >= PLAN_SPAN:
            sentences.append(stripped)
    return sentences


def _check_voice_lock(novel_dir: Path, manuscript: str) -> dict:
    path = novel_dir / VOICE_LOCK_FILENAME
    if not path.exists():
        return {}
    sentences = _forbidden_sentences(path.read_text(encoding='utf-8'))
    if not sentences:
        return {'voice_lock': _make_check(True, '声音锁没有可执行的禁止句')}
    book = _chinese_compact(manuscript)
    hits = [sentence for sentence in sentences if _chinese_compact(sentence) in book]
    if hits:
        return {'voice_lock': _make_check(False, f'正文原样出现禁止句：{hits[0]}')}
    return {'voice_lock': _make_check(True, '正文没有原样复现禁止句')}


def _marked_unisolated(*texts: str) -> bool:
    return any('未隔离' in (text or '') for text in texts)


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


def _read_blind_text(workspace: Path | None) -> str:
    if workspace is None:
        return ''
    path = workspace / 'blind-read.md'
    if not path.exists():
        return ''
    return path.read_text(encoding='utf-8')


def _check_blind_read(
    workspace: Path | None,
    required: bool,
    manuscript: str = '',
    plan_text: str = '',
) -> dict:
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

    if not required:
        return checks

    text = path.read_text(encoding='utf-8')
    checks['blind_read_file'] = _make_check(True, f'盲读：{path}')
    checks.update(assess_blind_read_text(text, manuscript, plan_text))
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
    require_perception = resolved_mode == AUTHOR_MODE
    factory_sample = (
        resolved_mode == FACTORY_MODE
        and chapter_num > 0
        and chapter_num % FACTORY_SAMPLE_EVERY == 0
    )

    checks = {}
    word_count = 0
    body = ''

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
        checks.update(_check_voice_lock(novel_path, body))

    if not review_path or not review_path.exists():
        checks['review_file'] = _make_check(False, '缺少 workspace/chapters/第N章*/review.md')
        review_text = ''
    else:
        checks['review_file'] = _make_check(True, f'复盘：{review_path}')
        review_text = review_path.read_text(encoding='utf-8')

    for key, labels in REVIEW_FIELDS.items():
        checks[key] = _review_field_check(review_text, labels)

    blind_text = _read_blind_text(workspace)
    marked_unisolated = _marked_unisolated(review_text, blind_text)
    require_blind = resolved_mode == AUTHOR_MODE or factory_sample or (
        resolved_mode == FACTORY_MODE and bool(blind_text) and not marked_unisolated
    )

    if resolved_mode == FACTORY_MODE and factory_sample and marked_unisolated:
        checks['factory_sample'] = _make_check(
            False,
            f'第{chapter_num}章是工厂抽检章，不能标注未隔离',
        )
    elif resolved_mode == FACTORY_MODE and factory_sample:
        checks['factory_sample'] = _make_check(True, f'第{chapter_num}章按隔离盲读抽检')
    elif resolved_mode == FACTORY_MODE:
        if not blind_text and not marked_unisolated:
            checks['factory_blind'] = _make_check(
                False,
                '工厂非抽检章缺少盲读，也未标注「未隔离」',
            )
        elif marked_unisolated and not require_blind:
            checks['factory_blind'] = _make_check(True, '已标注未隔离')
        else:
            checks['factory_blind'] = _make_check(True, '非抽检章提供了盲读，按隔离盲读验收')

    if require_blind and review_text:
        has_pointer = '盲读指出' in review_text and '正文改动' in review_text
        checks['review_blind_followup'] = _make_check(
            has_pointer,
            '复盘已引用盲读指出与正文改动' if has_pointer else '复盘缺少「盲读指出 / 正文改动」',
        )

    plan_text = _collect_plan_text(novel_path, workspace)
    checks.update(_check_blind_read(
        workspace,
        required=require_blind,
        manuscript=body,
        plan_text=plan_text,
    ))
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
    print('说明：本脚本核对正文、盲读复述、引文是否在正文、复述是否抄计划、禁止句是否原样出现、感知包、复盘和仪表盘。')
    print('这些一致只说明文件对得上，不能证明盲读来自另一次隔离调用，也不判断文学质量。')

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
