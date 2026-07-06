#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB 生成脚本
将小说项目导出为 EPUB 格式的电子书
"""

import argparse
import re
import sys
import uuid
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import extract_text_from_chapter, find_chapter_files

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# 非正文部分的章节标题模式（这些不是真正的章节标题）
NON_CONTENT_SECTIONS = {
    '本章任务卡', '场景拆分', '正文', '章节复盘',
    '章节摘要', '章节钩子', '本章摘要', '本章钩子',
    '人物状态变化', '下一章必须处理', '新增信息', '已回应悬念',
    '承接上章', '本章目标', '主要阻碍', '情绪推进', '关键转折',
    '结尾钩子', '章节功能'
}


def extract_content_from_chapter(file_path: Path) -> str:
    """从章节文件中提取正文内容。"""
    return extract_text_from_chapter(file_path)


def parse_outline(outline_path: Path) -> dict:
    """解析大纲文件，获取书名、作者等信息"""
    if not outline_path.exists():
        return {'title': '未知书名', 'author': '未知作者'}

    with open(outline_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取书名（从第一行 # [书名] 大纲）
    title_match = re.search(r'^#\s*(.+?)\s*大纲', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else '未知书名'

    # 提取作者
    author_match = re.search(r'\*\*作者\s*/\s*笔名\*\*[：:]\s*(.+)', content)
    author = author_match.group(1).strip() if author_match else ''

    # 如果作者为空或只有空白字符，设置为空字符串（后续会提示用户输入）
    if not author or not author.strip():
        author = ''

    return {'title': title, 'author': author}


def find_chapters(novel_dir: Path, lang: str = 'zh-CN') -> list:
    """查找目录下所有章节文件"""
    chapter_lang = 'en' if lang == 'en' else 'zh'
    chapter_files = find_chapter_files(novel_dir, chapter_lang)
    chapters = []

    for chapter_file in chapter_files:
        # 提取章节标题
        with open(chapter_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        # 从文件名提取标题作为后备
        title_match = re.search(r'第\d+章[-(]*(.+?)\.md$', chapter_file.name)
        en_title_match = re.search(r'Chapter[-_ ]?(\d+)[-( ]*(.*?)\.md$', chapter_file.name, re.IGNORECASE)
        if title_match:
            chapter_title = title_match.group(1)
        elif en_title_match and en_title_match.group(2).strip():
            chapter_title = en_title_match.group(2).strip()
        else:
            chapter_title = chapter_file.stem

        # 从文件内容中提取标题（优先使用文件内的标题）
        # 跳过非内容章节：## 本章任务卡, ## 场景拆分, ## 正文, ## 章节复盘 等
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找所有 ## 标题
        content_title_matches = re.findall(r'^##\s+(.+?)$', content, re.MULTILINE)
        explicit_title = _extract_english_title_section(content)
        plain_title = _extract_plain_translated_title(content)
        if explicit_title:
            chapter_title = explicit_title
        elif plain_title:
            chapter_title = plain_title
            explicit_title = plain_title

        # 找到第一个不是非内容章节的标题（前缀匹配，支持 "本章任务卡：xxx" 格式）
        if not explicit_title:
            for match in content_title_matches:
                section_title = match.strip()
                # 检查是否以非内容章节标题开头
                is_non_content = any(section_title.startswith(prefix) for prefix in NON_CONTENT_SECTIONS)
                if not is_non_content:
                    chapter_title = section_title
                    break

        chapters.append({
            'file': chapter_file,
            'title': chapter_title,
            'order': len(chapters) + 1
        })

    return chapters


def _chapter_sort_key(path: Path) -> tuple:
    """按中文或英文章节号排序。"""
    zh_match = re.match(r'第(\d+)章', path.name)
    if zh_match:
        return (int(zh_match.group(1)), path.name)

    en_match = re.match(r'Chapter[-_ ]?(\d+)', path.name, re.IGNORECASE)
    if en_match:
        return (int(en_match.group(1)), path.name)

    return (10**9, path.name)


def _extract_english_title_section(content: str) -> str:
    """提取 `## Title` 标题区块中的第一行标题。"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().lower() == '## title':
            for candidate in lines[i + 1:]:
                stripped = candidate.strip()
                if not stripped:
                    continue
                if stripped.startswith('## '):
                    return ''
                return stripped
    return ''


