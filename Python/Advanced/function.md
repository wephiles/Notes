---
aliases:
  - course of study
  - course
  - python function tutorial
  - Python function closures
  - function decorator
  - decorator
tags:
  - tutorial
  - computer-science
  - decorator
  - function-closure
  - builtin-function
category:
  - knowledge
  - Python
  - function
  - decorator
  - closure
datetime: " 2026-08-03 20:08:09 周一"
author: wephiles
rating: "9"
---
# 一、函数闭包

## 1.1 什么是闭包

**闭包** 是指有权访问另一个函数作用域中变量的函数，简单来说，闭包是一个函数，他记住了创建时的环境（外部变量），即使在创建他的外部函数已经执行完毕，闭包依然可以访问和操作这些变量。

- 形成闭包的三个途径
	- 嵌套函数：一个函数内部定义了另一个函数
	- 内部函数引用外部函数的变量：内部变量使用了外部函数的变量
	- 外部函数返回内部函数 ：外部函数将内部函数作为返回值返回

## 1.2  示例 1 —— 基本的闭包结构

```python
def outer_function(msg):  
    # msg 是一个外部变量（对外部函数而言是局部变量，对内部函数而言是环境变量）  
  
    def inner_func():  
        # 内部函数引用了外部函数的 变量 msg        print(f'我记住了外部函数的变量 {msg}')  
  
    return inner_func  
  
  
# 1. 调用 outer_function，返回 inner_func 对象，赋值给 my_func# 此时 outer_function 已经执行完毕，理论上 局部变量 msg 应该被销毁  
  
my_func = outer_function("Hello, Closure!")  
  
# 2. 调用 my_func （实际上是调用 inner_func）  
# 结果发现它依然能够访问 msg，这就是闭包的作用  
my_func()  # 我记住了外部函数的变量 Hello, Closure!
```

## 1.3 示例 2 —— 闭包实现计数器（状态保持）

闭包可以让函数拥有记忆，类似于面向对象中的对象属性。

```python
def make_count():  
    count = 0  
  
    def counter():  
        nonlocal count  
  
        count += 1  
  
        return count  
  
    return counter  
  
  
cnt = make_count()  
print(cnt())  # 1  
print(cnt())  # 2  
print(cnt())  # 3
```

## 1.4 关于闭包的一些问题的说明

1. 为什么外部函数执行完毕之后，内部函数和外部局部变量不会被销毁
   答：因为内部函数对象持有外部变量的引用，Python 的垃圾回收机制（引用计数器机制）发现这些变量还被 `活着的` 内部函数引用着，所以不会回收它们；
   1. `Python` 函数执行时，会创建一个临时的**栈帧（Stack Frame）**，里面存放局部变量。正常情况下，函数执行完毕，栈帧弹出并销毁，局部变量的引用计数归零，内存释放。
   2. 但是，当内部函数被定义并返回时，Python 会将外部函数中**被内部函数引用的变量**从“普通局部变量”升级为**“闭包单元格（Cell）”**。
   3. 这些单元格对象被存放在返回的内部函数的 `__closure__` 属性中。
   4. 当你把内部函数赋值给外部变量时，这个 变量引用了内部函数对象，而内部函数对象又通过 `__closure__` 引用了那些单元格，单元格又引用了实际的数据。
   5. 所以**引用链条**是：`外部变量` -> `内部函数对象` -> `闭包单元格` -> `外部变量值`。只要 `logger` 还在，这条链就不断，垃圾回收器就不会回收它们。
2. 外部函数接收到的参数是什么？
   答：外部函数接收到的参数（形参）属于该函数的局部作用域中的局部变量
   3. 在函数体内，参数名和你用 `=` 在函数内部定义的变量在作用域层级上是**完全平级**的，都存放在当前函数的局部命名空间（`locals()`）中。
   4. **特殊点（与闭包相关）**：如果这个参数被内部函数引用了，它同样会被升级为“闭包单元格（Cell）”，数据生命周期随之延长。
5. 实参是如何传递给形参的？实参和形参有何区别？
   答：Python参数传递采用的是 **对象引用传递**，也叫赋值传递
   传递过程：调用函数时，实参是一个在内存中存在的对象，Python 执行的是 **将实参对象的引用（内存地址）赋值给形参变量**。
