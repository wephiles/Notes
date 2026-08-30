# 1. `global`

**`global`**：用于声明变量来自**最外层的全局作用域**（模块级别）。

**作用**：在函数内部修改或定义全局变量。

**背景**：
Python 默认规定，在函数内部给变量赋值，该变量就是**局部变量**。如果你直接在函数里修改全局变量（例如 `x = 10`），Python 会创建一个新的同名局部变量，而不会改变外面的全局变量。使用 `global` 关键字就是为了告诉 Python：“我要用的是外面的那个全局变量”。

```
x = 10  # 这是一个全局变量

def modify_global():
    global x  # 声明我们要使用外面的全局变量 x
    x = 20    # 修改全局变量
    print(f"函数内部 x = {x}")

modify_global()
print(f"函数外部 x = {x}")
```

输出结果：

```python
函数内部 x = 20
函数外部 x = 20
```

> 如果不加 `global x`，函数内的 `x = 20` 会创建一个局部变量，函数外部的 `x` 依然会是 10。

常见误区提醒：

1. **尽量少用 `global`**：过度使用全局变量会让代码难以维护和调试，通常建议通过函数参数传递值。

2. **`nonlocal` 必须已定义**：

   ```python
       def outer():
           def inner():
               nonlocal x # 报错！因为 outer 里没有定义 x
               x = 10
           inner()
   ```

# 2. `nonlocal`

**`nonlocal`**：用于声明变量来自**外层的函数作用域**（闭包中），但不是全局作用域。

**作用**：在**嵌套函数**（闭包）中，修改外层（非全局）函数的变量。

**背景**：
当我们在一个函数内部定义了另一个函数时，内部函数可以读取外部函数的变量。但是，如果内部函数想要**修改**外部函数的变量，Python 默认会把它当作内部函数的局部变量处理（产生 `UnboundLocalError` 或遮蔽问题）。`nonlocal` 就是用来解决这个问题，它会向外寻找最近一层的函数作用域。

```python
def outer():
    x = 10  # 外部函数的局部变量

    def inner():
        nonlocal x  # 声明 x 不是局部变量，而是外层函数 outer 的变量
        x = 20      # 修改 outer 函数中的 x
        print(f"inner 内部 x = {x}")
    
    inner()
    print(f"outer 内部 x = {x}")

outer()
```

输出结果：

```python
inner 内部 x = 20
outer 内部 x = 20
```

补充：`global` 和 `nonlocal` 的区别：

| 特性            | `global`                                            | `nonlocal`                                           |
| :-------------- | :-------------------------------------------------- | :--------------------------------------------------- |
| **作用对象**    | 全局作用域                                          | 外层函数作用域                                       |
| **变量层级**    | 作用于最顶层（模块级）变量                          | 作用于直接外层函数的变量，不能是全局                 |
| **是否存在**    | 如果全局变量不存在，`global` 声明后会自动创建新变量 | 变量必须已经在外层函数中定义，否则报错 `SyntaxError` |
| **使用场景**    | 单层函数或嵌套函数中修改全局配置                    | 嵌套函数（闭包）中修改状态                           |
| **Python 版本** | 所有版本                                            | Python 3 引入 (Python 2 没有)                        |

# 3. `yield` & `yield from`

`yield` 和 `yield from` 是 `Python` 中定义生成器的核心关键字。理解它们，是掌握迭代器、协程和异步编程的基础。

## 3.1 `yield`：让函数变身生成器

### 3.1.1 基本定义

在一个函数体内，只要出现了 `yield` 表达式，这个函数就不再是普通函数，而变成一个**生成器函数**。调用该函数不会执行函数体，而是返回一个**生成器对象**。

```
def simple_gen():
    print("开始")
    yield 1
    print("中间")
    yield 2
    print("结束")

g = simple_gen()     # 未执行任何函数体，只得到生成器对象
print(next(g))       # 输出: 开始 → 1
print(next(g))       # 输出: 中间 → 2
print(next(g))       # 输出: 结束 → 抛出 StopIteration
```

### 3.1.2 `yield` 的执行模型

执行过程可以理解为“**暂停—恢复—暂停**”：

