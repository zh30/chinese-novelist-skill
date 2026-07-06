#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享工具函数
供 check_chapter_wordcount.py、check_ai_style.py、check_rhythm.py、
check_novel_health.py、check_timeline.py 等脚本共用
"""

import re
from pathlib import Path


BODY_SECTION_MARKERS = {'## 正文', '##正文', '## Body', '##Body'}
MANUSCRIPT_DIR = 'manuscript'


def extract_text_from_chapter(file_path: Path) -> str:
    """从章节文件中提取正文内容。

    支持三种格式：
    1. 新格式：首行章数 + 标题，空行后直接正文。
    2. 旧混合格式：正文位于 `## 正文` / `## Body` 区块。
    3. 旧简洁格式：Markdown 章节标题后直接正文，遇到下一个二级标题停止。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    body_start = None
    body_end = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in BODY_SECTION_MARKERS:
            body_start = i + 1
            continue
        if body_start is not None and stripped.startswith('## '):
            body_end = i
            break

    if body_start is not None:
        return _clean_extracted_text('\n'.join(lines[body_start:body_end]))

    plain_title_index = _find_plain_chapter_title_line(lines)
    if plain_title_index is not None:
        return _clean_extracted_text('\n'.join(lines[plain_title_index + 1:]))

    # 兼容旧模板：没有 ## 正文 标记时，取章节标题之后、下一个二级标题之前的内容
    content_start = 0
    content_end = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#') and '章' in stripped and not stripped.startswith('##'):
            content_start = i + 1
            continue
        if content_start > 0 and stripped.startswith('## '):
            content_end = i
            break

    if content_end is None:
        content_end = len(lines)

    return _clean_extracted_text('\n'.join(lines[content_start:content_end]))


def count_chinese_words(text: str) -> int:
    """统计中文字数（排除 Markdown 标记）"""
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def split_sentences(text: str) -> list:
    """中文分句（简化版）"""
    sentences = re.split(r'[。！？]+', text)
    return [s.strip() for s in sentences if s.strip()]


def find_chapter_files(directory: Path, lang: str = 'zh') -> list:
    """在目录中查找章节文件，按章节号排序。

    新项目优先读取：
    - 中文：`manuscript/zh/`
    - 英文：`manuscript/en/`

    为了兼容旧项目，找不到新目录正文时回退到旧的根目录章节；
    英文导出和翻译仍兼容旧 `en/` 目录。
    """
    for chapter_dir in iter_chapter_directories(directory, lang):
        chapter_files = _list_chapter_files(chapter_dir, lang)
        if chapter_files:
            return chapter_files
    return []


def iter_chapter_directories(directory: Path, lang: str = 'zh') -> list:
    """返回按优先级排序的章节目录候选。"""
    directory = Path(directory)
    candidates = []

    if lang == 'en':
        candidates.extend([
            directory / MANUSCRIPT_DIR / 'en',
            directory / 'en',
            directory,
        ])
    else:
        candidates.extend([
            directory / MANUSCRIPT_DIR / 'zh',
            directory / 'chapters',
            directory,
        ])

    seen = set()
    existing = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if candidate.exists() and candidate.is_dir():
            existing.append(candidate)
    return existing


def _extract_chapter_num(path: Path) -> int:
    """从文件名中提取章节号"""
    zh_match = re.match(r'第(\d+)章', path.name)
    if zh_match:
        return int(zh_match.group(1))

    en_match = re.match(r'Chapter[-_ ]?(\d+)', path.name, re.IGNORECASE)
    if en_match:
        return int(en_match.group(1))

    return 0


def _list_chapter_files(directory: Path, lang: str) -> list:
    """列出单个目录中的章节文件。"""
    if lang == 'en':
        patterns = ('Chapter-*.md', 'Chapter_*.md', 'Chapter *.md')
    else:
        patterns = ('第*.md',)

    files = []
    for pattern in patterns:
        files.extend(directory.glob(pattern))

    return sorted(files, key=lambda p: (_extract_chapter_num(p), p.name))


def _clean_extracted_text(text: str) -> str:
    """清理正文提取结果中的分隔线和边缘空白。"""
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    return text.strip()


def _find_plain_chapter_title_line(lines: list) -> int:
    """查找纯正文格式中的首行章节标题。"""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if _looks_like_plain_chapter_title(stripped):
            return i
        return None
    return None


def _looks_like_plain_chapter_title(line: str) -> bool:
    """判断是否为 `第001章：标题` 或 `Chapter 1: Title`。"""
    if line.startswith('#'):
        return False
    return bool(
        re.match(r'^(?:第\s*\d+\s*章|Chapter[-_ ]?\d+|Chapter\s+\d+)\b', line, re.IGNORECASE)
    )


def setup_windows_encoding():
    """修复 Windows 控制台编码问题"""
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