6. 形参的作用域：是属于定义的该函数的局部作用域的

# 二、装饰器

## 2.1 什么是装饰器

装饰器是一种**设计模式**，它允许在不修改原函数源代码和调用方式的前提下，为函数动态地添加额外的功能（如日志、计时、权限校验、缓存等）。

## 2.2 语法糖：`@`符号

Python 用 `@decorator_name` 放在函数定义上方，本质上是执行了 `func = decorator_name(func)` 的操作。[猛戳这里查看如何一步步实现装饰器](# 五、一步一步看)

## 2.3 基础装饰器（利用闭包）

一个最简单的计时装饰器，展示了闭包如何被用来包装函数：

```python
import time

def timer(func):
    # 这里的 func 是外部变量，wrapper 是内部函数，构成了闭包
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)  # 调用原函数
        end = time.time()
        print(f"{func.__name__} 执行耗时: {end - start:.4f}s")
        return result
    return wrapper  # 返回内部函数（闭包）

# 使用装饰器
@timer
def long_task(n):
    time.sleep(n)
    return n * 10

# 等价于： long_task = timer(long_task)
long_task(1)  # 输出: long_task 执行耗时: 1.000x s
```

## 2.4 带参数的装饰器（三层嵌套闭包）

如果装饰器本身需要接收参数（例如指定重复次数），则需要再嵌套一层函数：

```python
def repeat(times):  # 第一层：接收装饰器参数
    def decorator(func):  # 第二层：接收被装饰的函数
        def wrapper(*args, **kwargs):  # 第三层：接收原函数的实参
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    print("Hello!")

# 等价于：say_hello = repeat(3)(say_hello)
say_hello()  # 打印 3 次 "Hello!"
```

## 2.5 保留元数据

使用装饰器后，原函数的 `__name__` 和 `docstring` 会被 `wrapper` 覆盖。修复方法是在内部函数上加上 `@functools.wraps(func)`：

```python
import functools

def timer(func):
    @functools.wraps(func)  # 将 func 的元数据复制给 wrapper
    def wrapper(*args, **kwargs):
        # ... 
        return func(*args, **kwargs)
    return wrapper
```

## 2.6 闭包与装饰器的关系

| 维度         | **闭包（Closure）**                                    | **装饰器（Decorator）**                                      |
| :----------- | :----------------------------------------------------- | :----------------------------------------------------------- |
| **定义**     | 一种**函数式编程技术**，指函数持有外部环境变量的能力。 | 一种**语法结构和设计模式**，用于修改或增强函数行为。         |
| **关系**     | **底层实现手段**。                                     | **上层应用场景**。装饰器在底层完全依赖于闭包机制来实现函数包装。 |
| **目的**     | 数据隐藏、封装状态、生成定制函数（工厂模式）。         | AOP（面向切面编程），在不改动原有逻辑下插入横切关注点。      |
| **返回值**   | 返回一个**函数对象**（闭包实例）。                     | 同样返回一个**函数对象**，但通常该对象是对原函数的“增强版”。 |
| **参数焦点** | 外层函数传入的是**配置数据或初始状态**。               | 外层函数传入的是**一个可调用对象（原函数）**。               |

# 三、 高级补充：类装饰器与闭包的替代

虽然闭包是函数式实现装饰器的核心，但也可以用类来实现装饰器（利用 `__call__` 魔术方法），此时不涉及嵌套函数，自然也就不涉及闭包：

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"调用了 {self.count} 次")
        return self.func(*args, **kwargs)

@CountCalls
def test():
    pass
```

# 四、** 一步一步看

## 4.1 基础装饰器

### 4.1.1 最简单的装饰器实现

函数不带参数，并且不使用 `@` 符号。

```python
def decorate(func):
    def wrapper():
        print("执行前")
        func()
        print("执行后")

    return wrapper


def func():
    print('执行 func 函数')


decorated = decorate(func)  # decorated = wrapper
decorated()  # wrapper()

============== 输出结果 ==============
执行前
执行 func 函数
执行后
```

### 4.1.2 此时如果函数 `func` 有参数：

```python
def decorate(func):
    def wrapper(a, b):
        print("执行前")
        func(a, b)
        print("执行后")

    return wrapper


