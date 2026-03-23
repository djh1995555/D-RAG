#!/usr/bin/env python3
"""
合并多个分类文件的脚本

功能：
1. 传入多个文件名
2. 解析每个文件的目录结构和表格条目
3. 合并相同目录下的内容
4. 生成新文件
5. 验证合并前后条目数量是否一致
"""

import re
import sys
from pathlib import Path
from collections import OrderedDict
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class TableEntry:
    """表格条目"""

    original_id: int  # 原始编号
    source: str  # 来源
    function: str  # 功能
    entry_type: str  # 类型 (skills/agents)
    name: str  # 名称
    description: str  # 描述
    path: str  # 路径


@dataclass
class Section:
    """章节"""

    level: int  # 标题级别 (1-4)
    title: str  # 标题文本
    full_path: str  # 完整路径 (如 "二、开发/2.3 编程语言/Python")
    entries: List[TableEntry] = field(default_factory=list)
    subsections: Dict[str, "Section"] = field(default_factory=OrderedDict)


class ClassifiedFileMerger:
    """分类文件合并器"""

    def __init__(self):
        self.all_sections: Dict[str, Section] = OrderedDict()
        self.total_entries = 0
        self.file_entries: Dict[str, int] = {}  # 记录每个文件的条目数

    def parse_file(self, filepath: str) -> Tuple[Dict[str, Section], int]:
        """解析单个文件，返回章节结构和条目数"""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        sections: Dict[str, Section] = OrderedDict()
        entry_count = 0
        current_path: List[str] = []
        path_to_section: Dict[str, Section] = {}

        lines = content.split("\n")
        i = 0
        skip_title_level = 0
        in_stats_section = False

        while i < len(lines):
            line = lines[i]

            heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                skip_keywords = [
                    "统计",
                    "验证",
                    "分类统计",
                    "验证信息",
                    "验证结果",
                    "统计汇总",
                    "按分类统计",
                    "分类明细",
                    "Plugins 分类汇总",
                    "Awesome Copilot Skills",
                ]
                if any(kw in title for kw in skip_keywords):
                    in_stats_section = True
                    i += 1
                    continue

                in_stats_section = False

                # "Agents 目录" 特殊处理：跳过它，但继续处理子章节
                if "Agents 目录" in title or "Agents 分类汇总" in title:
                    skip_title_level = level
                    i += 1
                    continue

                # 如果当前在跳过级别之后，需要调整路径栈
                if skip_title_level > 0 and level > skip_title_level:
                    # 跳过此标题的处理（因为它是被跳过标题的子标题）
                    # 但我们仍然需要处理它的内容
                    while len(current_path) >= level - 1:
                        if current_path:
                            current_path.pop()
                    current_path.append(title)
                    full_path = "/".join(current_path)

                    if full_path not in path_to_section:
                        section = Section(
                            level=level - 1, title=title, full_path=full_path
                        )
                        sections[full_path] = section
                        path_to_section[full_path] = section
                    else:
                        section = path_to_section[full_path]

                    i += 1
                    continue

                skip_title_level = 0

                while len(current_path) >= level:
                    if current_path:
                        current_path.pop()

                current_path.append(title)
                full_path = "/".join(current_path)

                # 如果路径已存在，复用已有的 Section，避免覆盖
                if full_path not in path_to_section:
                    section = Section(level=level, title=title, full_path=full_path)
                    sections[full_path] = section
                    path_to_section[full_path] = section
                else:
                    section = path_to_section[full_path]

                i += 1
                continue

            if line.startswith("|") and "|" in line[1:]:
                if in_stats_section or "编号" in line:
                    i += 1
                    continue

                parts = [p.strip() for p in line.split("|")]
                parts = [p for p in parts if p]

                if len(parts) >= 2 and parts[1] == "来源":
                    i += 1
                    continue

                if re.match(r"^\|[\s\-:|]+\|$", line):
                    i += 1
                    continue

                if len(parts) >= 6:
                    try:
                        entry_id = int(parts[0])
                        entry = TableEntry(
                            original_id=entry_id,
                            source=parts[1],
                            function=parts[2],
                            entry_type=parts[3],
                            name=parts[4],
                            description=parts[5],
                            path=parts[6] if len(parts) >= 7 else "",
                        )

                        if current_path:
                            current_full_path = "/".join(current_path)
                            if current_full_path in path_to_section:
                                path_to_section[current_full_path].entries.append(entry)
                                entry_count += 1
                    except (ValueError, IndexError):
                        pass

            i += 1

        return sections, entry_count

    def merge_sections(
        self, base_sections: Dict[str, Section], new_sections: Dict[str, Section]
    ) -> Dict[str, Section]:
        """合并两个章节字典"""
        merged = OrderedDict(base_sections)

        for path, section in new_sections.items():
            if path in merged:
                # 合并条目
                merged[path].entries.extend(section.entries)
            else:
                # 添加新章节
                merged[path] = section

        return merged

    def merge_files(self, filepaths: List[str]) -> None:
        """合并多个文件"""
        for filepath in filepaths:
            print(f"正在解析: {filepath}")
            sections, count = self.parse_file(filepath)
            self.file_entries[filepath] = count
            self.all_sections = self.merge_sections(self.all_sections, sections)
            self.total_entries += count
            print(f"  - 条目数: {count}")

    def renumber_entries(self) -> None:
        """重新编号所有条目（按排序后的章节顺序）"""
        sorted_sections = sorted(
            self.all_sections.items(), key=lambda x: self.get_section_order_key(x[0])
        )
        new_id = 1
        for path, section in sorted_sections:
            for entry in section.entries:
                entry.original_id = new_id
                new_id += 1

    def get_section_order_key(self, path: str) -> Tuple[int, int, int, int, str]:
        """获取章节排序键，按数字顺序排列"""
        section_order = {
            "零、工具": 0,
            "一、开发前": 1,
            "一、开发前 (Pre-Development)": 1,
            "二、开发": 2,
            "二、开发 (Development)": 2,
            "三、运营": 3,
            "三、运营 (Operations)": 3,
            "Agents 目录": 4,
            "合并分类汇总": -1,
            "Awesome Claude Code Subagents 技能分类汇总": -1,
        }

        def extract_number(title: str) -> Tuple[int, int]:
            """从标题中提取编号，返回 (主编号, 子编号)"""
            match = re.search(r"(\d+)\.(\d+)", title)
            if match:
                return (int(match.group(1)), int(match.group(2)))
            match = re.search(r"^(\d+)\s", title)
            if match:
                return (0, int(match.group(1)))
            return (99, 99)

        parts = path.split("/")

        main_section = parts[0] if parts else ""
        main_order = section_order.get(main_section, 50)

        sub_order = (99, 99)
        subsub_order = 0
        subsubsub_order = 0
        title_sort = ""

        if len(parts) >= 2:
            sub_order = extract_number(parts[1])
            title_sort = parts[1]

        if len(parts) >= 3:
            subsub_order = extract_number(parts[2])[1]
            title_sort = parts[2]

        if len(parts) >= 4:
            subsubsub_order = extract_number(parts[3])[1]
            title_sort = parts[3]

        return (main_order, sub_order[0], sub_order[1], subsub_order, title_sort)

    def generate_output(self, output_path: str, title: str = "合并分类汇总") -> None:
        """生成合并后的文件"""
        lines = []

        # 文件头
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"> 本文件由多个分类文件合并生成")
        lines.append(f"> 总条目数: {self.total_entries}条")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 按顺序输出章节
        sorted_sections = sorted(
            self.all_sections.items(), key=lambda x: self.get_section_order_key(x[0])
        )

        current_level1 = ""
        current_level2 = ""
        current_level3 = ""

        for path, section in sorted_sections:
            parts = path.split("/")
            level = len(parts)

            # 跳过文件头类章节和无条目的章节
            order_key = self.get_section_order_key(path)
            if order_key[0] < 0 or not section.entries:
                continue

            # 输出标题
            if level >= 1 and parts[0] != current_level1:
                current_level1 = parts[0]
                current_level2 = ""
                current_level3 = ""
                lines.append(f"# {current_level1}")
                lines.append("")

            if level >= 2 and parts[1] != current_level2:
                current_level2 = parts[1]
                current_level3 = ""
                lines.append(f"## {current_level2}")
                lines.append("")

            if level >= 3 and (level < 3 or parts[2] != current_level3):
                current_level3 = parts[2]
                lines.append(f"### {current_level3}")
                lines.append("")

            if level >= 4:
                lines.append(f"#### {parts[3]}")
                lines.append("")

            # 输出表格
            if section.entries:
                lines.append("")
                lines.append("| 编号 | 来源 | 功能 | 类型 | 名称 | 描述 | 路径 |")
                lines.append("|------|------|------|------|------|------|------|")
                for entry in section.entries:
                    lines.append(
                        f"| {entry.original_id} | {entry.source} | {entry.function} | {entry.entry_type} | {entry.name} | {entry.description} | {entry.path} |"
                    )
                lines.append("")

        # 添加统计汇总
        lines.append("---")
        lines.append("")
        lines.append("# 统计汇总")
        lines.append("")
        lines.append("## 按分类统计")
        lines.append("")
        lines.append("| 分类 | 条目数量 |")
        lines.append("|------|---------|")

        # 统计各分类
        category_stats = OrderedDict()
        for path, section in sorted_sections:
            if section.entries:
                main_cat = path.split("/")[0]
                if main_cat not in category_stats:
                    category_stats[main_cat] = 0
                category_stats[main_cat] += len(section.entries)

        for cat, count in category_stats.items():
            lines.append(f"| {cat} | {count} |")

        lines.append(f"| **总计** | **{self.total_entries}** |")
        lines.append("")

        # 验证信息
        lines.append("---")
        lines.append("")
        lines.append("## 验证结果")
        lines.append("")

        for filepath, count in self.file_entries.items():
            filename = Path(filepath).name
            lines.append(f"- {filename}: {count}条")

        lines.append(f"- 合并后总条目数: {self.total_entries}条")
        lines.append("")

        # 计算实际条目数
        actual_count = sum(len(s.entries) for s in self.all_sections.values())
        if actual_count == self.total_entries:
            lines.append("**✅ 验证通过：合并前后条目数量一致。**")
        else:
            lines.append(
                f"**⚠️ 警告：条目数量不一致！预期 {self.total_entries}，实际 {actual_count}**"
            )

        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"\n输出文件已生成: {output_path}")

    def verify(self) -> bool:
        """验证合并结果"""
        actual_count = sum(len(s.entries) for s in self.all_sections.values())

        print("\n=== 验证结果 ===")
        print(f"源文件条目统计:")
        for filepath, count in self.file_entries.items():
            filename = Path(filepath).name
            print(f"  - {filename}: {count}条")

        print(f"\n预期总条目数: {self.total_entries}")
        print(f"实际合并条目数: {actual_count}")

        if actual_count == self.total_entries:
            print("✅ 验证通过：合并前后条目数量一致！")
            return True
        else:
            print(
                f"❌ 验证失败：条目数量不一致！差异: {self.total_entries - actual_count}"
            )
            return False


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print(
            "用法: python merge_classified_files.py <输出文件> <输入文件1> [输入文件2] ..."
        )
        print("示例: python merge_classified_files.py merged.md file1.md file2.md")
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]

    # 检查输入文件是否存在
    for filepath in input_files:
        if not Path(filepath).exists():
            print(f"错误: 文件不存在 - {filepath}")
            sys.exit(1)

    print(f"=== 开始合并 {len(input_files)} 个文件 ===\n")

    # 创建合并器并执行合并
    merger = ClassifiedFileMerger()
    merger.merge_files(input_files)

    # 重新编号
    merger.renumber_entries()

    # 验证
    if not merger.verify():
        print("\n警告：条目数量不一致，请检查输入文件！")

    # 生成输出
    merger.generate_output(output_file)

    print(f"\n=== 合并完成 ===")
    print(f"输出文件: {output_file}")
    print(f"总条目数: {merger.total_entries}")


if __name__ == "__main__":
    main()
