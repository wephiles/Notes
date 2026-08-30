---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-22 14:08:91 周六"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">builtin</h1>  

----
# 1. `sorted`

```python
data = [1, 5, 9, -3, 10, 0]  
  
x = sorted(data)  
  
print(x)
```

输出结果：

```plaintext
[-3, 0, 1, 5, 9, 10]
```

---

```python
data_info = {  
    'a': 1,  
    'd': 2,  
    'c': 3,  
    'b': 4,  
}  
  
x = sorted(data_info)  
y = sorted(data_info.keys())  
z = sorted(data_info.values())  
m = sorted(data_info.items())
n = sorted(data_info.items(), key=lambda x: x[1])  
  
print(x)  
print(y)  
print(z)  
print(m)
print(n)
```

输出结果：

```plaintext
['a', 'b', 'c', 'd']
['a', 'b', 'c', 'd']
[1, 2, 3, 4]
[('a', 1), ('b', 4), ('c', 3), ('d', 2)]
[('a', 1), ('d', 2), ('c', 3), ('b', 4)]
```

---

```python
a = (12, 5, 1, 0)  
print(sorted(a))
```

输出结果：

```plaintext
[0, 1, 5, 12]
```

# 2. `reduce`

`educe` 是一个**折叠函数**，它把一个**二元函数**（接受两个参数的函数）连续作用在一个可迭代对象上，把所有元素"累积"成**一个单一值**。

```python
from functools import reduce   # Python 3 中必须显式导入
```

历史背景：Python 2 中 `reduce` 是内置函数；Python 3 里被移到 `functools` 模块，因为大部分场景下它不如显式循环清晰。Guido 甚至一度想移除它，最终保留在 `functools` 中。

```
reduce(function, iterable[, initializer])
```

| 参数          | 说明                                                 |
| ------------- | ---------------------------------------------------- |
| `function`    | 二元函数 `f(累计值, 当前元素)`，返回值成为新的累计值 |
| `iterable`    | 任何可迭代对象（列表、元组、字符串、生成器…）        |
| `initializer` | 可选的初始值，作为累计的起点                         |

工作原理：

```
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        accumulator = next(it)      # 取第一个元素作为起点
    else:
        accumulator = initializer
    for element in it:
        accumulator = function(accumulator, element)
    return accumulator

```

```
# 阶乘/连乘
factorial = lambda n: reduce(lambda x, y: x * y, range(1, n + 1), 1)
factorial(5)  # 120
```

```python
# 找最大最小值
reduce(lambda a, b: a if a > b else b, [3, 7, 2, 9, 4])  # 9
```

```python
reduce(lambda a, b: a + b, [[1,2],[3,4],[5,6]])  # [1, 2, 3, 4, 5, 6]
```

```python
reduce(lambda a, b: {**a, **b}, [{"a":1}, {"b":2}, {"c":3}])
# {'a': 1, 'b': 2, 'c': 3}
```

```python
def flatten(a, b):
    if isinstance(b, list):
        return a + reduce(flatten, b, [])
    return a + [b]

reduce(flatten, [1, [2, [3, [4, 5]]]], [])  # [1, 2, 3, 4, 5]
```

```python
composed = reduce(lambda f, g: lambda x: f(g(x)), [double, add_one, square])
composed(3)  # double(add_one(square(3))) = double(add_one(9)) = 20
```

性能：

| 方式                | 耗时    | 相对速度 |
| ------------------- | ------- | -------- |
| `reduce` + `lambda` | 0.1035s | 最慢     |
| 普通 `for` 循环     | 0.0307s | 约 3.4×  |
| 内置 `sum()`        | 0.0070s | 约 15×   |

`reduce` + `lambda` 比**显式循环还慢**，因为每一步都有 Python 级函数调用开销。

**✅ 适合用 `reduce`：**

- 操作本身有天然的"折叠"语义（连乘、逻辑与/或、合并）；
- 想写出简洁的函数式一行代码；
- 有现成的二元函数可直接传入，例如 `reduce(operator.add, ...)`、`reduce(operator.mul, ...)`（用 `operator` 模块比 lambda 快）。

**❌ 不该用 `reduce`：**

- **求和 → 用 `sum()`**，求最大 → 用 `max()`，求长度 → 用 `len()`；
- 求字符串拼接 → 用 `''.join(...)`（`reduce` 版本是 O(n²)）；
- 逻辑判断所有/任一为真 → 用 `all()` / `any()`；
- 操作不够直观时——**可读性比"炫技"重要**。`reduce(lambda x, y: x + y, nums)` 远不如 `sum(nums)` 清晰。

**经验法则**：如果读者需要在脑中模拟 reduce 的折叠过程才能看懂，就换写成 for 循环。