def _find_plain_translated_title_line(lines: list) -> int:
    """查找纯译文格式的首行章数和标题。"""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if _looks_like_plain_translated_title(stripped):
            return i
        return None
    return None


def _extract_plain_translated_title(content: str) -> str:
    """提取纯译文格式首行标题。"""
    lines = content.split('\n')
    title_index = _find_plain_translated_title_line(lines)
    if title_index is None:
        return ''
    return lines[title_index].strip()


def _looks_like_plain_translated_title(line: str) -> bool:
    """判断一行是否是 `Chapter 1: Title` 或 `第1章 标题` 格式。"""
    if line.startswith('#'):
        return False
    return bool(
        re.match(r'^(?:Chapter\s*\d+|Chapter[-_ ]?\d+|第\s*\d+\s*章)\b', line, re.IGNORECASE)
    )


def convert_markdown_to_xhtml(content: str) -> str:
    """将简化的 Markdown 转换为 XHTML"""
    # 转义 HTML 特殊字符
    content = xml_escape(content)

    # 转换段落（空行分隔）
    paragraphs = content.split('\n\n')
    xhtml_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # 处理标题（以 # 开头的行）
        if para.startswith('#'):
            level = len(para) - len(para.lstrip('#'))
            text = para.lstrip('#').strip()
            xhtml_paragraphs.append(f'<h{level}>{text}</h{level}>')
        else:
            # 普通段落
            xhtml_paragraphs.append(f'<p>{para}</p>')

    return '\n'.join(xhtml_paragraphs)


def prompt_for_author(book_title: str) -> str:
    """提示用户输入作者名字"""
    print(f'\n图书 "{book_title}" 的作者名字未设置。')
    while True:
        author = input('请输入作者名字: ').strip()
        if author:
            return author
        print('作者名字不能为空，请重新输入。')


def generate_epub(
    novel_dir: Path,
    output_path: Path,
    author_override: str = None,
    lang: str = 'zh-CN'
) -> bool:
    """生成 EPUB 文件

    Args:
        novel_dir: 小说项目目录路径
        output_path: 输出 EPUB 文件路径
        author_override: 覆盖大纲中的作者
        lang: 语言设置，'zh-CN' 中文 或 'en' 英文
    """
    novel_dir = Path(novel_dir)
    original_novel_dir = novel_dir

    if not novel_dir.exists() or not novel_dir.is_dir():
        print(f'错误: 目录不存在 - {novel_dir}')
        return False

    # 处理英文版
    output_lang = lang
    if lang == 'en':
        en_dir = _resolve_language_dir(novel_dir, 'en')
        if en_dir.exists():
            novel_dir = en_dir
            print(f'使用英文目录: {en_dir}')
            # 尝试读取原大纲获取中文书名，然后翻译
            original_outline = original_novel_dir / '00-大纲.md'
            original_metadata = parse_outline(original_outline)
            original_title = original_metadata.get('title', 'Unknown')

            # 尝试从英文目录获取英文书名（查找包含书名信息的文件）
            en_title = None
            en_outline_files = list(novel_dir.glob('*.md'))
            for en_file in en_outline_files:
                # 跳过章节和翻译工作流文件，查找可能有书名的文件
                if not _is_english_metadata_file(en_file):
                    continue
                try:
                    with open(en_file, 'r', encoding='utf-8') as f:
                        en_content = f.read()
                    # 查找类似 "# Book Title" 的标题，且不是章节标题
                    en_title_match = re.search(r'^#\s+(.+?)(?:\s+大纲|\s+简介|$)', en_content, re.MULTILINE)
                    if en_title_match:
                        en_title = en_title_match.group(1).strip()
                        break
                except Exception:
                    continue

            title = en_title if en_title else f'{original_title} (English)'

            # 处理作者
            if author_override:
                author = author_override
            else:
                # 尝试从英文大纲获取作者
                author = 'Unknown Author'
                for en_file in en_outline_files:
                    if not _is_english_metadata_file(en_file):
                        continue
                    try:
                        with open(en_file, 'r', encoding='utf-8') as f:
                            en_content = f.read()
                        en_author_match = re.search(r'(?:作者|Author)[：:\s]+(.+)', en_content, re.MULTILINE)
                        if en_author_match:
                            author = en_author_match.group(1).strip()
                            break
                    except Exception:
                        continue

            metadata = {'title': title, 'author': author}
        else:
            print(f'警告: 英文目录不存在: {en_dir}')
            metadata = {'title': 'English Title', 'author': author_override or 'Unknown Author'}
            title = metadata['title']
            author = metadata['author']
    else:
        # 解析大纲
        outline_path = novel_dir / '00-大纲.md'
        metadata = parse_outline(outline_path)
        title = metadata['title']
        author = author_override if author_override else metadata['author']

        # 如果作者为空，提示用户输入
        if not author or author.strip() == '':
            author = prompt_for_author(title)
            print(f'已设置作者: {author}')

    # 查找章节
    chapters = find_chapters(novel_dir, lang)

    if not chapters:
        print(f'错误: 未找到章节文件 - {novel_dir}')
        return False

    print(f'生成 EPUB: {title} - {author}')
    print(f'章节数: {len(chapters)}')

    # 生成 UUID
    book_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    # 创建 EPUB
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as epub:
        # mimetype (必须是最先添加，不压缩)
        epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        # META-INF/container.xml
        container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''
        epub.writestr('META-INF/container.xml', container_xml)

        # OEBPS/content.opf
        content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{book_id}</dc:identifier>
    <dc:title>{xml_escape(title)}</dc:title>
    <dc:creator>{xml_escape(author)}</dc:creator>
    <dc:language>{output_lang}</dc:language>
    <meta property="dcterms:modified">{timestamp}</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="title-page" href="title-page.xhtml" media-type="application/xhtml+xml"/>
