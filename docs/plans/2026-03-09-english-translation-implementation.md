# English Translation Feature Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为中文小说写作技能增加"深度翻译"功能，将小说翻译为适合英文读者的英文版本。

**Architecture:** 基于 AI 的翻译功能，通过读取小说上下文（大纲、人物、世界观）构建提示词，调用 AI 翻译并保存到 `en/` 目录。

**Tech Stack:** Python, AI 模型（通过 API 调用）

---

## Task 1: Update SKILL.md - Add Translation Mode Documentation

**Files:**
- Modify: `SKILL.md:133` (at the end of file)

**Step 1: Add translation mode documentation to SKILL.md**

After line 132 (the Completion section), add:

```markdown
## Translation

当用户要求翻译成英文时执行：

1. 确认小说目录和翻译范围（全本 / 部分章节）
2. 读取上下文文件：
   - `00-大纲.md` → 书名、作者、类型、简介
   - `01-人物档案.md` → 人物信息
   - `02-世界观与伏笔.md` → 世界观要点
3. 运行翻译脚本：
   ```bash
   python3 scripts/translate_to_english.py <小说目录路径>
   ```
4. 可选参数：
   - `--chapters "1,3-5"` 指定翻译章节范围
   - `-o <输出目录>` 指定输出目录（默认 `en/`）
5. 英文版也支持 EPUB 导出：
   ```bash
   python3 scripts/generate_epub.py <小说目录路径> --lang en
   ```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs: add translation mode to SKILL.md"
```

---

## Task 2: Create Translation Script - translate_to_english.py

**Files:**
- Create: `scripts/translate_to_english.py`

**Step 1: Create the translation script**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English Translation Script
将中文小说深度翻译为英文版本
"""

import argparse
import os
import re
import sys
from pathlib import Path

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


def find_chapters(novel_dir: Path) -> list:
    """查找所有章节文件"""
    chapter_files = sorted(novel_dir.glob('第*.md'))
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

        chapters.append({
            'file': chapter_file,
            'number': chapter_num,
            'title': chapter_title
        })

    return chapters


def build_translation_prompt(novel_info: dict, chapter_content: str, chapter_title: str) -> str:
    """构建翻译提示词"""
    prompt = f"""# Translation Task

You are a professional novel translator. Translate the following Chinese novel chapter into fluent English.

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
1. Maintain the narrative rhythm and emotional tension
2. Use pinyin for character names (e.g., Zhang Wei)
3. Keep Chinese-specific terms (gongfu, qigong) with pinyin or explanatory translation
4. Preserve chapter structure with "## Title" and "## Body" headings
5. Use modern English, avoid stiff literal translations
6. Keep dialogue natural and fluent
7. Translate the chapter title as well

## Chapter Title
{chapter_title}

## Chapter to Translate
{chapter_content}

## Output Format
Provide only the translated chapter in Markdown format, with "## Title" for the chapter title and "## Body" for the content. Do not include any additional explanation.
"""
    return prompt


def translate_with_ai(prompt: str) -> str:
    """调用 AI 进行翻译"""
    # 这里需要根据用户的 AI 配置来调用
    # 默认使用环境变量或配置文件中的 API
    # 暂时返回占位符，实际使用时需要集成用户的 AI API

    print("请配置 AI API 以进行翻译。当前支持：")
    print("  - OpenAI API (设置 OPENAI_API_KEY)")
    print("  - Anthropic API (设置 ANTHROPIC_API_KEY)")
    print("  - Google Gemini API (设置 GEMINI_API_KEY)")

    # 示例：使用 OpenAI
    # from openai import OpenAI
    # client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.choices[0].message.content

    raise NotImplementedError("请在脚本中配置 AI API")


def save_translated_chapter(output_path: Path, title: str, content: str):
    """保存翻译后的章节"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"## {title}\n\n")
        f.write(f"## Body\n\n")
        f.write(content)