| 函数             | 目标           | 输出                       |
| ---------------- | -------------- | -------------------------- |
| `map(f, seq)`    | 对每个元素变换 | **与输入等长**的可迭代对象 |
| `filter(f, seq)` | 筛选元素       | ≤ 输入长度的可迭代对象     |
| `reduce(f, seq)` | 折叠累积       | **单一值**                 |

总结：

- `reduce(二元函数, 可迭代对象, 初始值)` 把序列从左到右折叠成单个值；
- 无初始值时空序列会抛 `TypeError`，**建议总是提供 initializer**；
- 它在**连乘、合并、函数组合**等真正"折叠"语义的场景下最合适；
- 实测性能不如内置函数和普通循环，**能用 `sum`/`max`/`join`/`all` 就不要用 `reduce`**；
- 核心判断标准永远是：**代码是否一眼能看懂**。

# 3. `map`

## 3.1 `map` 是什么

`map` 是一个**映射函数**：把一个函数依次应用到可迭代对象的**每个元素**上，返回一个**惰性迭代器**。它的本质是"批量函数调用"。

```
map(function, iterable, ...)
# Python 3 中是内置函数，无需导入
```

与 `reduce` 的区别：`map` 保持**一对多结构**（N 个进、N 个出），`reduce` 是**折叠成单值**（N 个进、1 个出）。

## 3.2 语法与参数

| 参数       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| `function` | 任意可调用对象：内置函数、lambda、自定义函数、类构造器、方法 |
| `iterable` | 一个或多个可迭代对象，多个时按位置**并行配对**               |

**等价的伪代码实现**（单个序列时）：

```
def map(function, iterable):
    for element in iterable:
        yield function(element)    # 注意是 yield：惰性生成
```

## 3.3 核心特性①：惰性求值（这是最重要的认知）

`map` 返回的是一个**迭代器对象**，创建它时**函数一次都不会被调用**：

```
m = map(lambda x: x * 2, [1, 2, 3])
print(m)        # <map object at 0x7fbdffb3c910>  ← 不是列表！

def shout(x):
    print(f"   -> 此刻才调用 shout({x!r})")
    return x.upper()

m = map(shout, ['a', 'b', 'c'])
print("map 已创建，但上面什么都没打印")     # 函数零调用
print(next(m))   # 'A'  ← 只有取值时才真正调用 shout('a')
```

实测输出证实：`map 已创建` 之后没有任何函数调用发生，直到 `next()` 执行才打印第一条调用记录。

**惰性的价值**：

- 可以处理**无限序列**（已验证）：

```
from itertools import count, islice
squares = map(lambda x: x ** 2, count(1))   # 无限序列！
print(list(islice(squares, 5)))             # [1, 4, 9, 16, 25]，只算用到的
```

- **内存优势巨大**（实测 100 万元素）：

| 对象       | 内存占用                                 |
| ---------- | ---------------------------------------- |
| `map` 对象 | **48 字节**                              |
| 完整列表   | **8,448,728 字节**（还不算每个元素本身） |

处理大数据流时，`map` 不需要一次性把结果全部装进内存。

## 3.4 核心特性②：一次性消费 + 迭代器本质

```
m = map(str.upper, ['a', 'b', 'c'])
list(m)   # ['A', 'B', 'C']
list(m)   # []  ← 已耗尽！同一个 map 对象只能遍历一次
```

它也不支持序列操作（已验证）：

```
m[0]      # TypeError: 'map' object is not subscriptable
len(m)    # TypeError: object of type 'map' has no len()
```

**⚠️ 真值陷阱**（已验证）：

```
bool(map(str, []))   # True！即使对应空序列
# 千万不要写 if map(f, data): 来判断结果是否为空
# 正确做法：if any(map(f, data)):
```

如果想反复使用、索引、切片，转换成列表：`results = list(map(f, data))`。

## 3.5 核心特性③：多序列并行迭代

传入多个可迭代对象时，`map` 按位置配对，把每组元素作为多个参数传给函数：

```
map(lambda x, y: x + y, [1, 2, 3], [10, 20, 30])
# 等价于 [f(1,10), f(2,20), f(3,30)] → [11, 22, 33]

map(pow, [2, 3, 4], [3, 2, 1])          # [8, 9, 4]（内置函数也能用）
map(lambda a, b, c: a+b+c, [1,2], [10,20], [100,200])   # [111, 222]
```

**两条规则**（均已验证）：

1. **短者为准**：序列长度不等时，到最短的为止（和 `zip` 一致）—— `map(lambda x, y: (x, y), [1,2,3,4], ['a','b'])` 只产出 2 对；
2. **参数个数必须匹配**：函数收几个参数，就传几个序列，否则 `TypeError: <lambda>() takes 1 positional argument but 2 were given`。

> Python 2 历史包袱：`map(None, a, b)` 曾等价于 `zip`，Python 3 中已移除（实测报 `'NoneType' object is not callable`）。