'''
        for i, chapter in enumerate(chapters):
            content_opf += f'    <item id="chapter{i+1}" href="chapter{i+1}.xhtml" media-type="application/xhtml+xml"/>\n'

        content_opf += '''  </manifest>
  <spine>
    <itemref idref="title-page"/>
    <itemref idref="nav"/>
'''
        for i in range(len(chapters)):
            content_opf += f'    <itemref idref="chapter{i+1}"/>\n'

        content_opf += '''  </spine>
</package>'''
        epub.writestr('OEBPS/content.opf', content_opf)

        # OEBPS/toc.ncx (目录)
        toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_id}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{xml_escape(title)}</text>
  </docTitle>
  <navMap>
    <navPoint id="title" playOrder="1">
      <navLabel><text>封面</text></navLabel>
      <content src="title-page.xhtml"/>
    </navPoint>
'''
        for i, chapter in enumerate(chapters):
            toc_ncx += f'''    <navPoint id="chapter{i+1}" playOrder="{i+2}">
      <navLabel><text>{xml_escape(chapter['title'])}</text></navLabel>
      <content src="chapter{i+1}.xhtml"/>
    </navPoint>
'''

        toc_ncx += '''  </navMap>
</ncx>'''
        epub.writestr('OEBPS/toc.ncx', toc_ncx)

        # OEBPS/nav.xhtml (Navigation Document)
        nav_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>目录</title>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>目录</h1>
    <ol>
      <li><a href="title-page.xhtml">封面</a></li>
'''
        for i, chapter in enumerate(chapters):
            nav_xhtml += f'      <li><a href="chapter{i+1}.xhtml">{xml_escape(chapter["title"])}</a></li>\n'

        nav_xhtml += '''    </ol>
  </nav>
</body>
</html>'''
        epub.writestr('OEBPS/nav.xhtml', nav_xhtml)

        # OEBPS/title-page.xhtml (封面)
        title_page_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{xml_escape(title)}</title>
</head>
<body>
  <div style="text-align: center; padding: 50% 0;">
    <h1>{xml_escape(title)}</h1>
    <p>作者: {xml_escape(author)}</p>
  </div>
</body>
</html>'''
        epub.writestr('OEBPS/title-page.xhtml', title_page_xhtml)

        # OEBPS/chapter*.xhtml (各章节)
        for i, chapter in enumerate(chapters):
            content = extract_content_from_chapter(chapter['file'])
            xhtml_content = convert_markdown_to_xhtml(content)

            chapter_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{xml_escape(chapter["title"])}</title>
