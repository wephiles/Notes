#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件树打印程序 —— 类似 Linux `tree` 命令的目录树可视化工具。

功能：
    1. 可选择只打印文件夹，或同时打印文件夹和文件。
    2. 可控制打印深度（width），0 表示不限制，默认 3。
    3. 可自定义忽略列表，跳过指定的文件/文件夹（如 .venv、__pycache__ 等）。
    4. 面向对象设计，使用 argparse 解析命令行参数。

用法示例：
    python file_tree.py                        # 打印当前目录，深度默认 3
    python file_tree.py /home/user             # 打印指定目录
    python file_tree.py -d                     # 只打印文件夹
    python file_tree.py -w 5                   # 深度设为 5
    python file_tree.py -w 0                   # 不限制深度
    python file_tree.py -i .venv -i .git        # 忽略 .venv 和 .git
    python file_tree.py -i .venv,.git          # 逗号分隔忽略列表
    python file_tree.py -a                     # 显示所有文件（不忽略任何文件）
"""

import os
import argparse


class FileTreePrinter:
    """
    文件树打印器类。
    用于以类似 Linux `tree` 命令的格式打印目录结构。

    功能说明：
        - 支持选择只打印文件夹，或打印文件夹+文件。
        - 支持控制打印深度（max_depth），0 表示不限制。
        - 支持自定义忽略列表，跳过指定的文件/文件夹名称。
    """

    def __init__(self, root_path, dirs_only=False, max_depth=3, ignore_list=None):
        """
        初始化文件树打印器。

        参数:
            root_path  (str)         : 要打印的根目录路径。
            dirs_only  (bool)        : 是否只打印文件夹。True 表示只打印文件夹，
                                        False 表示同时打印文件夹和文件。默认为 False。
            max_depth  (int)         : 最大打印深度。0 表示不限制。默认为 3。
                                        深度从根目录开始计算，根目录为第 0 层，
                                        其直接子项为第 1 层，以此类推。
            ignore_list(list or None): 需要忽略的文件/文件夹名称列表。
                                        例如 ['.venv', '__pycache__', '.git']。默认为 None。
        """
        self.root_path = os.path.abspath(root_path)
        self.dirs_only = dirs_only
        self.max_depth = max_depth
        # 如果没有传入忽略列表，则使用空列表
        self.ignore_list = ignore_list if ignore_list is not None else []
        # 用于统计的计数器
        self.dir_count = 0  # 目录计数（不包含根目录本身）
        self.file_count = 0  # 文件计数

    # ================================================================== #
    #  核心方法
    # ================================================================== #

    def print_tree(self):
        """
        打印文件树的入口方法。
        先打印根目录路径，然后递归打印其子内容，最后打印统计信息。
        """
        # 打印根目录的绝对路径
        print(self.root_path)

        # 递归打印根目录下的内容
        # depth=0 表示根目录的直接子项属于第 1 层
        self._print_tree_recursive(self.root_path, prefix="", depth=0)

        # 打印统计信息
        self._print_summary()

    def _print_tree_recursive(self, current_path, prefix, depth):
        """
        递归打印目录树的核心方法。

        参数:
            current_path (str) : 当前正在处理的目录路径。
            prefix       (str) : 当前行前缀字符串，用于控制缩进和树形连接线。
                                  例如 "│   " 或 "    "。
            depth        (int) : 当前深度层级。根目录的子项 depth=0，
                                  即根目录的子项是第 1 层（depth+1=1）。
        """
        # ---- 深度控制 ----
        # 如果设置了最大深度（>0），且当前深度已经达到最大深度，则停止递归
        # max_depth=0 是特殊值，表示不限制深度
        if self.max_depth > 0 and depth >= self.max_depth:
            return

        # ---- 获取目录内容 ----
        try:
            # 使用 os.listdir 获取当前目录下的所有条目
            # 排序规则：文件夹排在前面，文件排在后面；同类型内按名称不区分大小写排序
            entries = sorted(
                os.listdir(current_path),
                key=lambda name: (
                    not os.path.isdir(os.path.join(current_path, name)),  # 目录优先
                    name.lower()  # 同类型内按名称排序
                )
            )
        except PermissionError:
            # 如果没有权限访问该目录，打印提示信息并返回
            print(prefix + "└── [权限不足]")
            return

        # ---- 过滤忽略列表中的条目 ----
        entries = [e for e in entries if e not in self.ignore_list]

        # ---- 根据 dirs_only 参数决定是否包含文件 ----
        if self.dirs_only:
            entries = [e for e in entries if os.path.isdir(os.path.join(current_path, e))]

        # ---- 逐条打印 ----
        total = len(entries)
        for index, entry in enumerate(entries):
            entry_path = os.path.join(current_path, entry)
            is_last = (index == total - 1)  # 是否是最后一个条目

            # 构建当前行的树形连接符
            # 如果是最后一个，用 "└──"（拐角），否则用 "├──"（分支）
            connector = "└── " if is_last else "├── "

            # 打印当前条目（前缀 + 连接符 + 名称）
            print(prefix + connector + entry)

            # 如果当前条目是目录，则递归处理其子内容
            if os.path.isdir(entry_path):
                self.dir_count += 1
                # 计算下一层的 prefix：
                # 如果当前条目是最后一个，下一层前缀追加 "    "（四个空格）
                # 否则追加 "│   "（竖线+三个空格），用于保持树形结构的连续性
                next_prefix = prefix + ("    " if is_last else "│   ")
                self._print_tree_recursive(entry_path, next_prefix, depth + 1)
            else:
                self.file_count += 1

    # ================================================================== #
    #  辅助方法
    # ================================================================== #

    def _print_summary(self):
        """
        打印统计信息，包括目录数量和文件数量。
        格式类似 `tree` 命令的输出，如:
            "7 directories, 12 files"
            "5 directories"
            "1 directory, 1 file"
        """
        print()
        parts = []
        # 目录数：处理单复数
        parts.append(f"{self.dir_count} director{'ies' if self.dir_count != 1 else 'y'}")
        # 文件数：仅在 dirs_only=False 时统计
        if not self.dirs_only:
            parts.append(f"{self.file_count} file{'s' if self.file_count != 1 else ''}")
        print(", ".join(parts))


# ====================================================================== #
#  命令行参数解析 & 程序入口
# ====================================================================== #

def parse_args():
    """
    使用 argparse 解析命令行参数。

    支持的参数:
        path (位置参数)        : 要打印的目录路径，默认为当前目录 "."。
        -d / --dirs-only      : 只打印文件夹（不打印文件）。
        -w / --width N        : 打印深度，0 表示不限制，默认为 3。
        -i / --ignore NAME    : 忽略的文件/文件夹名称，可多次使用或逗号分隔。
        -a / --all            : 显示所有文件，不忽略任何内容（会覆盖 -i 参数）。

    返回:
        argparse.Namespace: 解析后的参数对象。
    """
    parser = argparse.ArgumentParser(
        description="打印目录文件树（类似 Linux tree 命令）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
        示例:
          python file_tree.py                            # 打印当前目录，深度默认 3
          python file_tree.py /home/user                 # 打印指定目录
          python file_tree.py -d                         # 只打印文件夹
          python file_tree.py -w 5                       # 深度设为 5
          python file_tree.py -w 0                       # 不限制深度
          python file_tree.py -i .venv -i .git           # 忽略 .venv 和 .git
          python file_tree.py -i .venv,.git,__pycache__  # 逗号分隔忽略列表
          python file_tree.py -a                         # 显示所有文件（不忽略任何文件）
        """
    )

    # 位置参数：目录路径，默认为当前目录
    parser.add_argument(
        "path",
        nargs="?",  # "?" 表示可选位置参数
        default=".",
        help="要打印的目录路径（默认: 当前目录 '.'）"
    )

    # 可选参数：只打印文件夹
    parser.add_argument(
        "-d", "--dirs-only",
        action="store_true",
        default=False,
        help="只打印文件夹（不打印文件）"
    )

    # 可选参数：打印深度（宽度）
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=3,
        metavar="N",
        help="打印深度，0 表示不限制（默认: 3）"
    )

    # 可选参数：忽略列表（可多次使用 -i 指定多个）
    parser.add_argument(
        "-i", "--ignore",
        action="append",
        default=None,
        metavar="NAME",
        help="要忽略的文件/文件夹名称，可多次使用。也支持逗号分隔（如: -i .venv,.git）"
    )

    # 可选参数：显示所有文件（清除忽略列表）
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        default=False,
        help="显示所有文件，不忽略任何文件或文件夹（会覆盖 -i 参数）"
    )

    return parser.parse_args()


