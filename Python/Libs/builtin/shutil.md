---
aliases:
  - course of study
  - course
  - shutil
  - tutorial
  - python builtin libraries
tags:
  - tutorial
  - computer-science
  - Python
  - shutil
category: knowledge
datetime: " 2026-08-08 12:08:91 周六"
author: wephiles
rating: "0"
---
[TOC]

<h1 style="text-align: center;">shutil 模块</h1>

作为 Python 标准库中用于**高级文件操作**的核心模块，`shutil`（shell utility）提供了文件复制、移动、删除、归档等强大功能，是对 `os` 模块的高级封装。

# 1. 模块概览

`shutil` 模块主要功能分类：

- **➕文件复制**：`copy()`, `copy2()`, `copyfile()`, `copymode()`, `copystat()`
- **📂目录复制**：`copytree()`
- **📝文件移动/重命名**：`move()`
- **❌目录删除**：`rmtree()`
- **💾磁盘信息**：`disk_usage()`
- **📦归档压缩**：`make_archive()`, `unpack_archive()`
- **🔍工具函数**：`which()`, `get_terminal_size()`, `chown()`
- **🤝辅助函数**：`ignore_patterns()`, `get_archive_formats()`, `get_unpack_formats()`

# 2. 文件复制功能(最常用)

## 2.1 `shutil.copy(src, dst, *, follow_symlinks=True)`

功能: 复制文件内容和权限模式, **不保留元数据**(如修改时间).

参数说明:

- `src`: 源文件路径
- `dst`: 目标路径(可以是文件名或目录)
- `follow_symlinks`: 是否跟随符号链接(默认 `True`)

示例代码:

```python
import shutil
import os
import time

# 准备测试文件
with open('source.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, shutil!')

# 基本用法：复制到指定文件名
shutil.copy('source.txt', 'destination.txt')

# 复制到指定目录（保留原文件名）
os.makedirs('backup', exist_ok=True)
shutil.copy('source.txt', 'backup/')

print("复制完成！")
print(f"原文件: {os.path.exists('source.txt')}")
print(f"新文件: {os.path.exists('destination.txt')}")
```

```python
import shutil

# 移动
shutil.copy("./data/origin_data.txt", "./new_data")

# 移动 + 重命名
shutil.copy("./data/origin_data.txt", "./new_data/moved_data.txt")

# 原地重命名
shutil.move("./data/origin_data.txt", "./data/origin_data_rename.txt")
```

## 2.2 `shutil.copy2(src, dst, *, follow_symlinks=True)`

**功能**：复制文件内容、权限模式**以及所有元数据**（修改时间、访问时间等）。

**与 copy() 的区别：**

- `copy()`：只复制内容 + 权限
- `copy2()`：复制内容 + 权限 + 元数据（推荐使用）

```python
import shutil
import os
import time

# 创建源文件并设置特定时间
with open('data.txt', 'w') as f:
    f.write('重要数据')

old_mtime = os.path.getmtime('data.txt')
print(f"复制前修改时间: {old_mtime}")

# 使用 copy2 复制（保留元数据）
shutil.copy2('data.txt', 'data_copy.txt')

new_mtime = os.path.getmtime('data_copy.txt')
print(f"复制后修改时间: {new_mtime}")
print(f"时间是否一致: {old_mtime == new_mtime}")
```

## 2.3 `shutil.copyfile(src, dst, *, follow_symlinks=True)`

**功能**：只复制文件内容，**不复制**权限和元数据。

**特点：**

- 最纯粹的文件内容复制
- 不检查文件类型
- 不处理特殊文件

```python
import shutil
import os
import stat

# 创建源文件
with open('original.txt', 'w') as f:
    f.write('原始内容')

# 设置可执行权限（仅 Unix）
os.chmod('original.txt', 0o755)
print(f"源文件权限: {oct(os.stat('original.txt').st_mode)}")

# 只复制内容
shutil.copyfile('original.txt', 'content_only.txt')

print(f"目标文件权限: {oct(os.stat('content_only.txt').st_mode)}")
print("注意：权限没有复制！")
```

```python
import shutil

# copy file only, this operate will not rename the old file and create a new file.
shutil.copyfile("./data/origin_data_rename.txt", "./data/origin_data_rename_rename.txt")
shutil.copyfile("./data/origin_data_rename.txt", "./new_data/origin_data_rename_rename.txt")
```

## 2.4 `shutil.copyfileobj(fsrc, fdst, length=16384)`

**功能**：将一个文件对象的内容复制到另一个文件对象（按块复制）。

**使用场景：**

- 处理大文件时控制内存使用
- 处理网络文件流
- 自定义缓冲区大小

```python
import shutil

# 从一个文件对象复制到另一个文件对象
with open('source.txt', 'rb') as fsrc:
    with open('destination.txt', 'wb') as fdst:
        # 使用较大的缓冲区（64KB）
        shutil.copyfileobj(fsrc, fdst, length=65536)

print("文件对象复制完成")

# 更实际的场景：复制网络流到文件
# import urllib.request
# 
# def download_file(url, local_path):
#     with urllib.request.urlopen(url) as response:
#         with open(local_path, 'wb') as f:
#             shutil.copyfileobj(response, f, length=8192)
```

## 2.5 `shutil.copymode(src, dst, *, follow_symlinks=True)`

**功能**：只复制权限模式，不复制文件内容。

```python
import shutil
import os
import stat

# 创建两个文件
with open('file1.txt', 'w') as f:
    f.write('file1')
with open('file2.txt', 'w') as f:
    f.write('file2')

# 设置 file1 的权限
os.chmod('file1.txt', 0o755)

# 复制权限到 file2
shutil.copymode('file1.txt', 'file2.txt')

print(f"file1 权限: {oct(os.stat('file1.txt').st_mode)}")
print(f"file2 权限: {oct(os.stat('file2.txt').st_mode)}")
print("file2 的内容仍然是: file2")
```

