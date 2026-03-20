#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说体检脚本
检查小说的健康状态，生成体检报告
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def extract_chapter_content(file_path: Path) -> str:
    """从章节文件中提取正文内容"""
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

    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('#') and '章' in line:
            content_start = i + 1
            break

    return '\n'.join(lines[content_start:]).strip()


def count_chinese_words(text: str) -> int:
    """统计中文字数"""
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def detect_scene_type(text: str) -> str:
    """简单检测场景类型"""
    indoor_keywords = ['房间', '室内', '屋里', '客厅', '卧室', '办公室']
    outdoor_keywords = ['外面', '户外', '街道', '天空', '花园', '野外']
    action_keywords = ['跑', '跳', '战斗', '打架', '追逐']

    indoor_count = sum(1 for kw in indoor_keywords if kw in text)
    outdoor_count = sum(1 for kw in outdoor_keywords if kw in text)
    action_count = sum(1 for kw in action_keywords if kw in text)

    if indoor_count > outdoor_count and indoor_count >= 2:
        return '室内'
    elif outdoor_count > indoor_count and outdoor_count >= 2:
        return '户外'
    elif action_count >= 2:
        return '动作'
    elif indoor_count >= 1:
        return '室内'
    return '其他'


def check_novel(novel_dir: Path) -> dict:
    """检查小说健康状态"""
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

        chapters.append({'number': chapter_num, 'word_count': word_count, 'scene_type': scene_type})
        word_counts.append(word_count)
        scene_types.append(scene_type)

    # 计算字数统计
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    variance = sum((w - avg_words) ** 2 for w in word_counts) / len(word_counts) if word_counts else 0
    std_dev = variance ** 0.5

    # 场景分布
    scene_counts = defaultdict(int)
    for st in scene_types:
        scene_counts[st] += 1

    # 检测场景重复
    scene_warnings = []
    consecutive_count = 1
    consecutive_type = scene_types[0] if scene_types else None
    for i in range(1, len(scene_types)):
        if scene_types[i] == consecutive_type:
            consecutive_count += 1
        else:
            if consecutive_count >= 3:
                scene_warnings.append(f"'{consecutive_type}'连续{consecutive_count}章")
            consecutive_count = 1
            consecutive_type = scene_types[i]
    if consecutive_count >= 3:
        scene_warnings.append(f"'{consecutive_type}'连续{consecutive_count}章")

    # 字数健康评分 (5分制)
    if std_dev < 500:
        word_score = 5
    elif std_dev < 800:
        word_score = 4
    elif std_dev < 1200:
        word_score = 3
    elif std_dev < 2000:
        word_score = 2
    else:
        word_score = 1

    # 节奏健康评分（场景多样性）
    unique_scenes = len(set(scene_types))
    if unique_scenes >= 4:
        rhythm_score = 5
    elif unique_scenes >= 3:
        rhythm_score = 4
    elif unique_scenes >= 2:
        rhythm_score = 3
    else:
        rhythm_score = 2
    if scene_warnings:
        rhythm_score = max(1, rhythm_score - 1)

    return {
        'chapters': chapters,
        'total_chapters': len(chapters),
        'total_words': sum(word_counts),
        'avg_words': avg_words,
        'std_dev': std_dev,
        'word_score': word_score,
        'scene_counts': dict(scene_counts),
        'scene_warnings': scene_warnings,
        'rhythm_score': rhythm_score,
    }


def print_report(novel_dir: Path, results: dict):
    """打印体检报告"""
    print('\n' + '=' * 60)
    print('小说体检报告')
    print('=' * 60)
    print(f'小说：{novel_dir.name}')
    print(f'检查章节：{results["total_chapters"]}章')
    print(f'总字数：{results["total_words"]:,}')
    print()

    print('【评分】')
    print(f'  字数健康：{results["word_score"]}/5 {"✅" if results["word_score"] >= 4 else "⚠️"}')
    print(f'  节奏健康：{results["rhythm_score"]}/5 {"✅" if results["rhythm_score"] >= 4 else "⚠️"}')
    print()

    print('【字数统计】')
    print(f'  平均：{results["avg_words"]:.0f}字/章')
    print(f'  标准差：{results["std_dev"]:.0f}')
    print()

    print('【场景分布】')
    for scene, count in results['scene_counts'].items():
        pct = count / results['total_chapters'] * 100
        print(f'  {scene}：{count}章（{pct:.0f}%）')
    print()

    if results.get('scene_warnings'):
        print('【警告】')
        for warning in results['scene_warnings']:
            print(f'  ⚠️ {warning}')
        print()

    # 计算综合评分（简化版）
    overall = (results['word_score'] * 0.5 + results['rhythm_score'] * 0.5)
    print(f'【综合评分】{overall:.1f}/5 {"✅" if overall >= 3.5 else "⚠️"}')
    print('=' * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法: python scripts/check_novel_health.py <小说目录路径>')
        print('示例: python scripts/check_novel_health.py novels/书名')
        return

    novel_dir = Path(sys.argv[1])
    if not novel_dir.exists():
        print(f'错误: 目录不存在 - {novel_dir}')
        return

    results = check_novel(novel_dir)
    if 'error' in results:
        print(f'错误: {results["error"]}')
        return

    print_report(novel_dir, results)


if __name__ == '__main__':
    main()