def main():
    """程序主入口函数。"""
    # 解析命令行参数
    args = parse_args()

    # ---- 处理忽略列表 ----
    # 默认忽略的文件/文件夹（可根据需要自行修改）
    default_ignore = []

    if args.all:
        # -a 参数：不忽略任何内容
        ignore_list = []
    elif args.ignore:
        # 用户通过 -i 传入了忽略列表
        # 支持逗号分隔的形式，例如 -i .venv,.git
        ignore_list = []
        for item in args.ignore:
            # 将逗号分隔的字符串拆分为单独的名称
            parts = [p.strip() for p in item.split(",")]
            ignore_list.extend(parts)
        # 合并默认忽略列表
        ignore_list = default_ignore + ignore_list
    else:
        # 没有传入 -i 也没有 -a，使用默认忽略列表
        ignore_list = default_ignore

    # ---- 校验路径 ----
    if not os.path.exists(args.path):
        print(f"错误: 路径 '{args.path}' 不存在！")
        return
    if not os.path.isdir(args.path):
        print(f"错误: '{args.path}' 不是一个目录！")
        return

    # ---- 创建打印器实例并打印文件树 ----
    printer = FileTreePrinter(
        root_path=args.path,
        dirs_only=args.dirs_only,
        max_depth=args.width,
        ignore_list=ignore_list
    )
    printer.print_tree()


if __name__ == "__main__":
    main()
