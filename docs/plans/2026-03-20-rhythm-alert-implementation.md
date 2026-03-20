# Rhythm Alert Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create rhythm alert system with check_rhythm.py script and rhythm health report template.

**Architecture:**
1. Create `scripts/check_rhythm.py` - scans chapters, generates health report
2. Create `references/05-节奏健康报告.md` - report template
3. Update `SKILL.md` - add rhythm check instructions

**Tech Stack:** Python script + Markdown templates.

---

## Task 1: Create check_rhythm.py Script

**Files:**
- Create: `scripts/check_rhythm.py`

**Step 1: Write the script**

Create the script with the following functionality:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节奏检查脚本
检查小说章节的节奏健康状态，生成报告
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
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def detect_scene_type(text: str) -> str:
    """简单检测场景类型"""
    # 基于关键词判断
    indoor_keywords = ['房间', '室内', '屋里', '屋内', '客厅', '卧室', '办公室', '教室']
    outdoor_keywords = ['外面', '户外', '街道', '路上', '天空', '花园', '广场', '野外']
    dialogue_keywords = ['说', '问', '答', '道', '喊', '叫', '对话', '聊天']

    indoor_count = sum(1 for kw in indoor_keywords if kw in text)
    outdoor_count = sum(1 for kw in outdoor_keywords if kw in text)
    dialogue_count = sum(1 for kw in dialogue_keywords if kw in text)

    if indoor_count > outdoor_count and indoor_count > dialogue_count:
        return '室内对话'
    elif outdoor_count > indoor_count:
        return '户外'
    elif dialogue_count > 0:
        return '对话为主'
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

        # 提取章节号
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

    # 字数统计
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    max_words = max(word_counts) if word_counts else 0
    min_words = min(word_counts) if word_counts else 0

    return {
        'chapters': chapters,
        'word_counts': word_counts,
        'scene_types': scene_types,
        'scene_warnings': scene_warnings,
        'avg_words': avg_words,
        'max_words': max_words,
        'min_words': min_words,
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

    # 场景警告
    if results.get('scene_warnings'):
        print('【警告】场景重复')
        for warning in results['scene_warnings']:
            print(f'  ⚠️ {warning}')
        print()

    # 字数统计
    print('【字数统计】')
    print(f'  平均：{results["avg_words"]:.0f}字/章')
    print(f'  最高：{results["max_words"]:,}字')
    print(f'  最低：{results["min_words"]:,}字')
    print()

    # 章节列表
    print('【章节概览】')
    for ch in results['chapters']:
        print(f"  第{ch['number']:2d}章: {ch['word_count']:,}字 | {ch['scene_type']}")
    print()

    if not results.get('scene_warnings') and not results.get('foreshadowing_warnings'):
        print('【状态】节奏健康，无明显警告')
    print('=' * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('用法: python scripts/check_rhythm.py <小说目录路径>')
        return

    novel_dir = Path(sys.argv[1])
    if not novel_dir.exists():
        print(f'错误: 目录不存在 - {novel_dir}')
        return

    results = check_chapters(novel_dir)
    print_report(novel_dir, results)


if __name__ == '__main__':
    main()
```

**Step 2: Commit**

```bash
git add scripts/check_rhythm.py
git commit -m "feat: add rhythm check script

Add scripts/check_rhythm.py for checking rhythm health:
- Scene type detection (indoor/outdoor/dialogue)
- Scene repetition warnings (3+ consecutive chapters)
- Word count statistics
- Chapter overview table

Usage: python scripts/check_rhythm.py <novel_dir>

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 2: Create 05-节奏健康报告.md Template

**Files:**
- Create: `references/05-节奏健康报告.md`

**Step 1: Write the template**

```markdown
# 节奏健康报告

> 每写完5-10章后生成一次，记录节奏健康状态。

## 基本信息
- 报告日期：
- 检查范围：第X章 - 第Y章
- 章节数量：N章
- 累计字数：

## 场景分析

### 场景类型分布
| 场景类型 | 出现次数 | 占比 |
|----------|----------|------|
| 室内对话 | 5 | 25% |
| 户外 | 3 | 15% |
| 动作 | 2 | 10% |
| 其他 | 10 | 50% |

### 警告
- [ ] 场景类型重复超过3章

## 伏笔跟踪

### 伏笔状态
| 伏笔 | 首次出现 | 最近回收 | 状态 |
|------|----------|----------|------|
| 神秘信封 | 第2章 | - | ⚠️ 未回收 |
| 反派身份 | 第5章 | 第8章 | ✅ 已回收 |

### 警告
- [ ] 有伏笔超过10章未回收

## 字数分析

### 统计
- 总字数：
- 平均字数：
- 最高章节：第X章（XXXX字）
- 最低章节：第Y章（XXXX字）

### 警告
- [ ] 有章节低于2000字
- [ ] 有章节超过5000字

## 钩子强度

### 章节钩子评分
| 章节 | 字数 | 钩子强度 | 备注 |
|------|------|----------|------|
| 第1章 | 3200 | ★★★★☆ | 悬念感强 |
| 第2章 | 2800 | ★★★☆☆ | 结尾略平 |
| ... | ... | ... | ... |

### 评分标准
- ★★★★★：强悬念（死亡威胁、重大揭示）
- ★★★★☆：明确悬念（未解问题、新危机）
- ★★★☆☆：一般悬念（轻微好奇）
- ★★☆☆☆：结尾较弱
- ★☆☆☆☆：平结尾

### 警告
- [ ] 有章节钩子强度低于2星

## 多线均衡（如适用）

### 叙事线状态
| 叙事线 | 最后出现 | 间隔章节 | 状态 |
|--------|----------|----------|------|
| 主线 | 第10章 | 0 | ✅ |
| 副线A | 第2章 | 8 | ⚠️ |
| 副线B | 第9章 | 1 | ✅ |

### 状态标准
- ✅ 正常（最近5章内出现过）
- ⚠️ 警告（5-8章未出现）
- 🔴 危险（超过8章未出现）

### 警告
- [ ] 有叙事线超过8章未出现

## 综合评估

**健康得分：** ★★★★☆ (4/5)

**主要问题：**
1. 副线A消失太久，需要安排出场
2. 室内对话场景过多

**建议：**
1. 下1-2章优先让副线A出现
2. 增加户外或动作场景平衡
3. 第6章结尾需要加强钩子
```

**Step 2: Commit**

```bash
git add references/05-节奏健康报告.md
git commit -m "feat: add rhythm health report template

Add references/05-节奏健康报告.md template:
- Basic info section
- Scene analysis with distribution table
- Foreshadowing tracking table
- Word count statistics
- Hook strength rating per chapter
- Multi-line balance check (if applicable)
- Overall health score and recommendations

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Task 3: Update SKILL.md

**Files:**
- Modify: `SKILL.md`

**Step 1: Find where to add rhythm check instructions**

Find the 修改工作流 section or the 精修模式 section and add a note about rhythm checks.

**Step 2: Add to 修改工作流 or create a reference**

In the 修改工作流 section's "第四步：验证" step, add a note about running rhythm checks.

Or add a new section reference in the "健康检查" part.

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: add rhythm check instructions to SKILL.md

Add reference to check_rhythm.py script and rhythm health report
template in the revision workflow or as a periodic check.

---

**Authored by Henry Zhang**

Website: <https://zhanghe.dev>

Contact: <hello@zhanghe.dev>"
```

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| 1 | Create scripts/check_rhythm.py | ⬜ |
| 2 | Create references/05-节奏健康报告.md | ⬜ |
| 3 | Update SKILL.md with rhythm check info | ⬜ |