## 2.6 `shutil.copystat(src, dst, *, follow_symlinks=True)`

**功能**：复制所有元数据（权限、最后访问时间、最后修改时间、标志位）。

```python
import shutil
import os
import time
import stat

# 创建源文件
with open('template.txt', 'w') as f:
    f.write('模板文件')

# 等待一秒，确保时间不同
time.sleep(1)

# 创建目标文件
with open('new_file.txt', 'w') as f:
    f.write('新文件')

print(f"复制前 - 模板修改时间: {os.path.getmtime('template.txt')}")
print(f"复制前 - 新文件修改时间: {os.path.getmtime('new_file.txt')}")

# 复制所有状态信息
shutil.copystat('template.txt', 'new_file.txt')

print(f"复制后 - 新文件修改时间: {os.path.getmtime('new_file.txt')}")
print("元数据已完全复制！")
```

# 3. 目录操作

## 3.1 `shutil.copytree()`

函数签名:

```python
shutil.copytree(
    src, 
    dst, 
    symlinks=False, 
    ignore=None, 
    copy_function=copy2, 
    ignore_dangling_symlinks=False, 
    dirs_exist_ok=False
)
```

**功能**：递归复制整个目录树。

| 参数            | 说明                                                |
| --------------- | --------------------------------------------------- |
| `src`           | 源目录路径                                          |
| `dst`           | 目标目录路径（不能已存在，除非 dirs_exist_ok=True） |
| `symlinks`      | True=复制符号链接本身，False=复制链接指向的文件     |
| `ignore`        | 忽略某些文件/目录的函数                             |
| `copy_function` | 使用的复制函数（默认 copy2）                        |
| `dirs_exist_ok` | Python 3.8+：目标目录存在时是否覆盖                 |

```python
import shutil
import os

# 创建复杂的目录结构
source_dir = 'my_project'
os.makedirs(f'{source_dir}/src', exist_ok=True)
os.makedirs(f'{source_dir}/tests', exist_ok=True)
os.makedirs(f'{source_dir}/__pycache__', exist_ok=True)

# 创建一些文件
with open(f'{source_dir}/main.py', 'w') as f:
    f.write('# 主程序')
with open(f'{source_dir}/src/utils.py', 'w') as f:
    f.write('# 工具函数')
with open(f'{source_dir}/tests/test_main.py', 'w') as f:
    f.write('# 测试')
with open(f'{source_dir}/__pycache__/module.pyc', 'w') as f:
    f.write('# 字节码')
with open(f'{source_dir}/.git/config', 'w') as f:
    f.write('# git 配置')

# 基本复制
shutil.copytree(source_dir, 'my_project_backup')

# 使用 ignore 忽略某些文件
def ignore_patterns(*patterns):
    """忽略匹配模式的文件"""
    def _ignore_patterns(path, names):
        ignored_names = []
        for pattern in patterns:
            if pattern in names:
                ignored_names.append(pattern)
        return set(ignored_names)
    return _ignore_patterns

# 复制时忽略 __pycache__ 和 .git 目录
shutil.copytree(
    source_dir, 
    'my_project_clean',
    ignore=ignore_patterns('__pycache__', '.git')
)

# 使用 shutil.ignore_patterns（内置）
shutil.copytree(
    source_dir,
    'my_project_clean_v2',
    ignore=shutil.ignore_patterns('__pycache__', '.git', '*.pyc')
)

print("目录树复制完成！")
print(f"完整备份包含: {os.listdir('my_project_backup')}")
print(f"清理备份包含: {os.listdir('my_project_clean')}")
```

```python
import shutil
import os

old_dir = "old_dir"
new_dir = "new/copy_from_old"

shutil.copytree(old_dir, new_dir)
```

高级示例:自定义 `ignore `函数:

```python
import shutil
import os

def custom_ignore(path, names):
    """自定义忽略规则"""
    ignored = set()
    
    # 忽略特定目录
    for name in names:
        if name.startswith('.') or name == '__pycache__':
            ignored.add(name)
        # 忽略大文件（超过 1MB）
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path):
            if os.path.getsize(full_path) > 1024 * 1024:
                ignored.add(name)
    
    return ignored

shutil.copytree('my_project', 'my_project_filtered', ignore=custom_ignore)

```

## 3.2 `shutil.rmtree()`

`shutil.rmtree(path, ignore_errors=False, onerror=None)`

**能**：递归删除整个目录树（类似 `rm -rf` 命令）。

**参数说明：**

- `ignore_errors`：True=忽略错误，False=抛出异常
- `onerror`：错误处理函数

```python
import shutil
import os

# 创建测试目录
os.makedirs('test_dir/subdir1/subdir2', exist_ok=True)
for i in range(3):
    with open(f'test_dir/file{i}.txt', 'w') as f:
        f.write(f'内容 {i}')

# 基本用法
shutil.rmtree('test_dir')
print("目录已删除")

# 使用 ignore_errors
os.makedirs('readonly_dir', exist_ok=True)
# 在 Unix 上设置只读
# os.chmod('readonly_dir', 0o444)

shutil.rmtree('readonly_dir', ignore_errors=True)
print("即使有错误也尝试删除")

# 自定义错误处理
def handle_remove_error(func, path, exc_info):
    """自定义删除错误处理"""
    import os
    import stat
    
    # 尝试修改只读文件权限
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)  # 重试删除
    else:
        print(f"无法删除 {path}: {exc_info[1]}")

shutil.rmtree('readonly_dir', onerror=handle_remove_error)

```

# 4. 文件移动与重命名

## 4.1 `shutil.move(src, dst, copy_function=copy2)`

**功能**：移动文件或目录，也可以用于重命名。

**工作原理：**

1. 同一文件系统：使用 `os.rename()`（快速）
2. 不同文件系统：先复制后删除
3. 跨设备操作会自动处理

