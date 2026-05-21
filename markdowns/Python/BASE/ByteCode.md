# 如何读懂 Python 字节码

## 一、先理解基础概念

Python 字节码是运行在 **CPython 虚拟机（栈式虚拟机）** 上的指令序列。每条指令由 **操作码（opcode）** + **操作数（argument）** 组成。

### 1. 栈式虚拟机的核心思想

```
┌─────────┐
│         │   ← 栈顶 (TOS)
│   x     │
│   b     │
│   a     │   ← 栈底
└─────────┘
```

**所有计算都通过入栈和出栈完成**，没有"寄存器"的概念。

### 2. 一条指令的结构

```
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

```
  2           0 LOAD_FAST                0 (a)    # 把局部变量 a 压入栈
              2 LOAD_FAST                1 (b)    # 把局部变量 b 压入栈
              4 BINARY_ADD                        # 弹出栈顶两个值相加，结果压栈
              6 RETURN_VALUE                      # 弹出栈顶值，作为返回值
```



| 列           | 含义                                                |
| ------------ | --------------------------------------------------- |
| `2`          | 源代码行号                                          |
| `0, 2, 4, 6` | **字节偏移量**（每条指令占用 2 字节，所以步长为 2） |
| `LOAD_FAST`  | **操作码**（做什么）                                |
| `0 (a)`      | **操作数**（对谁做）                                |

## 二、掌握字节码的四大类别

### 🟢 1. 加载 / 存储类（数据搬运）

```
import dis

x = 10
def demo():
    a = 1            # LOAD_CONST → STORE_FAST
    b = True         # LOAD_CONST → STORE_FAST
    c = [1, 2, 3]    # LOAD_CONST → BUILD_LIST → STORE_FAST
    d = a            # LOAD_FAST → STORE_FAST

dis.dis(demo)
```



```
  3           0 LOAD_CONST               1 (1)        # 常量池中取值 1 压栈
              2 STORE_FAST              0 (a)         # 栈顶弹出，存入局部变量 a

  4           4 LOAD_CONST               2 (True)
              6 STORE_FAST              1 (b)

  5           8 LOAD_CONST               3 ((1, 2, 3))
             10 BUILD_LIST               3             # 弹出 3 个元素，构建列表
             12 STORE_FAST              2 (c)

  6          14 LOAD_FAST                0 (a)         # 从局部变量取值
             16 STORE_FAST              3 (d)
```

> **关键**：所有赋值都是先 `LOAD` 再 `STORE`。

### 🔵 2. 运算类

```
def calc():
    a = 2 + 3        # LOAD + LOAD + BINARY_ADD
    b = 10 - 4       # BINARY_SUBTRACT
    c = 3 * 7        # BINARY_MULTIPLY
    d = 20 / 5       # BINARY_TRUE_DIVIDE
    e = 2 ** 10      # BINARY_POWER
    f = a > b        # COMPARE_OP

dis.dis(calc)
```

```
  2           0 LOAD_CONST               1 (2)
              2 LOAD_CONST               2 (3)
              4 BINARY_ADD
              6 STORE_FAST              0 (a)

  3           8 LOAD_CONST               3 (10)
             10 LOAD_CONST               4 (4)
             12 BINARY_SUBTRACT
             ...
```

**运算的通用模式**：`压左操作数 → 压右操作数 → 运算指令`

### 🟡 3. 函数调用类

```
def greet(name, greeting="Hello"):
    msg = greeting + ", " + name
    return msg

def caller():
    result = greet("Alice")        # 默认 greeting
    result2 = greet("Bob", "Hi")   # 指定 greeting

dis.dis(caller)
```

```
  5           0 LOAD_GLOBAL              0 (greet)     # 加载函数对象
              2 LOAD_CONST               1 ('Alice')    # 压入位置参数
              4 CALL_FUNCTION            1             # 调用，1个参数
              6 STORE_FAST              0 (result)

  6           8 LOAD_GLOBAL              0 (greet)
             10 LOAD_CONST               2 ('Bob')
             12 LOAD_CONST               3 ('Hi')
             14 CALL_FUNCTION            2             # 调用，2个参数
             16 STORE_FAST              1 (result2)
