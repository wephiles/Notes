---
aliases:
  - course of study
  - course
  - tutorial
  - sys tutorial
tags:
  - tutorial
  - computer-science
  - sys
  - Python
  - libraries
  - built-in
category:
  - knowledge
  - Python builtin libraries
  - sys
datetime: " 2026-08-02 14:08:64 周日"
author: wephiles
rating: "5"
---
`sys` 模块是 Python 标准库中最核心的模块之一，它提供了对 Python 解释器内部变量和函数的访问，让我们可以在运行时操控、查询解释器的状态，并与操作系统交互。

# 一、`sys` 模块概览

`sys` 模块始终可用，因为它内置于解释器中，不需要额外安装。它主要处理三类事务：

1. **解释器信息与配置**：版本、平台、编码、整数和浮点数精度等。
2. **运行时环境**：命令行参数、Python 路径、标准输入输出流、递归限制等。
3. **高级功能**：模块导入钩子、审计事件、异常处理、跟踪函数、垃圾回收等。

使用时只需 `import sys`。

# 二、 常用常量与变量

这些大多数是解释器启动时就设置好的只读或可读写的“属性”。

## 2.1 命令行参数和解释器路径

| 属性                             | 说明                                                         |
| :------------------------------- | :----------------------------------------------------------- |
| `sys.argv`                       | 命令行参数列表，`argv[0]` 为脚本名（或 `-c` 时是字符串 `'-c'`） |
| `sys.executable`                 | Python 解释器的绝对路径                                      |
| `sys.prefix` / `sys.exec_prefix` | Python 安装目录的前缀                                        |

示例：打印命令行参数

```python
import sys

print(sys.argv)  # ['.\\funcs\\my_args.py', 'a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
print('脚本名:', sys.argv[0])  # 脚本名: .\funcs\my_args.py
print('参数列表:', sys.argv[1:])  # 参数列表: ['a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
```

执行命令: `python .\funcs\my_args.py a b c --input a.txt --output b.txt` 后的输出结果：

```
['.\\funcs\\my_args.py', 'a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
脚本名: .\funcs\my_args.py
参数列表: ['a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
```

----

执行命令

```python
cd funcs 
python my_args.py a b c --input a.txt --output b.txt
```

后的输出结果：

```python
['my_args.py', 'a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
脚本名: my_args.py
参数列表: ['a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
```

---

上一步骤已经将当前工作目录切换到了 `my_args.py` 这个脚本所在的目录，执行命令

```python
python -m my_args a b c --input a.txt --output b.txt
```

的输出结果为：

```python
['E:\\Code\\PyProjects\\Demos\\practice\\funcs\\my_args.py', 'a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
脚本名: E:\Code\PyProjects\Demos\practice\funcs\my_args.py
参数列表: ['a', 'b', 'c', '--input', 'a.txt', '--output', 'b.txt']
```

---

```python
import sys

print(sys.executable)  # E:\Code\PyProjects\Demos\practice\.venv\Scripts\python.exe
print(sys.prefix)  # E:\Code\PyProjects\Demos\practice\.venv
print(sys.exec_prefix)  # E:\Code\PyProjects\Demos\practice\.venv
```

## 2.2 平台与版本信息

| 属性               | 说明                                                     | 典型值                           |
| :----------------- | :------------------------------------------------------- | :------------------------------- |
| `sys.platform`     | 操作系统标识符                                           | `'win32'`, `'linux'`, `'darwin'` |
| `sys.version`      | 完整的 Python 版本字符串                                 | `'3.11.5 (main, ...)'`           |
| `sys.version_info` | 命名的元组 `(major, minor, micro, releaselevel, serial)` | `sys.version_info.major` 为 3    |
| `sys.api_version`  | 解释器 C API 版本                                        | 如 `1013`                        |
| `sys.hexversion`   | 版本的十六进制编码，方便比较                             | `0x30b00a0`                      |

```python
import sys
if sys.platform == 'win32':
    print("运行在 Windows")
elif sys.platform == 'darwin':
    print("运行在 macOS")
else:
    print("运行在 Linux/Unix")
```

```python
运行在 Windows
```

---