```python
import shutil
import os

# 创建测试文件
with open('old_name.txt', 'w') as f:
    f.write('文件内容')

# 用法1：重命名文件
shutil.move('old_name.txt', 'new_name.txt')
print("文件已重命名")

# 用法2：移动到目录
os.makedirs('target_folder', exist_ok=True)
shutil.move('new_name.txt', 'target_folder/')
print("文件已移动到目录")

# 用法3：移动并重命名
shutil.move('target_folder/new_name.txt', 'target_folder/renamed.txt')
print("移动时同时重命名")

# 用法4：移动整个目录
os.makedirs('source_folder/sub', exist_ok=True)
with open('source_folder/file.txt', 'w') as f:
    f.write('内容')

shutil.move('source_folder', 'target_folder/')
print("目录已移动")

# 用法5：跨分区移动（会自动复制后删除）
# shutil.move('/path/on/partition1/file.txt', '/path/on/partition2/file.txt')
```

处理移动冲突:

```python
import shutil
import os

# 创建源文件和已存在的目标文件
with open('source.txt', 'w') as f:
    f.write('源内容')
with open('dest.txt', 'w') as f:
    f.write('目标已存在')

# 移动前先备份
if os.path.exists('dest.txt'):
    shutil.copy2('dest.txt', 'dest.txt.bak')

# 执行移动
shutil.move('source.txt', 'dest.txt')
print("已移动，原目标文件已备份")
```

# 5. 删除操作

## 5.1 `shutil.rmtree()`

已在上面章节中说明

## 5.2 实用的删除辅助函数

```python
import shutil
import os
import glob

def safe_remove(path):
    """安全删除文件"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"已删除文件: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"已删除目录: {path}")
    except Exception as e:
        print(f"删除失败 {path}: {e}")

def remove_by_pattern(pattern):
    """按模式删除文件"""
    files = glob.glob(pattern)
    for file in files:
        safe_remove(file)

# 使用示例
# safe_remove('temp_file.txt')
# remove_by_pattern('*.tmp')
# remove_by_pattern('cache/**/*')  # 需要 Python 3.10+

```

# 6. 归档与压缩

shutil 提供了便捷的文件归档和压缩功能。

## 6.1 `shutil.make_archive()`

函数签名:

```python
shutil.make_archive(
    base_name, 
    format, 
    root_dir=None, 
    base_dir=None, 
    verbose=0, 
    dry_run=0, 
    owner=None, 
    group=None, 
    logger=None
)
```

**功能**：创建归档文件（zip、tar 等）。

**支持的格式：**

- `zip`：ZIP 压缩格式
- `tar`：未压缩的 tar
- `gztar`：gzip 压缩的 tar（推荐）
- `bztar`：bzip2 压缩的 tar
- `xztar`：xz 压缩的 tar

参数详解:

| 参数          | 说明                                |
| ------------- | ----------------------------------- |
| `base_name`   | 归档文件名（不含扩展名）            |
| `format`      | 归档格式（`zip/tar/gztar` 等）      |
| `root_dir`    | 归档的根目录（可选）                |
| `base_dir`    | 要归档的相对路径（相对于 root_dir） |
| `verbose`     | 详细输出模式                        |
| `dry_run`     | 模拟运行，不实际创建                |
| `owner/group` | Unix 系统的所有者和组               |

```python
import shutil
import os

# 创建测试目录结构
os.makedirs('project/src', exist_ok=True)
os.makedirs('project/docs', exist_ok=True)
with open('project/README.md', 'w', encoding='utf-8') as f:
    f.write('# 项目文档')
with open('project/src/main.py', 'w', encoding='utf-8') as f:
    f.write('print("Hello")')
with open('project/docs/api.md', 'w', encoding='utf-8') as f:
    f.write('# API 文档')

# 示例1：创建 ZIP 归档
shutil.make_archive(
    base_name='project_backup',
    format='zip',
    root_dir='.',
    base_dir='project'
)
print("ZIP 归档已创建: project_backup.zip")

# 示例2：创建 tar.gz 归档（最常用）
shutil.make_archive(
    base_name='project_backup',
    format='gztar',
    root_dir='.',
    base_dir='project'
)
print("tar.gz 归档已创建: project_backup.tar.gz")

# 示例3：只归档 src 目录
shutil.make_archive(
    base_name='src_only',
    format='zip',
    root_dir='project',
    base_dir='src'
)
print("src_only.zip 已创建")

# 示例4：绝对路径归档
abs_path = os.path.abspath('project')
shutil.make_archive(
    base_name='full_project',
    format='gztar',
    root_dir=os.path.dirname(abs_path),
    base_dir=os.path.basename(abs_path)
)
print("使用绝对路径归档完成")
```

## 6.2 `shutil.get_archive_formats()`

**功能**：获取支持的归档格式列表。

```python
import shutil

formats = shutil.get_archive_formats()
print("支持的归档格式:")
for name, description in formats:
    print(f"  {name:8} - {description}")

# 输出示例：
# 支持的归档格式:
#   bztar    - tar'd archive file (bzip2 compressed)
#   gztar    - tar'd archive file (gzip compressed)
#   tar      - un-compressed tar archive file
#   xztar    - tar'd archive file (xz compressed)
#   zip      - ZIP file

```

## 6.3 `shutil.register_archive_format()`

```python
shutil.register_archive_format(name, function, extra_args=None, description=‘’)
```

**功能**：注册自定义归档格式。

```python
import shutil
import zipfile
import os

def make_custom_zip(base_name, base_dir, verbose=0, dry_run=0, **kwargs):
    """自定义 ZIP 创建函数"""
    if dry_run:
        print(f"[模拟] 创建 {base_name}.zip")
        return
    
    archive_name = f"{base_name}.zip"
    print(f"创建自定义归档: {archive_name}")
    
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_dir)
                zf.write(file_path, arcname)
                if verbose:
                    print(f"  添加: {arcname}")

# 注册自定义格式
shutil.register_archive_format(
    name='myzip',
    function=make_custom_zip,
    extra_args=[('verbose', 0)],
    description='自定义 ZIP 格式（带详细输出）'
)

# 使用自定义格式
shutil.make_archive(
    base_name='custom_backup',
    format='myzip',
    root_dir='.',
    base_dir='project',
    verbose=1
)

```

