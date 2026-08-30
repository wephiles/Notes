---
aliases:
  - course of study
  - course
  - tutorial
  - glob tutorial
tags:
  - tutorial
  - computer-science
  - glob
  - built-in
  - Python
  - libraries
category:
  - knowledge
  - glob
datetime: " 2026-08-02 17:08:86 周日"
author: wephiles
rating: "6"
---
`glob` 是 Python 标准库中用于**文件名模式匹配**的模块。它提供了一种便捷的方式，根据 Unix shell 风格的通配符规则来查找符合特定模式的文件和目录路径。该模块不依赖外部命令，完全由 Python 实现，跨平台兼容（Windows 下路径分隔符会自动适配）。

# 1. 支持的通配符规则

`glob` 使用与 shell 相同的规则，但**不支持**正则表达式中的复杂元字符。主要通配符有：

| 通配符               | 含义                                                      | 示例                                                         |
| :------------------- | :-------------------------------------------------------- | :----------------------------------------------------------- |
| `*`                  | 匹配任意数量的任意字符（**不包括**路径分隔符 `/` 或 `\`） | `*.txt` 匹配所有 `.txt` 文件                                 |
| `?`                  | 匹配**一个**任意字符（不包括路径分隔符）                  | `file?.py` 匹配 `file1.py`, `fileA.py`，但不匹配 `file10.py` |
| `[seq]`              | 匹配方括号中的任一字符（类似字符类）                      | `[abc].py` 匹配 `a.py`, `b.py`, `c.py`                       |
| `[!seq]` 或 `[^seq]` | 匹配**不在**方括号中的任一字符                            | `[!0-9].txt` 匹配非数字开头的 `.txt` 文件                    |
| `**`                 | 递归匹配任意层级的子目录（**需设置 `recursive=True`**）   | `**/*.py` 搜索当前目录及所有子目录下的 `.py` 文件            |

**注意**：`glob` 默认不匹配以点（`.`）开头的隐藏文件或目录（如 `.bashrc`），除非模式中显式包含点。

# 2. glob 模块中的函数

`glob` 模块提供了三个主要函数，没有定义类（所有操作均为函数式）。

## 2.1 `glob.glob(pathname, *, root_dir=None, dir_fd=None, recursive=False)`

- **功能**：返回一个列表，包含所有匹配 `pathname` 的路径名。
- **参数**：
  - `pathname`：字符串，要匹配的模式路径（可包含通配符）。
  - `recursive`：布尔值（默认 `False`）。若为 `True`，则 `**` 会递归匹配所有子目录。
  - `root_dir`（Python 3.10+）：指定搜索的根目录，路径将相对于此目录解析。
  - `dir_fd`（Python 3.10+）：文件描述符，用于指定起始目录（Unix 特定）。
- **返回值**：按字母顺序排序的路径字符串列表（不保证绝对路径，除非模式中给出）。

## 2.2 `glob.iglob(pathname, *, root_dir=None, dir_fd=None, recursive=False)`

- **功能**：与 `glob()` 相同，但返回一个**迭代器**，而不是列表。这在匹配大量文件时更节省内存。
- **参数**：同 `glob()`。
- **返回值**：生成器对象，可逐次 yield 匹配到的路径。

## 2.3 `glob.escape(pathname)`

- **功能**：转义 `pathname` 中所有的特殊字符（`*`, `?`, `[`, `]` 等），使它们被当作普通字面量匹配。
- **参数**：`pathname` 字符串。
- **返回值**：转义后的字符串。
- **用途**：当你需要按字面意思匹配包含通配符的文件名时使用。

# 3. 递归搜索（`**` 与 `recursive=True`）

Python 3.5 起，`glob` 支持 `**` 模式，但必须显式设置 `recursive=True`，否则 `**` 会被当作普通字符处理。

```python
glob.glob('**/*.txt', recursive=True)  # 递归查找所有 .txt 文件
```

**注意**：在大目录树下使用递归可能会消耗大量时间和资源，请谨慎使用。

# 4. 注意事项

- **排序**：`glob.glob()` 返回的列表按字母顺序排序（与 shell 的 `echo` 结果一致）。`iglob()` 则按搜索顺序 yield。
- **相对/绝对路径**：如果模式是相对路径，返回的也是相对路径；绝对路径则返回绝对路径。
- **隐藏文件**：默认不匹配隐藏文件（如 `.env`），除非显式匹配，如 `.*`。
- **跨平台分隔符**：Windows 下可使用正斜杠 `/` 或反斜杠 `\`，推荐使用 `/` 以保持可移植性。
- **性能**：对于大量文件，使用 `iglob()` 迭代比 `glob()` 一次性返回列表更高效。

# 5. 示例

## 5.1 基本用法

```
import glob

