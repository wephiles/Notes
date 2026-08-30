---
aliases:
  - course of study
  - course
  - tutorial
  - argparse tutorial
tags:
  - tutorial
  - computer-science
  - Python
  - argparse
  - built-in
  - libraries
category:
  - knowledge
  - argparse
  - Python builtin libraries
datetime: " 2026-08-02 14:08:43 周日"
author: wephiles
rating: "6"
---

`argparse` 是 Python 标准库中用于编写用户友好命令行接口的模块。它能自动生成帮助和用法信息，并在用户给程序传入无效参数时报错。

# 一、 核心概念

`argparse` 的工作流程通常是：

1. 创建一个 `ArgumentParser` 对象，它保存所有必要信息，用于将命令行参数解析为 Python 数据类型。
2. 通过调用 `add_argument()` 方法，向该对象添加你要支持的命令行参数信息。
3. 调用 `parse_args()` 方法，将命令行参数字符串（默认是 `sys.argv`）转换成具有属性的命名空间对象，参数值就可以通过该对象的属性来访问。

# 二、 主要类和函数

## 2.1 `ArgumentParser` 类

这是核心类，用于构造解析器。

### 2.1.1 构造方法主要参数

**参数全部都为可选参数**

- `prog`：程序名（默认为 `sys.argv[0]`）。
  - 补充：`sys.argv[0]` 可参考 [[sys#2.1 命令行参数和解释器路径|命令行参数和解释器路径]]
- `usage`：描述程序用法的字符串（默认由解析器自动生成）。
- `description`：在参数帮助文档之前显示的文本（简要说明程序是做什么的）。
- `epilog`：在参数帮助文档之后显示的文本。
- `parents`：一个 `ArgumentParser` 对象列表，可以共享它们的参数。
- `formatter_class`：定制帮助文档输出的格式类，如 `argparse.RawDescriptionHelpFormatter` 等。
- `prefix_chars`：前缀字符集，默认为 `'-'`，可设置如 `'-+'`。
- `fromfile_prefix_chars`：如果提供，以这些字符开头的参数会被当作文件读取。
- `argument_default`：全局默认参数值。
- `conflict_handler`：冲突处理策略，默认为 `'error'`。
- `add_help`：是否自动添加 `-h/--help` 选项，默认 `True`。
- `allow_abbrev`：是否允许长选项的缩写，默认 `True`（Python 3.5+）。
- `exit_on_error`：出错时是否退出程序，默认 `True`（Python 3.9+）。

### 2.1.2 主要方法

- `add_argument(name or flags...[, options...])`：添加一个参数说明。
- `parse_args(args=None, namespace=None)`：解析命令行参数，返回一个 `Namespace` 对象。`args` 是要解析的字符串列表，默认从 `sys.argv[1:]` 获取。
- `add_subparsers([title][, dest][, ...])`：添加子命令解析器，返回一个特殊的动作对象，可通过 `add_parser()` 添加子解析器。
- `set_defaults(**kwargs)`：设置一些默认属性值。
- `error(message: str)`：报告错误并退出。
- `exit(status=0, message=None)`：退出程序。
- `print_help(file=None)`：打印帮助信息。
- `format_help()`：返回帮助信息字符串。
- `print_usage(file=None)`：打印简短用法。
- `format_usage()`：返回简短用法字符串。

## 2.2 `add_argument` 方法

这是定义参数的核心方法

**参数名形式**：

- 位置参数：没有前导 `-` 的名字 ，如 `foo`
- 可选参数：以 `-` 开头（如 `-f`， `--foo`）

**常用选项**：

- `action`：匹配到参数时要执行的动作。常用值：
  - `'store'`：存储值（默认）。
  - `'store_const'`：存储 `const` 指定的值。
  - `'store_true'` / `'store_false'`：存储布尔值（`True`/`False`），适用于 `--verbose` 之类标志。
  - `'append'`：将值追加到列表。
  - `'append_const'`：将 `const` 值追加到列表。
  - `'count'`：统计参数出现次数，常用于 `-v` 增加冗长级别。
  - `'help'`：自动打印帮助信息并退出。
  - `'version'`：打印版本信息并退出（需配合 `version` 参数）。
  - 可扩展：自定义类，继承 `argparse.Action`。
- `nargs`：该参数消耗的命令行参数个数。支持：
  - `N`（整数）：恰好 N 个。
  - `'?'`：0 或 1 个参数。
  - `'*'`：0 或多个，结果放入列表。
  - `'+'`：1 或多个，结果放入列表。
  - `argparse.REMAINDER`：剩余所有参数。
- `const`：某些动作和 `nargs='?'` 时的常量值。
- `default`：参数未出现时的默认值。
- `type`：用于类型转换的可调用对象，如 `int`, `float`，也可为自定义函数（如 `type=open` 打开文件）。
- `choices`：允许参数值的容器（列表、集合等）。
- `required`：标记可选参数为必需（默认为 `False`，仅可选参数使用）。
- `help`：参数的帮助描述。
- `metavar`：在帮助信息中显示的参数占位名。
- `dest`：设置解析后存放结果的属性名，位置参数默认是其名字，可选参数默认是长选项去掉 `--` 并转换下划线。
- `version`：用于 `action='version'` 时的版本字符串。

## 2.3  `Namespace` 类

`parse_args()` 返回的对象，属性对应解析后的参数值。你可以直接使用 `args.参数名` 来获取，也可以像普通对象一样 `vars(args)` 转为字典。

## 2.4 `Action` 类

`argparse.Action` 是所有动作的基类。自定义动作时需要继承它并实现 `__call__(self, parser, namespace, values, option_string=None)` 方法。

## 2.5 子解析器相关

- `parser.add_subparsers()` 返回一个 `_SubParsersAction` 对象，它有一个 `add_parser(name, **kwargs)` 方法，返回一个新的 `ArgumentParser` 对象，用于定义子命令的参数。通过 `dest` 参数可以在主解析器中访问到是哪个子命令被调用。

## 2.6 格式化帮助类

位于 `argparse` 模块内，用于控制帮助信息输出格式：

- `HelpFormatter`
- `RawDescriptionHelpFormatter`：保留 `description` 和 `epilog` 中的原始格式（不自动换行）。
- `RawTextHelpFormatter`：保留所有帮助文本的原始格式。
- `ArgumentDefaultsHelpFormatter`：自动将默认值信息添加到参数帮助中。
- `MetavarTypeHelpFormatter`：使用参数类型名作为 `metavar`。

# 三、 详细用法与示例

## 3.1 最基本的位置参数与可选参数

```python
import argparse

parser = argparse.ArgumentParser(description='一个计算器程序', epilog='@author: balabala')

parser.add_argument('x', type=int, help='第一个操作数')
parser.add_argument('y', type=int, help='第二个操作数')
parser.add_argument('-o', '--operation', choices=['add', 'mul'], default='add', help='操作类型(默认: add)')
parser.add_argument('-v', '--verbose', action='store_true', help='增加输出详细程度')

args = parser.parse_args()

result = args.x + args.y if args.operation == 'add' else args.x * args.y

if args.verbose:
    print(f'{args.x} {args.operation} {args.y} = {result}')
else:
    print(result)
```

```python
>>> python cal.py 3 6
9

>>> python cal.py 3 6 -o mul
18

>>> python cal.py 3 6 -o mul -v
3 mul 6 = 18

>>> python cal.py -h
usage: cal.py [-h] [-o {add,mul}] [-v] x y

一个计算器程序

positional arguments:
  x                     第一个操作数
  y                     第二个操作数

options:
  -h, --help            show this help message and exit
  -o {add,mul}, --operation {add,mul}
                        操作类型(默认: add)
  -v, --verbose         增加输出详细程度

@author: balabala
```

## 3.2 `store_true` 、 `store_false` 与 计数 `count`

```python
import argparse

parser = argparse.ArgumentParser(description='一个 argparse 示例程序', epilog='@author: balabala')

parser.add_argument('--debug', action='store_true', help='开启调试模式')
parser.add_argument('--quiet', '-q', action='count', default=0, help='降低输出级别，可重复使用')

args = parser.parse_args(['--debug', '-qqq'])

print('debug 模式开启:', args.debug)  # debug 模式开启: True
print('计数 quiet 参数的数量:', args.quiet)  # 计数 quiet 参数的数量: 3
```

## 3.3 `nargs` 用法

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('names', nargs='+', help='输入至少一个名字')
parser.add_argument('--ids', nargs=2, type=int, help='两个整数ID')
parser.add_argument('--files', nargs='*', help='0或多个文件')

args = parser.parse_args()

print(args.names)
print(args.ids)
print(args.files)
```

```python
>>> python .\main.py jsmes jordan kobe --ids 1 2 --files a.txt b.txt c.log
['jsmes', 'jordan', 'kobe']
[1, 2]
['a.txt', 'b.txt', 'c.log']
```

## 3.4 `type` 与自定义类型转换

可以使用内置类型，也可以传入自定义函数，或者利用 `FileType` 工厂直接打开文件。

```python
import argparse


def valid_port(value):
    i_value = int(value)
    if 1 <= i_value <= 65535:
        return i_value
    raise argparse.ArgumentTypeError(f'{value} 不是有效端口号')


parser = argparse.ArgumentParser()
parser.add_argument('--port', type=valid_port, default=8080, help='服务端口')

# type=argparse.FileType('r', encoding='utf-8') 此方式已被禁用，此处只接收文件路径，在需要时才打开文件进行处理
# parser.add_argument('--config', type=argparse.FileType('r', encoding='utf-8'), help='配置文件路径')

args = parser.parse_args(['--port', '1000000', ])

print(args.port)
```

```python
usage: main.py [-h] [--port PORT]
main.py: error: argument --port: 1000000 不是有效端口号
```

---

```python
import argparse


def valid_port(value):
    i_value = int(value)
    if 1 <= i_value <= 65535:
        return i_value
    raise argparse.ArgumentTypeError(f'{value} 不是有效端口号')


parser = argparse.ArgumentParser()
parser.add_argument('--port', type=valid_port, default=8080, help='服务端口')

# type=argparse.FileType('r', encoding='utf-8') 此方式已被禁用，此处只接收文件路径，在需要时才打开文件进行处理
# parser.add_argument('--config', type=argparse.FileType('r', encoding='utf-8'), help='配置文件路径')

args = parser.parse_args(['--port', '9090', ])

print(args.port)
```

```python
9090
```

## 3.5 `default` 和 `nargs='?'`

当 `nargs='?'` 时，若命令行没有提供参数，则值为 `default`；若提供了，则取该值。结合 `const` 可在只出现选项但不给值的情况下使用 `const`。

```python
parser = argparse.ArgumentParser()
parser.add_argument('--output', nargs='?', const='out.txt', default=None, help='输出文件，未指定文件则用 out.txt')

args = parser.parse_args([])
print(args.output)   # None

args = parser.parse_args(['--output'])
print(args.output)   # out.txt

args = parser.parse_args(['--output', 'result.txt'])
print(args.output)   # result.txt
```

## 3.6 互斥组 (`add_mutually_exclusive_group`)

互斥组用来限制组内选项不能同时出现。

```python
parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--start', action='store_true', help='启动服务')
group.add_argument('--stop', action='store_true', help='停止服务')

args = parser.parse_args(['--start'])
print(args.start, args.stop)  # True False
# 同时指定 --start --stop 会报错
```

## 3.7 子命令

创建类似 `git commit`、`git push` 这样的带有子命令的程序。

```python
import argparse

parser = argparse.ArgumentParser('文件管理工具')

sub_parser = parser.add_subparsers(dest='subcommands', help='子命令')

# copy 子命令
copy_parser = sub_parser.add_parser('copy', help='复制文件')
copy_parser.add_argument('src', help='源文件')
copy_parser.add_argument('dest', help='目标位置')
copy_parser.add_argument('-r', '--recursive', action='store_true', help='是否递归复制')

# delete 子命令
copy_parser = sub_parser.add_parser('delete', help='删除文件')
copy_parser.add_argument('target', nargs='+', help='需要删除的文件')
copy_parser.add_argument('-f', '--force', action='store_true', help='强制删除')

# args = parser.parse_args(['copy', 'a.txt', 'b.txt', '-r'])
# print(args.subcommands)  # copy
# print(args.src)  # a.txt
# print(args.dest)  # b.txt
# print(args.recursive)  # True

# args = parser.parse_args(['delete', 'a.txt', 'b.txt', '-f'])
# print(args.subcommands)  # delete
# print(args.target)  # ['a.txt', 'b.txt']
# print(args.force)  # True

parser.parse_args(['-h'])
```

```python
usage: 文件管理工具 [-h] {copy,delete} ...

positional arguments:
  {copy,delete}  子命令
    copy         复制文件
    delete       删除文件

options:
  -h, --help     show this help message and exit
```

---

```python
parser.parse_args(['copy', '-h'])
```

```python
usage: 文件管理工具 copy [-h] [-r] src dest

positional arguments:
  src              源文件
  dest             目标位置

options:
  -h, --help       show this help message and exit
  -r, --recursive  是否递归复制
```

## 3.8 自定义 `Action`

当需要做一些特殊处理时，可以扩展 `argparse.Action`。

```python
class UpperCaseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.upper())

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', action=UpperCaseAction, help='名字将转换为大写')
args = parser.parse_args(['-n', 'hello'])
print(args.name)  # HELLO
```

## 3.9 修改帮助显示和默认值

```python
parser = argparse.ArgumentParser(
    description='程序功能说明',
    epilog='更多信息请访问官网',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('--timeout', type=int, default=30, help='超时秒数')
parser.add_argument('--host', default='localhost', help='主机地址')
args = parser.parse_args(['-h'])
```

输出帮助时会自动在每个参数的 help 后追加 `(default: 30)` 等。

```python
usage: main.py [-h] [--timeout TIMEOUT] [--host HOST]

程序功能说明

options:
  -h, --help         show this help message and exit
  --timeout TIMEOUT  超时秒数 (default: 30)
  --host HOST        主机地址 (default: localhost)

更多信息请访问官网
```

## 3.10 从文件读取参数 (`fromfile_prefix_chars`)

```python
import argparse

parser = argparse.ArgumentParser(fromfile_prefix_chars='#')
parser.add_argument('--file1')
parser.add_argument('--file2')
# args.txt 文件内容：--file1\na.txt\n--file2\nb.txt
# 注意：在文件中不能写成一行，例如 --file1 a.txt --file2 b.txt
args = parser.parse_args(['#args.txt'])
print(args.file1, args.file2)
```

## 3.11 解析已知参数和未知参数(`parse_known_args`)

当你需要将部分参数传递给其他程序或插件时，可以使用 `parse_known_args()`，它返回 `(namespace, 剩余参数列表)`。

```python
parser = argparse.ArgumentParser()
parser.add_argument('--foo')
args, unknown = parser.parse_known_args(['--foo', 'bar', '--baz', '123'])
print(args)      # Namespace(foo='bar')
print(unknown)   # ['--baz', '123']
```

# 四、 示例：多功能文件管理工具

## 4.1 **程序功能简介**

- 主命令支持全局选项：`--verbose` / `-v`（计数，增加详细度）、`--quiet` / `-q`（静默模式）、`--version` 显示版本、`@参数文件` 批量传参。
- 提供四个子命令：`list`、`copy`、`delete`、`archive`，每个子命令都运用了不同的 `argparse` 特性。
- 帮助信息自动包含默认值（使用 `ArgumentDefaultsHelpFormatter`）。
- 展示了位置参数、可选参数、动作（`store_true`、`count`、`append`、`store_const`、`version`）、`nargs` 的各种形式、`choices`、`type` 转换、互斥组、自定义 `Action`、`REMAINDER` 捕获额外参数等。

## 4.2 实现

```python
#!/usr/bin/env python3
"""
多功能文件管理工具 (fm)

用法示例：
  fm -vv list /home -a --json
  fm copy a.txt b.txt -r --mode 755
  fm delete *.tmp -f --exclude important.tmp --exclude readonly.tmp
  fm archive --format zip --output backup.zip file1 file2 --fast
  fm @args.txt              # 从文件读取参数
"""

import argparse
import sys

# ---------- 自定义类型与动作 ----------

def valid_octal_mode(value: str) -> int:
    """将八进制权限字符串（如 '755'）转换为整数，校验有效性。"""
    try:
        mode = int(value, 8)
        if 0 <= mode <= 0o777:
            return mode
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(f"无效的权限模式: '{value}'，应为 3 位八进制数")

class UpperCaseAction(argparse.Action):
    """自定义动作：将参数值转为大写后存入命名空间。"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.upper())

# ---------- 主解析器 ----------

def build_parser():
    parser = argparse.ArgumentParser(
        prog='fm',
        description='多功能文件管理工具 — 支持列出、复制、删除和归档文件。',
        epilog='使用 "fm <子命令> -h" 获取子命令详细帮助。',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # 自动显示默认值
        fromfile_prefix_chars='@'  # 允许通过 @文件 传递参数
    )

    # 全局可选参数
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='详细模式，可重复使用以增加级别（例如 -vv）')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='静默模式，只输出错误信息')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0',
                        help='显示版本号并退出')

    # 子命令
    subparsers = parser.add_subparsers(title='子命令', dest='command',
                                       description='可用的操作命令',
                                       help='选择一个子命令运行')
    # 为了 Python 3.6 兼容，不设置 required=True，下面手动检查

    # -------------------- 子命令: list --------------------
    list_parser = subparsers.add_parser('list', help='列出目录内容',
                                        description='显示指定目录的文件和子目录')
    list_parser.add_argument('directory', nargs='?', default='.',
                             help='目标目录（默认为当前目录）')
    list_parser.add_argument('-a', '--all', action='store_true',
                             help='显示所有文件，包括隐藏文件')
    # 互斥组：输出格式不能同时指定
    format_group = list_parser.add_mutually_exclusive_group()
    format_group.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    format_group.add_argument('--csv', action='store_true', help='以 CSV 格式输出')
    list_parser.add_argument('--sort', choices=['name', 'size', 'date'],
                             default='name', help='排序方式')
    # 使用 nargs='*' 接收零个或多个过滤扩展名
    list_parser.add_argument('--ext', nargs='*', metavar='EXT',
                             help='过滤文件扩展名，如 --ext .py .txt')

    # -------------------- 子命令: copy --------------------
    copy_parser = subparsers.add_parser('copy', help='复制文件或目录',
                                        description='将源文件复制到目标位置')
    copy_parser.add_argument('src', help='源文件路径')
    copy_parser.add_argument('dest', help='目标路径')
    copy_parser.add_argument('-r', '--recursive', action='store_true',
                             help='递归复制目录')
    copy_parser.add_argument('--mode', type=valid_octal_mode, default=0o644,
                             help='设置目标文件权限（八进制，如 755）', metavar='MODE')
    copy_parser.add_argument('--tag', action=UpperCaseAction,
                             help='为文件添加标签（标签将自动转为大写）')

    # -------------------- 子命令: delete --------------------
    delete_parser = subparsers.add_parser('delete', help='删除文件',
                                          description='永久删除指定的文件')
    delete_parser.add_argument('targets', nargs='+', help='要删除的文件（可多个）')
    delete_parser.add_argument('-f', '--force', action='store_true',
                               help='强制删除，不询问确认')
    delete_parser.add_argument('--backup-suffix', action='store_const',
                               const='.bak', default=None,
                               help='删除前备份，并添加此后缀（默认为 .bak）')
    # append 动作：可以多次指定 --exclude 来构建排除列表
    delete_parser.add_argument('--exclude', action='append', default=[],
                               help='排除文件模式，可重复使用（例：--exclude "*.log"）')

    # -------------------- 子命令: archive --------------------
    archive_parser = subparsers.add_parser('archive', help='归档文件',
                                           description='将多个文件打包为压缩文件')
    archive_parser.add_argument('files', nargs='+', help='要归档的文件')
    archive_parser.add_argument('--format', choices=['zip', 'tar', 'gz'],
                                default='zip', help='归档格式')
    archive_parser.add_argument('-o', '--output', required=True,
                                help='输出文件名', metavar='ARCHIVE')
    # 互斥组：压缩级别
    compress_group = archive_parser.add_mutually_exclusive_group()
    compress_group.add_argument('--fast', action='store_true',
                                help='快速压缩（较低压缩比）')
    compress_group.add_argument('--best', action='store_true',
                                help='最佳压缩（较慢，压缩比高）')
    # 使用 REMAINDER 捕获归档命令之后的额外参数（可用于传递给后端工具）
    archive_parser.add_argument('extra_args', nargs=argparse.REMAINDER,
                                help='传递给归档工具的其他参数（高级用法）')

    return parser

# ---------- 模拟命令处理 ----------

def handle_list(args):
    print(f"[list] 目录: {args.directory} | 详细级别: {args.verbose} | 静默: {args.quiet}")
    print(f"       显示所有: {args.all} | 排序: {args.sort} | 扩展名过滤: {args.ext}")
    if args.json:
        print("       输出格式: JSON")
    elif args.csv:
        print("       输出格式: CSV")
    else:
        print("       输出格式: 文本表格")

def handle_copy(args):
    print(f"[copy] 从 '{args.src}' 到 '{args.dest}'")
    print(f"       递归: {args.recursive} | 权限: {oct(args.mode)}")
    if args.tag:
        print(f"       标签: {args.tag}")

def handle_delete(args):
    print(f"[delete] 待删除: {args.targets}")
    print(f"       强制: {args.force} | 备份后缀: {args.backup_suffix}")
    print(f"       排除模式: {args.exclude}")

def handle_archive(args):
    print(f"[archive] 文件: {args.files}")
    print(f"       格式: {args.format} | 输出: {args.output}")
    print(f"       压缩策略: fast={args.fast}, best={args.best}")
    if args.extra_args:
        print(f"       额外参数: {args.extra_args}")

# ---------- 主入口 ----------

def main():
    parser = build_parser()
    # 展示 parse_known_args 的用法（此处仅用于说明，实际仍用 parse_args）
    # args, unknown = parser.parse_known_args()
    # if unknown:
    #     print(f"警告：忽略未知参数 {unknown}", file=sys.stderr)
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 简单实现静默与详细级别
    if args.quiet:
        print("[quiet] 静默模式激活，将抑制常规输出。")

    # 根据子命令分发
    if args.command == 'list':
        handle_list(args)
    elif args.command == 'copy':
        handle_copy(args)
    elif args.command == 'delete':
        handle_delete(args)
    elif args.command == 'archive':
        handle_archive(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

## 4.3 示例运行

### 4.3.1 **查看全局帮助**

```
$ python fm.py -h
```

显示描述、默认值，并列出子命令。

### 4.3.2 **list 子命令**

```
$ python fm.py -vv list /tmp --json --sort size --ext .log .txt
```

- `-vv`：verbose 级别为 2
- `--json`：指定 JSON 格式（与 `--csv` 互斥）
- `--ext .log .txt`：`nargs='*'` 捕获零或多个扩展名

### 4.3.3 **copy 子命令**

```
$ python fm.py copy a.txt b.txt --mode 755 --tag important
```

- `--mode 755`：由 `valid_octal_mode` 类型转换，无效值（如 888）会报错
- `--tag important`：`UpperCaseAction` 将值转为 `"IMPORTANT"`

### 4.3.4 **delete 子命令**

```
$ python fm.py delete *.tmp -f --backup-suffix --exclude "*.log" --exclude "readonly.*"
```

- `--backup-suffix`：无参数，使用 `store_const` 将 `const='.bak'` 存入
- `--exclude`：多次使用，`action='append'` 构建列表

### 4.3.5 **archive 子命令**

```
$ python fm.py archive f1.txt f2.txt -o backup.zip --fast --extra-opt
```

- `--fast` 与 `--best` 互斥，二者只能选一
- `extra_args` 使用 `argparse.REMAINDER` 捕获 `--extra-opt` 等额外参数

### 4.3.6 **通过文件传递参数**

创建 `args.txt`：

```
-vv list /etc --json
```

运行：

```
$ python fm.py @args.txt
```

`fromfile_prefix_chars='@'` 使解析器自动将文件内容读取为命令行参数。

## 4.4 知识点对应

| 知识点                                     | 代码中的体现                                                 |
| :----------------------------------------- | :----------------------------------------------------------- |
| `ArgumentParser` 构造参数                  | `description`、`epilog`、`formatter_class=ArgumentDefaultsHelpFormatter`、`fromfile_prefix_chars='@'` |
| `add_argument` 动作 `store_true`           | `-a/--all`、`-r/--recursive`、`--json`、`--csv` 等           |
| `action='count'`                           | `-v/--verbose`                                               |
| `action='append'`                          | `--exclude`（delete 子命令）                                 |
| `action='store_const'`                     | `--backup-suffix`（delete 子命令）                           |
| `action='version'`                         | `--version`                                                  |
| `nargs` 用法（`?`, `*`, `+`, `REMAINDER`） | `directory`（?）、`--ext`（*）、`targets`（+）、`extra_args`（REMAINDER） |
| `type` 自定义转换                          | `valid_octal_mode` 用于 `--mode`                             |
| `choices`                                  | `--sort`（list）、`--format`（archive）                      |
| 互斥组                                     | `--json/--csv`（list）、`--fast/--best`（archive）           |
| `metavar`                                  | `--ext`、`--mode`、`-o/--output`                             |
| `required` 可选参数                        | `-o/--output` 标记为 required=True                           |
| `default`                                  | 大量参数使用，`ArgumentDefaultsHelpFormatter` 自动显示       |
| 自定义 `Action`                            | `UpperCaseAction` 用于 `--tag`                               |
| 子命令 `add_subparsers`                    | `list`、`copy`、`delete`、`archive`                          |
| `Namespace` 属性访问                       | `args.quiet`、`args.command` 等分发逻辑                      |
| `parse_args` / `parse_known_args`          | 正常使用 `parse_args`，注释中保留了 `parse_known_args` 示例  |