## 6.4 `shutil.unnpack_archive()`

```python
shutil.unpack_archive(filename, extract_dir=None, format=None)
```

**功能**：解压归档文件。

**参数说明：**

- `filename`：归档文件路径
- `extract_dir`：解压目标目录（默认当前目录）
- `format`：归档格式（自动检测）

```python
import shutil
import os

# 准备一个测试归档文件
# shutil.make_archive('test_archive', 'gztar', root_dir='.', base_dir='project')

# 示例1：解压到当前目录
shutil.unpack_archive('project_backup.tar.gz')
print("已解压到当前目录")

# 示例2：解压到指定目录
os.makedirs('extracted', exist_ok=True)
shutil.unpack_archive('project_backup.tar.gz', extract_dir='extracted')
print("已解压到 extracted 目录")
print(f"解压内容: {os.listdir('extracted')}")

# 示例3：解压 ZIP 文件
shutil.unpack_archive('project_backup.zip', extract_dir='extracted_zip')
print("ZIP 文件已解压")

# 示例4：指定格式（当自动检测失败时）
# shutil.unpack_archive('archive.unknown', format='zip')
```

## 6.5 `shutil.get_unpack_formats()`

**功能**：获取支持的解压格式列表。

**功能**：获取支持的解压格式列表。

```python
import shutil

formats = shutil.get_unpack_formats()
print("支持的解压格式:")
for name, extensions, description in formats:
    ext_str = ', '.join(extensions)
    print(f"  {name:8} - {description}")
    print(f"          扩展名: {ext_str}")
```

## 6.6 注册/注销解压格式

```python
import shutil

def custom_unpacker(filename, extract_dir):
    """自定义解压函数"""
    print(f"使用自定义解压器处理: {filename}")
    # 实现解压逻辑...
    return extract_dir

# 注册自定义解压格式
shutil.register_unpack_format(
    name='custom',
    extensions=['.custom'],
    function=custom_unpacker,
    extra_args=[],
    description='自定义归档格式'
)

# 使用自定义解压
# shutil.unpack_archive('file.custom', format='custom')

# 注销解压格式
shutil.unregister_unpack_format('custom')
```

## 6.7 实用的备份与恢复工具类

```python
import shutil
import os
from datetime import datetime
from pathlib import Path

class BackupManager:
    """文件备份管理器"""
    
    def __init__(self, backup_root='backups'):
        self.backup_root = Path(backup_root)
        self.backup_root.mkdir(exist_ok=True)
    
    def create_backup(self, source_path, compress=True):
        """创建备份"""
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"源路径不存在: {source_path}")
        
        # 生成备份文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"{source.name}_{timestamp}"
        
        # 创建备份
        format = 'gztar' if compress else 'zip'
        archive_path = shutil.make_archive(
            base_name=str(self.backup_root / base_name),
            format=format,
            root_dir=str(source.parent),
            base_dir=source.name
        )
        
        return Path(archive_path)
    
    def restore_backup(self, archive_path, target_dir):
        """恢复备份"""
        shutil.unpack_archive(archive_path, extract_dir=target_dir)
        return target_dir
    
    def list_backups(self):
        """列出所有备份"""
        backups = []
        for file in self.backup_root.iterdir():
            if file.is_file() and file.suffix in ['.zip', '.gz', '.tar']:
                stat = file.stat()
                backups.append({
                    'name': file.name,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime)
                })
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_backups(self, keep=5):
        """清理旧备份，保留最新的 keep 个"""
        backups = self.list_backups()
        for old_backup in backups[keep:]:
            (self.backup_root / old_backup['name']).unlink()
            print(f"已删除旧备份: {old_backup['name']}")

# 使用示例
"""
backup_mgr = BackupManager('my_backups')

# 创建备份
archive = backup_mgr.create_backup('project', compress=True)
print(f"备份已创建: {archive}")

# 列出所有备份
for backup in backup_mgr.list_backups():
    print(f"{backup['name']} - {backup['size']} bytes")

# 恢复备份
backup_mgr.restore_backup('my_backups/project_20240115_120000.tar.gz', 'restored_project')

# 清理旧备份
backup_mgr.cleanup_old_backups(keep=3)
"""

```

# 7. 磁盘空间查询

## 7.1 `shutil.disk_usage(path)`

**功能**：获取磁盘使用情况统计信息。

**返回对象属性：**

- `total`：总容量（字节）
- `used`：已使用容量（字节）
- `free`：可用容量（字节）

```python
import shutil


def format_size(bytes_size):
    """格式化字节大小为可读格式"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


# 查询当前目录所在磁盘
usage = shutil.disk_usage(".")
print(f"磁盘: 当前目录所在磁盘")
print(f"总容量:  {format_size(usage.total)}")
print(f"已使用:  {format_size(usage.used)}")
print(f"可用:    {format_size(usage.free)}")
print(f"使用率:  {usage.used / usage.total * 100:.1f}%")
print("-" * 50)

# 查询多个路径
paths = ["C:", "D:", "E:"]
for path in paths:
    try:
        u = shutil.disk_usage(path)
        print(
            f"{path:10} - 总: {format_size(u.total):>10} | "
            f"已用: {format_size(u.used):>10} | "
            f"可用: {format_size(u.free):>10}"
        )
    except Exception as e:
        print(f"{path:10} - 错误: {e}")
```

```python
磁盘: 当前目录所在磁盘
总容量:  931.50 GB
已使用:  289.97 GB
可用:    641.53 GB
使用率:  31.1%
--------------------------------------------------
C:         - 总:  349.15 GB | 已用:  139.31 GB | 可用:  209.83 GB
D:         - 总:  602.87 GB | 已用:  195.05 GB | 可用:  407.82 GB
E:         - 总:  931.50 GB | 已用:  289.97 GB | 可用:  641.53 GB
```

