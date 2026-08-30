---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-09 17:08:20 周日"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">第一章: Python 数据模型</h1>

Python 的质量保障得益于一致性。使用 Python 一段时间之后，便可以根据自己掌握的知识，正确地猜出新功能的作用。

然而，如果你在接触 Python 之前有其他面向对象语言的经验，就会觉得奇怪：为什么获取容器大小不使用 `collection.len()`，而是使用 `len(collection)`？这一点表面上看确实奇怪，而且只是众多奇怪行为的冰山一角，不过知道背后的原因之后，你会发现这才真正符合“Python 风格”。一切的一切都埋藏在 Python 数据模型中。我们平常自己创建对象时就要使用这个 `API`，确保使用最地道的语言功能。

可以把 Python 视为一个框架，而数据模型就是对框架的描述，规范语言自身各个组成部分的接口，确立序列、函数、迭代器、协程、类、上下文管理器等部分的行为。

使用框架要花大量时间编写方法，交给框架调用。利用 Python 数据模型构建新类也是如此。Python 解释器调用特殊方法来执行基本对象操作，通常由特殊句法触发。特殊方法的名称前后两端都有双下划线。例如，在 `obj[key]` 句法背后提供支持的是特殊方法`__getitem__`。为了求解 `my_collection[key]`，Python 解释器要调用 `my_collection.__getitem__(key)`。

- 如果想让对象支持以下基本的语言结构并与其交互，就需要实现特殊
方法：

- 容器；
- 属性存取；
- 迭代（包括使用 `async for` 的异步迭代）；

- 运算符重载；

- 函数和方法调用；

- 字符串表示形式和格式化；

- 使用 await 的异步编程；

- 对象创建和析构；

- 使用 with 或 async with 语句管理上下文。

特殊方法用行话说叫作魔术方法（magic method）。需要把一个特殊方法（例如 `__getitem__`）说出来时，应该怎么表达呢？我一般说“`dunder-getitem`”，这是跟著名作家和教师 `SteveHolden` 学的。“`dunder`”表示“前后双下划线”。因此，特殊方法也叫“双下划线方法”。《Python 语言参考手册》中的第 2 章“词法分析”警告道：“任何时候，若不遵守文档明确说明的方式使用__*__ 名称，一切后果自负。”

# 1. 一摞 Python 风格的纸牌

示例 1-1 虽然简单，却展示了实现 `__getitem__` 和 `__len__` 两个特殊方法之后得到的强大功能。

