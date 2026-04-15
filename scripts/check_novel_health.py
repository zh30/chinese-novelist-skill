#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说健康检查脚本（整合版）
整合原有 check_novel_health.py 和 check_rhythm.py 的功能。
检查字数健康、节奏健康、场景多样性和连续性，生成体检报告。
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, count_chinese_words, find_chapter_files, setup_windows_encoding

setup_windows_encoding()


# 场景类型检测关键词（统一版本，移除重复定义）
SCENE_KEYWORDS = {
    '室内对话': ['房间', '室内', '屋里', '屋内', '客厅', '卧室', '办公室', '教室'],
    '户外场景': ['外面', '户外', '街道', '路上', '天空', '花园', '广场', '野外', '山上', '河边'],
    '动作场景': ['跑', '跳', '战斗', '打架', '追逐', '冲', '飞', '砍', '射'],
    '回忆闪回': ['想起', '记得', '回忆', '那时候', '从前', '曾经', '往事'],
    '情感沉淀': ['沉默', '久久', '凝视', '望着', '独自', '一个人'],
}

# 对白密度阈值
DIALOGUE_MARKER = re.compile(r'["「『]')


def detect_scene_type(text: str) -> str:
    """检测场景类型（升级版：6 种类型）"""
    scores = {}
    for scene_type, keywords in SCENE_KEYWORDS.items():
        scores[scene_type] = sum(1 for kw in keywords if kw in text)

    # 对白密度判定：对白占比高的归为对话场景
    dialogue_count = len(DIALOGUE_MARKER.findall(text))
    chinese_count = count_chinese_words(text)
    if chinese_count > 0 and dialogue_count / (chinese_count / 100) > 2:
        scores['室内对话'] = scores.get('室内对话', 0) + 3

    best_type = max(scores, key=scores.get) if any(scores.values()) else '其他'
    if scores[best_type] < 1:
        return '其他'
    return best_type


def check_novel(novel_dir: Path) -> dict:
    """检查小说健康状态"""
    chapter_files = find_chapter_files(novel_dir)

    if not chapter_files:
        return {'error': '未找到章节文件'}

    chapters = []
    word_counts = []
    scene_types = []

    for chapter_file in chapter_files:
        content = extract_text_from_chapter(chapter_file)
        word_count = count_chinese_words(content)
        scene_type = detect_scene_type(content)

        match = re.match(r'第(\d+)章', chapter_file.name)
        chapter_num = int(match.group(1)) if match else 0

        chapters.append({'number': chapter_num, 'word_count': word_count, 'scene_type': scene_type, 'file': chapter_file})
        word_counts.append(word_count)
        scene_types.append(scene_type)

    # 字数统计
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    max_words = max(word_counts) if word_counts else 0
    min_words = min(word_counts) if word_counts else 0
    max_chapter = chapters[word_counts.index(max_words)]['number'] if word_counts else 0
    min_chapter = chapters[word_counts.index(min_words)]['number'] if word_counts else 0
    variance = sum((w - avg_words) ** 2 for w in word_counts) / len(word_counts) if word_counts else 0
    std_dev = variance ** 0.5

    # 场景分布
    scene_counts = defaultdict(int)
    for st in scene_types:
        scene_counts[st] += 1

    # 场景重复警告
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

    # 字数健康评分 (5 分制)
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
    if unique_scenes >= 5:
        rhythm_score = 5
    elif unique_scenes >= 4:
        rhythm_score = 4
    elif unique_scenes >= 3:
        rhythm_score = 3
    elif unique_scenes >= 2:
        rhythm_score = 2
    else:
        rhythm_score = 1
    if scene_warnings:
        rhythm_score = max(1, rhythm_score - 1)

    return {
        'chapters': chapters,
        'total_chapters': len(chapters),
        'total_words': sum(word_counts),
        'avg_words': avg_words,
        'std_dev': std_dev,
        'max_words': max_words,
        'max_chapter': max_chapter,
        'min_words': min_words,
        'min_chapter': min_chapter,
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
    print(f'  最高：第{results["max_chapter"]}章（{results["max_words"]:,}字）')
    print(f'  最低：第{results["min_chapter"]}章（{results["min_words"]:,}字）')
    print()

    print('【场景分布】')
    for scene, count in sorted(results['scene_counts'].items(), key=lambda x: -x[1]):
        pct = count / results['total_chapters'] * 100
        print(f'  {scene}：{count}章（{pct:.0f}%）')
    print()

    if results.get('scene_warnings'):
        print('【警告】场景重复')
        for warning in results['scene_warnings']:
            print(f'  ⚠️ {warning}')
        print()

    print('【章节概览】')
    for ch in results['chapters']:
        print(f"  第{ch['number']:2d}章：{ch['word_count']:5,}字 | {ch['scene_type']}")
    print()

    overall = (results['word_score'] * 0.5 + results['rhythm_score'] * 0.5)
    print(f'【综合评分】{overall:.1f}/5 {"✅" if overall >= 3.5 else "⚠️"}')
    print('=' * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法：python scripts/check_novel_health.py <小说目录路径>')
        print('示例：python scripts/check_novel_health.py novels/书名')
        return

    novel_dir = Path(sys.argv[1])
    if not novel_dir.exists():
        print(f'错误：目录不存在 - {novel_dir}')
        return

    results = check_novel(novel_dir)
    if 'error' in results:
        print(f'错误：{results["error"]}')
        return

    print_report(novel_dir, results)


if __name__ == '__main__':
    main()