def func(a, b):
    print('执行 func 函数')
    print(f"a = {a}, b = {b}")


decorated = decorate(func)  # decorated = wrapper, 虽然这里看起来没变，但是其实这个 wrapper 执行是需要两个参数的
decorated(1, 2)  # wrapper(1, 2)

============== 输出结果 ==============
执行前
执行 func 函数
a = 1, b = 2
执行后
```

### 4.1.3 推广：可以让函数有任意参数

```python
def decorate(func):
    def wrapper(*args, **kwargs):
        print("执行前")
        func(*args, **kwargs)
        print("执行后")

    return wrapper


def func(a, b, c="c", d="d"):
    print('执行 func 函数')
    print(f"a = {a}, b = {b}")
    print(f"c = {c}, d = {d}")


# decorated = wrapper, 虽然这里看起来还是没变，但是其实这个 wrapper 执行是可以接受任何参数的
# 但是⚠️⚠️⚠️: 虽然 wrapper 可以接收任意参数, 但是根据 decorate 中的 wrapper 的实现,
# wrapper 接收的参数必须要能够放进 func 函数里面成功跑起来
decorated = decorate(func)
decorated(1, 2, c='ccc', d='ddd')  # wrapper(1, 2, c='ccc', d='ddd')

============== 输出结果 ==============
执行前
执行 func 函数
a = 1, b = 2
c = ccc, d = ddd
执行后
```

### 4.1.4 我函数想要有返回值怎么办？

1. 如果我们只给 `func` 这个函数加返回值：
   ```python
   def decorate(func):
       def wrapper(*args, **kwargs):
           print("执行前")
           res = func(*args, **kwargs)
           print("执行后")
   
       return wrapper
   
   
   def func(a, b, c="c", d="d"):
       print('执行 func 函数')
       print(f"a = {a}, b = {b}")
       print(f"c = {c}, d = {d}")
       return a, b, c, d
   
   
   # decorated = wrapper, 虽然这里看起来还是没变，但是其实这个 wrapper 执行是可以接受任何参数的
   # 但是⚠️⚠️⚠️: 虽然 wrapper 可以接收任意参数, 但是根据 decorate 中的 wrapper 的实现,
   # wrapper 接收的参数必须要能够放进 func 函数里面成功跑起来
   decorated = decorate(func)
   x = decorated(1, 2, c='ccc', d='ddd')  # wrapper(1, 2)
   print(x)  # None -- 这里永远会打印 None -- 因为 Python 函数没有返回值时默认返回 None
   
   ============== 输出结果 ==============
   执行前
   执行 func 函数
   a = 1, b = 2
   c = ccc, d = ddd
   执行后
   None
   ```

2. 怎么办呢，我们看 `decorated = decorate(func)` 其实是一个不带括号的函数，只要一给他加括号，就会调用 `decorate` 内部的 `wrapper` 函数，要想拿到返回值，只需要在 执行完 `wrapper()` 后拿到返回值不就行了吗？ -- 那就让 `wrapper` 有返回值不就可以了吗？
   ```python
   def decorate(func):
       def wrapper(*args, **kwargs):
           print("执行前")
           res = func(*args, **kwargs)
           print("执行后")
           return res
   
       return wrapper
   
   
   def func(a, b, c="c", d="d"):
       print('执行 func 函数')
       print(f"a = {a}, b = {b}")
       print(f"c = {c}, d = {d}")
       return a, b, c, d
   
   
   # decorated = wrapper, 虽然这里看起来还是没变，但是其实这个 wrapper 执行是可以接受任何参数的
   # 但是⚠️⚠️⚠️: 虽然 wrapper 可以接收任意参数, 但是根据 decorate 中的 wrapper 的实现,
   # wrapper 接收的参数必须要能够放进 func 函数里面成功跑起来
   decorated = decorate(func)
   x = decorated(1, 2, c='ccc', d='ddd')  # wrapper(1, 2, c='ccc', d='ddd')
   print(x)
   
   ============== 输出结果 ==============
   执行前
   执行 func 函数
   a = 1, b = 2
   c = ccc, d = ddd
   执行后
   (1, 2, 'ccc', 'ddd')
   ```

### 4.1.5 计算函数耗时

我现在突然想在函数执行前计算一下时间，在函数执行后计算一下时间，再一减，岂不是可以计算函数执行耗费了多长时间了？

```python
import time