## 3.6 `function` 参数的各种形态

`map` 只要求第一个参数是**可调用对象**，这带来很多优雅写法（全部实测通过）：

```
# ① 内置函数
list(map(int, ["1", "42", "100"]))            # [1, 42, 100] 批量类型转换
list(map(float, "1.5 2.5".split()))           # [1.5, 2.5]

# ② 类构造器
list(map(list, [(1, 2), (3, 4)]))             # [[1, 2], [3, 4]] 元组转列表

# ③ 字符串方法（str 的未绑定方法，无需 lambda！）
list(map(str.strip, ['  hello ', ' foo ']))   # ['hello', 'foo']
list(map(str.title, ['hello world']))         # ['Hello World']

# ④ dict.get（批量按 key 取值，缺 key 返回 None）
d = {'alice': 25, 'bob': 30}
list(map(d.get, ['bob', 'dave']))             # [30, None]

# ⑤ 自定义函数 / lambda
list(map(lambda r: (r[0].strip().title(), r[1]), [(" alice ", 25), ("bob", 30)])
# [('Alice', 25), ('Bob', 30)]
```

## 3.7 经典使用场景

**① 矩阵转置**（`map` + `zip` 星号解包，面试高频）：

```
matrix = [[1, 2, 3], [4, 5, 6]]
list(map(list, zip(*matrix)))    # [[1, 4], [2, 5], [3, 6]]
```

**② 函数式管道**（与上次的 `reduce` 串联）：

```
reduce(lambda a, b: a + b,
       map(str.upper, filter(lambda w: len(w) > 2, data)),
       "")
# filter 筛选 → map 变换 → reduce 聚合，全程惰性、无中间列表
```

**③ 大文件/流式处理**：`map` 配合生成器逐行处理，内存恒定。

## 3.8 性能实测真相

对 1000 个数操作、各执行 1000 次的实测结果：

| 写法                             | 耗时    | 结论             |
| -------------------------------- | ------- | ---------------- |
| `list(map(str, nums))`           | 0.1108s | 与列表推导式接近 |
| `[str(x) for x in nums]`         | 0.1031s | 略快             |
| `list(map(lambda x: x*2, nums))` | 0.0640s | **慢约 2 倍**    |
| `[x*2 for x in nums]`            | 0.0349s | 明显更快         |

**规律**：

- `map` + **lambda** 比列表推导式**慢**——每步都有 Python 层函数调用开销；
- `map` + **内置函数**（如 `str`、`int`）时两者接近，因为推导式也要逐个调用函数；
- 结论与 `reduce` 一致：**lambda 是性能杀手**。

## 3.9 `map` vs 列表推导式：如何选

```
list(map(str.title, words))          # map 写法
[w.title() for w in words]           # 推导式写法
```

**✅ 倾向用 `map` 的场景**：

- 已有现成函数可直接传入（`map(str, ...)`、`map(int, ...)`、`map(d.get, ...)`），零 lambda；
- 需要**惰性管道**（数据巨大或无限），且不需要中间列表；
- 函数式风格代码库中与 `filter` 链式组合。

**✅ 倾向用列表推导式的场景**：

- 变换逻辑简单（`[x*2 for x in nums]` 更快也更好读）；
- 需要附带条件过滤（推导式可加 `if`，`map` 做不到，得嵌套 `filter`）；
- 需要列表结果、索引、复用。

**经验法则**：`map(f, data)` 在 `f` 已经存在且有名有姓时最闪亮；一旦你为了 `map` 现场写 lambda，列表推导式几乎总是更好的选择。

## 3.10 常见坑总结

| 坑                    | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| 忘了转换就打印        | `print(map(f, data))` 输出 `<map object at ...>`，需 `list(map(...))` |
| 重复遍历              | map 对象是一次性的，第二次 `list()` 得 `[]`                  |
| 用 `if map(...)` 判空 | map 对象**永远为真**，要用 `any()`/`list()` 判断             |
| 参数个数不匹配        | N 个序列必须对应收 N 个参数的函数                            |
| 序列长度不等          | 静默截断到最短，不报错——小心数据悄悄丢失                     |

## 3.11 总结

- `map(函数, 序列...)` 对每个元素应用函数，**N 进 N 出**；
- 返回**惰性迭代器**：不取值不计算、一次性消费、内存几乎为零、可处理无限序列；
- 多序列时**按位置并行配对**，短者为准，参数个数必须匹配；
- 最优雅的用法是传入**现成的可调用对象**（`str`、`int`、`d.get`、`str.strip`…）；
- 实测：`map + lambda` 慢于列表推导式，**能写推导式就别为 map 造 lambda**；
- 它与 `filter`（筛选）、`reduce`（聚合）组成函数式三件套，链式组合时全程惰性、零中间列表。

# 4. `filter`

# 5. `dir`

# 6. `enumerate`

# 7. 