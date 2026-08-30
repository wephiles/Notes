---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-15 08:08:80 周六"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">tempfile</h1>

# 1. 什么是 `tempfile`

## 1.1 简介

`tempfile` 是 Python 标准库中的一个模块，专门用于**创建临时文件和临时目录**。它提供了一个安全、跨平台的方式来处理临时数据。

## 1.2 主要特点

| 特点         | 说明                                                |
| ------------ | --------------------------------------------------- |
| **安全性**   | 自动创建在系统的临时目录中（如 `/tmp` 或 `%TEMP%`） |
| **自动清理** | 文件/目录在使用后可自动删除，避免垃圾文件堆积       |
| **跨平台**   | `Windows`、`Linux`、`macOS` 都能正常工作            |
| **唯一性**   | 自动生成唯一文件名，避免冲突                        |
| **权限控制** | 仅限当前用户访问，保护数据安全                      |

## 1.3 常见应用场景

- 📤 处理大文件上传/下载时的中间存储
- 🔄 单元测试中需要临时文件
- 🗜️ 数据处理时的中间结果缓存
- 📋 需要外部工具处理但不需要永久保存的数据
- 🔒 处理敏感数据，用完即销毁

# 2. 如何使用

## 2.1 创建临时文件

### 2.1.1 `TemporaryFile` -- 无名临时文件(最常用)

**特点**：没有文件系统中的名称，关闭后自动删除

```
import tempfile

with tempfile.TemporaryFile(mode='w+') as tf:
    tf.write('Hello world!\n')
    tf.write('这是临时文件内容.')

    # 将指针移动到开头
    tf.seek(0)

    # 读取数据
    content = tf.read()
    print(content)

# 离开 with 后临时文件自动删除
```

### 2.1.2 `NamedTemporaryFile` -- 有名的临时文件

**特点**：有实际文件名，可以被其他进程访问，关闭后自动删除

```
# 创建有名字的临时文件
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', prefix='test_') as tf:
    print('临时文件路径:', tf.name)

    tf.write('This is temp file. 这是命名的临时文件.')
    tf.seek(0)

    print(tf.read())

# delete=True 时，关闭后自动删除
```

**参数说明**：

| 参数       | 说明                                      |
| ---------- | ----------------------------------------- |
| `mode`     | 文件模式（‘w+’ 读写，‘wb+’ 二进制读写等） |
| `delete`   | True=关闭时删除，False=保留文件           |
| `suffix`   | 文件名后缀（如 ‘.txt’, ‘.log’）           |
| `prefix`   | 文件名前缀（如 ‘temp_’, ‘data_’）         |
| `dir`      | 指定目录（默认系统临时目录）              |
| `encoding` | 文本编码（如 ‘utf-8’）                    |

### 2.1.3 `SpooledTemporaryFile` -- 内存型临时文件

**特点**：先存在内存中，超过指定大小才写入磁盘.

```python
# 最大 1MB 前存在内存中, 超过后写入磁盘
with tempfile.SpooledTemporaryFile(max_size=1024*1024, mode='w+') as tf:
    tf.write('Small data save in memory.\n' * 10)
    tf.seek(0)

    print(tf.read())

    # 检查是否在内存中
    print(f'是否在内存中: {tf._rolled}')  # False 表示在内存中
```

## 2.2 创建临时目录

### 2.2.1 `TemporaryDirectory` - 临时目录

```python
with tempfile.TemporaryDirectory(prefix='my_app', suffix='_temp') as tmpdir:
    print(f'临时文件目录: {tmpdir}')

    # 在临时目录中创建文件
    file_path = os.path.join(tmpdir, 'data.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('File in temporary directory.\n')

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        print(f.read())

# 离开 with 块, 整个目录及其内容都将会被删除
```

### 2.2.2 `mkdtemp` -- 创建临时目录(手动管理)

```python
import shutil
import time

# 创建临时目录 -- 需要手动删除
tmpdir = tempfile.mkdtemp()
print(f'创建的目录: {tmpdir}')

file_path = os.path.join(tmpdir, 'file.txt')

try:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(
            '这是一个临时文件, 用来存储一些临时的信息, 在临时目录下面, 当程序运行完毕后就会将此文件及临时目录全部删除.\n' * 10)
finally:
    time.sleep(60)
    shutil.rmtree(tmpdir)  # 递归删除目录
```

## 2.3 生成临时名称

### 2.4.1 `mktemp`(已弃用) 和 `mkstemp`(推荐)

