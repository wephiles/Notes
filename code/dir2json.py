# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件夹递归扫描器
功能：将文件夹结构递归遍历并转换为JSON格式的字典
作者：Python资深工程师
日期：2024
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Union


class FolderScanner:
    """
    文件夹扫描器 - 递归遍历文件夹并将其转换为字典结构

    =========================================
    核心功能：
    =========================================
    1. 递归遍历指定文件夹及其所有子文件夹
    2. 将文件和文件夹结构转换为嵌套字典对象
    3. 每个文件/文件夹包含详细信息（名称、路径、类型等）
    4. 支持自定义排除特定文件夹和文件
    5. 支持控制递归深度（避免无限递归）
    6. 支持导出为JSON文件或直接打印

    =========================================
    使用示例：
    =========================================
    scanner = FolderScanner(
        ignore_dirs=['.venv', '.idea', '.vscode'],
        ignore_files=['.gitignore'],
        max_depth=3
    )

    # 打印结构
    scanner.print_structure('/path/to/folder')

    # 保存为JSON文件
    scanner.to_json('/path/to/folder', output_file='structure.json')
    """

    # 类常量：默认忽略的文件夹
    DEFAULT_IGNORE_DIRS = ['.venv', '.idea', '.vscode', '__pycache__',
                           '.git', 'node_modules', '.pytest_cache']

    # 类常量：默认忽略的文件
    DEFAULT_IGNORE_FILES = ['.gitignore', '.DS_Store', 'Thumbs.db']

    def __init__(
            self,
            ignore_dirs: Optional[List[str]] = None,
            ignore_files: Optional[List[str]] = None,
            max_depth: int = 3,
            default_description: str = "",
            use_absolute_path: bool = True
    ):
        """
        初始化文件夹扫描器

        参数说明：
        --------------
        ignore_dirs : List[str] | None
            需要忽略的文件夹名称列表
            例如: ['.venv', '.idea', '.vscode', '__pycache__']
            如果为None，使用默认忽略列表
            如果为空列表[]，则不忽略任何文件夹

        ignore_files : List[str] | None
            需要忽略的文件名称列表
            例如: ['.gitignore', '.DS_Store']
            如果为None，使用默认忽略列表
            如果为空列表[]，则不忽略任何文件

        max_depth : int
            最大递归深度
            - 默认值: 3
            - 0 或 None: 不限制递归深度（遍历所有层级）
            - 正整数: 只遍历到指定深度

        default_description : str
            所有文件和文件夹的默认说明文字
            默认为空字符串 ""

        use_absolute_path : bool
            是否使用绝对路径
            - True: 返回绝对路径 (如 /home/user/project/file.py)
            - False: 返回相对路径 (如 ./project/file.py)
            默认为 True
        """
        # ====================================
        # 处理忽略文件夹列表
        # ====================================
        if ignore_dirs is None:
            # 使用默认忽略列表
            self.ignore_dirs: Set[str] = set(self.DEFAULT_IGNORE_DIRS)
        elif ignore_dirs == []:
            # 空列表表示不忽略任何文件夹
            self.ignore_dirs = set()
        else:
            # 使用用户自定义的忽略列表
            self.ignore_dirs = set(ignore_dirs)

        # ====================================
        # 处理忽略文件列表
        # ====================================
        if ignore_files is None:
            # 使用默认忽略列表
            self.ignore_files: Set[str] = set(self.DEFAULT_IGNORE_FILES)
        elif ignore_files == []:
            # 空列表表示不忽略任何文件
            self.ignore_files = set()
        else:
            # 使用用户自定义的忽略列表
            self.ignore_files = set(ignore_files)

        # ====================================
        # 处理递归深度
        # ====================================
        # 如果 max_depth 为 0 或 None，则不限制深度
        if max_depth is None or max_depth == 0:
            self.max_depth = None
        else:
            # 确保深度为正整数
            self.max_depth = max(1, int(max_depth))

        # ====================================
        # 设置其他参数
        # ====================================
        self.default_description = default_description
        self.use_absolute_path = use_absolute_path

        # ====================================
        # 扫描统计信息
        # ====================================
        self.stats = {
            'total_dirs': 0,  # 扫描的文件夹总数
            'total_files': 0,  # 扫描的文件总数
            'skipped_dirs': 0,  # 跳过的文件夹数
            'skipped_files': 0  # 跳过的文件数
        }

    def scan(self, root_path: str) -> Dict[str, Dict]:
        """
        扫描指定的文件夹，返回其结构字典

        参数说明：
        --------------
        root_path : str
            要扫描的根文件夹路径
            可以是相对路径或绝对路径

        返回值：
        --------------
        Dict[str, Dict]
            包含文件夹结构的嵌套字典

        异常：
        --------------
        FileNotFoundError
            当指定的路径不存在时抛出

        NotADirectoryError
            当指定的路径不是文件夹时抛出

        PermissionError
            当没有权限访问路径时抛出
        """
        # ====================================
        # 路径验证
        # ====================================
        # 将路径转换为 Path 对象便于处理
        root_path_obj = Path(root_path)

        # 检查路径是否存在
        if not root_path_obj.exists():
            raise FileNotFoundError(f"❌ 路径不存在: {root_path}")

        # 检查路径是否为文件夹
        if not root_path_obj.is_dir():
            raise NotADirectoryError(f"❌ 路径不是文件夹: {root_path}")

        # ====================================
        # 重置统计信息
        # ====================================
        self.stats = {
            'total_dirs': 0,
            'total_files': 0,
            'skipped_dirs': 0,
            'skipped_files': 0
        }

        # ====================================
        # 获取根文件夹名称和路径
        # ====================================
        root_name = root_path_obj.name  # 文件夹名称

        if self.use_absolute_path:
            root_abs_path = str(root_path_obj.resolve())  # 绝对路径
        else:
            root_abs_path = str(root_path_obj)  # 原始路径

        # ====================================
        # 构建结果字典结构
        # ====================================
        result = {
            root_name: {
                "name": root_name,  # 文件夹名称
                "path": root_abs_path,  # 完整路径
                "type": "dir",  # 类型：文件夹
                "description": self.default_description,  # 说明
                "children": {}  # 子项（文件和文件夹）
            }
        }

        # ====================================
        # 开始递归扫描
        # ====================================
        self._scan_recursive(
            dir_path=root_abs_path,
            result_dict=result[root_name]["children"],
            current_depth=1
        )

        # ====================================
        # 返回结果
        # ====================================
        return result

    def _scan_recursive(
            self,
            dir_path: str,
            result_dict: Dict[str, Dict],
            current_depth: int
    ) -> None:
        """
        递归扫描文件夹（核心方法）

        参数说明：
        --------------
        dir_path : str
            当前正在扫描的文件夹路径

        result_dict : Dict[str, Dict]
            用于存储结果的字典（传入引用，直接修改）

        current_depth : int
            当前递归深度（从1开始）
        """
        # ====================================
        # 检查是否超过最大递归深度
        # ====================================
        if self.max_depth is not None and current_depth > self.max_depth:
            # 超过最大深度，停止递归
            return

        # ====================================
        # 尝试获取文件夹内容
        # ====================================
        try:
            # 使用 os.listdir 获取文件夹中的所有条目
            entries = os.listdir(dir_path)
        except PermissionError:
            # 没有权限访问该文件夹，跳过
            return
        except OSError as e:
            # 其他操作系统错误，跳过
            return

        # ====================================
        # 遍历每个条目
        # ====================================
        for entry in entries:
            # 构建条目的完整路径
            full_path = os.path.join(dir_path, entry)

            # ====================================
            # 判断条目类型
            # ====================================
            if os.path.isdir(full_path):
                # ========================
                # 处理文件夹
                # ========================

                # 检查是否在忽略列表中
                if entry in self.ignore_dirs:
                    self.stats['skipped_dirs'] += 1
                    continue

                # 统计文件夹数量
                self.stats['total_dirs'] += 1

                # 确定路径类型
                if self.use_absolute_path:
                    entry_path = os.path.abspath(full_path)
                else:
                    entry_path = full_path

                # 创建文件夹信息字典
                result_dict[entry] = {
                    "name": entry,  # 文件夹名称
                    "path": entry_path,  # 完整路径
                    "type": "dir",  # 类型：文件夹
                    "description": self.default_description,  # 说明
                    "children": {}  # 子项（用于递归）
                }

                # 递归扫描子文件夹
                # 注意：递归调用时深度+1
                self._scan_recursive(
                    dir_path=entry_path,
                    result_dict=result_dict[entry]["children"],
                    current_depth=current_depth + 1
                )

            elif os.path.isfile(full_path):
                # ========================
                # 处理文件
                # ========================

                # 检查是否在忽略列表中
                if entry in self.ignore_files:
                    self.stats['skipped_files'] += 1
                    continue

                # 统计文件数量
                self.stats['total_files'] += 1

                # 确定路径类型
                if self.use_absolute_path:
                    entry_path = os.path.abspath(full_path)
                else:
                    entry_path = full_path

                # 创建文件信息字典
                result_dict[entry] = {
                    "name": entry,  # 文件名称
                    "path": entry_path,  # 完整路径
                    "type": "file",  # 类型：文件
                    "description": self.default_description  # 说明
                }

    def to_json(
            self,
            root_path: str,
            output_file: Optional[str] = None,
            indent: int = 4,
            ensure_ascii: bool = False,
            sort_keys: bool = False
    ) -> Union[str, None]:
        """
        将文件夹结构转换为JSON格式

        参数说明：
        --------------
        root_path : str
            要扫描的根文件夹路径

        output_file : str | None
            输出文件路径
            - 如果为 None：返回JSON字符串
            - 如果指定路径：保存到文件并返回成功消息

        indent : int
            JSON格式化缩进空格数
            - 默认为 4（美观的格式）
            - 设为 None 表示不格式化（压缩为一行）

        ensure_ascii : bool
            是否确保ASCII编码
            - True: 非ASCII字符会转义（如中文会变成 \uXXXX）
            - False: 直接输出原始字符（推荐用于中文环境）
            默认为 False

        sort_keys : bool
            是否对字典键进行排序
            - True: 按字母顺序排序键
            - False: 保持原始顺序
            默认为 False

        返回值：
        --------------
        str | None
            - 如果 output_file 为 None，返回JSON字符串
            - 如果 output_file 指定，返回成功消息字符串
        """
        # ====================================
        # 扫描文件夹结构
        # ====================================
        folder_structure = self.scan(root_path)

        # ====================================
        # 可以添加统计信息到结果中（可选）
        # ====================================
        # folder_structure["_stats"] = self.stats

        # ====================================
        # 转换为JSON格式
        # ====================================
        json_str = json.dumps(
            folder_structure,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys
        )

        # ====================================
        # 处理输出
        # ====================================
        if output_file:
            # 保存到文件
            try:
                # 确保输出目录存在
                output_dir = os.path.dirname(output_file)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)

                # 写入文件
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(json_str)

                return f"✅ JSON已保存到: {output_file}"

            except IOError as e:
                raise IOError(f"❌ 写入文件失败: {e}")

        # 返回JSON字符串
        return json_str

    def print_structure(
            self,
            root_path: str,
            indent: int = 4,
            include_stats: bool = True
    ) -> None:
        """
        打印文件夹结构（格式化输出）

        参数说明：
        --------------
        root_path : str
            要扫描的根文件夹路径

        indent : int
            JSON缩进空格数

        include_stats : bool
            是否在打印结果后显示统计信息
        """
        # ====================================
        # 获取JSON格式的字符串
        # ====================================
        json_str = self.to_json(root_path, indent=indent)

        # ====================================
        # 打印分隔线
        # ====================================
        print("\n" + "=" * 80)
        print("📁 文件夹结构（JSON格式）")
        print("=" * 80)

        # ====================================
        # 打印JSON内容
        # ====================================
        print(json_str)

        # ====================================
        # 打印统计信息（如果启用）
        # ====================================
        if include_stats:
            print("\n" + "=" * 80)
            print("📊 扫描统计")
            print("=" * 80)
            print(f"  扫描的文件夹数: {self.stats['total_dirs']}")
            print(f"  扫描的文件数:   {self.stats['total_files']}")
            print(f"  跳过的文件夹数: {self.stats['skipped_dirs']}")
            print(f"  跳过的文件数:   {self.stats['skipped_files']}")
            print(f"  合计扫描项:     {self.stats['total_dirs'] + self.stats['total_files']}")
            print("=" * 80 + "\n")

    def get_stats(self) -> Dict[str, int]:
        """
        获取扫描统计信息

        返回值：
        --------------
        Dict[str, int]
            包含以下键的字典：
            - total_dirs: 扫描的文件夹总数
            - total_files: 扫描的文件总数
            - skipped_dirs: 跳过的文件夹数
            - skipped_files: 跳过的文件数
        """
        return self.stats.copy()

    def add_ignore_dir(self, dir_name: str) -> None:
        """
        添加要忽略的文件夹名称

        参数说明：
        --------------
        dir_name : str
            要忽略的文件夹名称
        """
        self.ignore_dirs.add(dir_name)

    def add_ignore_file(self, file_name: str) -> None:
        """
        添加要忽略的文件名称

        参数说明：
        --------------
        file_name : str
            要忽略的文件名称
        """
        self.ignore_files.add(file_name)

    def remove_ignore_dir(self, dir_name: str) -> None:
        """
        移除要忽略的文件夹名称

        参数说明：
        --------------
        dir_name : str
            要移除的文件夹名称
        """
        self.ignore_dirs.discard(dir_name)

    def remove_ignore_file(self, file_name: str) -> None:
        """
        移除要忽略的文件名称

        参数说明：
        --------------
        file_name : str
            要移除的文件名称
        """
        self.ignore_files.discard(file_name)


