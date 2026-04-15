#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间线一致性检查脚本
从章节正文中提取时间线索（季节、天气、节日等），
检测前后矛盾的时间线问题。
"""

import re
import sys
from pathlib import Path

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, find_chapter_files, setup_windows_encoding

setup_windows_encoding()


# 时间线索提取规则
TIME_SIGNALS = {
    '季节': {
        '春': ['春天', '春季', '春日', '初春', '暮春', '三月', '四月', '桃花', '樱花', '柳絮'],
        '夏': ['夏天', '夏季', '夏日', '初夏', '盛夏', '六月', '七月', '酷暑', '蝉鸣', '荷花'],
        '秋': ['秋天', '秋季', '秋日', '初秋', '深秋', '九月', '十月', '落叶', '秋霜', '桂花'],
        '冬': ['冬天', '冬季', '冬日', '初冬', '寒冬', '十二月', '一月', '大雪', '寒风', '冰'],
    },
    '时段': {
        '早晨': ['清晨', '早上', '黎明', '拂晓', '日出', '晨光'],
        '白天': ['白天', '上午', '中午', '午后', '下午', '阳光'],
        '傍晚': ['傍晚', '黄昏', '日落', '夕阳', '暮色'],
        '夜晚': ['夜', '夜晚', '深夜', '凌晨', '月光', '星', '灯'],
    },
    '天气': {
        '晴': ['晴', '阳光', '万里无云', '艳阳'],
        '雨': ['雨', '暴雨', '细雨', '倾盆', '雷阵雨'],
        '雪': ['雪', '大雪', '暴雪', '鹅毛雪'],
        '雾': ['雾', '浓雾', '薄雾', '雾霾'],
    },
}


def extract_time_signals(text: str) -> dict:
    """从章节正文中提取时间线索"""
    signals = {}
    for category, groups in TIME_SIGNALS.items():
        found = {}
        for group_name, keywords in groups.items():
            count = sum(text.count(kw) for kw in keywords)
            if count > 0:
                found[group_name] = count
        if found:
            # 返回出现最多的信号
            dominant = max(found, key=found.get)
            signals[category] = {
                'dominant': dominant,
                'all': found,
            }
    return signals


def check_timeline(novel_dir: Path) -> dict:
    """检查时间线一致性"""
    chapter_files = find_chapter_files(novel_dir)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    chapters = []
    warnings = []

    for chapter_file in chapter_files:
        content = extract_text_from_chapter(chapter_file)
        match = re.match(r'第(\d+)章', chapter_file.name)
        chapter_num = int(match.group(1)) if match else 0

        signals = extract_time_signals(content)
        chapters.append({
            'chapter': chapter_num,
            'signals': signals,
        })

    # 检测季节不一致
    prev_season = None
    prev_chapter = None
    for ch in chapters:
        season_info = ch['signals'].get('季节')
        if not season_info:
            continue

        current_season = season_info['dominant']

        if prev_season and current_season != prev_season:
            # 季节跳跃是否合理（相邻章节不该从冬跳到夏）
            season_order = ['春', '夏', '秋', '冬']
            prev_idx = season_order.index(prev_season) if prev_season in season_order else -1
            curr_idx = season_order.index(current_season) if current_season in season_order else -1

            if prev_idx >= 0 and curr_idx >= 0:
                # 相邻章节，不该跳过 2+ 个季节
                gap = abs(curr_idx - prev_idx)
                if gap > 1 and gap != 3:  # gap=3 表示相邻（冬→春）
                    warnings.append({
                        'chapter': ch['chapter'],
                        'type': 'season_inconsistency',
                        'detail': f'第{prev_chapter}章是{prev_season}，第{ch["chapter"]}章突变为{current_season}',
                    })

        prev_season = current_season
        prev_chapter = ch['chapter']

    # 检测时段矛盾（同章内早晨和深夜同时出现大量）
    for ch in chapters:
        period_info = ch['signals'].get('时段')
        if not period_info:
            continue
        all_periods = period_info.get('all', {})
        if len(all_periods) >= 3:
            # 一章内出现 3 种以上时段，可能有叙事跳跃
            dominant = period_info['dominant']
            others = [p for p in all_periods if p != dominant and all_periods[p] >= 2]
            if len(others) >= 2:
                warnings.append({
                    'chapter': ch['chapter'],
                    'type': 'time_jump_heavy',
                    'detail': f'本章时段分散：{", ".join(f"{p}({c})" for p, c in all_periods.items())}',
                })

    # 检测天气快速切换
    prev_weather = None
    prev_chapter = None
    for ch in chapters:
        weather_info = ch['signals'].get('天气')
        if not weather_info:
            continue
        current_weather = weather_info['dominant']

        if prev_weather and current_weather != prev_weather:
            # 完全相反的天气在相邻章节
            opposites = [('晴', '雨'), ('晴', '雪'), ('雾', '晴')]
            if (prev_weather, current_weather) in opposites or (current_weather, prev_weather) in opposites:
                # 仅在两章都没有过渡时警告
                pass  # 天气变化本身合理，不标记为硬矛盾

        prev_weather = current_weather
        prev_chapter = ch['chapter']

    # 排序
    type_order = {'season_inconsistency': 0, 'time_jump_heavy': 1}
    warnings.sort(key=lambda w: type_order.get(w['type'], 2))

    return {
        'total_chapters': len(chapters),
        'chapters': chapters,
        'warnings': warnings,
    }


def print_report(novel_dir: Path, results: dict):
    """打印时间线检查报告"""
    print('\n' + '=' * 60)
    print('时间线一致性检查报告')
    print('=' * 60)
    print(f'小说：{novel_dir.name}')
    print(f'检查章节：{results["total_chapters"]}章')
    print()

    # 时间线概览
    print('【时间线概览】')
    for ch in results['chapters']:
        signals = ch['signals']
        parts = []
        for cat in ['季节', '时段', '天气']:
            info = signals.get(cat)
            if info:
                parts.append(f'{cat}:{info["dominant"]}')
        line = ', '.join(parts) if parts else '无明确时间线索'
        print(f"  第{ch['chapter']:2d}章：{line}")
    print()

    # 警告
    if results['warnings']:
        warn_icons = {'season_inconsistency': '🔴', 'time_jump_heavy': '🟡'}
        print('【警告】')
        for w in results['warnings']:
            icon = warn_icons.get(w['type'], '⚠️')
            print(f"  {icon} 第{w['chapter']}章 | {w['detail']}")
        print()
    else:
        print('✅ 未检测到时间线矛盾\n')

    print('=' * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法：python scripts/check_timeline.py <小说目录路径>')
        print('示例：python scripts/check_timeline.py novels/书名')
        return

    novel_dir = Path(sys.argv[1])
    if not novel_dir.exists():
        print(f'错误：目录不存在 - {novel_dir}')
        return

    results = check_timeline(novel_dir)
    if 'error' in results:
        print(f'错误：{results["error"]}')
        return

    print_report(novel_dir, results)


if __name__ == '__main__':
    main()
