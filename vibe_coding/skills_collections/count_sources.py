#!/usr/bin/env python3
"""
统计 Markdown 表格中不同来源的条目数量
用法: python count_sources.py <markdown_file>
"""

import re
import sys
from collections import Counter
from pathlib import Path


def count_table_rows(content: str) -> int:
    pattern = re.compile(r"^\|\s*\d+\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|", re.MULTILINE)
    return len(list(pattern.finditer(content)))


def count_sources(file_path: str) -> Counter:
    content = Path(file_path).read_text(encoding="utf-8")

    # 匹配完整 7 列表格行，来源列需包含 skills- 或 awesome-
    pattern = re.compile(
        r"^\|\s*\d+\s*\|\s*(skills-[\w-]+|awesome-[\w-]+)\s*\|.*\|.*\|.*\|.*\|",
        re.MULTILINE,
    )

    sources = []
    for match in pattern.finditer(content):
        source = match.group(1).strip()
        sources.append(source)

    if sources:
        return Counter(sources)

    # 无来源列的单文件，用文件名作为来源
    row_count = count_table_rows(content)
    if row_count > 0:
        source_name = Path(file_path).stem
        return Counter({source_name: row_count})

    return Counter()


def main():
    if len(sys.argv) < 2:
        print("用法: python count_sources.py <markdown_file>")
        print("示例: python count_sources.py skills-test.md")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)

    source_counts = count_sources(file_path)

    total = sum(source_counts.values())
    print(f"\n{'=' * 60}")
    print(f"来源统计 (总计: {total} 条)")
    print(f"{'=' * 60}\n")

    for source, count in source_counts.most_common():
        percentage = (count / total * 100) if total > 0 else 0
        print(f"{source:50} {count:5} 条 ({percentage:5.1f}%)")

    print(f"\n{'=' * 60}")
    print(f"共 {len(source_counts)} 个不同来源")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