```

### 🔴 4. 控制流类（循环、条件）

```
def flow(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"

dis.dis(flow)
```

```
  2           0 LOAD_FAST                0 (x)
              2 LOAD_CONST               1 (0)
              4 COMPARE_OP               4 (>)        # 比较，结果压栈
              6 POP_JUMP_IF_FALSE       16            # 如果 False，跳到偏移 16

  3           8 LOAD_CONST               2 ('positive')
             10 RETURN_VALUE

  4     >>   16 LOAD_FAST                0 (x)         # >> 表示跳转目标
             18 LOAD_CONST               1 (0)
             20 COMPARE_OP               0 (<)
             22 POP_JUMP_IF_FALSE       30

  5          24 LOAD_CONST               3 ('negative')
             26 RETURN_VALUE

  7     >>   30 LOAD_CONST               4 ('zero')
             32 RETURN_VALUE
```

> **关键指令**：
>
> - `POP_JUMP_IF_FALSE`：弹出栈顶，如果是 False 则跳转
> - `>>` 标记：这是一个跳转的目标位置

## 三、用手动模拟栈来练习

这是读懂字节码**最有效的方法**！

```
def mystery(a, b):
    c = a + b
    d = c * 2
    return d
```

```
import dis
dis.dis(mystery)
```

```
  2           0 LOAD_FAST    0 (a)
              2 LOAD_FAST    1 (b)
              4 BINARY_ADD
              6 STORE_FAST   2 (c)

  3           8 LOAD_FAST    2 (c)
             10 LOAD_CONST   1 (2)
             12 BINARY_MULTIPLY
             14 STORE_FAST   3 (d)

  4          16 LOAD_FAST    3 (d)
             18 RETURN_VALUE
```

### 逐步模拟栈变化（假设 a=3, b=5）：

| 偏移 | 指令              | 栈变化   | 局部变量                  |
| ---- | ----------------- | -------- | ------------------------- |
| 0    | `LOAD_FAST a`     | `[3]`    |                           |
| 2    | `LOAD_FAST b`     | `[3, 5]` |                           |
| 4    | `BINARY_ADD`      | `[8]`    | c=8（弹出两个，压入结果） |
| 6    | `STORE_FAST c`    | `[]`     | c=8                       |
| 8    | `LOAD_FAST c`     | `[8]`    |                           |
| 10   | `LOAD_CONST 2`    | `[8, 2]` |                           |
| 12   | `BINARY_MULTIPLY` | `[16]`   | d=16                      |
| 14   | `STORE_FAST d`    | `[]`     | d=16                      |
| 16   | `LOAD_FAST d`     | `[16]`   |                           |
| 18   | `RETURN_VALUE`    | `[]`     | **返回 16**               |

> 💡 **练习方法**：拿一支笔，像上面这样画表格，逐条指令追踪栈的变化。

## 四、常见指令速查表

### 加载类

| 指令          | 含义              | 从哪里取                  |
| ------------- | ----------------- | ------------------------- |
| `LOAD_CONST`  | 加载常量          | 常量池 `co_consts`        |
| `LOAD_FAST`   | 加载局部变量      | 局部变量数组（最快）      |
| `LOAD_NAME`   | 加载变量          | 局部/全局/内建 按顺序查找 |
| `LOAD_GLOBAL` | 加载全局变量/函数 | 全局命名空间              |
| `LOAD_ATTR`   | 加载对象属性      | `obj.attr`                |

### 存储类

| 指令           | 含义                          |
| -------------- | ----------------------------- |
| `STORE_FAST`   | 存到局部变量                  |
| `STORE_NAME`   | 存到变量（模块级别）          |
| `STORE_GLOBAL` | 存到全局变量                  |
| `STORE_ATTR`   | 存到对象属性 `obj.attr = val` |
| `STORE_SUBSCR` | 存到下标 `a[i] = val`         |

### 运算类

| 指令                 | 含义                                          |
| -------------------- | --------------------------------------------- |
| `BINARY_ADD`         | `+`                                           |
| `BINARY_SUBTRACT`    | `-`                                           |
| `BINARY_MULTIPLY`    | `*`                                           |
| `BINARY_TRUE_DIVIDE` | `/`（真除法）                                 |
| `BINARY_MODULO`      | `%`                                           |
| `BINARY_POWER`       | `**`                                          |
| `COMPARE_OP`         | `==`, `!=`, `<`, `>`, `<=`, `>=`, `in`, `is`… |

### 控制流类

| 指令                | 含义                       |
| ------------------- | -------------------------- |
| `POP_JUMP_IF_FALSE` | 栈顶为 False 时跳转        |
| `POP_JUMP_IF_TRUE`  | 栈顶为 True 时跳转         |
| `JUMP_FORWARD`      | 无条件向前跳转（用于循环） |
| `JUMP_ABSOLUTE`     | 跳到指定绝对位置           |
| `FOR_ITER`          | 获取迭代器的下一个值       |
| `SETUP_LOOP`        | 设置循环块（旧版本）       |

### 函数调用类

| 指令            | 含义                      |
| --------------- | ------------------------- |
| `CALL_FUNCTION` | 调用函数（Python ≤ 3.10） |
| `CALL`          | 调用函数（Python 3.11+）  |
| `MAKE_FUNCTION` | 创建函数对象              |
| `RETURN_VALUE`  | 返回栈顶值                |

### 容器构建类

| 指令           | 含义                      |
| -------------- | ------------------------- |
| `BUILD_LIST`   | 构建列表                  |
| `BUILD_TUPLE`  | 构建元组                  |
| `BUILD_MAP`    | 构建字典                  |
| `BUILD_SET`    | 构建集合                  |
| `BUILD_STRING` | 拼接字符串（f-string 用） |

## 五、进阶：看懂 for 循环

```
def total(items):
    s = 0
    for item in items:
        s += item
    return s
```

```
dis.dis(total)
```

复制

```
  2           0 LOAD_CONST               1 (0)
              2 STORE_FAST               1 (s)

  3           4 LOAD_GLOBAL              0 (range)     # 或迭代器
              6 LOAD_FAST                0 (items)
              8 GET_ITER                               # 获取迭代器
        >>   10 FOR_ITER                 8 (to 20)    # 取下一个值，没有则跳到 20
             12 STORE_FAST               2 (item)

  4          14 LOAD_FAST                1 (s)
             16 LOAD_FAST                2 (item)
             18 BINARY_ADD
             20 STORE_FAST               1 (s)
             22 JUMP_ABSOLUTE           10            # 回到 FOR_ITER
        >>   24 LOAD_FAST                1 (s)
             26 RETURN_VALUE
```

```
循环结构图解：

    ┌→ FOR_ITER ──→ 有值 ──→ STORE_FAST item
    │                             │
    │                          循环体
    │                             │
    └──── JUMP_ABSOLUTE ←─────────┘
          │
      没有值（迭代结束）
          ↓
     LOAD_FAST s → RETURN_VALUE
```

## 六、Python 3.11+ 的变化

Python 3.11 引入了 **特化指令（Specialized/Adaptive Instructions）**，字节码会有 `adapt` 和 `specialize` 的过程：

```
# Python 3.11+
dis.dis("x = a + b")
```

你可能看到 `_ADAPTIVE` 前缀的指令（如 `LOAD_FAST__LOAD_FAST`），这是 CPython 的 **JIT 预热机制**：

```
首次执行：通用指令（如 LOAD_FAST）
多次执行：自动替换为特化指令（如 LOAD_FAST__LOAD_FAST，一次完成两个加载）
```

> 不影响阅读理解，`dis` 模块默认会反编译为可读的形式。

## 七、推荐学习路线

```
1. ✅ 理解"栈"的概念
2. ✅ 学会 dis.dis() 打印字节码
3. ✅ 记住 LOAD/STORE/运算/控制流 四大类指令
4. ✅ 拿简单函数，手动画栈模拟执行过程
5. ✅ 尝试给简单的字节码"反向写回 Python 源码"
6. 🔬 研究 CPython 源码中的 ceval.c（解释器主循环）
```

> ![引用](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAPLSURBVHgBzZi/UxNBFMffW35EIZGkQLlIQQpsQfwDiDXqYAcMhRboUCEz0gL5A5RQMQIzYiNY0UjHDNgLgy0UxBmGY0KRSE4U8Hbdd5BALpdkE0KST5Pc7dvZ773dffv2IRSJfpgICuCdwLEbQHQCohcEeK1GhLgQIoKAEQHiB2NsXWv2rEMRYCHGu7vCe8ttjMjB36TEqBMRCOvMrAtp2u2IaiclgSTM1WhMAAkrAVLogqrQvAIPosYIBz5ZhMfyEeEIoda7dxZyGeUUuB9NTJXKa1lhGPY3e0azNTsKPJ/SxLL0WhDKgNxIW6fH/HEg4Ivb25hTh/oGY61c4gi52ztdjTXLTm0ZAmlakcJGuZEO2T+US8pG2hTvRY9eMAEfoZIIMepvaQonH1MCdf1Pm2Bna/JvG1SW+MmxGUiux8sprjmbgMqLI7wud+1E8sHy4IX3dqGKkF70kRdrrSfynlDvvLG5AYtLX2B7exv2dd16t7a6Ch6PJ8M2kUhI2yXZZxO2d3as56c9PTAxPp5zjPoGRvF30hIoCggp76amrAHtGAkjQyAJejs2lvqIQpChZ4QEMl1PBEFx7c3OzTmKc0KXoooVd4GXMqZazngQFXIGmpqvKysZ7x91dYFf08Dtcae9/y6n1C6OPPxETm+wuxtUECbvrJXiOlSMNxwGfNDeDh9mZhzt7Z6mjyBbTf6qIrdFUIYZbFMxpg1hJ5cn7PYkrBBxBCJ2MEDRpmKsO6ylbAPScigRXnadPO99OAwDg4PW5rmKYRgZtrREnvX2wuvhYcePzS7wGpCnKJTMzs8reY3WMAn9vLgIqjC64EAJoDiobGso28Zpiksi8EZAEaEp3oIqRXD4KT0ovkG1grDFULCq9SBd+JmmyRu/wkZxO2Qq6e2XR53b7c5tm6f9HBGhaoQVZoQppvOZD/T1WceVHTpfXw0NpWUyyXdO0PE40N8PeeUhrtOvlSXsxmJe12lNDKoI5GZA03zWLoaAzxfnIr8XywWVRkgc/U+dJGcuWd7AaoiJMvaZZij5lBJIXoR/IgQVhnMMJb1HpJ3Ffn9TuJJTTWO3aunFJMdUej96VNbSB0H1mfv3mh7a3ztmMyd15nPZpXwBXBY2qXjk3JSDvYNfYYbW7erGsKa1pSlriS9nPkgdkcNL2llQalDEqQ6TSxyRN2HV5KJFTu4Xn6BEkNdOfvPA1SJRNgoqout6TJZI2KT826162bocScSFCdOnf3nYqVCZtRsUCV34L+7U8toqL14oL/8CvUkx54kwblE6RxmTlZQUwX9+F568K5L+eAAAAABJRU5ErkJggg==)
>
> **最快上手的练习**：写一个包含 `if/else`、`for`、函数调用的函数，用 `dis.dis()` 打印出来，然后**逐行画栈**模拟执行。反复练 5-10 个例子，就能 fluently 阅读字节码了。

# 推荐资源

推荐三个方向/资源，都是圈内公认比较经典、权威的入口（顺带附一个视频）：

1. AOSA 上的《A Python Interpreter Written in Python (Byterun)》

- 入口：https://aosabook.org/en/500L/a-python-interpreter-written-in-python.htmlaosabook.org
- 特点：作者 Allison Kaptur（Dropbox，多年维护 Python 客户端）联合 Ned Batchelder 写的章节。用一个 500 行左右的“迷你解释器”把 CPython 的栈式虚拟机、字节码解释、值栈/帧等讲得很透，是理解“字节码是怎么被执行”的经典长文；页面顶部有“简体中文”版本链接aosabook.org。
- 适合：想从“实现一个解释器”的角度系统理解字节码和虚拟机运作。

1. CPython 官方文档：dis 模块（并由此延伸到 opcode 源码）

- 入口：https://docs.python.org/3/library/dis.htmlpython.org
- 特点：官方权威；对字节码格式、指令集、Cache/特化、各版本行为变更都有说明，并给出大量示例和命令行用法；文档里会指引你去看 Include/opcode.h 等源码python.org。
- 适合：查具体指令含义、版本差异，以及作为日常对照手册。

1. Black Duck Blog：《Understanding Python bytecode》（偏实战与“看懂真实字节码”）

- 入口：https://www.blackduck.com/blog/understanding-python-bytecode.htmlblackduck.com
- 特点：从“怎么看 .pyc、拿 CodeType、逐条指令解析”讲起，带完整示例，并解释操作数如何指向 co_consts/co_names 等字段blackduck.com；适合作为“第一次读真实字节码”的实践向教程。
- 适合：希望动手看/改字节码、从二进制层面理解 Python 的读者。

补充视频（非常值得一看）

- 《A Bit about Bytes: Understanding Python Bytecode》— James Bennett，PyCon US 2018：https://pyvideo.org/pycon-us-2018/a-bit-about-bytes-understanding-python-bytecode.htmlpyvideo.org

学习建议路径：

- 先看 Byterun 那章建立“栈式虚拟机+字节码”的整体图景aosabook.org；
- 再用官方 dis 文档做“字典”，随时查指令与细节python.org；
- 然后用 Black Duck 的文章练手，对着自己代码跑 `dis.dis`、对照阅读blackduck.com；
- 有余力再配上 PyCon 那个视频加深理解

# 如何读懂 Python 字节码

Python 字节码是 Python 源代码编译后的中间表示形式，由 Python 虚拟机（PVM）执行。理解字节码有助于你深入掌握 Python 的运行机制、进行性能调优和调试。下面从基础到进阶，系统性地介绍如何读懂它。

## 一、什么是 Python 字节码？

当你运行一个 `.py` 文件时，Python 会经历以下过程：

```
源代码 (.py)  →  编译器  →  字节码 (.pyc)  →  虚拟机 (PVM)  →  执行
```

- **编译阶段**：`CPython` 编译器将源代码翻译成字节码指令序列。
- **执行阶段**：Python 虚拟机逐条解释执行这些字节码指令。

字节码本质上是一系列**操作码（opcode）**和**操作数（argument）**，每条指令对应虚拟机的一个原子操作。

## 二、查看字节码的核心工具：`dis` 模块

Python 标准库中的 `dis` 模块是反汇编字节码的主要工具。

### 1. 基本用法

```
import dis

def greet(name):
    message = "Hello, " + name
    print(message)

dis.dis(greet)
```

输出类似：

```
  2           0 LOAD_CONST               1 ('Hello, ')
              2 LOAD_FAST                0 (name)
              4 BINARY_ADD
              6 STORE_FAST               1 (message)

  3           8 LOAD_GLOBAL              0 (print)
             10 LOAD_FAST                1 (message)
             12 CALL_FUNCTION            1
             14 POP_TOP
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE
```

### 2. `dis` 模块的其他有用函数



| 函数                        | 用途                                     |
| --------------------------- | ---------------------------------------- |
| `dis.dis(obj)`              | 反汇编函数、方法、类或代码对象           |
| `dis.disassemble(code_obj)` | 反汇编代码对象                           |
| `dis.code_info(func)`       | 显示函数的元信息（参数数量、局部变量等） |
| `dis.distb(tb)`             | 反汇编异常回溯中的栈帧                   |
| `dis.show_code(func)`       | 显示代码对象的详细信息                   |

### 3. 查看更详细的字节码

```
# 使用 dis.Bytecode 获取更结构化的信息
import dis

def add(a, b):
    return a + b

bytecode = dis.Bytecode(add)
for instr in bytecode:
    print(f"{instr.offset:4d} {instr.opname:<25s} {instr.argrepr}")
```

## 三、字节码指令的结构

每一行字节码通常包含以下字段：

```
偏移量  操作码          操作数          含义
  0     LOAD_CONST      1 ('Hello')    将常量 'Hello' 压入栈
  2     LOAD_FAST       0 (name)       将局部变量 name 压入栈
```



| 字段                  | 说明                                           |
| --------------------- | ---------------------------------------------- |
| **偏移量 (offset)**   | 字节码在指令序列中的位置（字节偏移）           |
| **操作码 (opcode)**   | 要执行的操作名称，如 `LOAD_FAST`、`BINARY_ADD` |
| **操作数 (argument)** | 操作码的参数，如变量索引、常量索引             |
| **argrepr**           | 操作数的可读表示                               |

## 四、核心操作码分类详解

### 1. 栈操作类

Python 虚拟机是一个**基于栈**的虚拟机，所有计算都通过操作栈来完成。



| 操作码         | 含义                         |
| -------------- | ---------------------------- |
| `LOAD_CONST`   | 将常量压入栈顶               |
| `LOAD_FAST`    | 将局部变量压入栈顶（速度快） |
| `LOAD_GLOBAL`  | 将全局变量压入栈顶           |
| `LOAD_ATTR`    | 加载对象属性                 |
| `LOAD_DEREF`   | 加载闭包中的自由变量         |
| `STORE_FAST`   | 将栈顶值存入局部变量         |
| `STORE_GLOBAL` | 将栈顶值存入全局变量         |
| `STORE_ATTR`   | 将栈顶值存入对象属性         |
| `POP_TOP`      | 弹出栈顶元素                 |
| `DUP_TOP`      | 复制栈顶元素                 |
| `ROT_TWO`      | 交换栈顶两个元素             |

### 2. 运算类



| 操作码                | 含义                          |
| --------------------- | ----------------------------- |
| `BINARY_ADD`          | 加法（栈顶两元素相加）        |
| `BINARY_SUBTRACT`     | 减法                          |
| `BINARY_MULTIPLY`     | 乘法                          |
| `BINARY_TRUE_DIVIDE`  | 真除法                        |
| `BINARY_FLOOR_DIVIDE` | 整除                          |
| `BINARY_MODULO`       | 取模                          |
| `BINARY_POWER`        | 幂运算                        |
| `BINARY_SUBSCR`       | 索引操作（如 `a[b]`）         |
| `COMPARE_OP`          | 比较操作（如 `<`, `>`, `==`） |

### 3. 函数调用类



| 操作码             | 含义                          |
| ------------------ | ----------------------------- |
| `CALL_FUNCTION`    | 调用函数（Python 3.6 及之前） |
| `CALL_FUNCTION_KW` | 调用带关键字参数的函数        |
| `CALL_METHOD`      | 调用方法                      |
| `CALL`             | 统一调用指令（Python 3.11+）  |
| `PRECALL`          | 预调用准备（Python 3.11+）    |
| `RETURN_VALUE`     | 返回函数结果                  |

### 4. 控制流类



| 操作码              | 含义               |
| ------------------- | ------------------ |
| `JUMP_FORWARD`      | 向前跳转           |
| `JUMP_ABSOLUTE`     | 跳转到绝对位置     |
| `POP_JUMP_IF_TRUE`  | 如果为真则跳转     |
| `POP_JUMP_IF_FALSE` | 如果为假则跳转     |
| `FOR_ITER`          | for 循环迭代       |
| `SETUP_LOOP`        | 设置循环（旧版本） |

### 5. 容器构建类



| 操作码                | 含义           |
| --------------------- | -------------- |
| `BUILD_LIST`          | 构建列表       |
| `BUILD_TUPLE`         | 构建元组       |
| `BUILD_MAP`           | 构建字典       |
| `BUILD_SET`           | 构建集合       |
| `BUILD_CONST_KEY_MAP` | 构建常量键字典 |
| `LIST_APPEND`         | 列表追加       |
| `LIST_EXTEND`         | 列表扩展       |

## 五、实战解读示例

### 示例 1：理解变量赋值

```
def example():
    x = 10
    y = x + 5
    return y
```

字节码解读：

```
  2           0 LOAD_CONST               1 (10)    # 将常量 10 压入栈
              2 STORE_FAST               0 (x)     # 栈顶值存入局部变量 x

  3           4 LOAD_FAST                0 (x)     # 读取局部变量 x，压入栈
              6 LOAD_CONST               2 (5)     # 将常量 5 压入栈
              8 BINARY_ADD                         # 弹出栈顶两值相加，结果压栈
             10 STORE_FAST               1 (y)     # 栈顶值存入局部变量 y

  4          12 LOAD_FAST                1 (y)     # 读取局部变量 y
             14 RETURN_VALUE                       # 返回栈顶值
```

**栈的变化过程**（以第 3 行为例）：

```
LOAD_FAST x  →  栈: [10]
LOAD_CONST 5 →  栈: [10, 5]
BINARY_ADD   →  栈: [15]
STORE_FAST y →  栈: []
```

### 示例 2：理解条件判断

```
def check(n):
    if n > 0:
        return "positive"
    else:
        return "non-positive"
  2           0 LOAD_FAST                0 (n)
              2 LOAD_CONST               1 (0)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE       12         # 如果为假，跳转到偏移量 12

  3           8 LOAD_CONST               2 ('positive')
             10 RETURN_VALUE

  5     >>   12 LOAD_CONST               3 ('non-positive')
             14 RETURN_VALUE
```

注意 `>>` 标记表示这是一个跳转目标。

### 示例 3：理解 for 循环

```
def total(items):
    s = 0
    for item in items:
        s += item
    return s
  2           0 LOAD_CONST               1 (0)
              2 STORE_FAST               1 (s)

  3           4 LOAD_GLOBAL              0 (range)
              6 LOAD_FAST                0 (items)
              8 GET_ITER
        >>   10 FOR_ITER                16 (to 28)  # 获取下一个元素，迭代结束则跳到 28
             12 STORE_FAST               2 (item)

  4          14 LOAD_FAST                1 (s)
             16 LOAD_FAST                2 (item)
             18 INPLACE_ADD                          # s += item（原地加法）
             20 STORE_FAST               1 (s)
             22 JUMP_ABSOLUTE           10           # 跳回 FOR_ITER 继续循环

  5     >>   28 LOAD_FAST                1 (s)
             30 RETURN_VALUE
```

### 示例 4：理解列表推导式

```
def squares(n):
    return [x**2 for x in range(n)]
```

列表推导式在字节码中会被编译为一个**内部函数**（代码对象），这解释了为什么列表推导式有自己的局部作用域。

## 六、进阶技巧

### 1. 查看代码对象的内部结构

```
def func(a, b):
    c = a + b
    return c * 2

code = func.__code__
print(f"参数数量: {code.co_argcount}")
print(f"局部变量: {code.co_varnames}")
print(f"常量: {code.co_consts}")
print(f"名称: {code.co_names}")
print(f"自由变量: {code.co_freevars}")
print(f"字节码: {list(code.co_code)}")
```

### 2. 使用 `dis.Bytecode` 进行编程式分析

```
import dis

def analyze_function(func):
    bytecode = dis.Bytecode(func)
    instructions = list(bytecode)
    
    print(f"函数: {func.__name__}")
    print(f"总指令数: {len(instructions)}")
    print(f"使用的操作码: {set(i.opname for i in instructions)}")
    
    # 统计操作码出现频率
    from collections import Counter
    op_counts = Counter(i.opname for i in instructions)
    print(f"\n操作码频率:")
    for op, count in op_counts.most_common():
        print(f"  {op:<25s}: {count}")
```

### 3. 不同 Python 版本间的差异

Python 字节码在不同版本间会发生变化，例如：



| 特性     | Python 3.10     | Python 3.11        | Python 3.12     |
| -------- | --------------- | ------------------ | --------------- |
| 函数调用 | `CALL_FUNCTION` | `PRECALL` + `CALL` | `CALL`（优化）  |
| 异常处理 | `SETUP_FINALLY` | `PUSH_EXC_INFO`    | `PUSH_EXC_INFO` |
| 行号追踪 | 每条指令        | 内联缓存           | 更精确的偏移表  |

Python 3.11 引入了 **specializing adaptive interpreter**，字节码中会出现 `CACHE` 指令和自适应优化指令（如 `LOAD_GLOBAL_ADAPTIVE`）。

### 4. 查看完整的操作码列表

```
import opcode

print(f"操作码总数: {len(opcode.opmap)}")
print("\n所有操作码:")
for name, code in sorted(opcode.opmap.items(), key=lambda x: x[1]):
    print(f"  {code:3d}  {name}")
```

## 七、学习路径建议

1. **入门**：用 `dis.dis()` 反汇编你写的简单函数，对照源码逐行理解
2. **基础**：掌握栈式虚拟机的工作原理，学会在脑中模拟栈的变化
3. **进阶**：研究控制流（循环、条件、异常处理）的字节码实现
4. **深入**：了解不同 Python 版本字节码的变化，特别是 3.11+ 的自适应优化
5. **实战**：通过字节码分析性能瓶颈，理解为什么某些写法更快

### 推荐资源

- **官方文档**：[Python `dis` 模块文档](https://docs.python.org/3/library/dis.html)
- **源码**：`Python/ceval.c` 是 CPython 字节码解释器的核心实现
- **书籍**：《CPython Internals》by Anthony Shaw 深入讲解了 CPython 内部机制

理解字节码就像理解一门新的低级语言，但它是读懂 Python 运行机制的钥匙。建议从简单的函数开始，逐步过渡到复杂结构，在实践中积累经验。

# 分割线

# Python 字节码完全教程 —— 从零开始读懂 Python 的"底层语言"

> 本教程面向 Python 初学者和中级开发者，无需编译原理或虚拟机背景知识，带你一步步理解 Python 字节码的原理、查看方法和实际应用。

---

## 目录

- [第一章：什么是 Python 字节码？](#第一章什么是-python-字节码)
- [第二章：为什么需要学习字节码？](#第二章为什么需要学习字节码)
- [第三章：Python 代码的执行流程](#第三章python-代码的执行流程)
- [第四章：如何查看字节码？](#第四章如何查看字节码)
- [第五章：字节码基础概念](#第五章字节码基础概念)
- [第六章：常见字节码指令详解](#第六章常见字节码指令详解)
- [第七章：实战分析 —— 从代码到字节码](#第七章实战分析--从代码到字节码)
- [第八章：函数与字节码](#第八章函数与字节码)
- [第九章：类与字节码](#第九章类与字节码)
- [第十章：控制流与字节码](#第十章控制流与字节码)
- [第十一章：推导式与字节码](#第十一章推导式与字节码)
- [第十二章：Python 3.11+ 的字节码变化](#第十二章python-311-的字节码变化)
- [第十三章：手写字节码 —— 进阶玩法](#第十三章手写字节码--进阶玩法)
- [第十四章：字节码与性能优化](#第十四章字节码与性能优化)
- [第十五章：常见问题与学习资源](#第十五章常见问题与学习资源)

---

## 第一章：什么是 Python 字节码？

### 1.1 一个通俗的比喻

想象你写了一封中文信（Python 源代码），但邮递员只懂英文。你需要一个翻译官先把中文翻译成一种"中间语言"（字节码），然后邮递员再根据这种中间语言去执行任务。

在 Python 的世界里：

| 角色         | 对应概念                    | 说明                   |
| ------------ | --------------------------- | ---------------------- |
| 你写的中文信 | `.py` 源代码                | 人类可读的 Python 代码 |
| 翻译官       | Python 编译器（`compiler`） | 把源代码翻译成字节码   |
| 中间语言     | 字节码（Bytecode）          | 一种低级指令格式       |
| 邮递员       | Python 虚拟机（PVM）        | 逐条执行字节码指令     |

### 1.2 字节码到底是什么？

字节码是 Python 源代码编译后产生的一种**低级指令序列**。每条指令由两部分组成：

- **操作码（Opcode）**：表示要执行什么操作，比如加载变量、做加法、调用函数等
- **操作数（Argument）**：操作码需要的额外数据，比如变量名、常量索引等

字节码不是机器码（CPU 直接执行的指令），它是由 Python 虚拟机（PVM）来解释执行的。这就是为什么 Python 被称为"解释型语言"——虽然它有编译步骤，但编译的产物是字节码，还需要虚拟机来解释执行。

### 1.3 字节码长什么样？

来看一个最简单的例子：

```python
# 源代码
a = 1
```

用 Python 的 `dis` 模块查看它的字节码（后面会详细讲怎么用）：

```
  1           0 LOAD_CONST               1 (1)
              2 STORE_NAME              0 (a)
```

这两行字节码的意思是：

1. `LOAD_CONST 1` —— 把常量 `1` 加载到栈上
2. `STORE_NAME 0 (a)` —— 把栈顶的值存到名字为 `a` 的变量中

就这么简单！字节码本质上就是一系列这样的指令，Python 虚拟机会从上到下依次执行它们。

---

## 第二章：为什么需要学习字节码？

### 2.1 理解 Python 的运行机制

学习字节码能让你真正理解 Python 代码是怎么被执行的。当你写 `x = x + 1` 时，Python 内部到底做了什么？字节码会告诉你答案。这种"知其然更知其所以然"的理解，能让你从"会用 Python"提升到"懂 Python"。

### 2.2 调试疑难问题

有些 Python 行为在源代码层面看起来很奇怪，但通过查看字节码就能一目了然。比如：

- 为什么 `a += b` 和 `a = a + b` 有时候行为不同？（涉及可变对象和 `__iadd__` 方法）
- 为什么 `is` 和 `==` 对小整数结果一样，对大整数却不同？（涉及小整数缓存机制）
- 为什么列表推导式比 `for` 循环快？（字节码层面有专门的优化指令）

### 2.3 性能优化

通过分析字节码，你可以发现代码中隐藏的性能问题。比如：

- 不必要的属性查找（多次调用 `obj.attr` 而不是缓存到局部变量）
- 循环中重复创建对象
- 可以用更高效的内建函数替代的复杂逻辑

### 2.4 深入学习 Python 的基础

如果你想深入理解 Python（比如阅读 CPython 源码、编写 C 扩展、或者研究 Python 的安全机制），字节码知识是必不可少的。它是连接高层 Python 代码和底层 C 实现的桥梁。

### 2.5 面试加分项

在高级 Python 开发岗位的面试中，字节码相关知识经常被用来考察候选人对 Python 的理解深度。能够解释字节码，说明你不仅仅是在"用"Python，而是真正"理解"了 Python。

---

## 第三章：Python 代码的执行流程

### 3.1 完整的执行链路

当你运行一个 Python 程序时，实际上经历了以下几个步骤：

```
源代码 (.py 文件)
    ↓  [词法分析 & 语法分析]
抽象语法树 (AST)
    ↓  [编译]
字节码 (.pyc 文件)
    ↓  [解释执行]
运行结果
```

让我们用一个具体的例子来走一遍这个流程：

```python
# hello.py
print("Hello, World!")
```

**第一步：词法分析（Lexical Analysis）**

Python 解析器把源代码拆分成一个个"词法单元"（Token）。对于上面的代码，会产生类似这样的 Token 序列：

```
NAME: 'print'
LPAREN: '('
STRING: 'Hello, World!'
RPAREN: ')'
NEWLINE: '\n'
ENDMARKER: ''
```

**第二步：语法分析（Syntax Analysis）**

解析器根据 Python 的语法规则，把 Token 序列组织成一棵"抽象语法树"（AST）。你可以用 `ast` 模块查看：

```python
import ast
tree = ast.parse('print("Hello, World!")')
print(ast.dump(tree, indent=2))
```

输出大致如下：

```
Module(body=[
  Expr(value=[
    Call(func=Name(id='print', ctx=Load()),
         args=[Constant(value='Hello, World!')],
         keywords=[])
  ])
])
```

**第三步：编译（Compilation）**

Python 编译器把 AST 编译成字节码。字节码会被存储在 `.pyc` 文件中（位于 `__pycache__` 目录下），这样下次运行同一个脚本时就不需要重新编译了。

**第四步：解释执行（Interpretation）**

Python 虚拟机（PVM）逐条读取字节码指令并执行，最终产生运行结果。

### 3.2 .pyc 文件是什么？

当你第一次 `import` 一个模块时，Python 会在 `__pycache__` 目录下生成一个 `.pyc` 文件。这个文件包含了编译后的字节码，以及一些元数据（如 Python 版本号、时间戳等）。

```
my_module.py          # 源代码
__pycache__/
  my_module.cpython-311.pyc   # 编译后的字节码
```

`.pyc` 文件的作用是**加速启动**——Python 不需要每次都重新编译源代码。但请注意，`.pyc` 文件不是加密的，任何人都可以用工具反编译它来查看字节码甚至还原部分源代码。

### 3.3 交互式模式下的字节码

在 Python 交互式解释器（REPL）中，每一行输入都会经历上述完整的编译和执行流程。这就是为什么交互式模式比运行脚本文件稍慢的原因——每次输入都需要重新编译。

---

## 第四章：如何查看字节码？

### 4.1 使用 dis 模块（最常用）

Python 标准库中的 `dis` 模块是查看字节码的官方工具。`dis` 是 "disassembler"（反汇编器）的缩写。

#### 方法一：在命令行中使用

```bash
python -m dis your_script.py
```

例如，创建一个文件 `test.py`：

```python
x = 10
y = 20
z = x + y
```

然后运行：

```bash
python -m dis test.py
```

#### 方法二：在 Python 代码中使用

```python
import dis

def my_function():
    x = 10
    y = 20
    z = x + y
    return z

dis.dis(my_function)
```

#### 方法三：查看一段代码字符串的字节码

```python
import dis

code = """
x = 10
y = 20
z = x + y
"""
dis.dis(code)
```

### 4.2 理解 dis 的输出格式

让我们来看一个完整的 `dis` 输出：

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

输出：

```
  2           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD               0 (None)
              6 RETURN_VALUE
```

每一行的含义：

| 列     | 含义                                     | 示例                         |
| ------ | ---------------------------------------- | ---------------------------- |
| 第一列 | 源代码行号                               | `2` 表示第 2 行              |
| 第二列 | 字节码偏移量（指令在字节码序列中的位置） | `0`, `2`, `4`, `6`           |
| 第三列 | 操作码名称                               | `LOAD_FAST`, `BINARY_ADD` 等 |
| 第四列 | 操作数（数字）                           | `0`, `1` 等                  |
| 第五列 | 操作数的可读表示（括号内）               | `(a)`, `(b)` 等              |

### 4.3 其他有用的 dis 函数

```python
import dis

# 查看字节码的详细信息（包括操作码编号）
dis.disco(my_function)

# 获取字节码指令列表（返回列表，方便程序化处理）
bytecode = dis.get_instructions(my_function)
for instr in bytecode:
    print(f"{instr.opname:20s} {instr.argrepr}")

# 查看所有操作码的说明
help(dis.opmap)    # 操作码名称 -> 编号的映射
help(dis.opname)   # 编号 -> 操作码名称的映射
```

### 4.4 使用 code 对象

每个 Python 函数都有一个 `__code__` 属性，它包含了编译后的代码对象：

```python
def greet(name):
    return f"Hello, {name}"

code = greet.__code__
print(code.co_varnames)    # ('name',)
print(code.co_consts)      # (None, 'Hello, ')
print(code.co_name)        # 'greet'
print(code.co_argcount)    # 1
```

常用的 `code` 对象属性：

| 属性           | 说明             |
| -------------- | ---------------- |
| `co_argcount`  | 参数个数         |
| `co_varnames`  | 局部变量名元组   |
| `co_names`     | 全局名称元组     |
| `co_consts`    | 常量元组         |
| `co_code`      | 原始字节码字符串 |
| `co_stacksize` | 需要的栈空间大小 |

---

## 第五章：字节码基础概念

### 5.1 栈式虚拟机

Python 虚拟机是一个**基于栈的虚拟机**（Stack-based VM）。这意味着大部分操作都是通过一个"栈"（Stack）来完成的。

栈是一种"后进先出"（LIFO）的数据结构，就像一叠盘子：

- 放盘子只能放在最上面（入栈 / Push）
- 拿盘子只能从最上面拿（出栈 / Pop）

Python 虚拟机在执行字节码时，维护着一个运行时栈。大部分指令的操作模式是：

1. 从栈顶弹出需要的值（0 个、1 个或 2 个）
2. 执行操作
3. 把结果压回栈顶

### 5.2 用一个例子理解栈操作

来看 `2 + 3` 的字节码执行过程：

```python
import dis
dis.dis("2 + 3")
```

输出：

```
  1           0 LOAD_CONST               1 (2)
              2 LOAD_CONST               2 (3)
              4 BINARY_ADD               0 (None)
              6 POP_TOP                  0 (None)
```

逐步执行过程：

```
步骤 0: LOAD_CONST 2
  栈: [2]                    ← 把常量 2 压入栈

步骤 2: LOAD_CONST 3
  栈: [2, 3]                 ← 把常量 3 压入栈

步骤 4: BINARY_ADD
  栈: [5]                    ← 弹出 2 和 3，相加，把结果 5 压入栈

步骤 6: POP_TOP
  栈: []                     ← 弹出栈顶的 5（因为没有赋值给变量，结果被丢弃）
```

### 5.3 帧对象（Frame Object）

每次调用一个函数时，Python 都会创建一个"帧对象"（Frame）。帧对象包含了函数执行所需的所有信息：

- **代码对象**（Code Object）：函数编译后的字节码
- **局部变量表**（Locals）：函数内的局部变量
- **全局变量表**（Globals）：模块级别的全局变量
- **运行时栈**（Stack）：用于计算的栈
- **指令指针**（Instruction Pointer）：当前执行到哪条指令
- **上一帧**（Previous Frame）：调用者的帧（形成调用链）

你可以用 `sys._getframe()` 获取当前帧对象：

```python
import sys

def show_frame():
    frame = sys._getframe()
    print(f"函数名: {frame.f_code.co_name}")
    print(f"局部变量: {frame.f_locals}")
    print(f"行号: {frame.f_lineno}")

show_frame()
# 输出:
# 函数名: show_frame
# 局部变量: {'frame': <frame object at 0x...>}
# 行号: 4
```

### 5.4 名字空间（Namespace）

Python 有多个名字空间，字节码中有不同的指令来访问不同的名字空间：

| 名字空间 | 说明                     | 对应的字节码指令                      |
| -------- | ------------------------ | ------------------------------------- |
| 局部变量 | 函数内部的变量           | `LOAD_FAST`, `STORE_FAST`             |
| 全局变量 | 模块级别的变量           | `LOAD_GLOBAL`, `STORE_GLOBAL`         |
| 自由变量 | 嵌套函数中引用的外层变量 | `LOAD_DEREF`, `STORE_DEREF`           |
| 内建名称 | `len`, `print` 等        | `LOAD_GLOBAL`（在内建命名空间中查找） |

`LOAD_FAST` 比 `LOAD_GLOBAL` 快，因为它直接通过索引访问局部变量数组，而 `LOAD_GLOBAL` 需要在字典中查找变量名。这就是为什么把频繁访问的全局变量缓存到局部变量可以提升性能。

---

## 第六章：常见字节码指令详解

本章按照功能分类，详细介绍最常用的字节码指令。每个指令都会给出操作码名称、功能说明和示例。

### 6.1 加载指令（Load Instructions）

加载指令负责把各种值"压入"栈顶。

#### LOAD_CONST（加载常量）

把一个常量值压入栈顶。常量包括数字、字符串、`None`、`True`、`False` 等。

```python
import dis
dis.dis("x = 42")
```

```
  1           0 LOAD_CONST               0 (42)
              2 STORE_NAME               0 (x)
```

#### LOAD_NAME（加载全局/局部名称）

在当前作用域中查找一个名字，把对应的值压入栈顶。通常用于模块级别的代码。

```python
import dis
dis.dis("print(x)")
```

```
  1           0 PUSH_NULL
              2 LOAD_NAME                0 (print)
              4 LOAD_NAME                1 (x)
              6 CALL                     1
             10 POP_TOP
```

#### LOAD_FAST（加载局部变量）

通过索引快速加载局部变量。这是最快的变量加载方式，因为局部变量存储在一个固定大小的数组中，通过索引直接访问。

```python
import dis

def foo():
    x = 1
    return x

dis.dis(foo)
```

```
  2           0 LOAD_CONST               1 (1)
              2 STORE_FAST               0 (x)

  3           4 LOAD_FAST                0 (x)
              6 RETURN_VALUE
```

#### LOAD_GLOBAL（加载全局变量）

从全局命名空间加载变量。在 Python 3.11 中，这个指令的行为有所变化（后面会讲）。

```python
import dis

def foo():
    return len([1, 2, 3])

dis.dis(foo)
```

```
  2           0 LOAD_GLOBAL              1 (len)
              2 LOAD_CONST               1 ((1, 2, 3))
              4 CALL                     1
              6 RETURN_VALUE
```

#### LOAD_ATTR（加载属性）

加载对象的属性值，等价于源代码中的 `obj.attr`。

```python
import dis
dis.dis("obj.name")
```

```
  1           0 LOAD_NAME                0 (obj)
              2 LOAD_ATTR                1 (name)
              4 POP_TOP
```

### 6.2 存储指令（Store Instructions）

存储指令负责把栈顶的值"弹出"并存储到某个位置。

#### STORE_NAME（存储到名称）

把栈顶的值存储到一个名字中。通常用于模块级别的变量赋值。

```python
import dis
dis.dis("x = 10")
```

```
  1           0 LOAD_CONST               0 (10)
              2 STORE_NAME               0 (x)
```

#### STORE_FAST（存储到局部变量）

把栈顶的值存储到局部变量中。这是最快的存储方式。

```python
import dis

def foo():
    x = 10

dis.dis(foo)
```

```
  2           0 LOAD_CONST               1 (10)
              2 STORE_FAST               0 (x)
```

#### STORE_SUBSCR（存储到下标）

把值存储到容器（列表、字典等）的指定下标位置。等价于 `obj[key] = value`。

```python
import dis
dis.dis("d['key'] = 42")
```

```
  1           0 LOAD_NAME                0 (d)
              2 LOAD_CONST               0 ('key')
              4 LOAD_CONST               1 (42)
              6 STORE_SUBSCR
```

注意 `STORE_SUBSCR` 的操作数顺序：它从栈上弹出三个值，依次是 `value`（栈顶）、`key`（次栈顶）、`obj`（第三层）。所以压栈顺序是先 `obj`，再 `key`，最后 `value`。

#### STORE_ATTR（存储到属性）

把值存储到对象的属性中。等价于 `obj.attr = value`。

```python
import dis
dis.dis("obj.name = 'Alice'")
```

```
  1           0 LOAD_NAME                0 (obj)
              2 LOAD_CONST               0 ('Alice')
              4 STORE_ATTR               1 (name)
```

### 6.3 运算指令（Arithmetic Instructions）

运算指令从栈上弹出操作数，执行运算，然后把结果压回栈顶。

#### BINARY_ADD（加法）

弹出栈顶两个值，执行加法运算，把结果压回栈顶。

```python
import dis
dis.dis("a + b")
```

```
  1           0 LOAD_NAME                0 (a)
              2 LOAD_NAME                1 (b)
              4 BINARY_ADD               0 (None)
              6 POP_TOP
```

#### BINARY_SUBTRACT（减法）

弹出栈顶两个值，执行减法运算。

```python
import dis
dis.dis("a - b")
```

```
  1           0 LOAD_NAME                0 (a)
              2 LOAD_NAME                1 (b)
              4 BINARY_SUBTRACT          0 (None)
              6 POP_TOP
```

#### 其他二元运算指令

| 指令                  | 对应运算      | 示例     |
| --------------------- | ------------- | -------- |
| `BINARY_MULTIPLY`     | `*` 乘法      | `a * b`  |
| `BINARY_TRUE_DIVIDE`  | `/` 真除法    | `a / b`  |
| `BINARY_FLOOR_DIVIDE` | `//` 地板除   | `a // b` |
| `BINARY_MODULO`       | `%` 取模      | `a % b`  |
| `BINARY_POWER`        | `**` 幂运算   | `a ** b` |
| `BINARY_SUBSCR`       | `[]` 下标访问 | `a[b]`   |
| `BINARY_LSHIFT`       | `<<` 左移     | `a << b` |
| `BINARY_RSHIFT`       | `>>` 右移     | `a >> b` |
| `BINARY_AND`          | `&` 按位与    | `a & b`  |
| `BINARY_OR`           | `\|` 按位或   | `a \| b` |
| `BINARY_XOR`          | `^` 按位异或  | `a ^ b`  |

#### UNARY_NEGATIVE / UNARY_NOT / UNARY_INVERT（一元运算）

| 指令             | 对应运算       | 示例    |
| ---------------- | -------------- | ------- |
| `UNARY_NEGATIVE` | `-x` 取负      | `-a`    |
| `UNARY_NOT`      | `not x` 逻辑非 | `not a` |
| `UNARY_INVERT`   | `~x` 按位取反  | `~a`    |

### 6.4 比较指令（Comparison Instructions）

#### COMPARE_OP（比较运算）

弹出栈顶两个值，执行比较运算，把布尔结果压回栈顶。

```python
import dis
dis.dis("a > b")
```

```
  1           0 LOAD_NAME                0 (a)
              2 LOAD_NAME                1 (b)
              4 COMPARE_OP               4 (>)
              6 POP_TOP
```

`COMPARE_OP` 的操作数是一个比较运算符的编号，常见的有：

| 编号 | 运算符            |
| ---- | ----------------- |
| 2    | `==`              |
| 3    | `!=`              |
| 4    | `<`               |
| 5    | `<=`              |
| 6    | `>`               |
| 7    | `>=`              |
| 8    | `in`              |
| 9    | `not in`          |
| 10   | `is`              |
| 11   | `is not`          |
| 12   | `exception match` |

### 6.5 函数调用指令（Call Instructions）

#### CALL（调用函数）

在 Python 3.11+ 中，`CALL` 替代了之前的 `CALL_FUNCTION`、`CALL_METHOD` 等指令，统一了函数调用。

```python
import dis
dis.dis("print('hello')")
```

```
  1           0 PUSH_NULL
              2 LOAD_NAME                0 (print)
              4 LOAD_CONST               0 ('hello')
              6 CALL                     1
             10 POP_TOP
```

`CALL` 的操作数表示参数的个数。在上面的例子中，`CALL 1` 表示有 1 个参数。

#### PRECALL（预调用，Python 3.11）

在 Python 3.11 中，函数调用被拆分为 `PRECALL` + `CALL` 两步。`PRECALL` 负责做一些准备工作（比如检查参数），`CALL` 负责实际的调用。在 Python 3.12 中，`PRECALL` 被移除了。

### 6.6 构建容器指令（Build Instructions）

#### BUILD_LIST（构建列表）

从栈上弹出指定数量的元素，构建一个列表。

```python
import dis
dis.dis("[1, 2, 3]")
```

```
  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 LOAD_CONST               2 (3)
              6 BUILD_LIST               3
              8 POP_TOP
```

`BUILD_LIST 3` 表示从栈上弹出 3 个元素，构建一个列表。

#### BUILD_TUPLE（构建元组）

类似 `BUILD_LIST`，但构建的是元组。

#### BUILD_MAP（构建字典）

从栈上弹出键值对，构建一个字典。

```python
import dis
dis.dis("{'a': 1, 'b': 2}")
```

```
  1           0 LOAD_CONST               0 ('a')
              2 LOAD_CONST               1 (1)
              4 LOAD_CONST               2 ('b')
              6 LOAD_CONST               3 (2)
              8 BUILD_MAP                2
             10 POP_TOP
```

`BUILD_MAP 2` 表示从栈上弹出 2 对键值对。

#### BUILD_SET（构建集合）

从栈上弹出指定数量的元素，构建一个集合。

### 6.7 控制流指令（Control Flow Instructions）

#### JUMP_FORWARD（向前跳转）

无条件向前跳转指定的字节数。

#### JUMP_ABSOLUTE（绝对跳转）

跳转到指定的字节码偏移量位置。

#### POP_JUMP_IF_TRUE / POP_JUMP_IF_FALSE

弹出栈顶的值，如果为 True/False 则跳转。

#### JUMP_IF_TRUE_OR_POP / JUMP_IF_FALSE_OR_POP

检查栈顶的值，如果为 True/False 则跳转，否则弹出该值。注意这个指令不会弹出值（除非条件不满足）。

---

## 第七章：实战分析 —— 从代码到字节码

### 7.1 变量赋值

```python
# 源代码
x = 10
y = "hello"
z = x
```

```python
import dis
dis.dis("""
x = 10
y = "hello"
z = x
""")
```

字节码：

```
  2           0 LOAD_CONST               0 (10)
              2 STORE_NAME               0 (x)

  3           4 LOAD_CONST               1 ('hello')
              6 STORE_NAME               1 (y)

  4           8 LOAD_NAME                0 (x)
             10 STORE_NAME               2 (z)
```

**逐行解读：**

1. `LOAD_CONST 0 (10)`：把常量 `10` 压入栈。操作数 `0` 是常量表中的索引。
2. `STORE_NAME 0 (x)`：弹出栈顶的 `10`，存储到名字 `x` 中。
3. `LOAD_CONST 1 ('hello')`：把常量 `'hello'` 压入栈。
4. `STORE_NAME 1 (y)`：弹出栈顶的 `'hello'`，存储到名字 `y` 中。
5. `LOAD_NAME 0 (x)`：查找名字 `x`，把它的值（`10`）压入栈。
6. `STORE_NAME 2 (z)`：弹出栈顶的 `10`，存储到名字 `z` 中。

### 7.2 多重赋值

```python
a, b = 1, 2
```

字节码：

```
  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 BUILD_TUPLE              2
              6 UNPACK_SEQUENCE          2
              8 STORE_NAME               0 (a)
             10 STORE_NAME               1 (b)
```

**解读：** Python 先构建一个元组 `(1, 2)`，然后用 `UNPACK_SEQUENCE` 把它拆包成两个值，分别存储到 `a` 和 `b` 中。这就是为什么你可以写 `a, b = b, a` 来交换变量——它实际上是先构建元组 `(b, a)`，再拆包。

### 7.3 交换变量的字节码

```python
a, b = b, a
```

字节码：

```
  1           0 LOAD_NAME                0 (b)
              2 LOAD_NAME                1 (a)
              4 BUILD_TUPLE              2
              6 UNPACK_SEQUENCE          2
              8 STORE_NAME               0 (a)
             10 STORE_NAME               1 (b)
```

注意：先加载 `b` 的值，再加载 `a` 的值，构建元组 `(b的值, a的值)`，然后拆包赋值。这就是为什么不需要临时变量就能交换——元组构建时已经保存了原始值。

### 7.4 链式比较

```python
1 < 2 < 3
```

字节码：

```
  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 DUP_TOP
              6 ROT_TWO
              8 COMPARE_OP               2 (<)
             10 JUMP_IF_FALSE_OR_POP    18 (to 18)
             12 LOAD_CONST               2 (3)
             14 COMPARE_OP               2 (<)
             16 RETURN_VALUE
        >>   18 LOAD_CONST               3 (False)
             20 RETURN_VALUE
```

**解读：** 链式比较 `1 < 2 < 3` 被编译为 `1 < 2 and 2 < 3`，但有一个优化——`2` 只被加载一次（通过 `DUP_TOP` 复制），而不是加载两次。这就是为什么 `1 < 2 < 3` 不会调用两次 `2` 的 `__lt__` 方法。

### 7.5 字符串格式化

```python
f"Hello, {name}!"
```

字节码：

```
  1           0 LOAD_CONST               0 ('Hello, ')
              2 LOAD_NAME                0 (name)
              4 FORMAT_SIMPLE
              6 LOAD_CONST               1 ('!')
              8 BUILD_STRING             3
             10 RETURN_VALUE
```

**解读：** f-string 被编译为一系列的字符串拼接操作。先加载各个部分，然后用 `BUILD_STRING` 把它们拼接在一起。

---

## 第八章：函数与字节码

### 8.1 函数定义

```python
def greet(name):
    return f"Hello, {name}"
```

字节码：

```
  1           0 LOAD_CONST               0 (<code object greet at 0x...>)
              2 LOAD_CONST               1 ('greet')
              4 MAKE_FUNCTION            0
              6 STORE_NAME               0 (greet)
```

**解读：** 定义函数时，Python 实际上是：

1. 加载函数的代码对象（编译好的字节码）
2. 加载函数名
3. 用 `MAKE_FUNCTION` 创建函数对象
4. 把函数对象存储到名字 `greet` 中

函数体本身的字节码是独立的，可以通过 `dis.dis(greet)` 查看：

```
  2           0 LOAD_FAST                0 (name)
              2 LOAD_CONST               1 ('Hello, ')
              4 FORMAT_SIMPLE
              6 LOAD_CONST               2 ('!')
              8 BUILD_STRING             3
             10 RETURN_VALUE
```

### 8.2 函数参数

```python
def add(a, b, c=0):
    return a + b + c
```

字节码（函数体）：

```
  2           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD               0 (None)
              6 LOAD_FAST                2 (c)
              8 BINARY_ADD               0 (None)
             10 RETURN_VALUE
```

注意：参数 `a`、`b`、`c` 在函数内部就是局部变量，通过 `LOAD_FAST` 访问。默认值 `c=0` 在函数定义时处理，不在函数体的字节码中。

### 8.3 *args 和 **kwargs

```python
def func(*args, **kwargs):
    pass
```

函数体的字节码中，`args` 和 `kwargs` 就是普通的局部变量，它们的值在函数调用时由虚拟机自动填充。

### 8.4 闭包

```python
def outer():
    x = 10
    def inner():
        return x
    return inner
```

查看 `inner` 函数的字节码：

```
  4           0 LOAD_DEREF               0 (x)
              2 RETURN_VALUE
```

注意这里用的是 `LOAD_DEREF` 而不是 `LOAD_FAST`。`LOAD_DEREF` 用于访问"自由变量"（Free Variable），即来自外层函数作用域的变量。

`outer` 函数的字节码：

```
  2           0 LOAD_CONST               1 (10)
              2 STORE_DEREF              0 (x)

  3           4 LOAD_CLOSURE             0 (x)
              6 BUILD_TUPLE              1
              8 LOAD_CONST               2 (<code object inner at 0x...>)
             10 LOAD_CONST               3 ('inner')
             12 MAKE_FUNCTION            8 (closure)
             14 STORE_FAST               0 (inner)

  5          16 LOAD_FAST                0 (inner)
             18 RETURN_VALUE
```

关键点：

- `STORE_DEREF`：把值存储到闭包单元（Cell）中，而不是普通的局部变量
- `LOAD_CLOSURE`：加载闭包单元的引用
- `MAKE_FUNCTION` 的操作数 `8` 表示这个函数有闭包

### 8.5 装饰器

```python
@decorator
def func():
    pass
```

等价于：

```python
func = decorator(func)
```

字节码：

```
  1           0 LOAD_NAME                0 (decorator)
              2 LOAD_CONST               0 (<code object func at 0x...>)
              4 LOAD_CONST               1 ('func')
              6 MAKE_FUNCTION            0
              8 CALL                     1
             10 STORE_NAME               2 (func)
```

可以看到，装饰器的本质就是：先创建函数对象，然后立即调用装饰器函数，把返回值重新赋值给原来的函数名。

---

## 第九章：类与字节码

### 9.1 基本类定义

```python
class Dog:
    species = "Canine"

    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says Woof!"
```

字节码：

```
  1           0 LOAD_BUILD_CLASS
              2 LOAD_CONST               0 (<code object Dog at 0x...>)
              4 LOAD_CONST               1 ('Dog')
              6 MAKE_FUNCTION            0
              8 LOAD_CONST               1 ('Dog')
             10 CALL_FUNCTION            2
             12 STORE_NAME               0 (Dog)
```

**解读：**

1. `LOAD_BUILD_CLASS`：加载内建的 `__build_class__` 函数
2. 加载类的代码对象和类名
3. `MAKE_FUNCTION`：创建类体函数
4. `CALL_FUNCTION 2`：调用 `__build_class__`，传入类体函数和类名
5. `STORE_NAME`：把创建的类对象存储到名字 `Dog` 中

### 9.2 方法调用

```python
dog = Dog("Buddy")
dog.bark()
```

字节码：

```
  1           0 LOAD_NAME                0 (Dog)
              2 LOAD_CONST               0 ('Buddy')
              4 CALL                     1
              6 STORE_NAME               1 (dog)

  2           8 LOAD_NAME                1 (dog)
             10 LOAD_METHOD              0 (bark)
             12 CALL                     0
             14 POP_TOP
```

注意 `LOAD_METHOD` 指令——它专门用于加载方法。在 Python 3.7+ 中，`LOAD_METHOD` + `CALL` 的组合比旧的 `LOAD_ATTR` + `CALL` 更高效，因为它避免了为方法调用创建绑定方法的临时对象。

### 9.3 属性访问

```python
dog.name
```

字节码：

```
  1           0 LOAD_NAME                0 (dog)
              2 LOAD_ATTR                1 (name)
              4 POP_TOP
```

`LOAD_ATTR` 会触发 Python 的描述符协议（Descriptor Protocol）。如果属性是一个数据描述符（定义了 `__get__` 和 `__set__`），则调用 `__get__` 方法。

---

## 第十章：控制流与字节码

### 10.1 if-else 语句

```python
x = 10
if x > 5:
    y = "big"
else:
    y = "small"
```

字节码：

```
  1           0 LOAD_CONST               0 (10)
              2 STORE_NAME               0 (x)

  2           4 LOAD_NAME                0 (x)
              6 LOAD_CONST               1 (5)
              8 COMPARE_OP               4 (>)
             10 POP_JUMP_IF_FALSE       22 (to 22)

  3          12 LOAD_CONST               2 ('big')
             14 STORE_NAME               1 (y)
             16 JUMP_FORWARD             6 (to 24)

  5     >>   22 LOAD_CONST               3 ('small')
             24 STORE_NAME               1 (y)
```

**解读：**

1. 先执行比较 `x > 5`
2. `POP_JUMP_IF_FALSE 22`：如果结果为 False，跳转到偏移量 22（即 `else` 分支）
3. 如果为 True，执行 `y = "big"`，然后 `JUMP_FORWARD 6` 跳过 `else` 分支
4. `>>` 标记表示这是一个跳转目标

### 10.2 for 循环

```python
total = 0
for i in range(5):
    total += i
```

字节码：

```
  1           0 LOAD_CONST               0 (0)
              2 STORE_NAME               0 (total)

  2           4 LOAD_NAME                1 (range)
              6 LOAD_CONST               1 (5)
              8 CALL                     1
             10 GET_ITER
        >>   12 FOR_ITER                10 (to 24)
             14 STORE_NAME               2 (i)

  3          16 LOAD_NAME                0 (total)
             18 LOAD_NAME                2 (i)
             20 BINARY_ADD               0 (None)
             22 STORE_NAME               0 (total)
             24 JUMP_BACKWARD            6 (to 12)

        >>   26 END_FOR
```

**解读：**

1. `GET_ITER`：从 `range(5)` 获取迭代器
2. `FOR_ITER`：尝试从迭代器获取下一个元素。如果成功，压入栈顶并继续；如果迭代结束，跳转到 `END_FOR`
3. 循环体执行完毕后，`JUMP_BACKWARD` 跳回 `FOR_ITER` 继续下一次迭代
4. `END_FOR`：清理迭代器

### 10.3 while 循环

```python
x = 0
while x < 5:
    x += 1
```

字节码：

```
  1           0 LOAD_CONST               0 (0)
              2 STORE_NAME               0 (x)

  2     >>    4 LOAD_NAME                0 (x)
              6 LOAD_CONST               1 (5)
              8 COMPARE_OP               0 (<)
             10 POP_JUMP_IF_FALSE       22 (to 22)

  3          12 LOAD_NAME                0 (x)
             14 LOAD_CONST               2 (1)
             16 BINARY_ADD               0 (None)
             18 STORE_NAME               0 (x)
             20 JUMP_BACKWARD            8 (to 4)

        >>   22 LOAD_CONST               3 (None)
             24 RETURN_VALUE
```

**解读：** `while` 循环比 `for` 循环简单——它就是一个条件判断 + 向后跳转。每次循环开始时检查条件，如果为 False 则跳出循环。

### 10.4 try-except

```python
try:
    x = 1 / 0
except ZeroDivisionError:
    x = 0
```

字节码：

```
  1           0 SETUP_FINALLY           12 (to 14)

  2           2 LOAD_CONST               0 (1)
              4 LOAD_CONST               1 (0)
              6 BINARY_TRUE_DIVIDE       0 (None)
              8 STORE_NAME               0 (x)
             10 POP_BLOCK
             12 JUMP_FORWARD            14 (to 28)

  3     >>   14 PUSH_EXC_INFO
             16 LOAD_GLOBAL              1 (ZeroDivisionError)
             18 CHECK_EXC_MATCH
             20 POP_JUMP_IF_FALSE       26 (to 26)
             22 POP_TOP

  4          24 POP_TOP
             26 POP_EXCEPT

  4     >>   28 LOAD_CONST               2 (0)
             30 STORE_NAME               0 (x)
             32 LOAD_CONST               3 (None)
             34 RETURN_VALUE
```

**解读：**

1. `SETUP_FINALLY`：设置异常处理入口。如果后面的代码抛出异常，跳转到偏移量 14
2. 正常执行路径：执行除法，存储结果，`POP_BLOCK` 清理块，`JUMP_FORWARD` 跳过异常处理
3. 异常处理路径：`PUSH_EXC_INFO` 把异常信息压入栈，`CHECK_EXC_MATCH` 检查异常类型是否匹配

### 10.5 with 语句

```python
with open("file.txt") as f:
    content = f.read()
```

`with` 语句的字节码涉及 `SETUP_WITH`（或 `WITH_EXCEPT_START`）等指令，本质上是 `try-finally` 的语法糖。它确保在代码块执行完毕后（无论是否发生异常），都会调用上下文管理器的 `__exit__` 方法。

---

## 第十一章：推导式与字节码

### 11.1 列表推导式

```python
[x * 2 for x in range(5)]
```

字节码：

```
  1           0 LOAD_CONST               0 (<code object <listcomp> at 0x...>)
              2 LOAD_CONST               1 ('<listcomp>')
              4 MAKE_FUNCTION            0
              6 LOAD_NAME                0 (range)
              8 LOAD_CONST               2 (5)
             10 CALL                     1
             12 GET_ITER
             14 CALL                     1
             16 RETURN_VALUE
```

**关键发现：** 列表推导式被编译为一个**独立的函数**（`<listcomp>`）！这就是为什么列表推导式中的变量不会泄漏到外部作用域（在 Python 3 中）。

查看推导式内部的字节码：

```python
dis.dis("[x * 2 for x in range(5)]")
```

内部字节码：

```
  1           0 BUILD_LIST               0
              2 LOAD_FAST                0 (.0)
        >>    4 FOR_ITER                12 (to 18)
              6 STORE_FAST               1 (x)
              8 LOAD_FAST                1 (x)
             10 LOAD_CONST               1 (2)
             12 BINARY_MULTIPLY          0 (None)
             14 LIST_APPEND              2
             16 JUMP_BACKWARD            6 (to 4)
        >>   18 END_FOR
             20 RETURN_VALUE
```

**解读：**

1. `BUILD_LIST 0`：创建一个空列表
2. `FOR_ITER`：迭代
3. `LIST_APPEND`：把结果追加到列表中（注意这个指令直接操作列表，不需要从栈上弹出列表）

### 11.2 字典推导式

```python
{x: x * 2 for x in range(5)}
```

字典推导式同样被编译为独立函数，内部使用 `BUILD_MAP` + `MAP_ADD` 指令。

### 11.3 集合推导式

```python
{x * 2 for x in range(5)}
```

集合推导式使用 `BUILD_SET` + `SET_ADD` 指令。

### 11.4 生成器表达式

```python
(x * 2 for x in range(5))
```

生成器表达式也编译为独立函数，但它返回的是一个生成器对象，而不是立即计算所有值。内部使用 `YIELD_VALUE` 指令来暂停和恢复执行。

### 11.5 为什么列表推导式比 for 循环快？

通过字节码可以清楚地看到原因：

1. **列表推导式使用专用的 `LIST_APPEND` 指令**，它直接操作内部列表，不需要通过 `list.append()` 方法查找
2. **推导式编译为独立函数**，使用 `LOAD_FAST` 访问迭代变量，比 `LOAD_ATTR` 更快
3. **减少了字节码指令数量**，循环的设置和清理更简洁

---

## 第十二章：Python 3.11+ 的字节码变化

Python 3.11 是一个重要的里程碑版本，它引入了"适配字节码"（Adaptive Bytecode）机制，大幅提升了执行速度（官方宣称 CPython 3.11 比 3.10 快 25%）。

### 12.1 内联缓存（Inline Caching）

Python 3.11 引入了内联缓存机制。当一条字节码指令被多次执行时，虚拟机会"记住"之前的操作结果，下次执行时可以直接使用缓存的结果，跳过一些耗时的查找步骤。

例如，`LOAD_GLOBAL` 指令在第一次执行时需要在全局字典中查找变量名，但后续执行可以直接使用缓存的偏移量。

### 12.2 适配指令

Python 3.11 中，一些指令有两个版本：

| 基础指令      | 适配指令                                            | 说明                       |
| ------------- | --------------------------------------------------- | -------------------------- |
| `LOAD_GLOBAL` | `LOAD_GLOBAL_MODULE` / `LOAD_GLOBAL_BUILTIN`        | 根据变量来源选择更快的版本 |
| `BINARY_OP`   | `BINARY_OP_ADD_INT` / `BINARY_OP_MULTIPLY_FLOAT` 等 | 根据操作数类型选择特化版本 |
| `COMPARE_OP`  | `COMPARE_OP_INT` / `COMPARE_OP_FLOAT` 等            | 根据比较类型选择特化版本   |
| `LOAD_ATTR`   | `LOAD_ATTR_MODULE` / `LOAD_ATTR_SLOT` 等            | 根据属性类型选择特化版本   |
| `CALL`        | `CALL_PY_EXACT_ARGS` 等                             | 根据调用模式选择特化版本   |

当虚拟机发现一条指令总是以相同的方式执行时（比如 `LOAD_GLOBAL` 总是找到模块级变量），它会自动把基础指令替换为适配指令。这个过程对程序员完全透明。

### 12.3 ZERO / ONE / POP_TOP 链

Python 3.12 进一步优化了常见模式：

- `LOAD_CONST 0` → `LOAD_CONST__LOAD_FAST`（把加载常量和加载变量合并为一条指令）
- `LOAD_CONST 1` → 类似的优化
- `COMPARE_OP` 返回 `True/False` 后紧跟 `POP_JUMP` → 合并为一条指令

### 12.4 查看适配字节码

使用 `dis` 模块时，默认不会显示适配指令。要查看它们，可以设置环境变量：

```bash
PYTHONNODEBUGRANGES=1 python -m dis your_script.py
```

或者使用 `dis.Bytecode` 对象：

```python
import dis

code = compile("x + y", "<string>", "eval")
for instr in dis.get_instructions(code, adaptive=True):
    print(instr)
```

### 12.5 更快的异常处理

Python 3.11 重写了异常处理机制，使用"零成本异常处理"（Zero-cost Exception Handling）。在没有异常发生时，`try` 块几乎没有任何额外开销。这是通过在异常表中记录信息，而不是在字节码中插入 `SETUP_FINALLY` 指令来实现的。

---

## 第十三章：手写字节码 —— 进阶玩法

### 13.1 使用 types.CodeType 创建代码对象

你可以手动创建代码对象并执行它。这是一个非常高级的玩法，但能帮助你深入理解字节码。

```python
import types

# 创建一个简单的代码对象：计算 2 + 3
# 字节码指令（以字节为单位）：
# LOAD_CONST 0    -> 100 (LOAD_CONST) + 0 (参数)
# LOAD_CONST 1    -> 100 (LOAD_CONST) + 1 (参数)
# BINARY_ADD      -> 23 (BINARY_ADD)
# RETURN_VALUE    -> 83 (RETURN_VALUE)

code_obj = types.CodeType(
    co_argcount=0,         # 参数个数
    co_posonlyargcount=0,  # 仅位置参数个数
    co_kwonlyargcount=0,   # 仅关键字参数个数
    co_nlocals=0,          # 局部变量个数
    co_stacksize=2,        # 需要的栈大小
    co_flags=64,           # 标志位 (CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE)
    co_code=b'\x64\x00\x64\x01\x17\x00S',  # 字节码
    co_consts=(2, 3),      # 常量表
    co_names=(),           # 名称表
    co_varnames=(),        # 局部变量名
    co_filename='<string>',
    co_name='my_code',
    co_firstlineno=1,
    co_lnotab=b'',         # 行号表
    co_freevars=(),
    co_cellvars=(),
)

# 执行代码对象
result = eval(code_obj)
print(result)  # 输出: 5
```

> **注意：** `types.CodeType` 的构造函数参数在不同 Python 版本中可能不同。上面的代码适用于 Python 3.8+。在 Python 3.11+ 中，参数有所变化，请参考对应版本的文档。

### 13.2 使用 bytecode 库（第三方）

`bytecode` 是一个第三方库，提供了更友好的 API 来操作字节码：

```bash
pip install bytecode
```

```python
from bytecode import Bytecode, Instr

# 创建字节码序列
bytecode = Bytecode([
    Instr("LOAD_CONST", 2),
    Instr("LOAD_CONST", 3),
    Instr("BINARY_ADD"),
    Instr("RETURN_VALUE"),
])

# 转换为代码对象
code = bytecode.to_code()

# 执行
print(eval(code))  # 输出: 5
```

### 13.3 修改现有函数的字节码

你可以读取一个函数的字节码，修改它，然后创建一个新的函数：

```python
from bytecode import Bytecode, Instr

def original():
    return 1 + 2

# 读取字节码
bytecode = Bytecode.from_code(original.__code__)

# 修改：把 2 改成 3
for instr in bytecode:
    if isinstance(instr, Instr) and instr.arg == 2:
        instr.arg = 3

# 创建新函数
new_code = bytecode.to_code()
original.__code__ = new_code

print(original())  # 输出: 4
```

> **警告：** 手动修改字节码是非常危险的操作，可能导致 Python 崩溃或产生不可预测的行为。请只在学习和实验环境中使用。

---

## 第十四章：字节码与性能优化

### 14.1 局部变量比全局变量快

```python
import dis

# 全局变量访问
dis.dis("len(data)")
```

```
  1           0 PUSH_NULL
              2 LOAD_NAME                0 (len)
              4 LOAD_NAME                1 (data)
              6 CALL                     1
              8 POP_TOP
```

```python
# 局部变量访问
def foo():
    data = [1, 2, 3]
    return len(data)

dis.dis(foo)
```

```
  2           0 LOAD_CONST               1 ((1, 2, 3))
              2 STORE_FAST               0 (data)

  3           4 LOAD_GLOBAL              1 (len + NULL)
              6 LOAD_FAST                0 (data)
              8 CALL                     1
             10 RETURN_VALUE
```

可以看到，`LOAD_FAST`（局部变量）比 `LOAD_NAME`（全局变量）更简洁。在循环中频繁访问全局变量时，把它缓存到局部变量可以提升性能：

```python
# 慢
def slow():
    for i in range(10000):
        len(data)  # 每次都要查找全局 len

# 快
def fast():
    _len = len    # 缓存到局部变量
    for i in range(10000):
        _len(data)  # LOAD_FAST 比 LOAD_GLOBAL 快
```

### 14.2 属性查找的代价

每次访问 `obj.attr` 都会执行 `LOAD_ATTR` 指令，这涉及字典查找。在循环中，你可以把属性缓存到局部变量：

```python
# 慢
def slow():
    for item in data:
        result.append(process(item))

# 快
def fast():
    append = result.append
    proc = process
    for item in data:
        append(proc(item))
```

### 14.3 用内建函数替代循环

```python
# 慢：显式循环
result = []
for x in data:
    if x > 0:
        result.append(x * 2)

# 快：列表推导式
result = [x * 2 for x in data if x > 0]

# 更快：用 map/filter（在某些情况下）
result = list(map(lambda x: x * 2, filter(lambda x: x > 0, data)))
```

列表推导式的字节码比显式循环更紧凑，且使用了专用的 `LIST_APPEND` 指令。

### 14.4 字符串拼接优化

```python
# 慢：循环中拼接字符串
s = ""
for x in items:
    s += x  # 每次都创建新字符串

# 快：使用 join
s = "".join(items)
```

`"".join(items)` 的字节码只有一条 `CALL` 指令，而循环拼接涉及多次 `BINARY_ADD` 和 `STORE_FAST`。

### 14.5 使用 dis 分析性能瓶颈

当你不确定两段代码哪个更快时，可以用 `dis` 查看它们的字节码，比较指令数量和类型：

```python
import dis

# 方案 A
code_a = compile("[x for x in range(100)]", "<string>", "eval")

# 方案 B
code_b = compile("list(range(100))", "<string>", "eval")

# 比较字节码长度
print(f"方案 A 字节码长度: {len(code_a.co_code)}")
print(f"方案 B 字节码长度: {len(code_b.co_code)}")
```

---

## 第十五章：常见问题与学习资源

### 15.1 常见问题

**Q: 字节码和机器码有什么区别？**

A: 字节码是 Python 虚拟机理解的指令，不是 CPU 直接执行的指令。CPU 执行的是机器码（由 C 编译器编译 CPython 源码生成）。Python 虚拟机本身是用 C 写的，它读取字节码并调用相应的 C 函数来执行操作。

**Q: 不同 Python 版本的字节码一样吗？**

A: 不一样。每个 Python 版本都可能引入新的操作码或修改现有操作码的行为。这就是为什么 `.pyc` 文件包含了 Python 版本号——不同版本的 `.pyc` 文件不兼容。

**Q: 字节码可以被反编译成源代码吗？**

A: 可以部分还原。工具如 `uncompyle6`、`decompyle3` 可以把字节码反编译为可读的 Python 代码，但通常无法完全还原原始代码（注释会丢失，变量名可能不同）。

**Q: 学习字节码对日常工作有帮助吗？**

A: 对于大多数日常开发工作，你不需要直接查看字节码。但在调试性能问题、理解 Python 内部机制、或者编写高级工具时，字节码知识非常有用。

**Q: Python 字节码是跨平台的吗？**

A: 是的。同一份 `.pyc` 文件可以在不同操作系统上运行（只要 Python 版本相同）。因为字节码是由 Python 虚拟机执行的，不依赖具体的 CPU 指令集。

### 15.2 学习资源

**官方文档：**

- [Python `dis` 模块文档](https://docs.python.org/3/library/dis.html) —— 最权威的参考
- [CPython 源码中的字节码定义](https://github.com/python/cpython/blob/main/Include/opcode.h) —— 所有操作码的编号和名称

**推荐书籍：**

- 《CPython Internals》 by Anthony Shaw —— 深入介绍 CPython 内部实现
- 《Python Cookbook》 —— 包含一些实用的字节码技巧

**在线工具：**

- [Python Bytecode Visualizer](https://pyvisualise.com/) —— 可视化字节码执行过程
- [Online Python Disassembler](https://python bytecode visualizer) —— 在线查看字节码

**进阶阅读：**

- [PEP 659](https://peps.python.org/pep-0659/) —— Python 3.11 适配字节码（Specializing Adaptive Interpreter）
- [PEP 578](https://peps.python.org/pep-0578/) —— Python Runtime Audit Hooks
- [The Architecture of Open Source Applications: CPython](https://aosabook.org/en/500L/a-python-interpreter-written-in-python.html) —— 用 Python 写的 Python 解释器

**实践建议：**

1. 从简单的表达式开始，用 `dis.dis()` 查看它们的字节码
2. 尝试预测一段代码的字节码，然后用 `dis` 验证
3. 对比不同写法的字节码，理解哪种写法更高效
4. 阅读 CPython 源码中 `Python/ceval.c` 文件，了解每个操作码的 C 实现
5. 尝试用 `bytecode` 库手写简单的字节码程序

---

## 附录：常用字节码指令速查表

### 加载与存储

| 指令             | 说明                  | 栈变化            |
| ---------------- | --------------------- | ----------------- |
| `LOAD_CONST i`   | 加载常量表第 i 个常量 | → value           |
| `LOAD_NAME i`    | 加载名字              | → value           |
| `LOAD_FAST i`    | 加载局部变量          | → value           |
| `LOAD_GLOBAL i`  | 加载全局变量          | → value           |
| `LOAD_DEREF i`   | 加载闭包变量          | → value           |
| `LOAD_ATTR i`    | 加载属性              | obj → value       |
| `STORE_NAME i`   | 存储到名字            | value →           |
| `STORE_FAST i`   | 存储到局部变量        | value →           |
| `STORE_GLOBAL i` | 存储到全局变量        | value →           |
| `STORE_DEREF i`  | 存储到闭包变量        | value →           |
| `STORE_ATTR i`   | 存储到属性            | value, obj →      |
| `STORE_SUBSCR`   | 存储到下标            | value, key, obj → |

### 运算

| 指令                  | 说明     | 栈变化              |
| --------------------- | -------- | ------------------- |
| `BINARY_ADD`          | 加法     | a, b → a+b          |
| `BINARY_SUBTRACT`     | 减法     | a, b → a-b          |
| `BINARY_MULTIPLY`     | 乘法     | a, b → a*b          |
| `BINARY_TRUE_DIVIDE`  | 真除法   | a, b → a/b          |
| `BINARY_FLOOR_DIVIDE` | 地板除   | a, b → a//b         |
| `BINARY_MODULO`       | 取模     | a, b → a%b          |
| `BINARY_POWER`        | 幂运算   | a, b → a**b         |
| `BINARY_SUBSCR`       | 下标访问 | obj, key → obj[key] |
| `UNARY_NEGATIVE`      | 取负     | a → -a              |
| `UNARY_NOT`           | 逻辑非   | a → not a           |
| `UNARY_INVERT`        | 按位取反 | a → ~a              |

### 比较

| 指令            | 说明     | 栈变化      |
| --------------- | -------- | ----------- |
| `COMPARE_OP op` | 比较运算 | a, b → bool |

### 控制流

| 指令                    | 说明                        |
| ----------------------- | --------------------------- |
| `JUMP_FORWARD n`        | 向前跳转 n 字节             |
| `JUMP_BACKWARD n`       | 向后跳转 n 字节             |
| `JUMP_ABSOLUTE pos`     | 跳转到绝对位置              |
| `POP_JUMP_IF_FALSE pos` | 弹出并判断，为 False 则跳转 |
| `POP_JUMP_IF_TRUE pos`  | 弹出并判断，为 True 则跳转  |
| `FOR_ITER`              | 迭代器获取下一个元素        |
| `RETURN_VALUE`          | 返回栈顶的值                |

### 函数

| 指令                  | 说明                 |
| --------------------- | -------------------- |
| `CALL n`              | 调用函数（n 个参数） |
| `MAKE_FUNCTION flags` | 创建函数对象         |
| `RETURN_VALUE`        | 从函数返回           |

### 容器

| 指令            | 说明       | 栈变化                     |
| --------------- | ---------- | -------------------------- |
| `BUILD_LIST n`  | 构建列表   | v1, v2, ..., vn → list     |
| `BUILD_TUPLE n` | 构建元组   | v1, v2, ..., vn → tuple    |
| `BUILD_MAP n`   | 构建字典   | k1, v1, ..., kn, vn → dict |
| `BUILD_SET n`   | 构建集合   | v1, v2, ..., vn → set      |
| `LIST_APPEND i` | 追加到列表 | value →                    |
| `SET_ADD i`     | 添加到集合 | value →                    |
| `MAP_ADD i`     | 添加到字典 | value, key →               |

### 其他

| 指令               | 说明             |
| ------------------ | ---------------- |
| `POP_TOP`          | 弹出栈顶值并丢弃 |
| `DUP_TOP`          | 复制栈顶值       |
| `ROT_TWO`          | 交换栈顶两个值   |
| `GET_ITER`         | 获取迭代器       |
| `NOP`              | 空操作           |
| `IMPORT_NAME`      | 导入模块         |
| `LOAD_BUILD_CLASS` | 加载类构建函数   |