实用场景: 检查磁盘空间后执行操作

```python
import shutil
import os

def ensure_disk_space(required_mb, path='.'):
    """确保有足够的磁盘空间"""
    usage = shutil.disk_usage(path)
    required_bytes = required_mb * 1024 * 1024
    
    if usage.free < required_bytes:
        raise OSError(
            f"磁盘空间不足！需要 {required_mb}MB，"
            f"但只有 {usage.free / (1024*1024):.2f}MB 可用"
        )
    return True

# 使用示例
try:
    ensure_disk_space(100)  # 确保至少 100MB 空间
    
    # 执行需要空间的操作
    shutil.copytree('large_directory', 'backup_large_directory')
    print("备份完成")
    
except OSError as e:
    print(f"操作失败: {e}")
```

# 8. 命令查找

## 8.1 `shutil.which()`

```python
shutil.which(cmd, mode=os.F_OK | os.X_OK, path=None)
```

**功能**：查找命令行程序的位置（类似 Unix 的 `which` 命令）。

**参数说明：**

- `cmd`：要查找的命令名
- `mode`：文件权限检查模式
- `path`：自定义搜索路径（默认使用 PATH 环境变量）

```python
import shutil
import os

# 查找常用命令
commands = ['python', 'python3', 'git', 'npm', 'docker', 'gcc', 'java']

print("命令查找结果:")
print("-" * 60)
for cmd in commands:
    path = shutil.which(cmd)
    if path:
        print(f"✓ {cmd:15} -> {path}")
    else:
        print(f"✗ {cmd:15} -> 未找到")

# 查找并执行
git_path = shutil.which('git')
if git_path:
    import subprocess
    result = subprocess.run([git_path, '--version'], 
                          capture_output=True, text=True)
    print(f"\nGit 版本: {result.stdout.strip()}")

# 检查多个命令是否都存在
def check_dependencies(required_commands):
    """检查依赖命令是否都存在"""
    missing = []
    for cmd in required_commands:
        if not shutil.which(cmd):
            missing.append(cmd)
    
    if missing:
        print(f"缺少以下依赖: {', '.join(missing)}")
        return False
    print("所有依赖都已满足")
    return True

# 使用示例
required = ['python', 'git', 'node']
check_dependencies(required)
```

# 9. 异常类

`shutil` 模块定义了以下异常类，继承自 `OSError` 或 `shutil.Error`：

## 9.1 `shutil.Error`

**功能**：`shutil` 操作的基础异常类。

```python
import shutil

try:
    shutil.copy('nonexistent.txt', 'dest.txt')
except shutil.Error as e:
    print(f"shutil.Error: {e}")
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")

```

## 9.2 `shutil.SameFileError`

功能:当源文件和目标文件是同一个文件时抛出.

```python
import shutil
import os

# 创建测试文件
with open('same.txt', 'w') as f:
    f.write('测试')

# 尝试复制到自身（会失败）
try:
    shutil.copy('same.txt', 'same.txt')
except shutil.SameFileError as e:
    print(f"捕获到 SameFileError: {e}")

# 判断是否是同一文件
if os.path.samefile('same.txt', 'same.txt'):
    print("检测到是同一文件，避免操作")

```

## 9.3 `shutil.SpecialFileErro`

**功能**：尝试复制特殊文件（如设备文件、命名管道）时抛出。

```python
import shutil

try:
    # 尝试复制设备文件（Unix）
    shutil.copy('/dev/null', 'null_copy')
except shutil.SpecialFileError as e:
    print(f"SpecialFileError: {e}")
except Exception as e:
    print(f"其他错误: {e}")

```

## 9.4 `shutil.ExecError`

功能: 执行命令失败时抛出.

## 9.5 `shutil.RegisteryError`

功能: Windows 注册表操作失败时抛出.

## 9.6 完整的异常处理示例

```python
import shutil
import os

class FileOperationError(Exception):
    """自定义文件操作异常"""
    pass

def safe_copy(src, dst):
    """安全的文件复制，包含完整错误处理"""
    try:
        # 检查源文件
        if not os.path.exists(src):
            raise FileNotFoundError(f"源文件不存在: {src}")
        
        # 检查是否是同一文件
        if os.path.exists(dst) and os.path.samefile(src, dst):
            raise FileOperationError("源文件和目标文件是同一文件")
        
        # 检查目标目录是否存在
        dst_dir = os.path.dirname(dst)
        if dst_dir and not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
        
        # 执行复制
        shutil.copy2(src, dst)
        return True
        
    except shutil.SameFileError:
        raise FileOperationError("不能复制到自身")
    except PermissionError:
        raise FileOperationError("权限不足")
    except OSError as e:
        raise FileOperationError(f"系统错误: {e}")
    except Exception as e:
        raise FileOperationError(f"未知错误: {e}")

# 使用示例
try:
    safe_copy('source.txt', 'backup/destination.txt')
    print("复制成功")
except FileOperationError as e:
    print(f"复制失败: {e}")
```

# 10. 实战案例

## 10.1 项目部署脚本

