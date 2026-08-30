<h1 style="text-align: center;">智能文件备份工具</h1>

**涉及库**: `os`, `pathlib`, `shutil`, `glob`, `json`, `argparse`

# 1. 功能需求

创建一个命令行备份工具，支持：

- 按文件扩展名筛选要备份的文件
- 增量备份（只备份修改过的文件）
- 记录备份历史（`JSON` 格式）
- 显示备份统计信息

# 2. 代码框架

```python
#!/usr/bin/env python3
"""
智能文件备份工具
使用方法: python backup_tool.py <源目录> <目标目录> --ext .py .txt --incremental
"""

import os
import json
import argparse
import shutil
from pathlib import Path
from glob import glob
from datetime import datetime


class BackupTool:
    def __init__(self, source, target, extensions=None, incremental=False):
        self.source = Path(source)
        self.target = Path(target)
        self.extensions = extensions or []
        self.incremental = incremental
        self.history_file = self.target / ".backup_history.json"
        self.history = self._load_history()
        
    def _load_history(self):
        """加载备份历史"""
        # TODO: 使用 json 模块加载历史记录
        pass
    
    def _save_history(self):
        """保存备份历史"""
        # TODO: 使用 json 模块保存历史记录
        pass
    
    def _should_backup(self, file_path):
        """判断文件是否需要备份（增量模式）"""
        # TODO: 比较文件修改时间
        pass
    
    def find_files(self):
        """查找所有需要备份的文件"""
        # TODO: 使用 os.walk 或 glob 查找文件
        pass
    
    def backup(self):
        """执行备份"""
        # TODO: 使用 shutil.copy2 备份文件
        # TODO: 使用 os.makedirs 或 Path.mkdir 创建目录
        pass
    
    def show_stats(self):
        """显示备份统计"""
        pass


def main():
    parser = argparse.ArgumentParser(description="智能文件备份工具")
    parser.add_argument("source", help="源目录路径")
    parser.add_argument("target", help="目标目录路径")
    parser.add_argument("--ext", nargs="+", help="要备份的文件扩展名，如 .py .txt")
    parser.add_argument("--incremental", action="store_true", help="增量备份模式")
    parser.add_argument("--dry-run", action="store_true", help="只显示将备份的文件，不实际执行")
    
    args = parser.parse_args()
    
    # TODO: 验证源目录是否存在
    # TODO: 创建备份工具实例并执行备份


if __name__ == "__main__":
    main()

```

# 3. 练习任务

1. 补全 `_load_history()` 和 `_save_history()` 方法
2. 实现 `_should_backup()` 方法，比较文件的修改时间
3. 使用 `os.walk()` 或 `pathlib.Path.rglob()` 查找文件
4. 用 `shutil.copy2()` 复制文件（保留元数据）
5. 添加 `--dry-run` 功能（只显示不执行）