def print_tree_view(data: Dict, prefix: str = "", is_last: bool = True) -> None:
    """
    将字典数据以树状结构打印出来

    参数说明：
    --------------
    data : Dict
        扫描结果字典

    prefix : str
        前缀字符串（用于缩进）

    is_last : bool
        是否是最后一个子项
    """
    for key, value in data.items():
        # 构建当前行的前缀
        connector = "└── " if is_last else "├── "
        current_prefix = prefix + connector

        # 打印当前项
        item_type = value.get('type', 'unknown')
        item_path = value.get('path', '')

        if item_type == 'dir':
            print(f"{current_prefix}📁 {key}/")
        else:
            print(f"{current_prefix}📄 {key}")

        # 如果有children，递归打印
        if 'children' in value and value['children']:
            # 计算下一级的前缀
            next_prefix = prefix + ("    " if is_last else "│   ")

            # 获取所有子项
            children = value['children']
            child_keys = list(children.keys())

            # 递归打印每个子项
            for i, child_key in enumerate(child_keys):
                is_last_child = (i == len(child_keys) - 1)
                child_data = {child_key: children[child_key]}
                print_tree_view(child_data, next_prefix, is_last_child)


# ============================================
# 使用示例和测试
# ============================================
if __name__ == "__main__":
    """
    演示 FolderScanner 的各种用法
    """

    # ========================================
    # 示例1：基本用法
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例1：基本用法 - 扫描当前文件夹")
    print("🔶" * 40)

    # 创建扫描器实例（使用默认配置）
    scanner1 = FolderScanner()

    # 打印当前文件夹结构
    scanner1.print_structure(".")

    # ========================================
    # 示例2：自定义忽略列表和深度
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例2：自定义配置")
    print("🔶" * 40)

    # 创建扫描器实例（自定义配置）
    scanner2 = FolderScanner(
        ignore_dirs=['.venv', '.idea', '.vscode', '__pycache__', '.git', 'node_modules'],
        ignore_files=['.gitignore', '.DS_Store', 'Thumbs.db'],
        max_depth=3,  # 限制递归深度为3层
        default_description="",  # 默认说明为空
        use_absolute_path=True  # 使用绝对路径
    )

    # 扫描当前文件夹
    scanner2.print_structure(".")

    # ========================================
    # 示例3：保存为JSON文件
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例3：保存为JSON文件")
    print("🔶" * 40)

    scanner3 = FolderScanner(
        ignore_dirs=['.venv', '.idea', '.vscode'],
        ignore_files=['.gitignore'],
        max_depth=2  # 只扫描2层
    )

    # 保存为JSON文件
    result = scanner3.to_json(".", output_file="folder_structure.json")
    print(result)

    # ========================================
    # 示例4：获取JSON字符串
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例4：获取JSON字符串")
    print("🔶" * 40)

    scanner4 = FolderScanner(max_depth=1)

    # 获取JSON字符串（不保存文件）
    json_string = scanner4.to_json(".")
    print("JSON字符串长度:", len(json_string), "字符")

    # ========================================
    # 示例5：不限制递归深度
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例5：不限制递归深度（max_depth=0）")
    print("🔶" * 40)

    scanner5 = FolderScanner(
        ignore_dirs=['.venv', '.idea', '.vscode', '__pycache__', '.git'],
        max_depth=0  # 0表示不限制深度
    )

    # 获取统计信息
    scanner5.print_structure(".", include_stats=True)

    # ========================================
    # 示例6：树状视图打印
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例6：树状视图")
    print("🔶" * 40)

    scanner6 = FolderScanner(max_depth=2)
    folder_data = scanner6.scan(".")

    print("\n📁 树状结构视图:")
    print_tree_view(folder_data)

    # ========================================
    # 示例7：动态添加忽略项
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例7：动态添加忽略项")
    print("🔶" * 40)

    scanner7 = FolderScanner(max_depth=2)

    # 动态添加要忽略的文件夹
    scanner7.add_ignore_dir("test_folder")
    scanner7.add_ignore_file("temp.txt")

    print("当前忽略的文件夹:", scanner7.ignore_dirs)
    print("当前忽略的文件:", scanner7.ignore_files)

    # ========================================
    # 示例8：使用相对路径
    # ========================================
    print("\n" + "🔶" * 40)
    print("示例8：使用相对路径")
    print("🔶" * 40)

    scanner8 = FolderScanner(
        max_depth=1,
        use_absolute_path=False  # 使用相对路径
    )

    scanner8.print_structure(".")

    print("\n✅ 所有示例运行完成！")
