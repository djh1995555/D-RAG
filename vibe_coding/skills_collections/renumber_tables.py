#!/usr/bin/env python3
"""
对目标 Markdown 文件中的表格进行重新编号
- 每个表格独立从1开始编号
- 自动识别序号列（第一列或包含"序号/编号/No"等关键词的列）
- 支持文件或目录路径
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional


def find_number_column(table_lines: List[str]) -> int:
    """识别表格中的序号列，返回列索引（0-based）"""
    if len(table_lines) < 2:
        return 0

    header = table_lines[0]
    cells = [
        c.strip() for c in header.split("|")[1:-1]
    ]  # cells: ['', 'col1', ...] 首尾有空元素

    keywords = [
        "序号",
        "编号",
        "No",
        "no",
        "NO",
        "序",
        "Num",
        "num",
        "ID",
        "id",
        "#",
        "Number",
    ]

    for idx, cell in enumerate(cells):
        for kw in keywords:
            if kw in cell:
                return idx

    return 0


def parse_markdown_tables(content: str) -> List[Tuple[int, int, List[str]]]:
    """解析 Markdown 中的所有表格，返回 [(起始行号, 结束行号, 行列表), ...]"""
    lines = content.split("\n")
    tables = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if "|" in line and not re.match(r"^[\|\-\:\s]+$", line):  # 表格行且非分隔线
            table_start = i
            table_lines = [line]
            i += 1

            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1

            if len(table_lines) >= 2 and any("|" in l for l in table_lines[1:]):
                tables.append((table_start, i - 1, table_lines))
        else:
            i += 1

    return tables


def renumber_table(
    table_lines: List[str], number_col: Optional[int] = None
) -> List[str]:
    """重新编号单个表格，从1开始"""
    if number_col is None:
        number_col = find_number_column(table_lines)

    new_lines = []
    current_num = 1

    for idx, line in enumerate(table_lines):
        if idx == 0:
            # 更新表头：将序号列改为"编号"
            cells = line.split("|")
            if len(cells) >= number_col + 2:
                cells[number_col + 1] = " 编号 "
            new_lines.append("|".join(cells))
            continue
        if idx == 1 and re.match(r"^[\|\-\:\s]+$", line):
            new_lines.append(line)
            continue

        cells = line.split("|")
        if len(cells) >= number_col + 2:
            cells[number_col + 1] = f" {current_num} "
            current_num += 1
            new_lines.append("|".join(cells))
        else:
            new_lines.append(line)

    return new_lines


def process_file(file_path: Path) -> int:
    """处理单个 Markdown 文件，返回处理的表格数"""
    content = file_path.read_text(encoding="utf-8")
    tables = parse_markdown_tables(content)

    if not tables:
        return 0

    new_content = content
    for start_line, end_line, table_lines in reversed(tables):
        new_table_lines = renumber_table(table_lines)
        lines = new_content.split("\n")
        lines[start_line : end_line + 1] = new_table_lines
        new_content = "\n".join(lines)

    file_path.write_text(new_content, encoding="utf-8")
    return len(tables)


def main(target_path: str):
    target = Path(target_path).resolve()

    if not target.exists():
        print(f"错误: 路径不存在 - {target}")
        sys.exit(1)

    if target.is_file():
        # 处理单个文件
        count = process_file(target)
        print(f"✓ {target.name}: {count} 个表格已重新编号")
    elif target.is_dir():
        # 处理目录下所有 md 文件
        print(f"目标目录: {target}")
        print("=" * 50)

        md_files = sorted(target.rglob("*.md"))
        total_tables = 0

        for md_file in md_files:
            count = process_file(md_file)
            if count > 0:
                print(f"  ✓ {md_file.name}: {count} 个表格已重新编号")
                total_tables += count

        print("\n" + "=" * 50)
        print(f"完成! 共处理 {total_tables} 个表格")
    else:
        print(f"错误: 不是有效的文件或目录 - {target}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python renumber_tables.py <文件或目录路径>")
        print("示例:")
        print("  python renumber_tables.py ./doc.md")
        print("  python renumber_tables.py ./docs")
        sys.exit(1)

    main(sys.argv[1])
