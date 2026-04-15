#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 味检测脚本
检测章节文件中的 9 种 AI 写作痕迹，提供量化报告和改进建议
支持单文件和批量检测（--all）
"""

import re
import sys
import math
from pathlib import Path

# Ensure scripts/ directory is in path for utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, count_chinese_words, find_chapter_files, setup_windows_encoding

setup_windows_encoding()


# AI 味检测规则（9 种症状，与 SKILL.md 和 ai-style-examples.md 对齐）
AI_PATTERNS = {
    'vague_adjectives': {
        'name': '空泛形容词',
        'patterns': [
            r'很\w{1,3}的',
            r'非常\w{1,3}的',
            r'无比\w{1,3}的',
            r'十分\w{1,3}的',
            r'相当\w{1,3}的',
            r'特别\w{1,3}的',
            r'极其\w{1,3}的',
            r'格外\w{1,3}的',
        ],
        'threshold': 3,
        'severity': 'high',
        'suggestion': '用具体动作或细节替代抽象形容词，如"他很悲伤"→"他盯着手机屏幕，拇指在玻璃上滑了三次"'
    },
    'four_char_idioms': {
        'name': '四字成语堆砌',
        'check_func': 'check_four_char_idioms',
        'common_idioms': {
            '情不自禁', '不由自主', '心潮澎湃', '思绪万千', '百感交集',
            '恍然大悟', '若有所思', '目不转睛', '聚精会神', '全神贯注',
            '忐忑不安', '心惊胆战', '惶恐不安', '惊慌失措', '大惊失色',
            '喜出望外', '欣喜若狂', '兴高采烈', '眉开眼笑', '笑容满面',
            '愁眉苦脸', '垂头丧气', '无精打采', '闷闷不乐', '唉声叹气',
            '心神不宁', '坐立不安', '魂不守舍', '心不在焉',
            '感慨万千', '不胜唏嘘', '五味杂陈', '难以言表',
            '心旷神怡', '义正辞严', '义愤填膺', '忧心忡忡',
            '瞠目结舌', '不寒而栗', '毛骨悚然', '如释重负',
            '心领神会', '心照不宣', '暗自心惊', '面如死灰',
        },
        'threshold': 5,
        'severity': 'medium',
        'suggestion': '减少成语使用，用自然描述替代。如"他喜出望外"→"他差点撞上门框"'
    },
    'explanatory_connectors': {
        'name': '解释性连接词',
        'patterns': [
            r'然而', '不过', '可是', '但是',
            r'因为', '由于', '因此', '所以',
            r'虽然', '尽管', '即使',
            r'而且', '并且', '同时',
            r'其实', '事实上', '实际上',
            r'这意味着', '这表明', '这说明',
            r'某种程度上', '从某种意义上',
            r'不难看出', '显而易见',
            r'总而言之', '总的来说',
        ],
        'threshold': 8,
        'severity': 'medium',
        'suggestion': '减少解释性连接词，让情节自然推进。如"然而他并不知道"→直接写"他不知道"'
    },
    'time_transitions': {
        'name': '时间转折词滥用',
        'patterns': [
            r'突然', '忽然', '猛然', '骤然',
            r'就在这时', '就在此时', '正在这时',
            r'下一秒', '下一刻', '转眼间',
            r'紧接着', '随即', '立刻', '马上',
            r'与此同时', '另一边', '另一边厢',
        ],
        'threshold': 5,
        'unit': 'chapter',
        'severity': 'low',
        'suggestion': '控制时间转折词频率，用场景自然过渡替代。如"突然门开了"→"门开了"'
    },
    'emotion_tags': {
        'name': '情绪标签句',
        'patterns': [
            r'[他她它]感到.*?的',
            r'[他她它]心中.*?的',
            r'[他她它]心里.*?的',
            r'[他她它]的.?里.*?的',
            r'一种.?的感觉涌上心头',
            r'[他她它]不禁',
            r'[他她它]不由得',
            r'前所未有的',
        ],
        'threshold': 2,
        'severity': 'high',
        'suggestion': '用动作和细节展示情绪，而非直接标签。如"他感到悲伤"→"他低下头，盯着地面"'
    },
    'stiff_dialogue': {
        'name': '过度书面化对白',
        'patterns': [
            r'"[^"]{0,5}(认为|认为这个|假设|假设存在|建议|提议|表示)[^"]*"',
            r'"[^"]{0,10}(有必要|不可或缺|至关重要|值得注意)[^"]*"',
            r'"[^"]*(也就是说|换言之|简而言之|综上所述)[^"]*"',
            r'"[^"]*(首先|其次|最后|第一|第二)[^"]{5,}"',
        ],
        'threshold': 2,
        'severity': 'medium',
        'suggestion': '对白应口语化，如"我认为这个假设存在漏洞"→"扯淡，这说法有三个问题"'
    },
    'pov_confusion': {
        'name': '视角混乱',
        'check_func': 'check_pov_confusion',
        'threshold': 2,
        'severity': 'high',
        'suggestion': '同一段内不应切换多个角色的内心视角。用对话和动作替代跳转'
    },
    'info_dump': {
        'name': '信息倾倒',
        'check_func': 'check_info_dump',
        'threshold': 2,
        'severity': 'medium',
        'suggestion': '背景信息应嵌入对话和行动，而非整段说明。每段不超过 3 句纯说明'
    },
    'uniform_sentences': {
        'name': '句式均匀度',
        'check_func': 'check_sentence_variety',
        'threshold': 10,
        'severity': 'low',
        'suggestion': '增加句式变化：短句破开长句、倒装句、省略句、碎片化表达'
    }
}


def check_four_char_idioms(text: str, pattern_info: dict) -> tuple:
    """检查四字成语堆砌——只匹配已知成语列表，避免误杀"""
    common = pattern_info['common_idioms']
    matches = []
    for idiom in common:
        count = text.count(idiom)
        if count > 0:
            matches.extend([idiom] * count)
    return len(matches), len(matches), matches[:5]


def check_pov_confusion(text: str, pattern_info: dict) -> tuple:
    """检查视角混乱——同一段内切换多个角色内心"""
    paragraphs = text.split('\n\n')
    matches = []
    pov_pattern = re.compile(r'([他她它])[^\n]{0,20}(想|觉得|感到|知道|明白|意识到|心[中里])')

    for para in paragraphs:
        found_persons = set()
        for m in pov_pattern.finditer(para):
            found_persons.add(m.group(1))
        # 如果同一段内出现"他想"+"她想"等混合人称内心，标记
        if len(found_persons) >= 2:
            matches.append(para[:50] + '...' if len(para) > 50 else para)

    return len(matches), len(matches), matches[:3]


def check_info_dump(text: str, pattern_info: dict) -> tuple:
    """检查信息倾倒——连续 3 句以上纯说明性内容（无对话、无动作、无情感反应）"""
    paragraphs = text.split('\n\n')
    matches = []
    has_dialogue = re.compile(r'["「『]')
    has_action = re.compile(r'[他她]([走跑坐站拿推拉打挥握伸点头摇头叹息微笑皱眉咬握紧攥])')

    for para in paragraphs:
        sentences = [s.strip() for s in re.split(r'[。！？]', para) if s.strip()]
        if len(sentences) < 3:
            continue
        consecutive_exposition = 0
        for sent in sentences:
            is_exposition = not has_dialogue.search(sent) and not has_action.search(sent)
            if is_exposition:
                consecutive_exposition += 1
            else:
                consecutive_exposition = 0
        if consecutive_exposition >= 3:
            matches.append(para[:60] + '...' if len(para) > 60 else para)

    return len(matches), len(matches), matches[:3]


def check_sentence_variety(text: str, pattern_info: dict) -> tuple:
    """检查句式均匀度——句长标准差"""
    sentences = re.split(r'[。！？]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) < 5:
        return 0, 0, []

    lengths = [count_chinese_words(s) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    std = math.sqrt(variance)

    return std, std, []


def check_pattern(text: str, pattern_name: str) -> tuple:
    """检查特定 AI 味模式"""
    pattern_info = AI_PATTERNS[pattern_name]

    # 特殊处理函数
    if 'check_func' in pattern_info:
        func_name = pattern_info['check_func']
        func_map = {
            'check_four_char_idioms': check_four_char_idioms,
            'check_pov_confusion': check_pov_confusion,
            'check_info_dump': check_info_dump,
            'check_sentence_variety': check_sentence_variety,
        }
        func = func_map.get(func_name)
        if func:
            return func(text, pattern_info)
        return 0, 0, []

    patterns = pattern_info['patterns']
    matches = []

    if isinstance(patterns, list):
        for pattern in patterns:
            if isinstance(pattern, str) and not pattern.startswith('\\'):
                count = text.count(pattern)
                if count > 0:
                    matches.extend([pattern] * count)
            else:
                found = re.findall(pattern, text)
                matches.extend(found)

    count = len(matches)
    return count, count, matches[:5]


def calculate_severity_score(check_results: dict, total_words: int) -> dict:
    """计算严重程度和 AI 味评级"""
    total_score = 0
    severity_weights = {'high': 3, 'medium': 2, 'low': 1}

    for pattern_name, result in check_results.items():
        if pattern_name in ('uniform_sentences', 'pov_confusion', 'info_dump'):
            if pattern_name == 'uniform_sentences':
                std = result['count']
                if std < 10:
                    total_score += (10 - std) * 0.5
            elif pattern_name == 'pov_confusion':
                ratio = result['count'] / AI_PATTERNS[pattern_name]['threshold'] if AI_PATTERNS[pattern_name]['threshold'] > 0 else 0
                total_score += ratio * 3
            elif pattern_name == 'info_dump':
                ratio = result['count'] / AI_PATTERNS[pattern_name]['threshold'] if AI_PATTERNS[pattern_name]['threshold'] > 0 else 0
                total_score += ratio * 2
            continue

        info = AI_PATTERNS[pattern_name]
        count = result['count']
        threshold = info['threshold']
        severity = info['severity']

        words_per_thousand = total_words / 1000 if total_words > 0 else 1
        if info.get('unit') == 'chapter':
            ratio = count / threshold if threshold > 0 else 0
        else:
            ratio = (count / words_per_thousand) / threshold if threshold > 0 else 0

        weight = severity_weights.get(severity, 1)
        total_score += ratio * weight

    if total_score < 3:
        rating = '轻度'
        rating_emoji = '🟢'
    elif total_score < 6:
        rating = '中度'
        rating_emoji = '🟡'
    else:
        rating = '重度'
        rating_emoji = '🔴'

    return {
        'score': round(total_score, 1),
        'rating': rating,
        'rating_emoji': rating_emoji
    }


def check_ai_style(file_path: str) -> dict:
    """检查单个文件的 AI 味"""
    path = Path(file_path)

    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'error': f'文件不存在：{file_path}'
        }

    text = extract_text_from_chapter(path)
    total_words = count_chinese_words(text)

    if total_words == 0:
        return {
            'file': str(path),
            'exists': True,
            'word_count': 0,
            'error': '未检测到正文内容'
        }

    results = {}
    for pattern_name, info in AI_PATTERNS.items():
        count, raw_count, examples = check_pattern(text, pattern_name)

        threshold = info['threshold']

        if info.get('unit') == 'chapter':
            density = count
            threshold_display = f'<{threshold}/章'
        elif pattern_name == 'uniform_sentences':
            density = round(count, 1)
            threshold_display = f'>{threshold}'
        else:
            density = round((count / total_words) * 1000, 2) if total_words > 0 else 0
            threshold_display = f'<{threshold}/千字'

        if pattern_name == 'uniform_sentences':
            status = '✅' if density >= threshold else '❌'
        elif pattern_name in ('pov_confusion', 'info_dump'):
            status = '✅' if count <= threshold else '❌'
        else:
            status = '✅' if density <= threshold else '❌'

        results[pattern_name] = {
            'name': info['name'],
            'count': count,
            'density': density,
            'threshold': threshold,
            'threshold_display': threshold_display,
            'severity': info['severity'],
            'status': status,
            'suggestion': info['suggestion'],
            'examples': examples
        }

    severity = calculate_severity_score(results, total_words)

    return {
        'file': str(path),
        'exists': True,
        'word_count': total_words,
        'check_results': results,
        'severity': severity
    }


def print_report(result: dict):
    """打印单个文件的检测报告"""
    if not result.get('exists', False):
        print(f'❌ {result.get("error", "文件不存在")}')
        return

    if 'error' in result:
        print(f'⚠️  {result["error"]}')
        return

    print('\n' + '=' * 70)
    print('🤖 AI 味检测报告')
    print('=' * 70)
    print(f'\n📄 文件：{Path(result["file"]).name}')
    print(f'📝 字数：{result["word_count"]:,} 字')

    severity = result['severity']
    print(f'\n{severity["rating_emoji"]} AI 味评级：{severity["rating"]} (综合得分：{severity["score"]})')

    print('\n' + '-' * 70)
    print('详细检测结果：')
    print('-' * 70)

    sorted_results = sorted(
        result['check_results'].items(),
        key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x[1]['severity'], 3)
    )

    for pattern_name, check in sorted_results:
        status = check['status']
        name = check['name']
        density = check['density']
        threshold_display = check['threshold_display']
        severity_level = check['severity']

        severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(severity_level, '⚪')

        print(f'\n{status} {severity_icon} {name}')
        print(f'   当前：{density} | 阈值：{threshold_display}')

        if check['examples']:
            ex_str = ', '.join(str(e)[:30] for e in check['examples'][:3])
            print(f'   示例：{ex_str}')

        if status == '❌':
            suggestion = check['suggestion']
            print(f'   💡 建议：{suggestion[:60]}{"..." if len(suggestion) > 60 else ""}')

    print('\n' + '=' * 70)

    if severity['rating'] == '重度':
        print('\n⚠️  重度 AI 味警告')
        print('   建议重写本章，重点参考以下改进方向：')
        print('   1. 用具体动作替代情绪标签（"他很悲伤"→"他低着头"）')
        print('   2. 减少成语和四字词堆砌')
        print('   3. 增加句式变化，使用短句、省略句')
        failed = [c for c in result['check_results'].values() if c['status'] == '❌']
        if failed:
            print(f'   4. 重点修复：{", ".join(c["name"] for c in failed[:3])}')
    elif severity['rating'] == '中度':
        print('\n💡 中度 AI 味，建议优化以下方面：')
        failed_checks = [c for c in result['check_results'].values() if c['status'] == '❌']
        for i, check in enumerate(failed_checks[:3], 1):
            print(f'   {i}. {check["name"]}: {check["suggestion"][:50]}...')
    else:
        print('\n✅ AI 味控制良好，保持当前写作风格')

    print('\n📚 参考文档：references/ai-style-examples.md')
    print('=' * 70 + '\n')


def print_batch_summary(results: list):
    """打印批量检测结果摘要"""
    print('\n' + '=' * 70)
    print('🤖 AI 味批量检测报告')
    print('=' * 70)

    total = len(results)
    mild = sum(1 for r in results if r.get('severity', {}).get('rating') == '轻度')
    moderate = sum(1 for r in results if r.get('severity', {}).get('rating') == '中度')
    severe = sum(1 for r in results if r.get('severity', {}).get('rating') == '重度')
    errors = sum(1 for r in results if 'error' in r and r.get('exists', True))

    print(f'\n📊 总览：{total} 章 | 🟢轻度 {mild} | 🟡中度 {moderate} | 🔴重度 {severe} | ⚠️错误 {errors}')

    # 按严重程度排序
    severity_order = {'重度': 0, '中度': 1, '轻度': 2}
    valid_results = [r for r in results if 'severity' in r]
    valid_results.sort(key=lambda r: severity_order.get(r['severity']['rating'], 3))

    print('\n' + '-' * 70)
    print(f'{"章节":<30} {"字数":>6} {"评级":>6} {"得分":>6} {"主要问题"}')
    print('-' * 70)

    for r in valid_results:
        name = Path(r['file']).name
        word_count = r['word_count']
        rating = r['severity']['rating']
        score = r['severity']['score']

        failed = [c['name'] for c in r['check_results'].values() if c['status'] == '❌']
        issues = ', '.join(failed[:2]) if failed else '—'

        print(f'{name:<30} {word_count:>6,} {rating:>6} {score:>6} {issues}')

    if severe > 0:
        print(f'\n⚠️  {severe} 章重度 AI 味，建议优先重写')
    if moderate > 0:
        print(f'💡 {moderate} 章中度 AI 味，建议针对性优化')

    print('\n📚 参考文档：references/ai-style-examples.md')
    print('=' * 70 + '\n')


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法：')
        print('  python scripts/check_ai_style.py <章节文件路径>')
        print('  python scripts/check_ai_style.py --all <小说目录路径>')
        print('')
        print('示例：')
        print('  python scripts/check_ai_style.py novels/故事/第01章.md')
        print('  python scripts/check_ai_style.py --all novels/故事')
        return

    if sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print('错误：使用 --all 时需要指定目录路径')
            return
        novel_dir = Path(sys.argv[2])
        if not novel_dir.exists():
            print(f'错误：目录不存在 - {novel_dir}')
            return

        chapter_files = find_chapter_files(novel_dir)
        if not chapter_files:
            print('未找到章节文件')
            return

        all_results = []
        for chapter_file in chapter_files:
            result = check_ai_style(str(chapter_file))
            all_results.append(result)

        # 打印每个文件的简要结果
        for result in all_results:
            if 'error' in result and not result.get('exists', True):
                print(f'❌ {Path(result["file"]).name}: {result["error"]}')
                continue
            if 'error' in result:
                continue

            severity = result['severity']
            name = Path(result['file']).name
            failed = [c['name'] for c in result['check_results'].values() if c['status'] == '❌']
            if failed:
                print(f'{severity["rating_emoji"]} {name}: {severity["rating"]}（{", ".join(failed[:2])}超标）')
            else:
                print(f'✅ {name}: {severity["rating"]}')

        # 打印汇总
        print_batch_summary(all_results)
    else:
        file_path = sys.argv[1]
        result = check_ai_style(file_path)
        print_report(result)


if __name__ == '__main__':
    main()
