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

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def extract_content_from_chapter(file_path: Path) -> str:
    """从章节文件中提取正文内容，优先只统计 `## 正文` 区块"""
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

    # 兼容旧模板：如果没有 `## 正文`，则退回到章节标题之后的所有内容
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('#') and '章' in line:
            content_start = i + 1
            break

    main_content = '\n'.join(lines[content_start:])
    return main_content


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
    author = author_match.group(1).strip() if author_match else '未知作者'

    return {'title': title, 'author': author}


def find_chapters(novel_dir: Path) -> list:
    """查找目录下所有章节文件"""
    chapter_files = sorted(novel_dir.glob('第*.md'))
    chapters = []

    for chapter_file in chapter_files:
        # 提取章节标题
        with open(chapter_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        # 从文件名或第一行提取标题
        title_match = re.search(r'第\d+章[-(]*(.+?)\.md$', chapter_file.name)
        if title_match:
            chapter_title = title_match.group(1)
        else:
            chapter_title = chapter_file.stem

        # 从文件内容中提取标题（优先使用文件内的标题）
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        content_title_match = re.search(r'^##\s+(.+?)$', content, re.MULTILINE)
        if content_title_match and content_title_match.group(1) != '正文':
            chapter_title = content_title_match.group(1).strip()

        chapters.append({
            'file': chapter_file,
            'title': chapter_title,
            'order': len(chapters) + 1
        })

    return chapters


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


def generate_epub(
    novel_dir: Path,
    output_path: Path,
    author_override: str = None
) -> bool:
    """生成 EPUB 文件"""
    novel_dir = Path(novel_dir)

    if not novel_dir.exists() or not novel_dir.is_dir():
        print(f'错误: 目录不存在 - {novel_dir}')
        return False

    # 解析大纲
    outline_path = novel_dir / '00-大纲.md'
    metadata = parse_outline(outline_path)

    title = metadata['title']
    author = author_override if author_override else metadata['author']

    # 查找章节
    chapters = find_chapters(novel_dir)

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
    <dc:language>zh-CN</dc:language>
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
'''
    )
    parser.add_argument('novel_dir', help='小说项目目录路径')
    parser.add_argument('-o', '--output', help='输出 EPUB 文件路径 (默认: <书名>.epub)')
    parser.add_argument('--author', help='覆盖大纲中的作者')

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
        outline_path = novel_dir / '00-大纲.md'
        metadata = parse_outline(outline_path)
        # 清理书名中的非法字符
        safe_title = re.sub(r'[<>:"/\\|?*]', '', metadata['title'])
        output_path = novel_dir / f'{safe_title}.epub'

    # 生成 EPUB
    success = generate_epub(novel_dir, output_path, args.author)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
