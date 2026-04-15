#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享工具函数
供 check_chapter_wordcount.py、check_ai_style.py、check_rhythm.py、
check_novel_health.py、check_timeline.py 等脚本共用
"""

import re
from pathlib import Path


def extract_text_from_chapter(file_path: Path) -> str:
    """从章节文件中提取正文内容，优先提取 `## 正文` 区块"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    body_start = None
    body_end = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '## 正文':
            body_start = i + 1
            continue
        if body_start is not None and stripped.startswith('## '):
            body_end = i
            break

    if body_start is not None:
        return '\n'.join(lines[body_start:body_end]).strip()

    # 兼容旧模板：没有 ## 正文 标记时，取章节标题之后的所有内容
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('#') and '章' in line:
            content_start = i + 1
            break

    return '\n'.join(lines[content_start:])


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


def find_chapter_files(directory: Path) -> list:
    """在目录中查找所有章节文件，按章节号排序"""
    chapter_files = sorted(
        directory.glob('第*.md'),
        key=lambda p: _extract_chapter_num(p)
    )
    return chapter_files


def _extract_chapter_num(path: Path) -> int:
    """从文件名中提取章节号"""
    match = re.match(r'第(\d+)章', path.name)
    return int(match.group(1)) if match else 0


def setup_windows_encoding():
    """修复 Windows 控制台编码问题"""
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