def decorate(func):
    def wrapper(*args, **kwargs):
        print("执行前")

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("执行后")
        print("程序执行耗时:", end - start)

        return result

    return wrapper


def func(a, b, c="c", d="d"):
    print('执行 func 函数')
    print(f"a = {a}, b = {b}")
    print(f"c = {c}, d = {d}")
    time.sleep(1)  # 为了看更清楚，这里延迟一秒
    return a, b, c, d


# decorated = wrapper, 虽然这里看起来还是没变，但是其实这个 wrapper 执行是可以接受任何参数的
# 但是⚠️⚠️⚠️: 虽然 wrapper 可以接收任意参数, 但是根据 decorate 中的 wrapper 的实现,
# wrapper 接收的参数必须要能够放进 func 函数里面成功跑起来
decorated = decorate(func)
res = decorated(1, 2, c='ccc', d='ddd')  # wrapper(1, 2, c='ccc', d='ddd')
print("函数执行最终结果:", res)

============== 输出结果 ==============
执行前
执行 func 函数
a = 1, b = 2
c = ccc, d = ddd
执行后
程序执行耗时: 1.0001566410064697
函数执行最终结果: (1, 2, 'ccc', 'ddd')
```

我好像发现了新大陆，我竟然可以**在不改变函数任何代码的前提下，能够给代码前后加功能**！这也太酷了吧！！！

### 4.1.6 简化操作

我发现每次都要写下面这段代码，很麻烦😭

```python
decorated = decorate(...)
res = decorated(...)
```

当当当当，我们的 `@` 闪亮登场：只需要在定义函数的头顶上 写 `@decorate`，它竟然神奇地帮我们简化了这个操作！

```python
import time


def decorate(func):
    def wrapper(*args, **kwargs):
        print("执行前")

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("执行后")
        print("程序执行耗时:", end - start)

        return result

    return wrapper


@decorate
def func(a, b, c="c", d="d"):
    print('执行 func 函数')
    print(f"a = {a}, b = {b}")
    print(f"c = {c}, d = {d}")
    time.sleep(1)  # 为了看更清楚，这里延迟一秒
    return a, b, c, d


print("函数执行最终结果:", func(1, 2, 'c', 'd'))

============== 输出结果 ==============
执行前
执行 func 函数
a = 1, b = 2
c = c, d = d
执行后
程序执行耗时: 1.0003767013549805
函数执行最终结果: (1, 2, 'c', 'd')
```

好了，这就是最基本的装饰器了。下面会介绍一个官方写的装饰器，使我们的函数能够**保留一些函数的元信息**，也会继续讲如何写一个**可以带参数的装饰器**以及如何**用类来实现一个装饰器**。

## 4.2 保留函数元信息

我们已经成功实现了一个装饰器，我们现在想看看经过我们装饰器装饰的函数名等函数属性：

```python
import time


def decorate(func):
    def wrapper(*args, **kwargs):
        print("执行前")

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("执行后")
        print("程序执行耗时:", end - start)

        return result

    return wrapper


@decorate
def func(a, b, c="c", d="d"):
    """这是函数的文档字符串.

    Args:
        a ():
        b ():
        c ():
        d ():

    Returns:

    """
    print('执行 func 函数')
    print(f"a = {a}, b = {b}")
    print(f"c = {c}, d = {d}")
    time.sleep(1)  # 为了看更清楚，这里延迟一秒
    return a, b, c, d


# print("函数执行最终结果:", func(1, 2, 'c', 'd'))
print("func_name:", func.__name__)  # 函数名
print("func_doc:", func.__doc__)  # 函数文档字符串
print("func_qualname:", func.__qualname__)  # 函数完整限定名
print("func_module:", func.__module__)  # 函数所在模块名

============== 输出结果 ==============
func_name: wrapper
func_doc: None
func_qualname: decorate.<locals>.wrapper
func_module: __main__
```

![image-20260804205827906](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260804205836222.png)

我们发现，`__name__/__doc__` 这些函数 `func` 的元信息都没有被保留，而保留的是 `wrapper` 的信息。

**保留函数元信息：**

```python
import time
from functools import wraps


def decorate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("执行前")

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("执行后")
        print("程序执行耗时:", end - start)

        return result

    return wrapper


