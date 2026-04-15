#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人物一致性检查脚本
从章节文件中提取人物出现、对白、情绪关键词，
与人物档案对照，标记可能的矛盾。
"""

import re
import sys
from pathlib import Path

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, find_chapter_files, setup_windows_encoding

setup_windows_encoding()


# 情绪关键词映射
EMOTION_KEYWORDS = {
    '愤怒': ['怒', '愤', '气', '吼', '咆哮', '拍桌', '踢', '摔', '咬牙', '攥拳'],
    '恐惧': ['怕', '恐惧', '惊恐', '战栗', '颤抖', '发抖', '后退', '冷汗'],
    '悲伤': ['悲', '哭', '泪', '抽泣', '哽咽', '低落', '黯然', '沉默'],
    '喜悦': ['笑', '喜', '乐', '欢呼', '跳跃', '兴奋', '激动'],
    '紧张': ['紧', '焦虑', '不安', '踱步', '来回', '坐立', '出汗'],
    '决心': ['决', '必须', '一定', '绝不', '发誓', '握拳'],
    '困惑': ['疑', '惑', '困惑', '不解', '皱眉', '思索', '纳闷'],
}

# 对白提取正则
DIALOGUE_RE = re.compile(r'["「『]([^"」』]+)["」』]')


def load_character_profiles(novel_dir: Path) -> list:
    """从人物档案文件中加载人物信息"""
    profiles = []

    # 尝试读取 v2 人物档案
    v2_files = list(novel_dir.glob('01-人物档案*.md'))
    for profile_file in v2_files:
        content = profile_file.read_text(encoding='utf-8')
        # 提取人物名和声音锚点
        name = _extract_character_name(content)
        voice_anchors = _extract_voice_anchors(content)
        forbidden_words = _extract_forbidden_words(content)
        if name:
            profiles.append({
                'name': name,
                'voice_anchors': voice_anchors,
                'forbidden_words': forbidden_words,
                'file': str(profile_file),
            })

    return profiles


def _extract_character_name(content: str) -> str:
    """从人物档案中提取人物名"""
    match = re.search(r'##\s*(?:人物|角色)[:：]?\s*(.+)', content)
    if match:
        return match.group(1).strip()
    # 尝试标题
    match = re.search(r'#\s*(.+?)(?:的|人物|角色)', content)
    if match:
        return match.group(1).strip()
    return ''


def _extract_voice_anchors(content: str) -> list:
    """从人物档案中提取声音锚点（标志性对白）"""
    anchors = []
    matches = re.findall(r'["「『]([^"」』]+)["」』]', content)
    anchors.extend(matches[:5])
    also = re.findall(r'"([^"]+)"', content)
    anchors.extend(a for a in also if a not in anchors)
    return anchors[:5]


def _extract_forbidden_words(content: str) -> list:
    """从人物档案中提取禁止用语"""
    forbidden = []
    section = ''
    for line in content.split('\n'):
        if '禁止' in line and ('用语' in line or '说话' in line):
            section = 'forbidden'
            continue
        if section == 'forbidden' and line.strip().startswith('-'):
            word = line.strip().lstrip('- ').strip()
            if word:
                forbidden.append(word)
        elif section == 'forbidden' and line.startswith('#'):
            section = ''
    return forbidden


def detect_character_mentions(text: str, profile_names: list) -> dict:
    """检测章节中人物的出现和情绪"""
    mentions = {}
    for name in profile_names:
        if name and name in text:
            # 提取该人物附近的对白
            dialogues = []
            for m in DIALOGUE_RE.finditer(text):
                dialogue = m.group(1)
                # 检查对白前后 200 字内是否有该人物名
                start = max(0, m.start() - 200)
                context = text[start:m.start()]
                if name in context:
                    dialogues.append(dialogue)

            # 检测该人物附近的情绪关键词
            emotions_detected = {}
            for emotion, keywords in EMOTION_KEYWORDS.items():
                count = 0
                for kw in keywords:
                    # 在人物名前后 500 字范围内搜索
                    for nm in re.finditer(re.escape(name), text):
                        start = max(0, nm.start() - 500)
                        end = min(len(text), nm.end() + 500)
                        context = text[start:end]
                        count += context.count(kw)
                if count > 0:
                    emotions_detected[emotion] = count

            mentions[name] = {
                'appearances': text.count(name),
                'dialogues': dialogues[:5],
                'emotions': emotions_detected,
            }

    return mentions


def check_consistency(novel_dir: Path) -> dict:
    """检查人物一致性"""
    chapter_files = find_chapter_files(novel_dir)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    profiles = load_character_profiles(novel_dir)
    profile_names = [p['name'] for p in profiles if p['name']]

    if not profile_names:
        return {'error': '未找到人物档案（01-人物档案*.md），无法执行一致性检查'}

    warnings = []
    chapter_data = []

    for chapter_file in chapter_files:
        content = extract_text_from_chapter(chapter_file)
        match = re.match(r'第(\d+)章', chapter_file.name)
        chapter_num = int(match.group(1)) if match else 0

        mentions = detect_character_mentions(content, profile_names)

        # 检查禁止用语
        for profile in profiles:
            name = profile['name']
            if name in mentions:
                for dialogue in mentions[name].get('dialogues', []):
                    for forbidden in profile['forbidden_words']:
                        if forbidden in dialogue:
                            warnings.append({
                                'chapter': chapter_num,
                                'character': name,
                                'type': 'forbidden_word',
                                'detail': f'使用了禁止用语"{forbidden}"',
                                'context': dialogue[:40],
                            })

        chapter_data.append({
            'chapter': chapter_num,
            'mentions': mentions,
        })

    # 检测情绪突变：同一人物连续章节情绪大幅波动
    for name in profile_names:
        prev_emotion = None
        prev_chapter = None
        for cd in chapter_data:
            if name not in cd['mentions']:
                continue
            emotions = cd['mentions'][name].get('emotions', {})
            dominant = max(emotions, key=emotions.get) if emotions else None

            if prev_emotion and dominant:
                # 敌对情绪突变（愤怒→喜悦 或 恐惧→决心 等）
                opposite_pairs = [('愤怒', '喜悦'), ('恐惧', '决心'), ('悲伤', '喜悦'), ('困惑', '决心')]
                if (prev_emotion, dominant) in opposite_pairs or (dominant, prev_emotion) in opposite_pairs:
                    if prev_chapter and cd['chapter'] - prev_chapter <= 1:
                        warnings.append({
                            'chapter': cd['chapter'],
                            'character': name,
                            'type': 'emotion_spike',
                            'detail': f'情绪从"{prev_emotion}"突变为"{dominant}"（第{prev_chapter}-{cd["chapter"]}章）',
                            'context': '',
                        })

            prev_emotion = dominant
            prev_chapter = cd['chapter']

    # 优先级排序
    type_order = {'forbidden_word': 0, 'emotion_spike': 1}
    warnings.sort(key=lambda w: type_order.get(w['type'], 2))

    return {
        'total_chapters': len(chapter_files),
        'profiles': profiles,
        'chapter_data': chapter_data,
        'warnings': warnings,
    }


def print_report(novel_dir: Path, results: dict):
    """打印人物一致性报告"""
    print('\n' + '=' * 60)
    print('人物一致性检查报告')
    print('=' * 60)
    print(f'小说：{novel_dir.name}')
    print(f'检查章节：{results["total_chapters"]}章')
    print(f'人物档案：{len(results["profiles"])}个')
    print()

    # 人物概览
    print('【人物出现统计】')
    for cd in results['chapter_data']:
        mentions_str = ', '.join(
            f'{name}({data["appearances"]}次)' for name, data in cd['mentions'].items()
        )
        if mentions_str:
            print(f"  第{cd['chapter']:2d}章：{mentions_str}")
    print()

    # 警告
    if results['warnings']:
        warn_icons = {'forbidden_word': '🔴', 'emotion_spike': '🟡'}
        print('【警告】')
        for w in results['warnings']:
            icon = warn_icons.get(w['type'], '⚠️')
            if w['context']:
                print(f"  {icon} 第{w['chapter']}章 | {w['character']} | {w['detail']}")
                print(f"      上下文：{w['context']}")
            else:
                print(f"  {icon} 第{w['chapter']}章 | {w['character']} | {w['detail']}")
        print()
    else:
        print('✅ 未检测到明显的人物一致性问题\n')

    print('=' * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法：python scripts/character_tracker.py <小说目录路径>')
        print('示例：python scripts/character_tracker.py novels/书名')
        return

    novel_dir = Path(sys.argv[1])
    if not novel_dir.exists():
        print(f'错误：目录不存在 - {novel_dir}')
        return

    results = check_consistency(novel_dir)
    if 'error' in results:
        print(f'错误：{results["error"]}')
        return

    print_report(novel_dir, results)


if __name__ == '__main__':
    main()