```
#!/usr/bin/env python3
"""
项目部署脚本
功能：备份旧版本 -> 部署新版本 -> 回滚支持
"""

import shutil
import os
import sys
from datetime import datetime
from pathlib import Path

class Deployer:
    def __init__(self, project_dir, backup_dir='./backups'):
        self.project_dir = Path(project_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def backup(self):
        """备份当前项目"""
        if not self.project_dir.exists():
            raise FileNotFoundError(f"项目目录不存在: {self.project_dir}")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        
        print(f"正在备份到 {backup_name}...")
        shutil.make_archive(
            base_name=str(self.backup_dir / backup_name),
            format='gztar',
            root_dir=str(self.project_dir.parent),
            base_dir=self.project_dir.name
        )
        print("✓ 备份完成")
        return self.backup_dir / f"{backup_name}.tar.gz"
    
    def deploy(self, source_dir):
        """部署新版本"""
        source = Path(source_dir)
        
        if not source.exists():
            raise FileNotFoundError(f"源目录不存在: {source}")
        
        # 如果目标存在，先备份
        if self.project_dir.exists():
            self.backup()
            print("删除旧版本...")
            shutil.rmtree(self.project_dir)
        
        print(f"正在部署 {source} -> {self.project_dir}...")
        shutil.copytree(source, self.project_dir)
        print("✓ 部署完成")
    
    def rollback(self, backup_file):
        """回滚到指定备份"""
        backup = Path(backup_file)
        if not backup.exists():
            raise FileNotFoundError(f"备份文件不存在: {backup}")
        
        # 备份当前版本（可选）
        if self.project_dir.exists():
            temp_backup = self.backup_dir / "rollback_temp"
            if temp_backup.exists():
                shutil.rmtree(temp_backup)
            shutil.move(str(self.project_dir), str(temp_backup))
        
        print(f"正在回滚: {backup}...")
        shutil.unpack_archive(str(backup), extract_dir=str(self.project_dir.parent))
        print("✓ 回滚完成")
    
    def status(self):
        """显示部署状态"""
        print("=" * 50)
        print("部署状态")
        print("=" * 50)
        
        if self.project_dir.exists():
            print(f"✓ 项目目录存在: {self.project_dir}")
            print(f"  最后修改: {datetime.fromtimestamp(self.project_dir.stat().st_mtime)}")
            print(f"  文件数量: {sum(1 for _ in self.project_dir.rglob('*'))}")
        else:
            print("✗ 项目目录不存在")
        
        print("\n可用备份:")
        backups = sorted(self.backup_dir.glob('backup_*.tar.gz'), 
                        reverse=True)
        for i, backup in enumerate(backups[:5], 1):
            size_mb = backup.stat().st_size / (1024 * 1024)
            print(f"  {i}. {backup.name} ({size_mb:.2f} MB)")
        
        print("\n磁盘空间:")
        usage = shutil.disk_usage(self.project_dir.parent if self.project_dir.exists() else '.')
        free_gb = usage.free / (1024 ** 3)
        print(f"  可用空间: {free_gb:.2f} GB")
        print("=" * 50)

# 使用示例
if __name__ == '__main__':
    deployer = Deployer('./myapp')
    
    # 查看状态
    deployer.status()
    
    # 部署新版本
    # deployer.deploy('./myapp-new')
    
    # 备份当前版本
    # backup_file = deployer.backup()
    
    # 回滚
    # deployer.rollback(backup_file)
```

## 10.2 日志清理工具

```
#!/usr/bin/env python3
"""
日志清理工具
功能：清理过期日志、归档旧日志、监控磁盘空间
"""

import shutil
import os
import gzip
from datetime import datetime, timedelta
from pathlib import Path

class LogCleaner:
    def __init__(self, log_dir, archive_dir='./log_archives', max_age_days=30):
        self.log_dir = Path(log_dir)
        self.archive_dir = Path(archive_dir)
        self.max_age = timedelta(days=max_age_days)
        self.archive_dir.mkdir(exist_ok=True)
    
    def archive_old_logs(self):
        """归档旧日志文件"""
        now = datetime.now()
        archived = 0
        total_size = 0
        
        print("开始归档旧日志...")
        
        for log_file in self.log_dir.glob('*.log'):
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            age = now - mtime
            
            # 归档超过7天的日志
            if age > timedelta(days=7):
                # 压缩
                archive_path = self.archive_dir / f"{log_file.name}.gz"
                with open(log_file, 'rb') as f_in:
                    with gzip.open(archive_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # 获取原始大小
                original_size = log_file.stat().st_size
                compressed_size = archive_path.stat().st_size
                
                # 删除原文件
                log_file.unlink()
                
                archived += 1
                total_size += original_size
                ratio = (1 - compressed_size / original_size) * 100
                
                print(f"  ✓ {log_file.name} "
                      f"(压缩率: {ratio:.1f}%, "
                      f"节省: {(original_size - compressed_size) / 1024:.1f} KB)")
        
        print(f"归档完成: {archived} 个文件, 节省 {total_size / 1024 / 1024:.2f} MB")
        return archived
    
    def clean_expired_archives(self):
        """清理过期的归档文件"""
        now = datetime.now()
        deleted = 0
        
        print("清理过期归档...")
        
        for archive_file in self.archive_dir.glob('*.gz'):
            mtime = datetime.fromtimestamp(archive_file.stat().st_mtime)
            age = now - mtime
            
            if age > self.max_age:
                archive_file.unlink()
                deleted += 1
                print(f"  ✓ 删除过期归档: {archive_file.name}")
        
        print(f"清理完成: 删除 {deleted} 个过期归档")
        return deleted
    
    def ensure_disk_space(self, min_free_gb=10):
        """确保有足够的磁盘空间"""
        usage = shutil.disk_usage(self.log_dir)
        free_gb = usage.free / (1024 ** 3)
        
        print(f"当前磁盘可用空间: {free_gb:.2f} GB")
        
        if free_gb < min_free_gb:
            print(f"⚠ 磁盘空间不足 (需要 {min_free_gb} GB)!")
            
            # 尝试清理更多归档
            print("尝试清理更多归档文件...")
            for archive_file in sorted(
                self.archive_dir.glob('*.gz'), 
                key=lambda f: f.stat().st_mtime
            )[:20]:  # 删除最旧的20个
                archive_file.unlink()
                print(f"  ✓ 删除: {archive_file.name}")
            
            # 重新检查
            usage = shutil.disk_usage(self.log_dir)
            free_gb = usage.free / (1024 ** 3)
            print(f"清理后可用空间: {free_gb:.2f} GB")
            
            if free_gb < min_free_gb:
                raise OSError(f"磁盘空间仍然不足: {free_gb:.2f} GB")
        
        return True
    
    def rotate_logs(self, max_size_mb=100):
        """日志轮转（当日志文件过大时重命名）"""
        max_size = max_size_mb * 1024 * 1024
        rotated = 0
        
        print("检查日志轮转...")
        
        for log_file in self.log_dir.glob('*.log'):
            if log_file.stat().st_size > max_size:
                # 生成归档名
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                archive_name = f"{log_file.stem}_{timestamp}.log"
                archive_path = self.log_dir / archive_name
                
                # 移动大文件
                shutil.move(str(log_file), str(archive_path))
                
                # 压缩
                gz_path = self.archive_dir / f"{archive_name}.gz"
                with open(archive_path, 'rb') as f_in:
                    with gzip.open(gz_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                archive_path.unlink()
                rotated += 1
                print(f"  ✓ 轮转: {log_file.name} ({max_size_mb} MB+)")
        
        print(f"轮转完成: {rotated} 个文件")
        return rotated
    
    def run_cleanup(self):
        """执行完整清理流程"""
        print("=" * 50)
        print(f"日志清理 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        try:
            # 1. 检查磁盘空间
            self.ensure_disk_space(min_free_gb=5)
            
            # 2. 日志轮转
            self.rotate_logs(max_size_mb=50)
            
            # 3. 归档旧日志
            self.archive_old_logs()
            
            # 4. 清理过期归档
            self.clean_expired_archives()
            
            # 5. 最终检查
            self.ensure_disk_space(min_free_gb=5)
            
            print("\n✓ 清理任务完成！")
            
        except Exception as e:
            print(f"\n✗ 清理失败: {e}")
            raise

# 使用示例
if __name__ == '__main__':
    cleaner = LogCleaner(
        log_dir='./logs',
        archive_dir='./log_archives',
        max_age_days=90
    )
    
    cleaner.run_cleanup()
```