@decorate
def func(a, b, c="c", d="d"):
    """这是函数的文档字符串.

    Args:
        a ():
        b ():
        c ():
        d ():

    Returns:

    """
    print('执行 func 函数')
    print(f"a = {a}, b = {b}")
    print(f"c = {c}, d = {d}")
    time.sleep(1)  # 为了看更清楚，这里延迟一秒
    return a, b, c, d


# print("函数执行最终结果:", func(1, 2, 'c', 'd'))
print("func_name:", func.__name__)  # 函数名
print("func_doc:", func.__doc__)  # 函数文档字符串
print("func_qualname:", func.__qualname__)  # 函数完整限定名
print("func_module:", func.__module__)  # 函数所在模块名

============== 输出结果 ==============
func_name: func
func_doc: 这是函数的文档字符串.

    Args:
        a ():
        b ():
        c ():
        d ():

    Returns:

    
func_qualname: func
func_module: __main__
```

![image-20260804210208612](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260804210209776.png)

## 4.3 带参数的装饰器

我们按照 不带参数的装饰器的步骤 一步一步地看：

### 4.3.1 一步步赋值

```python
import time
from functools import wraps


def repeat(times: int):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("执行前: repeat =", times)

            start = time.time()
            for i in range(times):
                result = func(*args, **kwargs)
            end = time.time()

            print("执行后, repeat = ", times)
            print("程序执行耗时:", end - start)

            return result

        return wrapper

    return decorate


def new_func(a, b=2):
    print('执行函数 new_func')
    time.sleep(0.5)
    return "OK" + str(a) + str(b)


# 首先调用 repeat 函数，其接收一个 int 类型参数 --> 得到一个函数对象 decorate(test_decorate_with_arg_func)
test_decorate_with_arg_func = repeat(3)  # test_decorate_with_arg_func = decorate

# decorate 函数对象接收一个 函数对象，调用 decorate 函数对象，传递过去我们的函数对象 new_func --> 得到一个函数对象 wrapper(new_f)
new_f = test_decorate_with_arg_func(new_func)  # decorate() = wrapper

# wrapper 接收任意参数 --> 接收 new_func 的参数
final_res = new_f(10, b=20)  # final_func = wrapper(10, 20)

print(final_res)

# ================= 输出结果 =================
执行前: repeat = 3
执行函数 new_func
执行函数 new_func
执行函数 new_func
执行后, repeat =  3
程序执行耗时: 1.5019125938415527
OK1020
```

### 4.3.2 改的简洁一点

```python
import time
from functools import wraps


def repeat(times: int):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("执行前: repeat =", times)

            start = time.time()
            for i in range(times):
                result = func(*args, **kwargs)
            end = time.time()

            print("执行后, repeat = ", times)
            print("程序执行耗时:", end - start)

            return result

        return wrapper

    return decorate


def new_func(a, b=2):
    print('执行函数 new_func')
    time.sleep(0.5)
    return "OK" + str(a) + str(b)


new_func = repeat(3)(new_func)
print(new_func(123, 456))

================= 输出结果 =================
执行前: repeat = 3
执行函数 new_func
执行函数 new_func
执行函数 new_func
执行后, repeat =  3
程序执行耗时: 1.5011389255523682
OK123456
```

### 4.3.3 最终版

```python
import time
from functools import wraps


def repeat(times: int):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("执行前: repeat =", times)

            start = time.time()
            for i in range(times):
                result = func(*args, **kwargs)
            end = time.time()

            print("执行后, repeat = ", times)
            print("程序执行耗时:", end - start)

            return result

        return wrapper

    return decorate


@repeat(3)
def func(a, b, c="c", d="d"):
    """这是函数的文档字符串.

    Args:
        a ():
        b ():
        c ():
        d ():

    Returns:

    """
    print('执行 func 函数')
    print(f"a = {a}, b = {b}")
    print(f"c = {c}, d = {d}")
    time.sleep(1)  # 为了看更清楚，这里延迟一秒
    return a, b, c, d


@repeat(3)
def new_func(a, b=2):
    print('执行函数 new_func')
    time.sleep(0.5)
    return "OK" + str(a) + str(b)


