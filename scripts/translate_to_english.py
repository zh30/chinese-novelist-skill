#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Current AI Translation Task Generator
为当前 AI 准备中文小说意译翻译任务包
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, find_chapter_files

# 修复编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def extract_novel_info(novel_dir: Path) -> dict:
    """提取小说基本信息"""
    info = {
        'title': 'Unknown Title',
        'author': 'Unknown Author',
        'genre': '',
        'synopsis': '',
        'characters': '',
        'worldbuilding': ''
    }

    # 提取大纲信息
    outline_path = novel_dir / '00-大纲.md'
    if outline_path.exists():
        with open(outline_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 书名
        title_match = re.search(r'^#\s*(.+?)\s*大纲', content, re.MULTILINE)
        if title_match:
            info['title'] = title_match.group(1).strip()

        # 作者
        author_match = re.search(r'\*\*作者\s*/\s*笔名\*\*[：:]\s*(.+)', content)
        if author_match:
            info['author'] = author_match.group(1).strip()

        # 类型
        genre_match = re.search(r'\*\*题材\s*/\s*类型\*\*[：:]\s*(.+)', content)
        if genre_match:
            info['genre'] = genre_match.group(1).strip()

        # 简介
        synopsis_match = re.search(r'\*\*一句话简介\*\*[：:]\s*(.+?)(?=\n\*\*|\Z)', content, re.DOTALL)
        if synopsis_match:
            info['synopsis'] = synopsis_match.group(1).strip()

    # 提取人物档案
    characters_path = novel_dir / '01-人物档案.md'
    if characters_path.exists():
        with open(characters_path, 'r', encoding='utf-8') as f:
            info['characters'] = f.read()

    # 提取世界观
    worldbuilding_path = novel_dir / '02-世界观与伏笔.md'
    if worldbuilding_path.exists():
        with open(worldbuilding_path, 'r', encoding='utf-8') as f:
            info['worldbuilding'] = f.read()

    return info


def extract_chapter_content(file_path: Path) -> str:
    """提取章节正文内容"""
    return extract_text_from_chapter(file_path)


def find_chapters(novel_dir: Path) -> list:
    """查找所有章节文件"""
    chapter_files = find_chapter_files(novel_dir, 'zh')
    chapters = []

    for chapter_file in chapter_files:
        # 从文件名提取章节号和标题
        match = re.match(r'第(\d+)章[-(]*(.+?)\.md$', chapter_file.name)
        if match:
            chapter_num = int(match.group(1))
            chapter_title = match.group(2)
        else:
            chapter_num = len(chapters) + 1
            chapter_title = chapter_file.stem

        content_title = _extract_plain_chapter_title(chapter_file)
        if content_title:
            chapter_title = content_title

        chapters.append({
            'file': chapter_file,
            'number': chapter_num,
            'title': chapter_title
        })

    return chapters


def _extract_plain_chapter_title(chapter_file: Path) -> str:
    """从干净章节首行提取标题。"""
    try:
        with open(chapter_file, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith('#'):
                    return ''
                if re.match(r'^第\s*\d+\s*章\b', stripped):
                    return stripped
                return ''
    except OSError:
        return ''
    return ''


def build_translation_prompt(
    novel_info: dict,
    chapter_content: str,
    chapter_title: str,
    chapter_number: int = None
) -> str:
    """构建翻译提示词"""
    chapter_label = f"Chapter {chapter_number}: " if chapter_number else "Chapter [number]: "
    prompt = f"""# 当前 AI 意译翻译任务 / Current AI Adaptive Translation Task

You are the current AI in this conversation. Translate the following Chinese novel chapter into fluent English using 意译翻译 / adaptive translation.

Do not translate word-for-word. Preserve the scene's intent, rhythm, emotional pressure, subtext, and character voice so the English reads like an original novel chapter, not a literal conversion.

Follow the project workflow files before drafting:
- 翻译简报: `../00-translation-brief.md`
- 术语表: `../01-termbase.md`
- 风格表: `../02-style-sheet.md`
- 查询日志: `../03-query-log.md`
- QA checklist: `../04-qa-checklist.md`

## Novel Information
- Title: {novel_info['title']}
- Author: {novel_info['author']}
- Genre: {novel_info['genre']}
- Synopsis: {novel_info['synopsis']}

## Characters
{novel_info['characters'][:2000] if novel_info['characters'] else 'N/A'}

## Worldview
{novel_info['worldbuilding'][:2000] if novel_info['worldbuilding'] else 'N/A'}

## Translation Requirements
1. Use 意译翻译 / adaptive translation as the default mode
2. Maintain the narrative rhythm and emotional tension
3. Use pinyin for character names (e.g., Zhang Wei)
4. Keep Chinese-specific terms (gongfu, qigong) with pinyin or explanatory translation
5. Use modern English, avoid stiff literal translations
6. Keep dialogue natural and fluent
7. Translate the chapter title as well
8. Finish with 译者自检: compare source and target for omissions, meaning drift, terminology, and formatting before saving

## Professional Stages For This Chapter
1. Pre-drafting: read the source for plot function, POV, register, imagery, and culture-specific problems.
2. Drafting: produce the adaptive English version according to the brief, termbase, and style sheet.
3. 译者自检: compare the source and draft line-by-line for omissions and changed facts.
4. 双语修订: run the separate revision task against the saved draft.
5. 单语润色: run the separate monolingual edit task on the revised English.

## Chapter Title
{chapter_title}

## Chapter to Translate
{chapter_content}

## Output Format
Provide only the plain translated Markdown chapter. Use exactly this structure:

{chapter_label}[translated chapter title]

[body text]

Rules:
- The first line contains only the chapter number and translated chapter title.
- Leave one blank line after the first line.
- Put the translated body text immediately after that blank line.
- Use no Markdown headings, section labels, translator notes, QA notes, or explanations.
"""
    return prompt


def extract_candidate_terms(novel_info: dict) -> list:
    """从人物档案和世界观中提取术语候选"""
    terms = []
    seen = set()
    sources = [
        ("人物", novel_info.get('characters', '')),
        ("世界观", novel_info.get('worldbuilding', '')),
    ]

    for category, content in sources:
        for line in content.splitlines():
            stripped = line.strip().lstrip("-*0123456789. ")
            if not stripped:
                continue

            if "：" in stripped:
                candidate = stripped.split("：", 1)[0].strip()
            elif ":" in stripped:
                candidate = stripped.split(":", 1)[0].strip()
            else:
                match = re.match(r'([\u4e00-\u9fff]{2,8})', stripped)
                candidate = match.group(1) if match else ""

            if not candidate or candidate in seen:
                continue
            if len(candidate) > 12:
                continue

            seen.add(candidate)
            terms.append((candidate, category))

    return terms


def build_translation_brief(novel_info: dict, task_count: int) -> str:
    """生成翻译项目简报"""
    return f"""# Translation Brief / 翻译简报

## 项目概况
- 书名: {novel_info['title']}
- 作者: {novel_info['author']}
- 类型: {novel_info['genre'] or '未注明'}
- 待处理章节数: {task_count}

## 翻译目的
将中文小说意译为自然、可读、具备英文小说叙事质感的英文版本。译文服务于阅读体验，不服务于逐字对照。

## 目标读者
- 主要读者: 英文小说读者，默认不熟悉中文网文术语。
- 阅读预期: 情节清楚、人物声音稳定、悬念和情绪压力能被直接感知。
- 文化处理: 核心文化设定保留质感，非核心表达转换为英文自然说法。

## 交付规格
- 每章文件: `manuscript/en/Chapter-XXX.md`
- 章节结构: 第一行写章数和章标题，空一行后直接写正文。
- 任务文件: `manuscript/en/_translation_tasks/Chapter-XXX.*.prompt.md`
- 查询日志: `manuscript/en/03-query-log.md`

## 第一性原则
1. 目的优先: 译文必须满足目标读者和出版交付目的。
2. 意义优先: 不牺牲事实、因果、伏笔、人物关系。
3. 效果优先: 悬念、张力、幽默、讽刺、压迫感要在英文中重新成立。
4. 一致性优先: 人名、术语、称谓、境界、地名和口吻必须全书统一。
5. 可验证优先: 每章经过译者自检、双语修订、单语润色和终检。

## 源文本摘要
{novel_info['synopsis'] or '未提供。翻译前应先通读大纲和相关章节补足。'}
"""


def build_termbase(novel_info: dict) -> str:
    """生成术语表模板"""
    rows = [
        "| 中文术语 | 英文处理 | 类型 | 说明 | 状态 |",
        "|----------|----------|------|------|------|",
    ]

    for term, category in extract_candidate_terms(novel_info):
        rows.append(f"| {term} | TBD | {category} | 从项目资料自动提取，当前 AI 翻译前确认 | 待定 |")

    if len(rows) == 2:
        rows.append("| TBD | TBD | 待定 | 翻译前由当前 AI 从章节中补充 | 待定 |")

    return """# Termbase / 术语表

使用规则：
- 人名默认拼音，除非用户或风格表另有规定。
- 地名、门派、法宝、境界等先入表再翻译，避免前后漂移。
- 修改术语时，同步检查已译章节。

""" + "\n".join(rows) + "\n"


def build_style_sheet(novel_info: dict) -> str:
    """生成英文风格表"""
    return f"""# Style Sheet / 风格表

## Voice And Tone
- 类型基调: {novel_info['genre'] or '按原文判断'}
- 英文口吻: 自然、清晰、有小说感；避免机器翻译腔。
- 叙述节奏: 保留原文的悬念推进和段落张力，可重组句子以贴合英文阅读。

## 意译边界
- 可以调整: 语序、分句/合句、语气词、俗语、隐喻表达、称谓的英文承载方式。
- 不可调整: 事件事实、人物动机、伏笔线索、关系状态、时间线、世界观规则。
- 需要查询: 双关、诗词、专名、制度称谓、文化负载词、可能影响后文伏笔的句子。

## Names And Terms
- 人名: 使用拼音，首字母大写。
- 称谓: 能自然转写时转写；承载关系张力时保留称谓感并解释。
- 文化词: 核心设定可保留拼音，普通表达转成自然英文。

## Dialogue
- 目标: 像英文人物真实说话，而不是中文句式套壳。
- 允许: 拆句、停顿、补足主语、调整语气。
- 禁止: 把人物声音统一成中性解释腔。
"""


def build_query_log() -> str:
    """生成查询日志模板"""
    return """# Query Log / 查询日志

| 编号 | 章节 | 原文问题 | 暂定处理 | 需要用户确认 | 状态 |
|------|------|----------|----------|--------------|------|
| Q001 | TBD | TBD | TBD | 否 | 待处理 |

使用规则：
- 不确定的双关、伏笔、专名、文化词先记录，不擅自定死。
- 能通过上下文解决的，记录处理依据。
- 会影响后文一致性的，标记为需要用户确认。
"""


def build_qa_checklist() -> str:
    """生成专业翻译 QA 清单"""
    return """# Translation QA Checklist / 翻译 QA 清单

## 译者自检
- [ ] 无漏译、错译、反译。
- [ ] 人物关系、动机、时间线没有漂移。
- [ ] 术语表中的术语使用一致。
- [ ] plain translated Markdown 格式正确：第一行是章数和章标题，空一行后直接正文。

## 双语修订
- [ ] 对照 source against target 检查意义、事实、语气、伏笔。
- [ ] 检查文化负载词处理是否符合翻译简报。
- [ ] 检查人名、称谓、境界、地名和专有名词。

## 单语润色
- [ ] read the English only，确认英文像自然小说。
- [ ] 删除翻译腔、解释腔和生硬中文句式。
- [ ] 对白符合人物身份和场景压力。

## 终检
- [ ] 文件命名为 `Chapter-XXX.md`。
- [ ] 章节顺序完整。
- [ ] 没有任务说明、译者笔记或未处理 TBD 混入正文。
- [ ] 译文文件内没有 Markdown 标题、章节标签、QA 说明或译者说明。
- [ ] 可继续运行 `python3 scripts/generate_epub.py <小说目录路径> --lang en`。
"""


def build_revision_prompt(chapter_num: int, chapter_title: str, chapter_content: str) -> str:
    """生成双语修订任务"""
    return f"""# 双语修订任务 / Bilingual Revision Task

Role: revise the translated chapter by comparing source against target. This is not rewriting from scratch unless the draft fails.

Inputs:
- Source chapter title: {chapter_title}
- Source chapter body:
{chapter_content}

Required files to read:
- `../Chapter-{chapter_num:03d}.md`
- `../00-translation-brief.md`
- `../01-termbase.md`
- `../02-style-sheet.md`
- `../04-qa-checklist.md`

Check:
1. Meaning transfer: no omissions, additions, changed facts, or weakened causality.
2. Terminology: names, places, titles, ranks, objects, and culture-specific terms match the termbase.
3. Style/register: English follows the style sheet and preserves narrative pressure.
4. Format: preserve plain translated Markdown: first line is the chapter number and title, then one blank line, then body text.

Output: overwrite `../Chapter-{chapter_num:03d}.md` only after corrections are applied.
"""


def build_edit_prompt(chapter_num: int) -> str:
    """生成单语润色任务"""
    return f"""# 单语润色任务 / Monolingual Edit Task

Role: read the English only as an English fiction editor. Do not consult the source unless a sentence is incoherent or seems factually broken.

Required file:
- `../Chapter-{chapter_num:03d}.md`

Edit for:
1. Natural English fiction prose.
2. Dialogue rhythm and character voice.
3. Paragraph flow, tension, and clarity.
4. Removal of translationese while preserving facts already verified in bilingual revision.
5. Preserve the plain translated Markdown format: first line title, blank line, body only.

Output: overwrite `../Chapter-{chapter_num:03d}.md` with the polished version.
"""


def save_project_workflow_files(output_path: Path, novel_info: dict, task_count: int):
    """保存项目级专业翻译流程文件"""
    output_path.mkdir(parents=True, exist_ok=True)
    files = {
        "00-translation-brief.md": build_translation_brief(novel_info, task_count),
        "01-termbase.md": build_termbase(novel_info),
        "02-style-sheet.md": build_style_sheet(novel_info),
        "03-query-log.md": build_query_log(),
        "04-qa-checklist.md": build_qa_checklist(),
    }
    for name, content in files.items():
        (output_path / name).write_text(content, encoding='utf-8')


def save_translation_task(task_path: Path, prompt: str):
    """保存当前 AI 可直接执行的意译任务"""
    task_path.parent.mkdir(parents=True, exist_ok=True)
    with open(task_path, 'w', encoding='utf-8') as f:
        f.write(prompt)


def save_translation_readme(output_path: Path, task_count: int):
    """保存当前 AI 翻译任务说明"""
    output_path.mkdir(parents=True, exist_ok=True)
    readme_path = output_path / "_translation_tasks" / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(
        f"""# 当前 AI 意译翻译任务包

本目录由 `scripts/translate_to_english.py` 生成，不调用独立翻译接口。

使用方式：
1. 先读 `../00-translation-brief.md`、`../01-termbase.md`、`../02-style-sheet.md`、`../04-qa-checklist.md`。
2. 逐章执行 `Chapter-XXX.translate.prompt.md`，把译文保存为 `../Chapter-XXX.md`。
3. 执行 `Chapter-XXX.revise.prompt.md` 做双语修订。
4. 执行 `Chapter-XXX.edit.prompt.md` 做单语润色。
5. 用 `../04-qa-checklist.md` 做终检。

已生成任务数：{task_count}
""",
        encoding='utf-8',
    )


def translate_novel(
    novel_dir: Path,
    output_dir: str = 'manuscript/en',
    chapters: str = None
):
    """为当前 AI 准备意译翻译任务包"""
    novel_dir = Path(novel_dir)

    if not novel_dir.exists():
        print(f"错误: 目录不存在 - {novel_dir}")
        return False

    print(f"准备当前 AI 意译翻译任务: {novel_dir.name}")

    # 提取小说信息
    novel_info = extract_novel_info(novel_dir)
    print(f"书名: {novel_info['title']}")
    print(f"作者: {novel_info['author']}")
    print("翻译模式: 意译翻译（使用当前 AI，不调用独立接口）")

    # 确定输出目录
    output_path = novel_dir / output_dir
    task_path = output_path / "_translation_tasks"

    # 查找章节
    chapter_files = find_chapters(novel_dir)

    if not chapter_files:
        print(f"错误: 未找到章节文件")
        return False

    print(f"找到 {len(chapter_files)} 个章节")

    # 解析要翻译的章节范围
    chapters_to_translate = None
    if chapters:
        chapters_to_translate = parse_chapter_range(chapters, len(chapter_files))

    selected_chapters = [
        chapter
        for chapter in chapter_files
        if not chapters_to_translate or chapter['number'] in chapters_to_translate
    ]

    if not selected_chapters:
        print("\n错误: 没有匹配到需要翻译的章节")
        return False

    save_project_workflow_files(output_path, novel_info, len(selected_chapters))

    for chapter in selected_chapters:
        print(f"\n生成第 {chapter['number']} 章意译任务: {chapter['title']}")

        # 提取章节内容
        content = extract_chapter_content(chapter['file'])

        # 构建提示词
        prompt = build_translation_prompt(novel_info, content, chapter['title'], chapter['number'])
        revision_prompt = build_revision_prompt(chapter['number'], chapter['title'], content)
        edit_prompt = build_edit_prompt(chapter['number'])

        translate_file = task_path / f"Chapter-{chapter['number']:03d}.translate.prompt.md"
        legacy_file = task_path / f"Chapter-{chapter['number']:03d}.prompt.md"
        revise_file = task_path / f"Chapter-{chapter['number']:03d}.revise.prompt.md"
        edit_file = task_path / f"Chapter-{chapter['number']:03d}.edit.prompt.md"
        save_translation_task(translate_file, prompt)
        save_translation_task(legacy_file, prompt)
        save_translation_task(revise_file, revision_prompt)
        save_translation_task(edit_file, edit_prompt)
        print(f"已保存任务: {translate_file}")
        print(f"已保存修订任务: {revise_file}")
        print(f"已保存润色任务: {edit_file}")

    save_translation_readme(output_path, len(selected_chapters))
    print(f"\n任务包已生成: {task_path}")
    print("下一步: 让当前 AI 按翻译简报、术语表、风格表和 QA 清单执行翻译、双语修订、单语润色。")
    return True


def parse_chapter_range(chapters_str: str, max_chapters: int) -> set:
    """解析章节范围字符串，如 "1,3-5,10" """
    chapters = set()
    parts = chapters_str.split(',')

    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            chapters.update(range(int(start), int(end) + 1))
        else:
            chapters.add(int(part))

    return chapters


def main():
    parser = argparse.ArgumentParser(
        description='为当前 AI 生成中文小说意译翻译任务包',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python scripts/translate_to_english.py novels/书名
  python scripts/translate_to_english.py novels/书名 --chapters "1,3-5"
  python scripts/translate_to_english.py novels/书名 -o manuscript/en

说明:
  本脚本不调用独立翻译接口，只生成当前 AI 可直接执行的意译任务包。
  真正译文由当前 AI 生成，并保存到 manuscript/en/Chapter-XXX.md。
'''
    )
    parser.add_argument('novel_dir', help='小说项目目录路径')
    parser.add_argument('-o', '--output', default='manuscript/en', help='输出目录 (默认: manuscript/en)')
    parser.add_argument('--chapters', help='要翻译的章节范围，如 "1,3-5,10"')

    args = parser.parse_args()

    success = translate_novel(
        Path(args.novel_dir),
        output_dir=args.output,
        chapters=args.chapters
    )
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
