---
tags:
  - type/tutorial
  - lang/Python
  - lange/Python/libs
  - domain/computer-science
  - domain/computer-science/basic
  - topic/objprint
  - status/draft
  - source/glm
aliases:
  - objprint
description: 学习Python库 objprint
datetime: " 2026-09-05 12:09:64 周六"
author: wephiles
rating:
introduction:
motto: 有志者，事竟成。破釜沉舟，百二秦关终属楚。苦心人，天不负。卧薪尝胆，三千越甲可吞吴。
---
[TOC]

<h1 style="text-align: center;">objprint</h1>

---

# 1. `objprint` 是什么

`objprint`：是一个轻量级的 Python 第三方库，用来把对象以 **人类可读的树状结构** 打印出来，主要服务于调试场景。

直接 `print()` 一个自定义对象，通常只能看到毫无信息量的：

```
<__main__.Player object at 0x7f9a6a4b4d30>
```

而 `objprint` 会把对象的属性一层层展开：

```
<Player object at 0x7f9a6a4b4d30>
  name = 'Alice'
  age = 30
  positions = [
    <Position object at 0x7f9a6a4b4d60>
      x = 0
      y = 0,
    <Position object at 0x7f9a6a4b4d90>
      x = 1
      y = 2
  ]
```

作者是 `Tian Gao（GitHub: gaogaotiantian）`，`CPython` 核心开发者、微软 Python 工具团队成员。这个库核心代码只有一个文件、几百行，质量很高，也适合拿来阅读学习。

# 2. 安装

```python
pip install objprint
```

# 3. 基本用法

## 3.1 `op()/objprint()`

核心函数。

```python
from objprint import op   # op 是 objprint 的简写别名

op(player)                          # 直接打印
op(player, depth=2, indent=4)       # 打印时可传配置
```

它不仅能打印自定义对象，列表、字典、以及它们的任意嵌套组合都能处理。

```
from objprint import op


class Demo:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.formatter = f"{self.name.title()} {self.age} years old."


obj = Demo("Jack", 20)

op(obj)
```

```
<Demo 0x25c5b4f9160
  .age = 20,
  .formatter = 'Jack 20 years old.',
  .name = 'Jack'
>
```

## 3.2 `objstr`

只要字符串，不要直接打印。

```
from objprint import op, objstr


class Demo:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.formatter = f"{self.name.title()} {self.age} years old."


obj = Demo("Jack", 20)

s = objstr(obj)
print(s)  # 或者写进日志，拼接到保存信息中
```

```
<Demo 0x1786d789160
  .age = 20,
  .formatter = 'Jack 20 years old.',
  .name = 'Jack'
>
```

## 3.3 `install`

让内置 `print` 也能打印对象。注意：此代码会报错。

```
from objprint import install, uninstall

install()
print(player)    # 自动用 objprint 格式输出
uninstall()      # 恢复默认行为
```

## 3.4 其他进阶 API

还有 `add_print_function`（让某个类的实例直接支持被 `print()`）、`config_class`（针对特定类定制输出格式）等，用法见 `GitHub README`。

# 4. 常见配置参数

| 参数              | 作用                                   |
| ----------------- | -------------------------------------- |
| `indent`          | 缩进宽度，默认 2                       |
| `depth`           | 最大递归深度                           |
| `elements`        | 只打印指定属性                         |
| `skip`            | 跳过指定属性                           |
| `color`           | 彩色输出                               |
| `methods`         | 是否打印方法（默认不打印）             |
| `max_line_length` | 单行最大长度                           |
| `line_numbers`    | 显示行号                               |
| `unsorted`        | 保持属性原始顺序（默认按字母序排列）   |
| `str`             | 用 `str(obj)` 展示对象，而不是展开属性 |

```
op(player, elements=["name", "positions"])  # 只看关心的属性
op(player, skip=["password"])               # 跳过敏感/冗余属性
op(player, color=True, max_line_length=60)  # 终端里彩色输出
```

# 5. 使用过程中可能出现的坑

1. **读取属性是"真执行"**：`objprint` 通过 `getattr` 取属性，`property` 和 `__getattr__` 里的代码会被真正运行。如果 property 里有 IO、网络请求或可能抛异常的逻辑，打印对象时就会触发。`op(obj)` 报错时，先怀疑 `property`。
2. **`ORM` 懒加载对象要小心**：打印 `SQLAlchemy / Django` 的模型实例时，访问未加载的属性可能触发数据库查询，甚至抛 `DetachedInstanceError`。这类对象建议先转成 `dict` 再打印。
3. **输出体积可能爆炸**：大列表、深嵌套、循环引用的结构会让输出失控。记得用 `depth`、`elements`、`skip`、`max_line_length` 控制。
4. **敏感信息全量暴露**：`_password`、`token` 之类的私有属性也会被打印。往日志、截图、聊天工具里贴输出前注意脱敏。
5. **彩色输出写文件会乱码**：`color=True` 会带 ANSI 转义码，重定向到文件或非终端环境会看到 `\x1b[36m` 之类的乱码。
6. **install() 是全局改动**：会改变整个进程里 `print` 的行为。个人脚本里很爽，但在团队代码或库中慎用，用完记得 `uninstall()`。
7. **默认行为细节**：属性默认按字母序排序（不是定义顺序）；方法默认不打印；对没有 `__dict__` 的对象（内置类型、C 扩展等）能展示的信息有限。
8. **定位是调试工具**：有运行时开销和潜在副作用，不要写进生产代码或正式日志。生产环境用结构化日志（`JSON` 等）更合适。

**顺便对比**：标准库 `pprint` 适合纯 `dict/list`；`rich.inspect(obj)` 功能更强、自带美化；`IPython` 里可以用 `obj??` 内省。`objprint` 的独特价值在于专攻"自定义对象属性树"，轻量、格式清爽，`Jupyter` 里也很好用。

# 6. 学习资源

1. **`GitHub` 仓库（主要文档，`README` 有中英文，非常详细）**：https://github.com/gaogaotiantian/objprint
2. **`PyPI` 页面**（版本与兼容性信息）：https://pypi.org/project/objprint/
3. **读源码**：核心就一个 `objprint/objprint.py`，是学习 Python 内省机制（`__dict__`、`vars()`、`inspect` 模块、`__repr__` 协议）的绝佳范例。
4. **Issues 区**：作者回复很积极，很多边角用法和问题都能搜到答案。
5. **延伸阅读**：作者的其他项目如 `pystack`；以及 Python 官方文档中的数据模型章节（理解 `__repr__` / `__str__`）。