# # 首先调用 repeat 函数，其接收一个 int 类型参数 --> 得到一个函数对象 decorate(test_decorate_with_arg_func)
# test_decorate_with_arg_func = repeat(3)  # test_decorate_with_arg_func = decorate
#
# # decorate 函数对象接收一个 函数对象，调用 decorate 函数对象，传递过去我们的函数对象 new_func --> 得到一个函数对象 wrapper(new_f)
# new_f = test_decorate_with_arg_func(new_func)  # decorate() = wrapper
#
# # wrapper 接收任意参数 --> 接收 new_func 的参数
# final_res = new_f(10, b=20)  # final_func = wrapper(10, 20)
#
# print(final_res)

res = new_func(100, 200)
print(res)
# ================= 输出结果 =================
执行前: repeat = 3
执行函数 new_func
执行函数 new_func
执行函数 new_func
执行后, repeat =  3
程序执行耗时: 1.501814365386963
OK100200
```

我们可以发现，执行过程完全相同！

### 4.3.4 小结

到此为止，我们所实现的装饰器全部基于[**函数闭包**](#二、函数闭包)实现，下面要讲的基于类的装饰器则不是基于闭包实现的。

## 4.4  用类实现装饰器

### 4.4.1 示例

```python
import time
from functools import wraps
import functools


class Record:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('record: before run ...')
        res = self.func(*args, **kwargs)
        print('record: after run ...')
        return res


class Repeat:
    def __init__(self, times: int = 3):
        self.times = times

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            print('开始执行')
            for i in range(0, self.times):
                result = func(*args, **kwargs)
            print('执行结束')
            return result

        return wrapper


@Record
def test_func(x, y=10):
    print('call function test_func ...')
    return x + y


@Repeat(3)
def my_func(a, b=6):
    print('参数: a =', a, 'b =', b)
    return f"return: {a} - {b}"


test_res = test_func(5, 6)
print('=' * 20)
my_res = my_func(3, 4)

# ================= 输出结果 =================
record: before run ...
call function test_func ...
record: after run ...
====================
开始执行
参数: a = 3 b = 4
参数: a = 3 b = 4
参数: a = 3 b = 4
执行结束
```

上述两个例子分别展示了如何实用类实现不带参数和带参数的装饰器，如果觉得难理解可以这样想：

```python
@Record                         
def test_func(x, y=10):         
    pass

# test_func = Record(test_func)   ---> test_func = __init__(test_func) --> 
# test_func 此时成为了一个 Record 类的实例对象，而 __call__ 恰好能够实现对象加括号
# test_func(1, 2) --> 其实就是 Record(test_func)(1, 2) --> 最终还是调用了 Record.__call__ 方法而已
```

### 4.4.2 关于 不带参数的类装饰器 中的保留函数元信息问题

```python
from functools import wraps
import functools


class Record:
    def __init__(self, func):
        self.func = func
        # @wraps 只是 update_wrapper 的语法糖
        # 在类装饰器中，我们要更新的 wrapper 是 self --> 即 have_decorated_func 所以直接写
        # =========================================================================
        # # @wraps(func) 本质上就是：
        # def wraps(func):
        #     def decorator(wrapper):
        #         functools.update_wrapper(wrapper, func)
        #         return wrapper
        #     return decorator
        # =========================================================================

        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print('record: before run ...')
        res = self.func(*args, **kwargs)
        print('record: after run ...')
        return res


class Repeat:
    def __init__(self, times: int = 3):
        self.times = times

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            print('开始执行')
            for i in range(0, self.times):
                result = func(*args, **kwargs)
            print('执行结束')
            return result

        return wrapper


@Record
def test_func(x, y=10):
    print('call function test_func ...')
    return x + y


@Repeat(3)
def my_func(a, b=6):
    print('参数: a =', a, 'b =', b)
    return f"return: {a} - {b}"


test_res = test_func(5, 6)
print('=' * 20)
my_res = my_func(3, 4)
```

如果我们对 `__call__` 使用  `@wraps(func)`，是会报错的，因为执行到此处的时候 `func` 还不存在.

## 4.5 小结

1. 不带参数的装饰器: `func = decorator(func)`
2. 带参数的装饰器: `func = decorator(xxx)(func)`
3. 同类实现的装饰器: 实现原理同用闭包实现的装饰器