</head>
<body>
  <h2>{xml_escape(chapter["title"])}</h2>
  {xhtml_content}
</body>
</html>'''
            epub.writestr(f'OEBPS/chapter{i+1}.xhtml', chapter_xhtml)

    print(f'EPUB 已生成: {output_path}')
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='将小说项目导出为 EPUB 格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python scripts/generate_epub.py novels/书名
  python scripts/generate_epub.py novels/书名 --author "金庸"
  python scripts/generate_epub.py novels/书名 -o output.epub
  python scripts/generate_epub.py novels/书名 --author "金庸" -o output.epub
  python scripts/generate_epub.py novels/书名 --lang en
'''
    )
    parser.add_argument('novel_dir', help='小说项目目录路径')
    parser.add_argument('-o', '--output', help='输出 EPUB 文件路径 (默认: <书名>.epub)')
    parser.add_argument('--author', help='覆盖大纲中的作者')
    parser.add_argument('--lang', default='zh-CN', choices=['zh-CN', 'en'],
                        help='语言: zh-CN (中文) 或 en (英文，默认: zh-CN)')

    args = parser.parse_args()

    novel_dir = Path(args.novel_dir)

    if not novel_dir.exists():
        print(f'错误: 目录不存在 - {novel_dir}')
        sys.exit(1)

    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        # 从大纲获取书名作为默认文件名
        if args.lang == 'en':
            # 尝试获取英文书名
            en_dir = _resolve_language_dir(novel_dir, 'en')
            if en_dir.exists():
                en_outline_files = list(en_dir.glob('*.md'))
                title = None
                for en_file in en_outline_files:
                    if not _is_english_metadata_file(en_file):
                        continue
                    try:
                        with open(en_file, 'r', encoding='utf-8') as f:
                            en_content = f.read()
                        en_title_match = re.search(r'^#\s+(.+?)(?:\s+大纲|\s+简介|$)', en_content, re.MULTILINE)
                        if en_title_match:
                            title = en_title_match.group(1).strip()
                            break
                    except Exception:
                        continue

                if not title:
                    # 回退到中文书名
                    outline_path = novel_dir / '00-大纲.md'
                    metadata = parse_outline(outline_path)
                    title = f"{metadata['title']} (English)"
            else:
                outline_path = novel_dir / '00-大纲.md'
                metadata = parse_outline(outline_path)
                title = f"{metadata['title']} (English)"
        else:
            outline_path = novel_dir / '00-大纲.md'
            metadata = parse_outline(outline_path)
            title = metadata['title']

        # 清理书名中的非法字符
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        if args.lang == 'en':
            output_path = novel_dir / f'{safe_title}-en.epub'
        else:
            output_path = novel_dir / f'{safe_title}.epub'

    # 生成 EPUB
    success = generate_epub(novel_dir, output_path, args.author, args.lang)
    sys.exit(0 if success else 1)


def _resolve_language_dir(novel_dir: Path, lang: str) -> Path:
    """解析语言正文目录。英文优先使用 manuscript/en，再兼容旧 en/。"""
    if lang == 'en':
        candidates = [novel_dir / 'manuscript' / 'en', novel_dir / 'en']
        for candidate in candidates:
            if candidate.exists() and find_chapter_files(candidate, 'en'):
                return candidate
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0]
    manuscript_zh = novel_dir / 'manuscript' / 'zh'
    if manuscript_zh.exists():
        return manuscript_zh
    return novel_dir


def _is_english_metadata_file(path: Path) -> bool:
    """判断英文目录中的 Markdown 是否可作为书籍元数据来源。"""
    name = path.name
    lower_name = name.lower()
    if name.startswith('第') or lower_name.startswith('chapter'):
        return False

    workflow_files = {
        '00-translation-brief.md',
        '01-termbase.md',
        '02-style-sheet.md',
        '03-query-log.md',
        '04-qa-checklist.md',
        'readme.md',
    }
    if lower_name in workflow_files:
        return False

    if re.match(r'^\d{2}-', name):
        return False

    return True


if __name__ == '__main__':
    main()