**示例 1-1：**

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
```

![image-20260809174149534](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260809174150874.png)

首先用 `collections.namedtuple` 构建了一个简单的类，表示单张纸牌。使用 `namedtuple` 构建只有属性而没有自定义方法的类对象，例如数据库中的一条记录。这个示例中使用这个类表示一摞牌中的各张纸牌，如以下控制台会话所示。

```python
>>> beer_card = Card(7, 'diamonds')
>>> print(beer_card)
Card(rank=7, suit='diamonds')
```

但是，这个示例的重点是简短精炼的 `FrenchDeck` 类。首先，与标准的 Python 容器一样，一摞牌响应 `len()` 函数，返回一摞牌有多少张。

```python
>>> deck = FrenchDeck()
>>> len(deck)
52
```

得益于 `__getitem__ `方法，我们可以轻松地从这摞牌中抽取某一张，比如说第一张或最后一张。

```python
>>> deck[0]
>>> Card(rank='2', suit='spades')
>>> deck[-1]
>>> Card(rank='A', suit='hearts')
```

如果想随机选一张牌，需要定义一个方法吗？不需要，因为 `Python` 已经提供了从序列中随机获取一项的函数，即 `random.choice`。我们可以在一摞牌上使用这个函数。

```python
>>> from random import choice
>>> choice(deck)
>>> Card(rank='3', suit='clubs')
>>> choice(deck)
>>> Card(rank='10', suit='hearts')
>>> choice(deck)
>>> Card(rank='10', suit='hearts')
```

可以看到，通过特殊方法利用 Python 数据模型，这样做有两个优点:

- 类的用户不需要记住标准操作的方法名称（“怎样获取项数？使用 `.size()`、`.length()`，还是其他方法？”）。
- 可以充分利用 Python 标准库，例如 `random.choice` 函数，无须重新发明轮子。

由于 `__getitem__` 方法把操作委托给 `self._cards` 的 [] 运算符，一摞牌自动支持切片（`slicing`）。下面展示如何从一摞新牌中抽取最上面三张，再从索引 12 位开始，跳过 13 张牌，只抽取 4 张 A。

```python
>>> deck[:3]
[Card(rank='2', suit='spades'), Card(rank='3', suit='spades'),
Card(rank='4', suit='spades')]
>>> deck[12::13]
[Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'),
Card(rank='A', suit='clubs'), Card(rank='A', suit='hearts')]
```

实现特殊方法 `__getitem__` 之后，这摞纸牌还可以迭代。

```python
>>> for card in deck: # doctest: +ELLIPSIS
... print(card)
Card(rank='2', suit='spades')
Card(rank='3', suit='spades')
Card(rank='4', suit='spades')
...
```

另外，也可以反向迭代这摞纸牌。

```python
>>> for card in reversed(deck): # doctest: +ELLIPSIS
... print(card)
Card(rank='A', suit='hearts')
Card(rank='K', suit='hearts')
Card(rank='Q', suit='hearts')
...
```

迭代往往是隐式的。如果一个容器没有实现 `__contains__` 方法，那么 in 运算符就会做一次顺序扫描。本例就是这样，`FrenchDeck` 类支持 in 运算符，因为该类可迭代。下面来试试。

```python
>>> Card('Q', 'hearts') in deck
True
>>> Card('7', 'beasts') in deck
False
```

那么排序呢？按照常规，牌面大小按点数（A 最大），以及黑桃（最大）、红心、方块、梅花（最小）的顺序排列。下面按照这个规则定义扑克牌排序函数，梅花 2 返回 0，黑桃 A 返回 51。

```python
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
# suit_values = {'spades': 3, 'hearts': 2, 'diamonds': 1, 'clubs': 0}
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
```

定义好 spades_high 函数后，现在按照牌面大小升序列出一副牌。

```python
>>> for card in sorted(deck, key=spades_high):# doctest: +ELLIPSIS
... print(card)
Card(rank='2', suit='clubs')
Card(rank='2', suit='diamonds')
Card(rank='2', suit='hearts')
... (46 cards omitted)
Card(rank='A', suit='diamonds')
Card(rank='A', suit='hearts')
Card(rank='A', suit='spades')
```

虽然 `FrenchDeck` 类隐式继承 `object` 类，但是前者的多数功能不是继承而来的，而是源自数据模型和组合模式。通过前面使用 r`andom.choice`、`reversed`和 `sorted` 的示例可以看出，实现`__len__` 和 `__getitem__` 两个特殊方法后，`FrenchDeck` 的行为就像标准的 Python 序列一样，受益于语言核心特性（例如迭代和切片）和标准库。`__len__` 和 `__getitem__` 的实现利用组合模式，把所有工作委托给一个 `list` 对象，即 `self._cards`。

问题：如何洗牌？

按照目前的设计，`FrenchDeck` 对象不能洗牌，因为它是不可变的：纸牌自身及其位置不能变化，除非违背封装原则，直接处理 `_cards` 属性。第 13 章将添加只有一行代码的 `__setitem__` 方法，解决这个问题。

# 2. 特殊方法是如何使用的

首先要明确一点，特殊方法供 Python 解释器调用，而不是你自己。也就是说，没有 `my_object.__len__()` 这种写法，正确的写法是 `len(my_object)`。如果 `my_object` 是用户定义的类的实例，Python 将调用你实现的 `__len__` 方法。

然而，处理内置类型时，例如 `list`、`str`、`bytearray `或 `NumPy` 数组等扩展，Python 解释器会抄个近路。Python 中可变长度容器的底层 C 语言实现中有一个结构体， 名为 `PyVarObject`。在这个结构体中，`ob_size` 字段保存着容器中的项数。如果 my_object 是某个内置类型的实例，则 `len(my_object)` 直接取 `ob_size` 字段的值，这比调用方法快很多。

很多时候，特殊方法是隐式调用的。例如，`for i in x:` 语句其实在背后调用 `iter(x)`，接着又调用 `x.__iter__()`（前提是有该方法）或 `x.__getitem__()`。在 `FrenchDeck` 示例中，调用的是后者。

我们在编写代码时一般不直接调用特殊方法，除非涉及大量元编程。即便如此，大部分时间也是实现特殊方法，很少显式调用。唯一例外的是 `__init__` 方法，为自定义的类实现 `__init__` 方法时经常直接调用它调取超类的初始化方法。如果需要调用特殊方法，则最好调用相应的内置函数，例如 `len`、`iter`、`str` 等。这些内置函数不仅调用对应的特殊方法，通常还提供额外服务，而且对于内置类型来说，速度比调用方法更快。17.3 节(**序列可以迭代的原因： `iter` 函数**)有一个示例。

接下来几节会说明特殊方法最重要的用途：

- 模拟数值类型；
- 对象的字符串表示形式；
- 对象的布尔值；
- 实现容器。

## 2.1 模拟数值类型

有几个特殊方法可以让用户对象响应 + 等运算符。第 16 章对此有详细探讨，这里只是借此再举一个简单的例子，说明特殊方法的用途。接下来将实现一个二维向量类，即数学和物理中使用的欧几里得向量（见图 1-1）。

内置的 `complex` 类型可用于表示二维向量，不过我们实现的类经过扩展可以表示 n 维向量，详见第 17 章。

![image-20260809181243138](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260809181244161.png)

为了给这个类设计 API，先写出模拟的控制台会话，作为 doctest。以下代码片段测试图 1-1 中的向量加法。

```python
>>> v1 = Vector(2, 4)
>>> v2 = Vector(2, 1)
>>> v1 + v2
Vector(4, 5)
```

注意，+ 运算符的结果是一个新 `Vector` 对象，在控制台中以友好的格式显示。

内置函数 abs 返回整数和浮点数的绝对值，以及复数的模。为了保持一致性，我们的 API 也使用 abs 函数计算向量的模。

```python
>>> v = Vector(3, 4)
>>> abs(v)
5.0
```

还可以实现 * 运算符，计算向量的标量积（即一个向量乘以一个数，得到一个方向相同、模为一定倍数的新向量）。

```python
>>> v * 3
Vector(9, 12)
>>> abs(v * 3)
15.0
```

示例 1-2 使用 `__repr__、__abs__、__add__ 和 __mul__` 等特殊方法为 `Vector` 类实现这几种运算。

**示例 1-2：**一个简单的二维向量类

```python
"""
vector2d.py：一个简单的类，演示一些特殊方法

只是演示，一些问题做简化处理。缺少错误处理，尤其是__add__和__mul__方法。

本书后文还会扩充这个示例。

加法::
>>> v1 = Vector(2, 4)
>>> v2 = Vector(2, 1)
>>> v1 + v2
Vector(4, 5)

绝对值::
>>> v = Vector(3, 4)
>>> abs(v)
5.0

标量积::
 >>> v * 3
Vector(9, 12)

>>> abs(v * 3)
15.0
"""