```python
import sys

print(sys.platform)  # win32
print(sys.version)  # 3.12.12 (main, Dec  5 2025, 21:31:16) [MSC v.1944 64 bit (AMD64)]
print(sys.version_info)  # sys.version_info(major=3, minor=12, micro=12, releaselevel='final', serial=0)
print(sys.api_version)  # 1013
print(sys.hexversion)  # 51121392
```

## 2.3 编码与文件系统

| 属性                                         | 说明                           |
| :------------------------------------------- | :----------------------------- |
| `sys.getdefaultencoding()`                   | 默认字符串编码，通常 `'utf-8'` |
| `sys.getfilesystemencoding()`                | 操作系统文件名编码             |
| `sys.stdin.encoding` / `sys.stdout.encoding` | 标准输入输出流的编码           |

```python
import sys

print(sys.getdefaultencoding())  # utf-8
print(sys.getfilesystemencoding())  # utf-8
print(sys.stdin.encoding)  # utf-8
print(sys.stdout.encoding)  # utf-8
```

## 2.4 递归限制与整数大小

| 属性                       | 说明                                                   |
| :------------------------- | :----------------------------------------------------- |
| `sys.getrecursionlimit()`  | 返回当前递归最大深度（默认 1000）                      |
| `sys.setrecursionlimit(n)` | 设置递归最大深度                                       |
| `sys.maxsize`              | 平台相关的最大整数值（`2**63-1` 在 64 位系统）         |
| `sys.maxunicode`           | Unicode 字符的最大码点，通常是 `1114111`（`0x10FFFF`） |

```python
import sys

print(sys.getrecursionlimit())  # 1000
print(sys.maxsize)  # 9223372036854775807(2 ** 63 - 1)
print(sys.maxunicode)  # 1114111
```

## 2.5 导入相关路径

| 属性                      | 说明                                           |
| :------------------------ | :--------------------------------------------- |
| `sys.path`                | 一个字符串列表，指定模块搜索路径。可修改。     |
| `sys.meta_path`           | 元路径查找器列表，用于自定义导入逻辑           |
| `sys.path_hooks`          | 路径钩子列表，为 `sys.path` 中的路径创建查找器 |
| `sys.path_importer_cache` | 缓存路径对应的查找器对象                       |
| `sys.modules`             | 已加载模块的字典，可手动注入或删除             |

**示例：临时添加搜索路径**

```
import sys
sys.path.insert(0, '/my/custom/libs')
import my_module
```

## 2.6 标准流

| 属性                                          | 说明                                                  |
| :-------------------------------------------- | :---------------------------------------------------- |
| `sys.stdin`                                   | 标准输入流（可被重定向）                              |
| `sys.stdout`                                  | 标准输出流                                            |
| `sys.stderr`                                  | 标准错误流                                            |
| `sys.__stdin__` / `__stdout__` / `__stderr__` | 保存初始的原始标准流，即使 `sys.stdin` 被替换也能访问 |

## 2.7 对象信息与内存

| 属性/函数                          | 说明                                                         |
| :--------------------------------- | :----------------------------------------------------------- |
| `sys.getsizeof(object[, default])` | 返回对象占用的内存字节数（只计对象本身，不计引用的其他对象） |
| `sys.getrefcount(object)`          | 返回对象的引用计数                                           |

```python
import sys


class Foo:

    def __init__(self):
        self.a = 0
        self.b = 10

    def fun(self):
        print('good', self.a + self.b)


obj = Foo()

print(sys.getsizeof(obj))  # 48
print(sys.getrefcount(obj))  # 2
```

## 2.8 线程、异步与底层信息

| 属性                 | 说明                                       |
| :------------------- | :----------------------------------------- |
| `sys.thread_info`    | 线程实现的信息（名、锁类型、版本）         |
| `sys.float_info`     | 浮点数精度和内部表示的详细信息             |
| `sys.int_info`       | 整数的内部表示信息（位数等）               |
| `sys.flags`          | 命令行标志（如 `-O`、`-v`）的结构体        |
| `sys.implementation` | 当前 Python 实现的信息（如 cpython, pypy） |

# 三、 核心函数和方法

## 3.1 退出程序

**`sys.exit([arg])`**： 引发 `SystemExit` 异常，从而退出解释器。`arg` 可为：

- 整数：0 表示正常退出，非 0 表示异常。
- 字符串：打印该字符串并退出。
- 其他对象：打印对象并返回退出码 1。

