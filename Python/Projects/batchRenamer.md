<h1 style="text-align: center;">批量重命名工具</h1>

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量文件重命名工具
使用方法:
  python renamer.py <目录> --prefix "photo_"
  python renamer.py <目录> --suffix "_backup"
  python renamer.py <目录> --seq "img" --start 1
  python renamer.py <目录> --regex "old" --replace "new"
  python renamer.py <目录> --undo
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class FileRenamer:
    """批量文件重命名工具"""

    def __init__(self, directory: str):
        self.directory = Path(directory).resolve()
        self.history_file = self.directory / ".rename_history.json"
        self.rename_map: Dict[str, str] = {}

    def _load_history(self) -> Dict:
        """加载历史记录（JSON）"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_history(self, history: Dict) -> None:
        """保存历史记录"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def _get_files(self, ext: Optional[str] = None) -> List[Path]:
        """获取文件列表"""
        pattern = f"*{ext}" if ext else "*"
        files = [f for f in self.directory.glob(pattern)
                 if f.is_file() and not f.name.startswith('.')]
        return sorted(files, key=lambda x: x.name)

    def add_prefix(self, prefix: str, ext: Optional[str] = None) -> int:
        """添加前缀"""
        files = self._get_files(ext)
        for f in files:
            self.rename_map[f.name] = prefix + f.name
        return len(files)

    def add_suffix(self, suffix: str, ext: Optional[str] = None) -> int:
        """添加后缀（扩展名前）"""
        files = self._get_files(ext)
        for f in files:
            name, extension = os.path.splitext(f.name)
            self.rename_map[f.name] = f"{name}{suffix}{extension}"
        return len(files)

    def sequential_rename(self, base_name: str, start: int = 1,
                          ext: Optional[str] = None, padding: int = 3) -> int:
        """序号命名"""
        files = self._get_files(ext)
        for i, f in enumerate(files):
            _, extension = os.path.splitext(f.name)
            num = str(start + i).zfill(padding)
            self.rename_map[f.name] = f"{base_name}_{num}{extension}"
        return len(files)

    def regex_replace(self, pattern: str, replacement: str,
                      ext: Optional[str] = None) -> int:
        """正则替换"""
        files = self._get_files(ext)
        count = 0
        for f in files:
            new_name = re.sub(pattern, replacement, f.name)
            if new_name != f.name:
                self.rename_map[f.name] = new_name
                count += 1
        return count

    def preview(self) -> None:
        """预览重命名"""
        if not self.rename_map:
            print("没有文件需要重命名")
            return

        print(f"\n{'=' * 60}")
        print("预览重命名:")
        print(f"{'=' * 60}")
        for old, new in self.rename_map.items():
            print(f"  {old} → {new}")
        print(f"\n共 {len(self.rename_map)} 个文件")

    def execute(self, dry_run: bool = False, yes: bool = False) -> bool:
        """执行重命名"""
        if not self.rename_map:
            return False

        self.preview()

        if dry_run:
            print("\n[模拟运行] 未实际修改")
            return True

        if not yes:
            response = input("\n确认执行? [y/N]: ").strip().lower()
            if response not in ('y', 'yes'):
                print("已取消")
                return False

        # 执行
        backup_map = {}
        for old_name, new_name in self.rename_map.items():
            old_path = self.directory / old_name
            new_path = self.directory / new_name

            try:
                old_path.rename(new_path)  # Path.rename
                backup_map[new_name] = old_name
                print(f"  ✓ {old_name} → {new_name}")
            except OSError as e:
                print(f"  ✗ {old_name}: {e}")

        # 保存历史
        if backup_map:
            history = self._load_history()
            history[datetime.now().isoformat()] = {
                "operations": backup_map
            }
            self._save_history(history)

        return True

    def undo(self) -> bool:
        """撤销上次操作"""
        history = self._load_history()
        if not history:
            print("没有可撤销的操作", file=sys.stderr)
            return False

        latest = max(history.keys())
        operations = history[latest]["operations"]

        print(f"\n撤销操作 ({latest}):")
        for new_name, old_name in operations.items():
            current = self.directory / new_name
            original = self.directory / old_name
            if current.exists():
                current.rename(original)
                print(f"  ✓ {new_name} → {old_name}")

        del history[latest]
        self._save_history(history)
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="批量文件重命名工具")

    parser.add_argument("directory", help="要处理的目录")

    # 重命名模式（互斥）
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--prefix", metavar="PREFIX", help="添加前缀")
    group.add_argument("--suffix", metavar="SUFFIX", help="添加后缀")
    group.add_argument("--seq", metavar="NAME", help="序号命名")
    group.add_argument("--regex", metavar="PATTERN", help="正则表达式")
    group.add_argument("--undo", action="store_true", help="撤销")

    parser.add_argument("--replace", metavar="TEXT", help="替换字符串")
    parser.add_argument("--start", type=int, default=1, help="起始序号")
    parser.add_argument("--ext", metavar=".EXT", help="文件扩展名")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("-y", action="store_true", help="跳过确认")

    args = parser.parse_args()

    # 验证目录
    if not os.path.isdir(args.directory):
        print(f"错误: 目录不存在", file=sys.stderr)
        sys.exit(1)

    renamer = FileRenamer(args.directory)

    # 执行操作
    if args.undo:
        success = renamer.undo()
        sys.exit(0 if success else 1)

    if args.regex and not args.replace:
        print("错误: 需要 --replace 参数", file=sys.stderr)
        sys.exit(1)

    # 执行重命名
    count = 0
    if args.prefix:
        count = renamer.add_prefix(args.prefix, args.ext)
    elif args.suffix:
        count = renamer.add_suffix(args.suffix, args.ext)
    elif args.seq:
        count = renamer.sequential_rename(args.seq, args.start, args.ext)
    elif args.regex:
        count = renamer.regex_replace(args.regex, args.replace, args.ext)

    if count > 0:
        renamer.execute(args.dry_run, args.y)
    else:
        print("没有匹配的文件")

    sys.exit(0)


if __name__ == "__main__":
    main()

```