def translate_novel(
    novel_dir: Path,
    output_dir: str = 'en',
    chapters: str = None
):
    """翻译小说"""
    novel_dir = Path(novel_dir)

    if not novel_dir.exists():
        print(f"错误: 目录不存在 - {novel_dir}")
        return False

    print(f"开始翻译: {novel_dir.name}")

    # 提取小说信息
    novel_info = extract_novel_info(novel_dir)
    print(f"书名: {novel_info['title']}")
    print(f"作者: {novel_info['author']}")

    # 确定输出目录
    output_path = novel_dir / output_dir

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

    # 翻译每个章节
    for i, chapter in enumerate(chapter_files):
        if chapters_to_translate and chapter['number'] not in chapters_to_translate:
            continue

        print(f"\n翻译第 {chapter['number']} 章: {chapter['title']}")

        # 提取章节内容
        content = extract_chapter_content(chapter['file'])

        # 构建提示词
        prompt = build_translation_prompt(novel_info, content, chapter['title'])

        try:
            # 调用 AI 翻译
            translated_content = translate_with_ai(prompt)

            # 保存翻译结果
            output_file = output_path / f"Chapter-{chapter['number']:03d}.md"
            save_translated_chapter(output_file, chapter['title'], translated_content)

            print(f"已保存: {output_file}")

        except NotImplementedError as e:
            print(f"错误: {e}")
            return False
        except Exception as e:
            print(f"翻译第 {chapter['number']} 章失败: {e}")
            continue

    print(f"\n翻译完成！英文版保存在: {output_path}")
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
        description='将中文小说翻译为英文版本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python scripts/translate_to_english.py novels/书名
  python scripts/translate_to_english.py novels/书名 --chapters "1,3-5"
  python scripts/translate_to_english.py novels/书名 -o en
'''
    )
    parser.add_argument('novel_dir', help='小说项目目录路径')
    parser.add_argument('-o', '--output', default='en', help='输出目录 (默认: en)')
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
```

**Step 2: Commit**

```bash
git add scripts/translate_to_english.py
git commit -m "feat: add English translation script"
```

---

## Task 3: Update generate_epub.py - Add Language Support

**Files:**
- Modify: `scripts/generate_epub.py:135-153` (generate_epub function signature)
- Modify: `scripts/generate_epub.py:300-342` (main function)

**Step 1: Add lang parameter to generate_epub function**

Replace the generate_epub function signature (around line 135):

```python
def generate_epub(
    novel_dir: Path,
    output_path: Path,
    author_override: str = None,
    lang: str = 'zh-CN'
) -> bool:
```

Add after line 152 (after `author = author_override...`):

```python
    # 设置语言
    if lang == 'en':
        output_lang = 'en'
        # 查找英文目录
        en_dir = novel_dir / 'en'
        if en_dir.exists():
            novel_dir = en_dir
            # 尝试读取英文大纲获取英文书名
            en_outline = en_dir / '00-outline.md'
            if en_outline.exists():
                with open(en_outline, 'r', encoding='utf-8') as f:
                    en_content = f.read()
                en_title_match = re.search(r'^#\s*(.+?)$', en_content, re.MULTILINE)
                if en_title_match:
                    title = en_title_match.group(1).strip()
    else:
        output_lang = 'zh-CN'
```

**Step 2: Update content.opf language**

Find the line around 189:
```python
    <dc:language>zh-CN</dc:language>
```

Replace with:
```python
    <dc:language>{output_lang}</dc:language>
```

**Step 3: Update CLI to support --lang parameter**

In main() function, around line 315, add:

```python
    parser.add_argument('--lang', default='zh-CN', choices=['zh-CN', 'en'],
                        help='语言: zh-CN (中文) 或 en (英文)')
```

And update the generate_epub call (around line 337):

```python
    success = generate_epub(novel_dir, output_path, args.author, args.lang)
```

**Step 4: Commit**

```bash
git add scripts/generate_epub.py
git commit -m "feat: add --lang parameter for English EPUB export"
```

---

## Task 4: Update SKILL.md Export Section - Add Language Parameter

**Files:**
- Modify: `SKILL.md:98-111` (Export section)

**Step 1: Update export documentation**

Replace the Export section with:

````markdown
## Export

当用户要求导出 EPUB 时：

1. 确认小说目录路径（用户已提供或在 novels/ 下查找）
2. 运行导出脚本：
   ```bash
   python3 scripts/generate_epub.py <小说目录路径>
   ```
3. 可选参数：
   - `--author <作者名>` 覆盖大纲中的作者
   - `-o <输出路径>` 指定输出文件位置
   - `--lang <语言>` 指定语言 (zh-CN 中文 / en 英文)
4. 英文版 EPUB 导出示例：
   ```bash
   python3 scripts/generate_epub.py <小说目录路径> --lang en
   ```
5. 告诉用户生成的 EPUB 文件路径
````

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs: update export section with language parameter"
```

---

## Summary

完成以上 4 个任务后，功能实现完毕：

| Task | Description |
|------|-------------|
| 1 | SKILL.md 添加翻译模式文档 |
| 2 | 创建 translate_to_english.py 翻译脚本 |
| 3 | generate_epub.py 添加 --lang 参数 |
| 4 | 更新 Export 文档说明 |