# 4. 实现

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能文件备份工具
"""

import os
import json
import shutil
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Iterable

logger = logging.getLogger(__name__)


class BackupTool(object):

    def __init__(
            self,
            source_dir: str | os.PathLike | Path,
            target_dir: str | os.PathLike | Path,
            extensions: Optional[Iterable] = None,
            ignore_dirs: Optional[Iterable] = None,
            incremental: bool = True,
            dry_run: bool = False,
    ):
        """

        Args:
            source_dir (): 需要备份的源文件的文件夹地址
            target_dir (): 需要将源文件备份到此文件夹下面
            extensions (): 需要备份的文件扩展名
            ignore_dirs (): 需要忽略备份的文件夹
            incremental (): 是否增量备份, 默认为是
            dry_run (): 如果此参数为 True, 只显示不执行
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.extensions = [item.lower() for item in (extensions or [])]
        self.ignore_dirs = ignore_dirs or [
            '.venv', 'venv', '.idea', '.vscode', 'node_modules'
        ]
        self.incremental = incremental
        self.dry_run = dry_run

        start_time: Optional[datetime] | str = None
        end_time: Optional[datetime] | str = None

        self._history_file = self.target_dir / ".backup_history.json"
        self._history = self._load_history()

        # 当前批次备份状态统计
        self._stats = {
            'total': 0,
            'backed': 0,
            'skipped': 0,
            'failed': 0,
            'total_size': 0,
            'start': start_time,
            'end': end_time,
            'backup_files': [],
        }

        Path('E:\\Code\\PyProjects\\Demos\\practice\\logs').mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=self.source_dir / 'logs' / 'log.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

    def _load_history(self) -> Dict:
        """加载备份记录(JSON格式)"""
        if not self._history_file.exists():
            return {}

        try:
            with open(self._history_file, 'r', encoding='utf-8') as fp:
                return json.load(fp)
        except (PermissionError, IOError) as e:
            logger.error(f'加载历史备份文件出错: {e}')
        except Exception as e:
            logger.error(f'加载历史备份文件出现其他未知错误: {e}')

        return {}

    def _save_history(self) -> None:
        """保存备份历史记录到JSON文件"""
        self._history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._history_file, 'w', encoding='utf-8') as fp:
            json.dump(self._history, fp, indent=4, ensure_ascii=False)

    @staticmethod
    def _get_file_info(file_path: Path) -> Dict:
        """获取文件信息"""
        stat = file_path.stat()
        # stat = os.stat(str(file_path))
        return {
            'file_size': stat.st_size,  # 备份文件的大小
            'file_mtime': stat.st_mtime,  # 备份文件的最后一次修改时间
            'file_mode': stat.st_mode,  # 备份文件的权限模式
            'file_backup_time': datetime.now().isoformat(),  # 备份的时间
        }

    def _should_backup(self, file_path: Path) -> bool:
        """是否需要备份文件"""
        if not self.incremental:
            return True

        rel_path = str(file_path.relative_to(self.source_dir))
        if rel_path not in self._history:
            return True

        cur_file_info = self._get_file_info(file_path)
        old_history = self._history[rel_path]

        # 如果大小不同或上次备份后又进行了修改
        return old_history['file_mtime'] < cur_file_info['file_mtime'] \
            or old_history['file_size'] != cur_file_info['file_size']

    def _matches_extensions(self, file_path: Path) -> bool:
        """判断文件扩展名是否匹配"""
        if not self.extensions:
            return True
        return file_path.suffix.lower() in self.extensions

    def find_files(self):
        """查找所有可备份的文件"""
        files = []

        for root, dirs, filenames in os.walk(self.source_dir):
            # 首先要将忽略文件夹排除在外
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith('.') and d not in self.ignore_dirs
            ]

            for filename in filenames:
                if filename.startswith('.'):
                    self._stats['skipped'] += 1
                    continue

                full_path = Path(root) / filename
                if self._matches_extensions(full_path):
                    files.append(full_path)
        return files

    def backup_single(self, file_path: Path, dry_run: bool = False):
        """备份一个文件 -- shutil.copy2 备份, 可以备份元信息."""

        # 为了让备份过去的备份文件和源目录中的被备份文件具有相同的目录结构
        rel_path = file_path.relative_to(self.source_dir)
        target_file_path = self.target_dir / rel_path

        if not self._should_backup(file_path):
            self._stats['skipped'] += 1
            return True

        if dry_run:
            self._stats['backed'] += 1
            self._stats['total'] += 1
            self._stats['total_size'] += file_path.stat().st_size
            self._stats['backup_files'].append(file_path)
            return True

        try:
            target_file_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(file_path, target_file_path)

            self._stats['backed'] += 1
            self._stats['total'] += 1
            self._stats['total_size'] += file_path.stat().st_size
            self._stats['backup_files'].append(file_path)
            return True
        except (PermissionError, IOError) as e:
            logger.error(f'拷贝文件过程出错: {e}')
        except Exception as e:
            logger.error(f'拷贝文件过程中出现未知错误: {e}')

        self._stats['failed'] += 1
        return False

    def _show_stats(self):
        """显示统计"""
        duration = (self._stats["end"] - self._stats["start"]).total_seconds()
        print(f"\n已备份: {self._stats['backed']} | "
              f"跳过: {self._stats['skipped']} | "
              f"失败: {self._stats['failed']} | "
              f"耗时: {duration:.2f}秒\n")

    def backup(self, dry_run: bool = False):
        """备份所有文件"""
        self._stats['start'] = datetime.now()

        print('=' * 120)
        print(f"源目录:\t\t{self.source_dir}")
        print(f"目标目录:\t{self.target_dir}")
        print(f"备份模式:\t{'增量备份' if self.incremental else '全量备份'}")
        print(f"忽略文件夹:\t{self.ignore_dirs}")
        print(f"备份扩展名:\t{self.extensions}")
        print('=' * 120)

        if not os.path.isdir(self.source_dir):
            print("源文件夹不存在！")
            return self._stats

        files = self.find_files()
        self._stats["total"] = len(files)
        print(f"找到 {len(files)} 个文件\n")

        if not dry_run:
            self.target_dir.mkdir(parents=True, exist_ok=True)

        # 备份每个文件
        for i, file_path in enumerate(files):
            rel_path = file_path.relative_to(self.source_dir)
            print(f"[{i}/{len(files)}] {rel_path}", end="")
            success = self.backup_single(file_path, dry_run)
            print(" ✓" if success else " ✗")

        # 保存历史
        if not dry_run:
            self._save_history()

        self._stats["end"] = datetime.now()
        self._show_stats()
        return self._stats


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('source', help='源目录')
    parser.add_argument('target', help='目标目录')
    parser.add_argument('-e', '--extensions', nargs='+', help='文件扩展名过滤')
    parser.add_argument('-n', '--neglect', nargs='*', help='忽略的文件夹列表')
    parser.add_argument('-i', '--inmcrement', action='store_true', help='增量备份模式开关')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行')

    args = parser.parse_args(
        [
            r'E:\Code\PyProjects\Demos\practice',
            r'E:\000backup\001ok',
            '-e',
            '.json',
            '.jsonl',
            '.md',
            '.py',
            '-i',
        ]
    )

    BackupTool(
        args.source,
        args.target,
        args.extensions,
        args.neglect,
        args.inmcrement,
        args.dry_run,
    ).backup(args.dry_run)


if __name__ == '__main__':
    main()

```

