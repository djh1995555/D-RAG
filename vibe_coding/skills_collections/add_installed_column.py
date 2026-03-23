#!/usr/bin/env python3
import sys
from pathlib import Path


def add_installed_column_to_table(table_lines):
    result = []
    for i, line in enumerate(table_lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            result.append(line)
            continue

        cells = stripped.split("|")
        cells = [c.strip() for c in cells[1:-1]] if cells[0] == "" else cells
        new_value = "installed" if i == 0 else ("---" if i == 1 else "[]")
        cells.insert(1, new_value)
        result.append("| " + " | ".join(cells) + " |")
    return result


def process_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("#"):
            result.append(line)
            i += 1
            table_lines = []
            while i < len(lines):
                current = lines[i]
                if current.strip() == "":
                    if table_lines:
                        break
                    result.append(current)
                    i += 1
                    continue
                if current.strip().startswith("|"):
                    table_lines.append(current)
                    i += 1
                else:
                    break
            if table_lines:
                result.extend(add_installed_column_to_table(table_lines))
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


def main():
    if len(sys.argv) < 2:
        print("用法: python add_installed_column.py <markdown文件路径>")
        print("示例: python add_installed_column.py skills-superpowers.md")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)

    new_content = process_markdown_file(file_path)
    output_path = Path(file_path).stem + "-updated.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ 处理完成！输出文件: {output_path}")
    print(f"   已为表格添加 'installed' 列（内容填充为 []）")


if __name__ == "__main__":
    main()