## 3.2 异常信息

- **`sys.exc_info()`**：返回当前正在处理的异常的三元组 `(type, value, traceback)`，适合在 `except` 块中获取完整信息。

  ```python
  try:
      1/0
  except:
      exc_type, exc_value, exc_tb = sys.exc_info()
      print(f"类型: {exc_type.__name__}, 消息: {exc_value}")
  ```

- **`sys.excepthook(type, value, traceback)`**：未被捕获的异常最终会调用这个函数，可以自定义全局异常处理，例如将错误写入日志。

  ```python
  import sys, traceback
  
  def my_excepthook(exc_type, exc_value, exc_tb):
      print("自定义异常处理:")
      traceback.print_exception(exc_type, exc_value, exc_tb)
  
  sys.excepthook = my_excepthook
  raise RuntimeError("测试")
  ```

## 3.3 输出钩子

**`sys.displayhook(value)`**：在交互模式下，表达式求值结果会交给 `displayhook` 显示。可重定义以实现自定义打印。

python

```
import sys
old_hook = sys.displayhook
def my_display(value):
    if value is not None:
        print(f"结果: {value!r}")
sys.displayhook = my_display
# 在交互式环境下测试
```

## 3.4 跟踪与分析

- **`sys.settrace(tracefunc)`**：设置系统级跟踪函数，用于调试器实现。跟踪函数会在每行代码执行前被调用（frame, event, arg）。
- **`sys.setprofile(profilefunc)`**：设置性能分析函数，比 `settrace` 事件更少（`'call'`, `'return'`, `'c_call'`, `'c_return'`, `'c_exception'`）。

**简单跟踪示例（打印每行执行的代码）**

```
import sys

def trace_calls(frame, event, arg):
    if event == 'line':
        print(f"执行行号: {frame.f_lineno}, 文件: {frame.f_code.co_filename}")
    return trace_calls

def test():
    x = 1
    y = 2
    print(x + y)

sys.settrace(trace_calls)
test()
sys.settrace(None)  # 关闭跟踪
```

## 3.5 审计与安全

Python 3.8+ 引入了审计事件系统，允许监控敏感操作。

- **`sys.audit(event, \*args)`**：触发一个审计事件。
- **`sys.addaudithook(hook)`**：注册一个回调，当审计事件触发时调用。

```
import sys

def audit_hook(event, args):
    print(f"审计事件: {event}, 参数: {args}")

sys.addaudithook(audit_hook)
# 内置的 open 操作会触发 'open' 事件
f = open("test.txt", "w")
f.close()
```

## 3.6 模块与导入相关函数

- **`sys._getframe([depth])`**：获取当前的栈帧对象。
- **`sys._current_frames()`**：返回所有线程当前栈帧的字典，用于调试死锁。

## 3.7 其他实用函数

- **`sys.getsizeof(object)`**：如前所述。
- **`sys.intern(string)`**：返回字符串的“驻留”版本，节省内存，适用于大量重复字符串比较。
- **`sys.getallocatedblocks()`**：返回当前分配的内存块数量（仅用于 `CPython` 内存追踪）。

# 四、 以 `sys.flags` 等为代表的信息结构体

这些不是函数，而是包含特定属性的命名元组或类似结构体的对象，提供了对解释器标志的详细描述。

- **`sys.flags`**：包含命令行标志，如 `sys.flags.debug`（是否 -d），`sys.flags.optimize`（优化级别），`sys.flags.isolated`（隔离模式）等。
- **`sys.float_info`**：`max`, `min`, `epsilon`, `dig`, `mant_dig` 等。
- **`sys.int_info`**：`bits_per_digit`, `sizeof_digit`。
- **`sys.hash_info`**：哈希算法的参数（宽度、模数、种子等）。
- **`sys.thread_info`**：`name`（如 `'nt'` 或 `'pthread'`），`lock` 实现，`version`。

```
import sys
print(sys.float_info)
# sys.float_info(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, min=2.2250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, epsilon=2.220446049250313e-16, radix=2, rounds=1)
```

`sys` 模块的功能贯穿 Python 程序的生命周期，熟练掌握它能让你更好地控制解释器行为、构建更健壮和灵活的应用。无论是编写命令行工具、调试器、性能分析器，还是进行底层系统集成，`sys` 都是必须精通的模块之一。
