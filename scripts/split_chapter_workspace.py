#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把旧的混合章节拆分为干净正文和章节工作台。

默认行为是保守迁移：
- 写入 `manuscript/zh/第XXX章-标题.md`
- 写入 `workspace/chapters/第XXX章-标题/*.md`
- 不移动、不删除原始章节

如需归档原始章节，显式传入 `--move-originals`。
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, setup_windows_encoding

setup_windows_encoding()


SECTION_FILE_MAP = {
    '本章任务卡': 'task-card.md',
    '场景拆分': 'scene-plan.md',
    '角色沙盘': 'sandbox.md',
    '导演裁决': 'sandbox.md',
    '章节复盘': 'review.md',
}


def split_chapter_workspace(
    novel_dir: Path,
    move_originals: bool = False,
    overwrite: bool = False,
) -> dict:
    """拆分旧混合章节目录。"""
    novel_dir = Path(novel_dir)
    if not novel_dir.exists() or not novel_dir.is_dir():
        return {'ok': False, 'error': f'目录不存在: {novel_dir}', 'chapters': []}

    source_files = find_legacy_chapter_files(novel_dir)
    if not source_files:
        return {'ok': False, 'error': '未找到根目录旧章节文件', 'chapters': []}

    manuscript_dir = novel_dir / 'manuscript' / 'zh'
    workspace_root = novel_dir / 'workspace' / 'chapters'
    archive_dir = novel_dir / '_archive' / 'mixed-chapters'
    manuscript_dir.mkdir(parents=True, exist_ok=True)
    workspace_root.mkdir(parents=True, exist_ok=True)
    if move_originals:
        archive_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for source in source_files:
        parsed = parse_mixed_chapter(source)
        output_chapter = manuscript_dir / source.name
        workspace_dir = workspace_root / source.stem

        status = 'written'
        if output_chapter.exists() and not overwrite:
            status = 'skipped'
        else:
            output_chapter.write_text(parsed['clean_chapter'], encoding='utf-8')

        workspace_dir.mkdir(parents=True, exist_ok=True)
        write_workspace_files(workspace_dir, parsed['sections'], overwrite=overwrite)

        archived_to = None
        if move_originals:
            archived_to = archive_dir / source.name
            archived_to = unique_path(archived_to)
            shutil.move(str(source), str(archived_to))

        results.append({
            'source': str(source),
            'manuscript': str(output_chapter),
            'workspace': str(workspace_dir),
            'status': status,
            'archived_to': str(archived_to) if archived_to else None,
        })

    return {'ok': True, 'chapters': results}


def find_legacy_chapter_files(novel_dir: Path) -> list:
    """只查找旧项目根目录下的中文章节文件。"""
    files = [p for p in novel_dir.glob('第*.md') if p.is_file()]
    return sorted(files, key=lambda p: (extract_chapter_number(p.name), p.name))


def parse_mixed_chapter(path: Path) -> dict:
    """解析一个旧混合章节。"""
    content = path.read_text(encoding='utf-8')
    title = extract_chapter_title(content, path)
    body = extract_text_from_chapter(path)
    sections = extract_non_body_sections(content)
    clean_chapter = f"{title}\n\n{body.strip()}\n"

    return {
        'title': title,
        'body': body,
        'sections': sections,
        'clean_chapter': clean_chapter,
    }


def extract_chapter_title(content: str, path: Path) -> str:
    """提取并规范化章节标题。"""
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#') and '章' in stripped:
            stripped = stripped.lstrip('#').strip()
            return normalize_chapter_title(stripped)
        if re.match(r'^第\s*\d+\s*章\b', stripped):
            return normalize_chapter_title(stripped)
        break
    return normalize_chapter_title(path.stem)


