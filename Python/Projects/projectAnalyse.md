<h1 style="text-align: center;">项目分析器</h1>

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
项目结构分析器
使用方法:
  python analyzer.py <项目目录>
  python analyzer.py <项目目录> --output report.json
  python analyzer.py <项目目录> --max-depth 3 --tree
  python analyzer.py <项目目录> --duplicates
"""

import sys
import os
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Any


class ProjectAnalyzer:
    """项目结构分析器"""

    def __init__(self, project_path: str,
                 max_depth: Optional[int] = None,
                 exclude_dirs: Optional[List[str]] = None):
        self.project_path = Path(project_path).resolve()
        self.max_depth = max_depth
        self.exclude_dirs = set(exclude_dirs or [])

        # 使用 defaultdict 自动初始化
        self.stats = {
            "files_by_ext": defaultdict(list),
            "total_size": 0,
            "total_files": 0,
            "total_dirs": 0,
            "empty_dirs": [],
            "largest_files": []
        }

        # 默认排除目录
        self.default_excludes = {
            '.git', '__pycache__', 'node_modules',
            '.venv', 'venv', '.idea', '.vscode'
        }
        self.all_excludes = self.default_excludes | self.exclude_dirs

    def _should_skip(self, dir_name: str) -> bool:
        """判断是否跳过目录"""
        return dir_name.startswith('.') or dir_name in self.all_excludes

    def _get_depth(self, path: Path) -> int:
        """计算路径深度"""
        try:
            return len(path.relative_to(self.project_path).parts)
        except ValueError:
            return 0

    def analyze(self) -> Dict[str, Any]:
        """分析项目结构"""
        if not self.project_path.is_dir():
            print(f"错误: 目录不存在", file=sys.stderr)
            return dict(self.stats)

        print(f"\n正在分析: {self.project_path}")

        # 使用 os.walk 遍历
        for root, dirs, files in os.walk(self.project_path):
            current_path = Path(root)
            depth = self._get_depth(current_path)

            # 深度限制
            if self.max_depth and depth > self.max_depth:
                dirs.clear()
                continue

            # 过滤目录（原地修改 dirs）
            dirs[:] = [d for d in dirs if not self._should_skip(d)]

            # 统计目录
            self.stats["total_dirs"] += 1

            # 检测空目录
            if not files and not dirs:
                rel_path = current_path.relative_to(self.project_path)
                self.stats["empty_dirs"].append(str(rel_path))

            # 处理文件
            for filename in files:
                if filename.startswith('.'):
                    continue
                file_path = current_path / filename
                self._process_file(file_path)

        # 找出最大文件
        self._find_largest_files()

        return dict(self.stats)

    def _process_file(self, file_path: Path) -> None:
        """处理单个文件"""
        try:
            stat = file_path.stat()
            size = stat.st_size

            self.stats["total_files"] += 1
            self.stats["total_size"] += size

            # 扩展名
            ext = file_path.suffix.lower() or '<无扩展名>'

            file_info = {
                "path": str(file_path.relative_to(self.project_path)),
                "size": size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }

            # defaultdict 自动处理不存在的键
            self.stats["files_by_ext"][ext].append(file_info)

        except OSError:
            pass

    def _find_largest_files(self, top_n: int = 10) -> None:
        """找出最大的文件"""
        all_files = []

        for files in self.stats["files_by_ext"].values():
            all_files.extend(files)

        # 按大小排序
        sorted_files = sorted(all_files, key=lambda x: x["size"], reverse=True)
        self.stats["largest_files"] = sorted_files[:top_n]

    def generate_tree(self, max_depth: Optional[int] = None) -> str:
        """生成目录树"""
        lines = [f"{self.project_path.name}/"]

        def _build_tree(path: Path, prefix: str = "", depth: int = 0):
            if max_depth and depth >= max_depth:
                return

            try:
                entries = sorted(
                    path.iterdir(),
                    key=lambda x: (x.is_file(), x.name.lower())
                )
                entries = [e for e in entries if not (
                        e.is_dir() and self._should_skip(e.name)
                ) and not e.name.startswith('.')]

                for i, entry in enumerate(entries):
                    is_last = i == len(entries) - 1
                    symbol = "└── " if is_last else "├── "

                    if entry.is_dir():
                        lines.append(f"{prefix}{symbol}{entry.name}/")
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        _build_tree(entry, next_prefix, depth + 1)
                    else:
                        size = entry.stat().st_size
                        lines.append(f"{prefix}{symbol}{entry.name} ({self._format_size(size)})")

            except PermissionError:
                lines.append(f"{prefix}[权限不足]")

        _build_tree(self.project_path)
        return "\n".join(lines)

    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def print_summary(self) -> None:
        """打印摘要"""
        print(f"\n{'=' * 50}")
        print("项目分析报告")
        print(f"{'=' * 50}")
        print(f"总文件数: {self.stats['total_files']}")
        print(f"总目录数: {self.stats['total_dirs']}")
        print(f"总大小: {self._format_size(self.stats['total_size'])}")

        # 按扩展名
        print(f"\n{'─' * 50}")
        print("文件类型分布:")
        for ext, files in sorted(self.stats["files_by_ext"].items()):
            total = sum(f["size"] for f in files)
            print(f"  {ext:<15} {len(files):>3} 个文件  {self._format_size(total)}")

        # 最大文件
        if self.stats["largest_files"]:
            print(f"\n{'─' * 50}")
            print("最大的文件:")
            for i, f in enumerate(self.stats["largest_files"][:5], 1):
                print(f"  {i}. {f['path']:<30} {self._format_size(f['size'])}")

        # 空目录
        if self.stats["empty_dirs"]:
            print(f"\n{'─' * 50}")
            print(f"空目录 ({len(self.stats['empty_dirs'])} 个):")
            for d in self.stats["empty_dirs"]:
                print(f"  {d}")

        print(f"{'=' * 50}\n")

    def export_json(self, output_file: str) -> None:
        """导出到JSON"""
        # 转换 defaultdict 为普通 dict
        export_data = {
            "summary": {
                "total_files": self.stats["total_files"],
                "total_dirs": self.stats["total_dirs"],
                "total_size": self.stats["total_size"]
            },
            "files_by_extension": dict(self.stats["files_by_ext"]),
            "largest_files": self.stats["largest_files"],
            "empty_dirs": self.stats["empty_dirs"]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"✓ 报告已导出: {output_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="项目结构分析器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("path", help="项目目录")
    parser.add_argument("--output", "-o", metavar="FILE", help="输出JSON报告")
    parser.add_argument("--max-depth", type=int, metavar="N", help="最大扫描深度")
    parser.add_argument("--exclude", nargs="*", metavar="DIR", help="排除目录")
    parser.add_argument("--tree", action="store_true", help="显示目录树")
    parser.add_argument("--tree-depth", type=int, help="目录树深度")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式")

    args = parser.parse_args()

    # 验证路径
    if not os.path.exists(args.path):
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.path):
        print(f"错误: 不是目录: {args.path}", file=sys.stderr)
        sys.exit(1)

    # 创建分析器
    analyzer = ProjectAnalyzer(
        project_path=args.path,
        max_depth=args.max_depth,
        exclude_dirs=args.exclude
    )

    # 执行分析
    analyzer.analyze()

    # 显示目录树
    if args.tree:
        print("\n" + analyzer.generate_tree(args.tree_depth))

    # 打印摘要
    if not args.quiet:
        analyzer.print_summary()

    # 导出
    if args.output:
        analyzer.export_json(args.output)

    sys.exit(0)


if __name__ == "__main__":
    main()

```