# 匹配当前目录下所有 .py 文件
py_files = glob.glob('*.py')
print("Python files in current dir:", py_files)

# 匹配子目录中的 .txt 文件（非递归）
txt_files = glob.glob('subdir/*.txt')
print("TXT files in subdir:", txt_files)

# 使用字符类
abc_files = glob.glob('[abc].txt')
print("Files a.txt, b.txt, c.txt if exist:", abc_files)
```

## 5.2 递归匹配（`**`）

```
# 递归查找所有 .log 文件（包括子目录）
all_logs = glob.glob('**/*.log', recursive=True)
print("All .log files recursively:", all_logs)

# 使用 iglob 迭代输出
for path in glob.iglob('**/*.py', recursive=True):
    print("Found Python file:", path)
```

## 5.3 转义特殊字符

```
# 假设有一个文件名为 "test[1].txt"，直接 glob('test[1].txt') 会报错或匹配不到
# 因为方括号被解释为字符类，需要转义
escaped = glob.escape('test[1].txt')
print("Escaped pattern:", escaped)  # test[1].txt 变为 test[[]1].txt
matches = glob.glob(escaped)
print("Exact match:", matches)
```

## 5.4 结合 `root_dir` 使用（Python 3.10+）

```
# 在指定目录中搜索，而不必切换工作目录
root = '/home/user/project'
found = glob.glob('src/*.c', root_dir=root)
# 返回的是相对于 root_dir 的路径，如 'src/main.c'
print("C files in project/src:", found)
```

## 5.5 过滤隐藏文件与非隐藏文件

```
# 匹配所有隐藏文件（以点开头）
hidden = glob.glob('.*')
print("Hidden files:", hidden)

# 匹配所有 .txt，但不包括隐藏的 .txt
txt = glob.glob('*.txt')
print("Non-hidden .txt:", txt)
```

# 6. `os.listdir` + 自定义过滤的对比

`glob` 内部使用 `os.scandir()` 和 `fnmatch.fnmatch()`，它的优点是：

- 语法简洁，直接支持递归和通配符。
- 返回格式与输入路径一致（相对/绝对）。
- 自动处理路径分隔符。

如果你只需要简单的通配符，`glob` 是首选。若需要更复杂的条件（如根据文件大小、修改时间），则需结合 `os.path` 或 `pathlib` 自行过滤。

# 7. 与 `pathlib.Path.glob()` 的关系

`pathlib` 模块也提供了 `Path.glob()` 方法，功能类似且更面向对象，返回生成器。例如：

```
from pathlib import Path
list(Path('.').glob('*.py'))  # 返回 Path 对象列表
```

两者基本等价，但 `pathlib` 更现代化。若你需要在传统字符串路径上工作，`glob` 模块更为直接。

# 8. 总结

| 数              | 返回值         | 适用场景                                   |
| :-------------- | :------------- | :----------------------------------------- |
| `glob.glob()`   | 列表（已排序） | 需要一次性获取所有匹配路径，文件数量不大时 |
| `glob.iglob()`  | 迭代器         | 匹配海量文件，需逐次处理时                 |
| `glob.escape()` | 转义后的字符串 | 匹配文件名本身包含通配符字符的情况         |

`glob` 模块简单、轻量，是文件系统模式匹配的得力工具。配合 `os`、`shutil` 等模块，可以轻松实现批量文件处理、数据采集等任务。

**版本提示**：以上特性均适用于 Python 3.5+（`**` 支持）和 Python 3.10+（`root_dir` 和 `dir_fd`）。如果使用更早版本，请相应调整代码。

# 9. 补充

递归地遍历一个文件夹下面的所有 `txt` 文件：下面两种方法是比较推荐的。

## 9.1 方法一：最推荐 

推荐值：⭐⭐⭐⭐⭐

```python
from pathlib import Path

# 返回生成器，每个元素是 Path 对象
your_dir = '.'
for file in Path(your_dir).rglob('*.txt'):
    print(file)                # 打印路径
    print(file.stat().st_size) # 可直接获取属性
```

## 9.2 方法二：更加细粒度地控制时选择此方法 

推荐值：⭐⭐⭐⭐

```python
import os

txt_files = []
for dirpath, dirnames, filenames in os.walk('.'):
    for f in filenames:
        if f.endswith('.txt'):
            txt_files.append(os.path.join(dirpath, f))
```
