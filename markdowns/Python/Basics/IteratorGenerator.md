<h1 style="text-align: center;font-size: 40px; font-family: '楷体';">迭代器和生成器</h1>

# 1. 迭代器

迭代器类型的定义

1. 当类中定义了 `__iter__` 和  `__next__`  两个方法.
2. `__iter__`  方法要返回对象本身, 即 `self`
3. `__next__`  方法，返回下一个数据，如果没有数据了，则需要炮抛出一个 `StopIteration `异常

> 官方文档：https://docs.python.org/3.14/library/stdtypes.html#iterator-types

创建迭代器类型：

```python
class IT:
    """迭代器类型"""
    def __init__(self):
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter == 3:
            raise StopIteration
        return self.counter


# 根据类实例化创建一个迭代器对象
# obj1 和 obj2 --> 都是迭代器对象
obj1 = IT()

# v1 = obj1.__next__()
# v1 = obj1.__next__()
# v1 = obj1.__next__()  # 抛出异常


print(next(obj1))  # 1
print(next(obj1))  # 2
print(next(obj1))  # 抛出异常

obj2 = IT()
for item in obj2:
    print(item)
# # for 循环输出：
# 1
# 2
```



```txt
迭代器对象支持通过 next 方法取值，如果取值结束则自动抛出 `StopIteration` 异常.
for 循环内部在循环时，先执行 __iter__ 方法，获取一个迭代器对象，然后不断执行 next 取值（有异常 StopIteration 则终止循环）.
```



# 2. 生成器

```python
# 创建生成器函数
def func():
    yield 1
    yield 2


# 创建生成器对象 （内部是根据生成器类 generator 创建的对象），生成器内部也声明了 __iter__ 和 __next__ 方法
obj1 = func()
v1 = next(obj1)
print(v1)

v2 = next(obj1)
print(v2)

v3 = next(obj1)
print(v3)

obj2 = func()
for item in obj2:
    print(item)
```

```txt
如果按照迭代器的规定来看，其实生成器也是一种特殊的迭代器类。（生成器也是一种特殊的迭代器）.
```

# 3. 可迭代对象

```python
# 如果一个类中有 __iter__ 方法并且返回一个迭代器对象，则我们称这个类创建的对象为可迭代对象

class Foo:
    def __iter__(self):
        return 迭代器对象/生成器对象
    
    
obj = Foo()  # 可迭代对象 range(int)就是一个可迭代对象

# 可迭代对象是可以使用 for 来进行循环的, 在循环的内部其实是先执行 __iter__ 方法，获取其迭代器对象，然后再在内部执行这个迭代器对象的next功能，逐步取值。
```

```python
class IT(object):
    def __init__(self):
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter >= 3:
            raise StopIteration
        return self.counter


class Foo(object):

    def __iter__(self):
        return IT()


obj = Foo()
for item in obj:
    print(item)
```

```python
# 基于迭代器和可迭代对象，实现自定义 range

class IterRange(object):
    """迭代器类"""

    def __init__(self, num):
        self.num = num
        self.counter = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter >= self.num:
            raise StopIteration()
        return self.counter


class XRange(object):
    """可迭代的类"""

    def __init__(self, max_num):
        self.max_num = max_num

    def __iter__(self):
        return IterRange(self.max_num)


x = XRange(10)  # x 是一个`可迭代对象`(不是迭代器对象)
for i in x:
    print(i)
```

```python
class Foo:
    def __iter__(self):
        yield 1
        yield 2
        yield 3
        

obj = Foo()
for item in obj:
    print(item)
```

```python
# 基于生成器和可迭代对象，实现自定义 range


class XRange:
    def __init__(self, max_num):
        self.max_num = max_num

    def __iter__(self):
        counter = 0
        while counter < self.max_num:
            yield counter
            counter += 1


obj = XRange(10)
for i in obj:
    print(i)
```

- 列表 是可迭代对象
  ```python
  v1 = list([11, 22, 33])  # v1 是一个可迭代对象 因为在列表中有 __iter__ 没有 __next__ 并且 v1.__iter__() 有 __iter__和__next__
  print(dir(v1))  # ['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
  
  print(dir(v1.__iter__()))  # ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__length_hint__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__']
  
  ```

- 如何判断
  ```python
  # from collections import Iterator, Iterable  # python 3.10 以后 Iterator, Iterable 被移入 collections.abc，彻底无法从 collections 直接导入
  from collections.abc import Iterator, Iterable
  v1 = [1, 2, 3]
  isinstance(v1, Iterator)  # False
  isinstance(v1, Iterable)  # True
  
  v2 = v1.__iter__()
  isinstance(v2, Iterator)  # True
  isinstance(v2, Iterable)  # True
  ```

  









































