import math


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x} {self.y})'

    def __abs__(self):
        # return math.sqrt(self.x ** 2 + self.y ** 2)
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)


```

除了我们熟悉的 `__init__` 方法，这个类还实现了另外 5 个特殊方法。注意，这些方法在类内部，或者在前面的 `doctest` 中都没有直接调用。正如前文所说，多数特殊方法最常被 Python 解释器调用。

示例 1-2 实现了 + 和 * 两个运算符，展示了 `__add__` 和 `__mul__`方法的基本用法。这两个方法创建并返回一个新 `Vector` 实例，没有修改运算对象，只是读取 self 或 other。这是中缀运算符的预期行为，即创建新对象，不修改运算对象。这一点会在第 16 章详谈。

注意： 按照示例 1-2 中的实现，一个 `Vector` 对象可以乘以一个数，但是一个数不能乘以一个 `Vector` 对象，这违背了标量积的交换律。这个问题在第 16 章会使用特殊方法 `__rmul__` 解决。

接下来的几节讨论 Vector 类的其他特殊方法。

## 2.2 字符串表示形式

特殊方法 `__repr__` 供内置函数 `repr` 调用，获取对象的字符串表示形式。如未定义 `__repr__` 方法，`Vector` 实例在 Python 控制台中显示为 `<Vector object at 0x10e100070>` 形式。

交互式控制台和调试器在表达式求值结果上调用 `repr` 函数，处理方式与使用 % 运算符处理经典格式化方式中的 %r 占位符，以及使用 `str.format` 方法处理新字符串格式化句法中的 `!r` 转换字段一样。

注意，`Vector` 类 `__repr__` 方法中的 `f 字符串`使用 `!r` 以标准的表示形式显示属性。这样做比较好，因为 `Vector(1, 2)` 和 `Vector('1', '2')` 之间是有区别的，后者在这个示例中不可用，因为构造函数接受的参数是数值而不是字符串。

`__repr__` 方法返回的字符串应当没有歧义，如果可能，最好与源码保持一致，方便重新创建所表示的对象。鉴于此，我们才以类似构造函数的形式（例如 `Vector(3, 4)`）返回 `Vector` 对象的字符串表示形式。

与此形成对照的是，`__str__` 方法由内置函数 `str()` 调用，在背后供 `print` 函数使用，返回对终端用户友好的字符串。

有时，`__repr__` 方法返回的字符串足够友好，无须再定义`__str__` 方法，因为继承自 `object` 类的实现最终会调用 `__repr__` 方法。本书中有几个示例定义了 `__str__` 方法，例如示例 5-2。

如果你熟悉的编程语言使用 `toString` 方法，那么你可能习惯实现 `__str__` 方法而不是 `__repr__` 方法。在 Python中，如果必须二选一的话，请选择 `__repr__` 方法。

`Stack Overflow` 网站中有一个问题，`“What is the difference between __str__ and __repr__?”`，Python 专家 `Alex Martelli 和 Martijn Pieters` 对此做出了详尽解答。

## 2.3 自定义类型的布尔值

