## 10.3 文件同步工具

```
#!/usr/bin/env python3
"""
文件同步工具
功能：将源目录同步到目标目录
"""

import shutil
import os
import filecmp
from pathlib import Path
from typing import Set, Tuple

class FileSyncer:
    def __init__(self, source, destination, exclude=None):
        self.source = Path(source)
        self.destination = Path(destination)
        self.exclude = exclude or ['.git', '__pycache__', '*.pyc', '.DS_Store']
    
    def _should_exclude(self, path):
        """检查是否应该排除此路径"""
        path_str = str(path)
        for pattern in self.exclude:
            if pattern in path_str or path.name == pattern:
                return True
            # 处理通配符
            if pattern.startswith('*') and path.suffix == pattern[1:]:
                return True
        return False
    
    def _copy_with_preserve(self, src, dst):
        """复制文件并保留所有属性"""
        shutil.copy2(src, dst)
        # 尝试复制权限
        shutil.copystat(src, dst)
    
    def sync(self, dry_run=False):
        """执行同步"""
        if not self.source.exists():
            raise FileNotFoundError(f"源目录不存在: {self.source}")
        
        # 确保目标目录存在
        self.destination.mkdir(parents=True, exist_ok=True)
        
        # 统计信息
        copied = []
        updated = []
        deleted = []
        skipped = []
        
        print("开始文件同步...")
        print(f"源: {self.source}")
        print(f"目标: {self.destination}")
        print("-" * 50)
        
        # 1. 复制/更新源中的文件
        for src_file in self.source.rglob('*'):
            if not src_file.is_file():
                continue
            
            if self._should_exclude(src_file):
                skipped.append(src_file)
                continue
            
            rel_path = src_file.relative_to(self.source)
            dst_file = self.destination / rel_path
            
            # 确保目标目录存在
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            if not dst_file.exists():
                # 新文件，复制
                if not dry_run:
                    self._copy_with_preserve(src_file, dst_file)
                copied.append(rel_path)
                print(f"  + {rel_path}")
            elif not filecmp.cmp(src_file, dst_file, shallow=False):
                # 文件不同，更新
                if not dry_run:
                    self._copy_with_preserve(src_file, dst_file)
                updated.append(rel_path)
                print(f"  ~ {rel_path}")
        
        # 2. 删除目标中源没有的文件
        for dst_file in self.destination.rglob('*'):
            if not dst_file.is_file():
                continue
            
            if self._should_exclude(dst_file):
                continue
            
            rel_path = dst_file.relative_to(self.destination)
            src_file = self.source / rel_path
            
            if not src_file.exists():
                if not dry_run:
                    dst_file.unlink()
                deleted.append(rel_path)
                print(f"  - {rel_path}")
        
        # 清理空目录
        if not dry_run:
            self._remove_empty_dirs()
        
        # 打印摘要
        print("-" * 50)
        print(f"新增: {len(copied)} 个文件")
        print(f"更新: {len(updated)} 个文件")
        print(f"删除: {len(deleted)} 个文件")
        print(f"跳过: {len(skipped)} 个文件")
        
        if dry_run:
            print("\n[预览模式] 未执行实际操作")
        
        return {
            'copied': copied,
            'updated': updated,
            'deleted': deleted,
            'skipped': skipped
        }
    
    def _remove_empty_dirs(self):
        """删除空目录"""
        for dirpath in sorted(self.destination.rglob('*'), reverse=True):
            if dirpath.is_dir():
                try:
                    if not any(dirpath.iterdir()):
                        dirpath.rmdir()
                        print(f"  (删除空目录: {dirpath.relative_to(self.destination)})")
                except OSError:
                    pass  # 目录不为空
    
    def diff(self):
        """显示源和目标的差异"""
        print("文件差异分析:")
        print("-" * 50)
        
        comparison = filecmp.dircmp(self.source, self.destination)
        
        # 只在源中的文件
        if comparison.left_only:
            print("只在源中 (需复制):")
            for f in sorted(comparison.left_only):
                print(f"  {f}")
        
        # 只在目标中的文件
        if comparison.right_only:
            print("只在目标中 (需删除):")
            for f in sorted(comparison.right_only):
                print(f"  {f}")
        
        # 不同的文件
        if comparison.diff_files:
            print("内容不同的文件 (需更新):")
            for f in sorted(comparison.diff_files):
                print(f"  {f}")
        
        if not any([comparison.left_only, comparison.right_only, comparison.diff_files]):
            print("✓ 文件完全一致")
        
        print("-" * 50)

# 使用示例
if __name__ == '__main__':
    syncer = FileSyncer(
        source='./project_src',
        destination='./project_dst',
        exclude=['.git', '__pycache__', '*.tmp', '.DS_Store']
    )
    
    # 先查看差异
    syncer.diff()
    
    # 预览同步操作
    syncer.sync(dry_run=True)
    
    # 执行同步
    # syncer.sync(dry_run=False)
```

