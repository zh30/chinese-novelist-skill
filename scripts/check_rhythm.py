#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节奏检查脚本
检查小说章节的节奏健康状态，生成报告
"""

import re
import sys
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def extract_chapter_content(file_path: Path) -> str:
    """从章节文件中提取正文内容，优先只统计 `## 正文` 区块"""
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

    # 兼容旧模板
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('#') and '章' in line:
            content_start = i + 1
            break

    return '\n'.join(lines[content_start:]).strip()


def count_chinese_words(text: str) -> int:
    """统计中文字数（排除标点符号和Markdown标记）"""
    # 移除Markdown标记
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)

    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def detect_scene_type(text: str) -> str:
    """简单检测场景类型"""
    indoor_keywords = ['房间', '室内', '屋里', '屋内', '客厅', '卧室', '办公室', '教室', '酒店', '餐厅']
    outdoor_keywords = ['外面', '户外', '街道', '路上', '天空', '花园', '广场', '野外', '山上', '河边']
    action_keywords = ['跑', '跳', '战斗', '打架', '追逐', '冲', '飞']

    indoor_count = sum(1 for kw in indoor_keywords if kw in text)
    outdoor_count = sum(1 for kw in outdoor_keywords if kw in text)
    action_count = sum(1 for kw in action_keywords if kw in text)

    if indoor_count > outdoor_count and indoor_count >= 2:
        return '室内对话'
    elif outdoor_count > indoor_count and outdoor_count >= 2:
        return '户外'
    elif action_count >= 3:
        return '动作'
    elif indoor_count >= 1:
        return '室内'
    else:
        return '其他'


def check_chapters(novel_dir: Path) -> dict:
    """检查章节节奏"""
    chapter_files = sorted(novel_dir.glob('第*.md'))

    if not chapter_files:
        return {'error': '未找到章节文件'}

    chapters = []
    word_counts = []
    scene_types = []

    for chapter_file in chapter_files:
        content = extract_chapter_content(chapter_file)
        word_count = count_chinese_words(content)
        scene_type = detect_scene_type(content)

        match = re.match(r'第(\d+)章', chapter_file.name)
        chapter_num = int(match.group(1)) if match else 0

        chapters.append({
            'file': chapter_file,
            'number': chapter_num,
            'word_count': word_count,
            'scene_type': scene_type
        })
        word_counts.append(word_count)
        scene_types.append(scene_type)

    # 检测场景重复
    scene_warnings = []
    consecutive_count = 1
    consecutive_type = scene_types[0] if scene_types else None

    for i in range(1, len(scene_types)):
        if scene_types[i] == consecutive_type:
            consecutive_count += 1
        else:
            if consecutive_count >= 3:
                scene_warnings.append(f"场景'{consecutive_type}'连续出现{consecutive_count}章")
            consecutive_count = 1
            consecutive_type = scene_types[i]

    if consecutive_count >= 3:
        scene_warnings.append(f"场景'{consecutive_type}'连续出现{consecutive_count}章")

    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    max_words = max(word_counts) if word_counts else 0
    min_words = min(word_counts) if word_counts else 0
    max_chapter = chapters[word_counts.index(max_words)]['number'] if word_counts else 0
    min_chapter = chapters[word_counts.index(min_words)]['number'] if word_counts else 0

    return {
        'chapters': chapters,
        'word_counts': word_counts,
        'scene_types': scene_types,
        'scene_warnings': scene_warnings,
        'avg_words': avg_words,
        'max_words': max_words,
        'max_chapter': max_chapter,
        'min_words': min_words,
        'min_chapter': min_chapter,
        'total_chapters': len(chapters),
        'total_words': sum(word_counts)
    }


def print_report(novel_dir: Path, results: dict):
    """打印报告"""
    print('\n' + '=' * 60)
    print('节奏健康报告')
    print('=' * 60)
    print(f'小说：{novel_dir.name}')
    print(f'检查章节：{results["total_chapters"]}章')
    print(f'总字数：{results["total_words"]:,}')
    print()

    if results.get('scene_warnings'):
        print('【警告】场景重复')
        for warning in results['scene_warnings']:
            print(f'  ⚠️ {warning}')
        print()

    print('【字数统计】')
    print(f'  平均：{results["avg_words"]:.0f}字/章')
    print(f'  最高：第{results["max_chapter"]}章（{results["max_words"]:,}字）')
    print(f'  最低：第{results["min_chapter"]}章（{results["min_words"]:,}字）')
    print()

    print('【章节概览】')
    for ch in results['chapters']:
        print(f"  第{ch['number']:2d}章: {ch['word_count']:5,}字 | {ch['scene_type']}")
    print()

    if not results.get('scene_warnings'):
        print('【状态】节奏健康，无明显警告')
    print('=' * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法: python scripts/check_rhythm.py <小说目录路径>')
        print('示例: python scripts/check_rhythm.py novels/书名')
        return

    novel_dir = Path(sys.argv[1])
    if not novel_dir.exists():
        print(f'错误: 目录不存在 - {novel_dir}')
        return

    results = check_chapters(novel_dir)
    if 'error' in results:
        print(f'错误: {results["error"]}')
        return

    print_report(novel_dir, results)


if __name__ == '__main__':
    main()