#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI味检测脚本
检测章节文件中的AI写作痕迹，提供量化报告和改进建议
"""

import re
import sys
import math
from pathlib import Path
from collections import Counter

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# AI味检测规则
AI_PATTERNS = {
    'vague_adjectives': {
        'name': '空泛形容词',
        'patterns': [
            r'很\w{1,3}的',           # "很悲伤的", "很开心的"
            r'非常\w{1,3}的',         # "非常高兴的"
            r'无比\w{1,3}的',         # "无比激动的"
            r'十分\w{1,3}的',         # "十分生气的"
            r'相当\w{1,3}的',         # "相当不错的"
            r'特别\w{1,3}的',         # "特别重要的"
            r'极其\w{1,3}的',         # "极其危险的"
            r'格外\w{1,3}的',         # "格外美丽的"
        ],
        'threshold': 3,  # 每千字阈值
        'severity': 'high',
        'suggestion': '用具体动作或细节替代抽象形容词，如"他很悲伤"→"他盯着手机屏幕，拇指在玻璃上滑了三次"'
    },
    'four_char_idioms': {
        'name': '四字成语堆砌',
        'patterns': [
            r'[\u4e00-\u9fa9]{4}(?=[，。！？、\s])',  # 四字词
        ],
        'common_idioms': [  # 常见成语列表（可选，用于提高精度）
            '情不自禁', '不由自主', '心潮澎湃', '思绪万千', '百感交集',
            '恍然大悟', '若有所思', '目不转睛', '聚精会神', '全神贯注',
            '忐忑不安', '心惊胆战', '惶恐不安', '惊慌失措', '大惊失色',
            '喜出望外', '欣喜若狂', '兴高采烈', '眉开眼笑', '笑容满面',
            '愁眉苦脸', '垂头丧气', '无精打采', '闷闷不乐', '唉声叹气',
            '忐忑不安', '心神不宁', '坐立不安', '魂不守舍', '心不在焉',
            '感慨万千', '不胜唏嘘', '百感交集', '五味杂陈', '难以言表',
        ],
        'threshold': 5,  # 每千字阈值
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
        'threshold': 8,  # 每千字阈值
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
        'threshold': 5,  # 每章阈值
        'severity': 'low',
        'suggestion': '控制时间转折词频率，用场景自然过渡替代。如"突然门开了"→"门开了"'
    },
    'emotion_tags': {
        'name': '情绪标签句',
        'patterns': [
            r'[他她它]感到.*?的',           # "他感到前所未有的..."
            r'[他她它]心中.*?的',           # "他心中涌起..."
            r'[他她它]心里.*?的',           # "他心里一阵..."
            r'[他她它]的.?里.*?的',          # "他的心里..."
            r'一种.?的感觉涌上心头',
            r'[他她它]不禁',                 # "他不禁感到..."
            r'[他她它]不由得',               # "他不由得..."
            r'前所未有的',                  # "前所未有的孤独"
        ],
        'threshold': 2,  # 每千字阈值
        'severity': 'high',
        'suggestion': '用动作和细节展示情绪，而非直接标签。如"他感到悲伤"→"他低下头，盯着地面"'
    },
    'uniform_sentences': {
        'name': '句式均匀度',
        'check_func': 'check_sentence_variety',  # 特殊处理函数
        'threshold': 10,  # 句长标准差阈值
        'severity': 'low',
        'suggestion': '增加句式变化：短句破开长句、倒装句、省略句、碎片化表达'
    }
}


def extract_text_from_chapter(file_path: Path) -> str:
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

    # 兼容旧模板
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('#') and '章' in line:
            content_start = i + 1
            break

    return '\n'.join(lines[content_start:])


def count_chinese_words(text: str) -> int:
    """统计中文字数"""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def split_sentences(text: str) -> list:
    """分句（简化版）"""
    # 按句号、感叹号、问号分句
    sentences = re.split(r'[。！？]+', text)
    return [s.strip() for s in sentences if s.strip()]


def calculate_sentence_std(sentences: list) -> float:
    """计算句长标准差"""
    if len(sentences) < 2:
        return 0
    
    lengths = [count_chinese_words(s) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    return math.sqrt(variance)


def check_pattern(text: str, pattern_name: str) -> tuple:
    """检查特定AI味模式"""
    pattern_info = AI_PATTERNS[pattern_name]
    
    if 'check_func' in pattern_info:
        # 特殊处理（如句式均匀度）
        if pattern_info['check_func'] == 'check_sentence_variety':
            sentences = split_sentences(text)
            if len(sentences) < 5:
                return 0, 0, []
            std = calculate_sentence_std(sentences)
            return std, std, []  # 直接返回标准差
    
    patterns = pattern_info['patterns']
    matches = []
    
    if isinstance(patterns, list):
        for pattern in patterns:
            if isinstance(pattern, str) and not pattern.startswith(r'\'):
                # 普通字符串匹配
                if len(pattern) < 10:  # 短词，用简单包含检查
                    count = text.count(pattern)
                    if count > 0:
                        matches.extend([pattern] * count)
                else:
                    found = re.findall(pattern, text)
                    matches.extend(found)
            else:
                # 正则匹配
                found = re.findall(pattern, text)
                matches.extend(found)
    
    count = len(matches)
    
    # 如果是成语，过滤常见成语（可选）
    if pattern_name == 'four_char_idioms' and 'common_idioms' in pattern_info:
        common = pattern_info['common_idioms']
        matches = [m for m in matches if m in common]
        count = len(matches)
    
    return count, count, matches[:5]  # 返回前5个示例


def calculate_severity_score(check_results: dict, total_words: int) -> dict:
    """计算严重程度和AI味评级"""
    total_score = 0
    severity_weights = {'high': 3, 'medium': 2, 'low': 1}
    
    for pattern_name, result in check_results.items():
        if pattern_name == 'uniform_sentences':
            continue
        
        info = AI_PATTERNS[pattern_name]
        count = result['count']
        threshold = info['threshold']
        severity = info['severity']
        
        # 计算超标倍数
        words_per_thousand = total_words / 1000 if total_words > 0 else 1
        if pattern_name == 'time_transitions':
            # 按章计算，不按千字
            ratio = count / threshold if threshold > 0 else 0
        else:
            ratio = (count / words_per_thousand) / threshold if threshold > 0 else 0
        
        weight = severity_weights.get(severity, 1)
        total_score += ratio * weight
    
    # 句式均匀度扣分
    if 'uniform_sentences' in check_results:
        std = check_results['uniform_sentences']['count']
        if std < 10:
            total_score += (10 - std) * 0.5
    
    # 评级
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
        'score': total_score,
        'rating': rating,
        'rating_emoji': rating_emoji
    }


def check_ai_style(file_path: str) -> dict:
    """检查单个文件的AI味"""
    path = Path(file_path)
    
    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'error': f'文件不存在: {file_path}'
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
    
    # 执行各项检查
    results = {}
    for pattern_name, info in AI_PATTERNS.items():
        count, raw_count, examples = check_pattern(text, pattern_name)
        
        threshold = info['threshold']
        
        # 计算每千字频次
        if pattern_name == 'time_transitions':
            # 按章计算
            density = count
            threshold_display = f'<{threshold}/章'
        else:
            density = (count / total_words) * 1000 if total_words > 0 else 0
            threshold_display = f'<{threshold}/千字'
        
        status = '✅' if density <= threshold else '❌'
        
        results[pattern_name] = {
            'name': info['name'],
            'count': count,
            'density': round(density, 2),
            'threshold': threshold,
            'threshold_display': threshold_display,
            'severity': info['severity'],
            'status': status,
            'suggestion': info['suggestion'],
            'examples': examples
        }
    
    # 计算总体评级
    severity = calculate_severity_score(results, total_words)
    
    return {
        'file': str(path),
        'exists': True,
        'word_count': total_words,
        'check_results': results,
        'severity': severity
    }


def print_report(result: dict):
    """打印检测报告"""
    if not result['exists']:
        print(f'❌ {result["error"]}')
        return
    
    if 'error' in result:
        print(f'⚠️  {result["error"]}')
        return
    
    print('\n' + '=' * 70)
    print(f'🤖 AI味检测报告')
    print('=' * 70)
    print(f'\n📄 文件: {Path(result["file"]).name}')
    print(f'📝 字数: {result["word_count"]:,} 字')
    
    severity = result['severity']
    print(f'\n{severity["rating_emoji"]} AI味评级: {severity["rating"]} (综合得分: {severity["score"]:.1f})')
    
    print('\n' + '-' * 70)
    print('详细检测结果:')
    print('-' * 70)
    
    # 按严重程度排序
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
        print(f'   当前: {density} | 阈值: {threshold_display}')
        
        if check['examples']:
            print(f'   示例: {", ".join(check["examples"][:3])}')
        
        if status == '❌':
            print(f'   💡 建议: {check["suggestion"][:60]}...')
    
    print('\n' + '=' * 70)
    
    # 总结建议
    if severity['rating'] == '重度':
        print('\n⚠️  重度AI味警告')
        print('   建议重写本章，重点参考以下改进方向:')
        print('   1. 用具体动作替代情绪标签（"他很悲伤"→"他低着头"）')
        print('   2. 减少成语和四字词堆砌')
        print('   3. 增加句式变化，使用短句、省略句')
    elif severity['rating'] == '中度':
        print('\n💡 中度AI味，建议优化以下方面:')
        failed_checks = [c for c in result['check_results'].values() if c['status'] == '❌']
        for i, check in enumerate(failed_checks[:3], 1):
            print(f'   {i}. {check["name"]}: {check["suggestion"][:50]}...')
    else:
        print('\n✅ AI味控制良好，保持当前写作风格')
    
    print('\n📚 参考文档: references/style-polishing.md')
    print('=' * 70 + '\n')


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法:')
        print('  python scripts/check_ai_style.py <章节文件路径>')
        print('')
        print('示例:')
        print('  python scripts/check_ai_style.py novels/故事/第01章.md')
        return
    
    file_path = sys.argv[1]
    result = check_ai_style(file_path)
    print_report(result)


if __name__ == '__main__':
    main()