def normalize_chapter_title(title: str) -> str:
    """把 `第01章-标题` 规范为 `第01章：标题`。"""
    title = title.strip()
    title = re.sub(r'\s+', ' ', title)
    match = re.match(r'^(第\s*\d+\s*章)[：:\-\s]*(.*)$', title)
    if not match:
        return title
    prefix = re.sub(r'\s+', '', match.group(1))
    rest = match.group(2).strip()
    return f'{prefix}：{rest}' if rest else prefix


def extract_non_body_sections(content: str) -> dict:
    """提取除正文外的二级标题区块。"""
    lines = content.splitlines()
    sections = {}
    current_title = None
    current_lines = []

    def flush():
        if not current_title:
            return
        normalized = normalize_section_title(current_title)
        if normalized in ('正文', 'Body'):
            return
        sections.setdefault(normalized, [])
        sections[normalized].append('\n'.join(current_lines).strip())

    for line in lines:
        match = re.match(r'^##\s*(.+?)\s*$', line.strip())
        if match:
            flush()
            current_title = match.group(1).strip()
            current_lines = []
            continue
        if current_title:
            current_lines.append(line)

    flush()
    return sections


def normalize_section_title(title: str) -> str:
    """把带说明的标题归并到核心标题。"""
    title = title.strip()
    for known in SECTION_FILE_MAP:
        if title.startswith(known):
            return known
    return title


def write_workspace_files(workspace_dir: Path, sections: dict, overwrite: bool = False):
    """写出工作台文件。"""
    misc_parts = []
    pending = {}

    for title, chunks in sections.items():
        target_name = SECTION_FILE_MAP.get(title)
        body = '\n\n'.join(chunk for chunk in chunks if chunk).strip()
        if not body:
            continue
        if target_name:
            pending.setdefault(target_name, []).append(f'# {title}\n\n{body}\n')
        else:
            misc_parts.append(f'# {title}\n\n{body}\n')

    for target_name, chunks in pending.items():
        target = workspace_dir / target_name
        if target.exists() and not overwrite:
            continue
        target.write_text('\n'.join(chunks).strip() + '\n', encoding='utf-8')

    if misc_parts:
        target = workspace_dir / 'misc-notes.md'
        if not target.exists() or overwrite:
            target.write_text('\n'.join(misc_parts).strip() + '\n', encoding='utf-8')


def extract_chapter_number(name: str) -> int:
    """从文件名提取章节号。"""
    match = re.match(r'第(\d+)章', name)
    return int(match.group(1)) if match else 0


def unique_path(path: Path) -> Path:
    """避免归档覆盖已有文件。"""
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 2
    while True:
        candidate = parent / f'{stem}-{index}{suffix}'
        if not candidate.exists():
            return candidate
        index += 1


def print_summary(result: dict):
    """打印迁移结果。"""
    if not result.get('ok'):
        print(f"错误: {result.get('error', '迁移失败')}")
        return

    print('\n章节工作台迁移完成')
    print('=' * 60)
    for chapter in result['chapters']:
        print(f"源文件: {chapter['source']}")
        print(f"正文:   {chapter['manuscript']}")
        print(f"工作台: {chapter['workspace']}")
        if chapter.get('archived_to'):
            print(f"归档:   {chapter['archived_to']}")
        elif chapter['status'] == 'skipped':
            print('状态:   正文已存在，已跳过覆盖')
        print('-' * 60)


def main():
    parser = argparse.ArgumentParser(
        description='把旧混合章节拆分为 manuscript/zh 正文和 workspace/chapters 工作台',
    )
    parser.add_argument('novel_dir', help='小说项目目录路径')
    parser.add_argument('--move-originals', action='store_true', help='迁移后把原始章节移动到 _archive/mixed-chapters/')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在的正文和工作台文件')
    args = parser.parse_args()

    result = split_chapter_workspace(
        Path(args.novel_dir),
        move_originals=args.move_originals,
        overwrite=args.overwrite,
    )
    print_summary(result)
    sys.exit(0 if result.get('ok') else 1)


if __name__ == '__main__':
    main()
