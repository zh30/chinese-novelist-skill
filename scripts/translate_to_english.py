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


def translate_with_openai(prompt: str) -> str:
    """使用 OpenAI API 翻译"""
    try:
        from openai import OpenAI
    except ImportError:
        print("错误: 请安装 openai 库 (pip install openai)")
        raise

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("错误: 请设置 OPENAI_API_KEY 环境变量")
        raise ValueError("Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def translate_with_anthropic(prompt: str) -> str:
    """使用 Anthropic API 翻译"""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("错误: 请安装 anthropic 库 (pip install anthropic)")
        raise

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("错误: 请设置 ANTHROPIC_API_KEY 环境变量")
        raise ValueError("Missing ANTHROPIC_API_KEY")

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def translate_with_gemini(prompt: str) -> str:
    """使用 Google Gemini API 翻译"""
    try:
        import google.genai as genai
    except ImportError:
        print("错误: 请安装 google-generativeai 库 (pip install google-generativeai)")
        raise

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("错误: 请设置 GEMINI_API_KEY 环境变量")
        raise ValueError("Missing GEMINI_API_KEY")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text


def translate_with_ai(prompt: str, provider: str = None) -> str:
    """调用 AI 进行翻译

    Args:
        prompt: 翻译提示词
        provider: AI 提供商 (openai/anthropic/gemini)，如果为 None 则自动检测

    Returns:
        翻译后的内容
    """
    if provider:
        providers = [provider]
    else:
        # 自动检测可用的 API
        providers = []
        if os.getenv('OPENAI_API_KEY'):
            providers.append('openai')
        if os.getenv('ANTHROPIC_API_KEY'):
            providers.append('anthropic')
        if os.getenv('GEMINI_API_KEY'):
            providers.append('gemini')

        if not providers:
            print("\n请配置以下任一 AI API 环境变量:")
            print("  - OPENAI_API_KEY")
            print("  - ANTHROPIC_API_KEY")
            print("  - GEMINI_API_KEY")
            print("\n或者通过 --provider 参数指定提供商")
            raise ValueError("No AI API configured")

    # 尝试第一个可用的提供商
    for p in providers:
        try:
            if p == 'openai':
                return translate_with_openai(prompt)
            elif p == 'anthropic':
                return translate_with_anthropic(prompt)
            elif p == 'gemini':
                return translate_with_gemini(prompt)
        except Exception as e:
            print(f"警告: {p} API 调用失败: {e}")
            continue

    raise RuntimeError("所有配置的 AI API 都不可用")


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
    chapters: str = None,
    provider: str = None
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
    if provider:
        print(f"使用 AI: {provider}")
    else:
        print("自动检测 AI 提供商...")

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
            translated_content = translate_with_ai(prompt, provider)

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
  python scripts/translate_to_english.py novels/书名 --provider openai

环境变量:
  OPENAI_API_KEY      OpenAI API 密钥
  ANTHROPIC_API_KEY  Anthropic API 密钥
  GEMINI_API_KEY     Google Gemini API 密钥
'''
    )
    parser.add_argument('novel_dir', help='小说项目目录路径')
    parser.add_argument('-o', '--output', default='en', help='输出目录 (默认: en)')
    parser.add_argument('--chapters', help='要翻译的章节范围，如 "1,3-5,10"')
    parser.add_argument('--provider', choices=['openai', 'anthropic', 'gemini'],
                        help='指定 AI 提供商')

    args = parser.parse_args()

    success = translate_novel(
        Path(args.novel_dir),
        output_dir=args.output,
        chapters=args.chapters,
        provider=args.provider
    )
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