```python
import tempfile
import os

# mkstemp - 创建临时文件，返回文件描述符和路径
fd, path = tempfile.mkstemp(suffix='.tmp', prefix='demo_')
print(f"文件描述符: {fd}, 文件路径: {path}")

# 使用文件描述符或路径
with os.fdopen(fd, 'w') as f:
    f.write('使用 mkstemp 创建的文件')

# 使用完后需要手动删除
os.unlink(path)
```

### 2.4.2 `gettempdir` -- 获取系统临时目录

```python
import tempfile

print(f"系统临时目录: {tempfile.gettempdir()}")
print(f"临时目录前缀: {tempfile.gettempprefix()}")

# 输出示例：
# 系统临时目录: /tmp (Linux) 或 C:\Users\xxx\AppData\Local\Temp (Windows)
# 临时目录前缀: tmp
```

## 2.4 示例

```python
import tempfile
import json
import os

def process_large_json(data_list):
    """将大量数据临时保存到文件中处理"""
    
    # 使用有名字的临时文件，方便调试
    with tempfile.NamedTemporaryFile(
        mode='w+',
        suffix='.json',
        prefix='process_',
        delete=False,  # 不自动删除，方便查看
        encoding='utf-8'
    ) as tf:
        # 写入原始数据
        json.dump(data_list, tf, ensure_ascii=False, indent=2)
        temp_path = tf.name
    
    try:
        # 模拟外部程序处理文件
        print(f"临时文件已创建: {temp_path}")
        
        # 重新读取处理
        with open(temp_path, 'r', encoding='utf-8') as f:
            processed = json.load(f)
            # 处理数据...
            processed = [item.upper() for item in processed]
            return processed
    finally:
        # 手动清理
        if os.path.exists(temp_path):
            os.unlink(temp_path)
            print(f"临时文件已删除: {temp_path}")

# 使用示例
data = ['hello', 'world', 'python']
result = process_large_json(data)
print(f"处理结果: {result}")
```

## 2.5 常用函数速查表

| 函数                     | 返回值     | 自动删除 | 用途                    |
| ------------------------ | ---------- | -------- | ----------------------- |
| `TemporaryFile()`        | 文件对象   | ✅        | 无名临时文件，内存+磁盘 |
| `NamedTemporaryFile()`   | 文件对象   | ✅        | 有名临时文件            |
| `SpooledTemporaryFile()` | 文件对象   | ✅        | 先内存后磁盘            |
| `TemporaryDirectory()`   | 目录路径   | ✅        | 临时目录                |
| `mkstemp()`              | (fd, path) | ❌        | 手动管理临时文件        |
| `mkdtemp()`              | 目录路径   | ❌        | 手动管理临时目录        |
| `gettempdir()`           | 路径       | -        | 获取临时目录            |

## 2.6 最佳实践

```python
# ✅ 推荐：使用上下文管理器
with tempfile.TemporaryFile() as tf:
    tf.write(b'some data')
    # 自动清理

# ✅ 推荐：设置合理的模式
with tempfile.NamedTemporaryFile(mode='w+b', suffix='.bin') as tf:
    pass

# ✅ 推荐：指定后缀帮助识别
with tempfile.NamedTemporaryFile(suffix='.log') as tf:
    pass

# ⚠️ 需要文件名时用 NamedTemporaryFile
with tempfile.NamedTemporaryFile(delete=False) as tf:
    temp_path = tf.name
# ... 使用 temp_path ...
os.unlink(temp_path)  # 记得删除

# ⚠️ 需要跨进程访问时用 delete=False
with tempfile.NamedTemporaryFile(delete=False) as tf:
    path = tf.name
    # 其他进程可以访问 path
```

## 2.7 一些问题

**Q: TemporaryFile 和 NamedTemporaryFile 有什么区别？**

A: `TemporaryFile` 没有文件名，更适合程序内部使用；`NamedTemporaryFile` 有真实文件名，可以被其他程序或进程访问。

**Q: 如何在 Windows 和 Linux 上保持一致的行为？**

A: 直接使用 tempfile 模块即可，它会自动处理平台差异，无需特殊配置。

**Q: 临时文件会保存在哪里？**

A: 默认保存在系统临时目录中，可通过 `tempfile.gettempdir()` 查看。

**Q: 如何查看生成的临时文件？**

A: 使用 `NamedTemporaryFile(delete=False)` 或在调试时暂停程序。