1. 第一次 `next(g)` 或 `g.send(None)` 启动生成器，执行到第一个 `yield` 处暂停，把 `yield` 后面的值返回给调用方。
2. 再次调用 `next(g)`，从上次暂停的地方恢复执行，直到下一个 `yield`。
3. 函数执行完毕或遇到 `return` 时，自动抛出 `StopIteration` 异常。若 `return` 带有值，这个值会附加在 `StopIteration.value` 中。

### 3.1.3 双向通信：`send()`、`throw()`、`close()`

`yield` 不仅仅是“产出”数据，还可以**接收外部数据**，让生成器变成协程。

- **`send(value)`**
  恢复生成器运行，并将 `value` 作为当前暂停的 `yield` 表达式的值。

  ```
  def echo():
      while True:
          received = yield
          print(f"收到: {received}")
  
  g = echo()
  next(g)          # 必须先启动，前进到 yield 处
  g.send("hello")  # 输出: 收到: hello
  ```

- **`throw(exc)`**
  在生成器暂停处抛出一个异常，可由生成器内部捕获。

- **`close()`**
  在暂停处抛出 `GeneratorExit` 异常，用于清理资源。生成器内部通常用 `try/finally` 处理。

### 3.1.4 `yield` 与 `return` 的区别

| 特性      | `yield`              | `return`                                               |
| :-------- | :------------------- | :----------------------------------------------------- |
| 暂停/结束 | 暂停函数，保存状态   | 结束函数，释放局部状态                                 |
| 多次调用  | 可多次 `yield`       | 仅一次                                                 |
| 返回值    | 返回给生成器的调用方 | 给函数的调用方（生成器返回值在 `StopIteration.value`） |
| 函数类型  | 生成器函数           | 普通函数                                               |

### 3.1.5 实际使用场景

- **惰性生成大数据流**：逐行读取大文件，避免内存爆炸。
- **管道式数据处理**：例如 `(x*2 for x in data if x>0)`。
- **实现简易协程**（在现代 `asyncio` 之前）。
- **状态机**：用 `yield` 保存当前状态。

------

## 3.2 `yield from`：委托给子生成器

`yield from` 是 Python 3.3 引入的语法，用于**将一个生成器的迭代委托给另一个生成器**。它极大简化了嵌套生成器的写法，并建立了调用方和子生成器之间的直接通道。

### 3.2.1 简单例子：扁平化嵌套

假设你有一个生成器，内部需要遍历另一个可迭代对象：

**没有 `yield from` 的老办法：**

```
def chain(*iterables):
    for it in iterables:
        for item in it:
            yield item
```

**使用 `yield from`：**

```
def chain(*iterables):
    for it in iterables:
        yield from it
```

`yield from it` 等价于“逐个产出 `it` 中的值”，但远不止这么简单。

### 3.2.2 `yield from` 的完整功能

`yield from <subgen>` 会建立一个透明的双向通道，使得：

1. **所有从调用方发来的 `send(value)` 都直接传给子生成器。**
2. **所有从调用方发来的 `throw(exc)` 都直接传给子生成器。**
3. **子生成器抛出的 `StopIteration` 会被捕获，其 `value` 成为 `yield from` 表达式的最终值。**
4. **主生成器调用 `close()` 时，`GeneratorExit` 也会传给子生成器。**

这相当于一个“代理”，让子生成器直接面对最终的调用方。

### 3.2.3 图解控制流与数据流

```
调用方 (main)
   │
   │ send/next/throw/close
   ▼
主生成器 (含 yield from 子生成器)
   │         ▲
   │ 将调用透传给子生成器，子生成器的 yield 值直接返回给调用方
   ▼         │
子生成器
```

主生成器在 `yield from` 处暂停，直到子生成器结束。期间主生成器无法干预调用方与子生成器的交互。

### 3.2.4 `yield from` 的等价代码（PEP 380）

PEP 380 给出了接近等价的伪代码，这里提炼核心逻辑：

```
# yield from EXPR 的简化实现
_i = iter(EXPR)          # 取得子迭代器
try:
    _y = next(_i)        # 启动子生成器
except StopIteration as _e:
    _r = _e.value
else:
    while True:
        try:
            _s = yield _y   # ① 把子生成器的产出直传调用方，同时接收调用方发送的值
        except GeneratorExit as _e:
            # ② 处理主生成器的 close()
            try:
                _m = _i.close
            except AttributeError:
                pass
            else:
                _m()
            raise _e
        except BaseException as _e:
            # ③ 处理调用方 throw 异常
            _x = sys.exc_info()
            try:
                _m = _i.throw
            except AttributeError:
                raise _e
            else:
                try:
                    _y = _m(*_x)
                except StopIteration as _e:
                    _r = _e.value
                    break
        else:
            # ④ 正常情况：把接收到的值 _s 发送给子生成器
            try:
                if _s is None:
                    _y = next(_i)
                else:
                    _y = _i.send(_s)
            except StopIteration as _e:
                _r = _e.value
                break
result = _r  # 最终 StopIteration 的值成为整个 yield from 的值
```