## 10.4 项目模板生成器

```
#!/usr/bin/env python3
"""
项目模板生成器
功能：从模板创建新项目，支持变量替换
"""

import shutil
import os
import re
from pathlib import Path
from typing import Dict

class ProjectTemplate:
    def __init__(self, template_dir):
        self.template_dir = Path(template_dir)
        self.variables = {}
    
    def set_variable(self, name, value):
        """设置模板变量"""
        self.variables[name] = value
    
    def set_variables(self, vars_dict):
        """批量设置模板变量"""
        self.variables.update(vars_dict)
    
    def _replace_variables(self, content):
        """替换文件内容中的变量"""
        for name, value in self.variables.items():
            # 支持多种格式: {{name}}, ${name}, %name%
            patterns = [
                (r'\{\{' + re.escape(name) + r'\}\}', str(value)),
                (r'\$\{' + re.escape(name) + r'\}', str(value)),
                (r'%' + re.escape(name) + r'%', str(value)),
            ]
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
        return content
    
    def _replace_filename(self, filename):
        """替换文件名中的变量"""
        for name, value in self.variables.items():
            filename = filename.replace(f'__{name}__', str(value))
            filename = filename.replace(f'{{{name}}}', str(value))
        return filename
    
    def create_project(self, output_dir, project_name):
        """从模板创建项目"""
        output_path = Path(output_dir) / project_name
        
        if output_path.exists():
            raise FileExistsError(f"项目目录已存在: {output_path}")
        
        # 设置项目名变量
        self.variables['PROJECT_NAME'] = project_name
        self.variables['PROJECT_NAME_LOWER'] = project_name.lower()
        self.variables['PROJECT_NAME_UPPER'] = project_name.upper()
        self.variables['PROJECT_NAME_TITLE'] = project_name.title()
        
        print(f"从模板创建项目: {project_name}")
        print(f"模板目录: {self.template_dir}")
        print(f"输出目录: {output_path}")
        print("-" * 50)
        
        # 复制模板目录
        shutil.copytree(self.template_dir, output_path)
        
        # 处理所有文件
        for file_path in output_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            # 读取并替换内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = self._replace_variables(content)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # 处理文件名（如果有变量需要替换）
            new_name = self._replace_filename(file_path.name)
            if new_name != file_path.name:
                new_path = file_path.parent / new_name
                file_path.rename(new_path)
                print(f"  重命名: {file_path.name} -> {new_name}")
            
            print(f"  处理: {file_path.relative_to(output_path)}")
        
        print("-" * 50)
        print(f"✓ 项目创建成功: {output_path}")
        
        # 显示后续步骤
        print("\n后续步骤:")
        print(f"  cd {project_name}")
        print(f"  # 查看项目结构")
        print(f"  # 根据需要修改配置")
        
        return output_path

# 使用示例
if __name__ == '__main__':
    # 假设有一个模板目录结构：
    # templates/python-project/
    #   ├── __PROJECT_NAME__/
    #   │   ├── __PROJECT_NAME_LOWER__.py
    #   │   └── tests/
    #   │       └── test___PROJECT_NAME_LOWER__.py
    #   ├── setup.py
    #   ├── README.md
    #   └── requirements.txt
    
    template = ProjectTemplate('templates/python-project')
    
    # 设置变量
    template.set_variables({
        'AUTHOR': 'Your Name',
        'EMAIL': 'your.email@example.com',
        'YEAR': '2024',
        'DESCRIPTION': 'A new Python project',
    })
    
    # 创建项目
    template.create_project('./projects', 'MyAwesomeApp')
```

# 11. 总结

| 功能分类        | 函数/方法                   | 用途                         |
| --------------- | --------------------------- | ---------------------------- |
| **文件复制**    | `copy()`                    | 复制文件+权限                |
|                 | `copy2()`                   | 复制文件+权限+元数据（推荐） |
|                 | `copyfile()`                | 只复制内容                   |
|                 | `copyfileobj()`             | 复制文件对象                 |
|                 | `copymode()`                | 只复制权限                   |
|                 | `copystat()`                | 复制元数据                   |
| **目录操作**    | `copytree()`                | 递归复制目录树               |
|                 | `rmtree()`                  | 递归删除目录树               |
| **移动/重命名** | `move()`                    | 移动或重命名文件/目录        |
| **归档/压缩**   | `make_archive()`            | 创建归档文件                 |
|                 | `unpack_archive()`          | 解压归档文件                 |
|                 | `get_archive_formats()`     | 获取支持的归档格式           |
|                 | `register_archive_format()` | 注册自定义归档格式           |
|                 | `get_unpack_formats()`      | 获取支持的解压格式           |
|                 | `register_unpack_format()`  | 注册自定义解压格式           |
| **磁盘查询**    | `disk_usage()`              | 查询磁盘使用情况             |
| **命令查找**    | `which()`                   | 查找命令行程序               |

最佳实践建议:

1. **优先使用 `copy2()`**：它会保留所有元数据
2. **使用 `ignore_patterns`**：复制目录时过滤不需要的文件
3. **异常处理**：始终捕获和处理可能的异常
4. **检查磁盘空间**：大文件操作前先检查可用空间
5. **使用 `Path` 对象**：代码更清晰、跨平台兼容