可以看到，`yield from` 自动处理了大量繁琐的异常和值传递工作。

### 3.2.5 利用 `yield from` 返回值

子生成器终止时的 `return` 值可以被主生成器捕获：

```
def sub():
    yield 1
    yield 2
    return "子生成器结束"

def main():
    result = yield from sub()
    print(f"子生成器返回: {result}")

g = main()
print(next(g))   # 1
print(next(g))   # 2
# 再调一次 next(g) → 打印 "子生成器返回: 子生成器结束"，然后抛出 StopIteration
```

## 3.3 `yield` 与 `yield from` 的区别和联系

| 维度   | `yield`                     | `yield from`                        |
| :--- | :-------------------------- | :---------------------------------- |
| 作用   | 暂停并产出一个值（或接收一个值）            | 将迭代操作委托给子生成器                        |
| 连接对象 | 直接与调用方交互                    | 建立调用方与子生成器的透明通道                     |
| 自动处理 | 无，需手动在生成器内写 for 循环和 send 逻辑 | 自动处理 send、throw、close、StopIteration |
| 返回值  | 可接收外部 send 的值，本身不产生“最终结果”   | 可获取子生成器的 return 值                   |
| 适用场景 | 基本的值产出或协程通信                 | 嵌套生成器扁平化，重构复杂的生成器代理                 |

------

## 3.4 实际应用与高级模式

### 3.4.1 用 `yield from` 构建可复用的生成器包装器

假设要编写一个带有日志、异常捕获的生成器包装：

```
def logging_wrapper(gen_func, *args, **kwargs):
    gen = gen_func(*args, **kwargs)
    try:
        value = yield from gen
        print(f"生成器正常结束，返回值：{value}")
    except Exception as e:
        print(f"发生异常：{e}")
    finally:
        print("清理资源")
```

### 3.4.2 扁平化树形结构

遍历树形结构（如文件系统、`JSON`）时非常优雅：

```
def traverse(node):
    yield node
    if hasattr(node, 'children'):
        for child in node.children:
            yield from traverse(child)
```

### 3.4.3 用作协程（虽已不是主流）

在 `asyncio` 出现前，`yield from` 被用于基于生成器的协程（`@asyncio.coroutine`）。现在已基本被 `async/await` 取代，但底层思想相通。

## 3.5 常见陷阱与注意事项

1. **生成器函数与生成器对象**：
   `def gen(): yield 1` 是生成器函数；`gen()` 才是生成器对象。每次调用都创建全新生成器，状态独立。
2. **忘记启动生成器就 send**：
   必须先 `next(g)` 或 `g.send(None)`，让生成器行进到第一个 `yield` 表达式处，才能发送非 None 值。
3. **`yield from` 之后不要手动迭代**：
   `yield from iterable` 已经完成了全部迭代，如果在同一个 `for` 循环里再次 `yield from`，可能造成逻辑重复。
4. **用 `return` 结束生成器**：
   Python 3.3+ 允许 `return x` 在生成器中使用，但只能用于携带 `StopIteration.value`。不要在 `try` 块中用 `return`，因为它仍然触发 `StopIteration`。
5. **生成器中的异常处理**：
   生成器内未捕获的异常会传播给调用方。如果要实现 `close()` 清理，务必用 `try/finally`。

## 3.6 总结

- **`yield`** 将函数变为可以暂停和恢复的生成器，支持数据双向传递，适合构建惰性序列和简单协程。
- **`yield from`** 是一个强大的“委托”语法，它透明地连接调用方与子生成器，自动处理迭代、发送、异常及最终返回值，极大简化了嵌套生成器的编写，也是理解 `await` 实现原理的重要基石。

掌握了它们，你就拥有了处理 Python 中数据流、并发模型和异步编程的基础思维工具。