
python 中的 `@cache`  装饰器(Python 3.9+ 中正式加入 `functools`, 之前版本叫 `@lru_cache(max_sizeNone)`) 的作用是 **备忘录模式**,: 将函数的参数和返回值存入字典, 下次遇到相同参数时直接返回结果, 跳过函数执行。

# 一、`@cache` 底层原理

Python 官方实现 `@cache` 的核心思想非常简单：[[function#二、函数闭包|👉闭包]] + **字典**。

本文会用到装饰器，详情查看 [[function#三、装饰器|装饰器]]

1. **字典做映射**：内部维护了一个字典 `_cache`，字典的 `key` 是函数的参数，`value` 是函数的返回值。
2. **闭包保存状态**：利用装饰器的闭包特性，这个 `_cache` 字典会常驻在内存中，不会随着函数调用结束而销毁。
3. **Key 的生成（难点）**：因为函数参数有位置参数 `*args` 和关键字参数 `**kwargs`，必须把它们转换成一个唯一且不可变的对象（通常是元组）才能作为字典的键。官方在底层使用了一个用 C 语言编写的函数 `_make_key` 来高效完成这件事。
4. **附加功能**：官方版本还动态给被装饰的函数添加了 `cache_info()` (查看命中率) 和 `cache_clear()` (清空缓存) 方法。

*(注：在 `Python 3.8` 及以前，`@cache` 就是 `@lru_cache(maxsize=None)`，因为不需要淘汰旧数据，所以实现相对纯粹的 `cache` 更复杂。`Python 3.9` 将其独立出来，去掉了 `LRU` 链表相关的 C 代码，性能更好。)*

# 二、手动实现 `@cache`

## 2.1 极简版（仅支持位置参数）

```python
def simple_cache(func):  
    cache = {}  
  
    def wrapper(*args):  
        # 如果参数在缓存中，那么直接返回结果即可  
        if args in cache:  
            print('命中缓存', *args)  
            return cache[args]  
  
        # 参数不在缓存中，需要调用函数计算并存入缓存  
        print('未命中缓存', *args)  
        result = func(*args)  
        cache[args] = result  
        return result  
  
    return wrapper  
  
  
@simple_cache  
def cal_add(a, b):  
    return a + b  
  
  
print(cal_add(1, 2))  
print(cal_add(3, 4))  
print(cal_add(1, 2))
```

上述代码运行结果:

```plaintext
未命中缓存 1 2
3
未命中缓存 3 4
7
命中缓存 1 2
3
```

## 2.2  进阶版（支持关键字参数）

实际的函数经常有 `f(a=1, b=2)`，而且 `f(a=1, b=2)` 和 `f(b=2, a=1)` 应该被视为同一个调用。我们需要手动构造一个稳定的 Key。

关于 `sorted()` ，查看 [[function#1.6 `sorted`|pythonFunction.sorted]]

```python
def keywords_cache(func):  
    cache = {}  
  
    def wrapper(*args, **kwargs):  
        # 核心：如何将 args 和 kwargs 变成一个唯一且不可变的 key
        # 1. 将 kwargs 按照键排序，变成元组，防止顺序不同导致 key 不同
        # 2. 将 args 和排序后的 kwargs 拼成一个大元组
  
        key = (args, tuple(sorted(kwargs.items())))  
		  
        if key in cache:  
            print("命中缓存", args, kwargs, key)  
            return cache[key]  
  
        # 未命中缓存  
        print('未命中缓存', args, kwargs, key)  
        res = func(*args, **kwargs)  
        cache[key] = res  
        return res  
  
    return wrapper  
  
  
@keywords_cache  
def cal_res(a, b, c='name', d='age'):  
    return c * a + d * b  


if __name__ == '__main__':  
    # print(cal_add(1, 2))  
    # print(cal_add(3, 4))    # print(cal_add(1, 2))  
    print(cal_res(2, 3, c='a', d='b'))  
    print(cal_res(2, 3, 'a', 'b'))  
    print(cal_res(4, 5, 'a', 'b'))  
    print(cal_res(2, 3, d='b', c='a'))  
    print(cal_res(a=2, b=3, d='b', c='a'))
```

运行上述代码后, 结果为:
```plaintext
未命中缓存 (2, 3) {'c': 'a', 'd': 'b'} ((2, 3), (('c', 'a'), ('d', 'b')))
aabbb
未命中缓存 (2, 3, 'a', 'b') {} ((2, 3, 'a', 'b'), ())
aabbb
未命中缓存 (4, 5, 'a', 'b') {} ((4, 5, 'a', 'b'), ())
aaaabbbbb
命中缓存 (2, 3) {'d': 'b', 'c': 'a'} ((2, 3), (('c', 'a'), ('d', 'b')))
aabbb
未命中缓存 () {'a': 2, 'b': 3, 'd': 'b', 'c': 'a'} ((), (('a', 2), ('b', 3), ('c', 'a'), ('d', 'b')))
aabbb
```

## 2.3 完整版（对标官方 `functools.cache`）

```python
import time  
from functools import wraps  


def complete_cache(func):  
    cache = {}  
    hits = 0  
    misses = 0  
  
    @wraps(func)  # 保留原函数的 name, docstring 等元信息  
    def wrapper(*args, **kwargs):  
        # 声明使用外层的变量  
        nonlocal hits, misses  
  
        key = (args, tuple(sorted(kwargs.items())))  
  
        if key in cache:  
            hits += 1  
            return cache[key]  
  
        misses += 1  
        res = func(*args, **kwargs)  
        cache[key] = res  
        return res  
  
    def cache_info():  
        return f'hits: {hits}, misses: {misses}, current size: {len(cache)}'  
  
    def cache_clear():  
        nonlocal hits, misses  
        cache.clear()  
        hits = 0  
        misses = 0  
  
    # 将方法绑定到 wrapper 函数上  
    wrapper.cache_info = cache_info  
    wrapper.cache_clear = cache_clear  
  
    return wrapper  
  
  
if __name__ == '__main__':  
    @complete_cache  
    def fibonacci(n):  
        """计算斐波那契数列"""  
        if n < 2:  
            return n  
        return fibonacci(n - 1) + fibonacci(n - 2)  
  
  
    need_cal_num = 50  
  
    print(f"1-函数名: {fibonacci.__name__}")  
    print(f"1-缓存状态: {fibonacci.cache_info()}")  
  
    print(f"执行前状态: {fibonacci.cache_info()}")  
  
    start = time.time()  
    print(fibonacci(need_cal_num))  
    print('第一次计算耗时:', time.time() - start)  
  
    start_ = time.time()  
    print(fibonacci(need_cal_num))  
    print('第二次计算耗时:', time.time() - start_)  
  
    print(f"2-函数名: {fibonacci.__name__}")  
    print(f"2-缓存状态: {fibonacci.cache_info()}")  
  
    fibonacci.cache_clear()  
    print(f"清空后状态: {fibonacci.cache_info()}")
```

输出结果：

```plaintext
1-函数名: fibonacci
1-缓存状态: hits: 0, misses: 0, current size: 0
执行前状态: hits: 0, misses: 0, current size: 0
12586269025
第一次计算耗时: 6.651878356933594e-05
12586269025
第二次计算耗时: 2.3126602172851562e-05
2-函数名: fibonacci
2-缓存状态: hits: 49, misses: 51, current size: 51
清空后状态: hits: 0, misses: 0, current size: 0
```

---

```python
print(6.651878356933594e-05 / 2.3126602172851562e-05)
# 2.8762886597938144
```

可以看出来，使用 `cache` 能够使得计算速度快两倍左右

## 2.4 `@lru_cache`

Python 的 `@lru_cache` 是一个非常实用的装饰器，用于实现**缓存（`Memoization`）**，它基于 **`LRU（Least Recently Used，最近最少使用）`** 策略来管理缓存。

### 2.4.1 实现原理

在 Python 的 `functools` 模块中，`lru_cache` 的底层实现（CPython 版本）主要依赖于两个核心数据结构：

1. **哈希表**：用于存储缓存数据。Python 中的字典就是基于哈希表实现的，查找速度是 O(1)。通过将函数的参数作为 `key`，函数的返回值作为 `value`，可以实现快速的缓存命中。

2. **双向链表**：用于维护访问顺序。
    - 每次访问（读取或写入）缓存中的某个数据时，该数据对应的节点会被移动到链表的头部（表示最近使用）。
    - 当缓存空间（`maxsize`）满了之后，需要淘汰数据时，链表尾部的节点（最近最少使用）就会被移除。

虽然 `CPython` 的底层是用 C 语言写的，但在 Python 层面，我们可以利用 `collections.OrderedDict` 来完美模拟这一行为。

- `OrderedDict` 会在维护字典键值对的同时，维护一个插入顺序。
- 关键方法 `move_to_end(key)` 可以将某个键值对移到末尾（代表最近使用）。
- 关键方法 `popitem(last=False)` 会弹出并移除最先插入的元素（代表最近最少使用）。

### 2.4.2 手动实现一个 `lru_cache`

下面是一个完整的、使用 `OrderedDict` 手动实现的 `lru_cache` 装饰器。

这个实现包含了以下功能：

- 支持设置最大缓存数量 `maxsize`。
- 支持位置参数和关键字参数。
- 缓存未命中时自动调用原函数并存储结果。
- 缓存命中时更新顺序（移动到最新）。

```python
import time  
from functools import wraps  
from collections import OrderedDict  
  
  
def simple_cache(func):  
    cache = {}  
  
    def wrapper(*args):  
        # 如果参数在缓存中，那么直接返回结果即可  
        if args in cache:  
            print('命中缓存', *args)  
            return cache[args]  
  
        # 参数不在缓存中，需要调用函数计算并存入缓存  
        print('未命中缓存', *args)  
        result = func(*args)  
        cache[args] = result  
        return result  
  
    return wrapper  
  
  
def keywords_cache(func):  
    cache = {}  
  
    def wrapper(*args, **kwargs):  
        # 核心：如何将 args 和 kwargs 变成一个唯一且不可变的 key        # 1. 将 kwargs 按照键排序，变成元组，防止顺序不同导致 key 不同  
        # 2. 将 args 和排序后的 kwargs 拼成一个大元组  
  
        key = (*args, tuple(sorted(kwargs.items())))  
  
        if key in cache:  
            print("命中缓存", args, kwargs, key)  
            return cache[key]  
  
        # 未命中缓存  
        print('未命中缓存', args, kwargs, key)  
        res = func(*args, **kwargs)  
        cache[key] = res  
        return res  
  
    return wrapper  
  
  
def complete_cache(func):  
    cache = {}  
    hits = 0  
    misses = 0  
  
    @wraps(func)  # 保留原函数的 name, docstring 等元信息  
    def wrapper(*args, **kwargs):  
        # 声明使用外层的变量  
        nonlocal hits, misses  
  
        key = (args, tuple(sorted(kwargs.items())))  
  
        if key in cache:  
            hits += 1  
            return cache[key]  
  
        misses += 1  
        res = func(*args, **kwargs)  
        cache[key] = res  
        return res  
  
    def cache_info():  
        return f'hits: {hits}, misses: {misses}, current size: {len(cache)}'  
  
    def cache_clear():  
        nonlocal hits, misses  
        cache.clear()  
        hits = 0  
        misses = 0  
  
    # 将方法绑定到 wrapper 函数上  
    wrapper.cache_info = cache_info  
    wrapper.cache_clear = cache_clear  
  
    return wrapper  
  
  
def lru_cache(max_size: int = 128):  
    """手动实现的 lru_cache 装饰器  
  
    Args:        max_size (): 最大缓存数量，设为 0 则表示无限缓存  
    """  
    def decorator(func):  
        _cache = OrderedDict()  
  
        @wraps(func)  
        def wrapper(*args, **kwargs):  
            # 生成 key            # 注意: 参数必须可哈希。为了简单起见，这里直接将 args 和 kwargs 组合成元组  
            #   在标准库实现中，使用了更复杂的 make_key 函数来处理不同类型的参数  
            key = (args, frozenset(sorted(kwargs.items())))  
  
            if key in _cache:  
                _cache.move_to_end(key)  
                return _cache[key]  
  
            # 缓存未命中 存入缓存  
            res = func(*args, **kwargs)  
            _cache[key] = res  
  
            if max_size != 0 and len(_cache) > max_size:  
                # 移除最旧的一项  
                _cache.popitem(last=False)  
            return res  
  
        def cache_clear():  
            _cache.clear()  
  
        wrapper.cache_clear = cache_clear  
        wrapper.cache_info = lambda: f"size: {len(_cache)}"  
  
        return wrapper  
  
    return decorator  
  
  
if __name__ == '__main__':  
    # 应用我们手写的装饰器  
    @lru_cache(max_size=3)  
    def heavy_computation(x):  
        print(f"Computing {x}...")  
        time.sleep(1)  # 模拟耗时操作  
        return x * x  
  
  
    print(heavy_computation(1))  
  
    print(heavy_computation(1))  
  
    print(heavy_computation(2))  
  
    print(heavy_computation(3))  
  
    print(heavy_computation(1))  
  
    print(heavy_computation(4))  
  
    print(heavy_computation(2))  
  
    print(f"Cache info: {heavy_computation.cache_info()}")  
    heavy_computation.cache_clear() # 清空缓存
```

上述程序运行后输出结果:

```plaintext
Computing 1...
1
1
Computing 2...
4
Computing 3...
9
1
Computing 4...
16
Computing 2...
4
Cache info: size: 3
```


## 2.5 手动实现 `OrderedDict`

可以参考力扣第146题 [LRU 缓存](https://leetcode.cn/problems/lru-cache/)

```python
"""
lru cache 算法

此模块中的 LRUCache 使用自定义双向链表作为主要数据结构, 尾部存放最新的 key value 键值对.
当然可以选择在头部存放最新的 key value 键值对, 本模块的类 LRUCache 已经实现了 move_to_head 方法,能够很快速地实现.
"""


from functools import wraps  
  
  
class NodeNotIndependentException(Exception):  
	
    def __init__(self, msg):  
        super().__init__(msg)  
  
  
class ValueRemoveException(Exception):  
    def __init__(self, msg):  
        super().__init__(msg)  
  
  
class DLinkedListNode:  
    """双向链表结点，用于实现 LRU 缓存"""  
  
    def __init__(self, key=0, value=0):  
        self.value = value  
        self.key = key  
        self.next = None  
        self.prev = None  
  
  
class LRUCache:  
  
    def __init__(self, capacity: int = 128):  
        self._capacity = capacity  # 最大容量  
        self._size = 0  # 当前容量  
  
        self._cache_map = {}  
  
        # 伪头结点和伪尾结点  
        self._head = DLinkedListNode()  
        self._tail = DLinkedListNode()  
        self._head.next = self._tail  
        self._tail.prev = self._head  
  
    @property  
    def capacity(self):  
        return self._capacity  
  
    @property  
    def size(self):  
        return self._size  
  
    @property  
    def head(self):  
        return self._head  
  
    @property  
    def tail(self):  
        return self._tail  
  
    def __str__(self):  
        head = self._head  
        tail = self._tail  
  
        if head.next == tail:  
            return "LRUCache<{}>"  
  
        lst = []  
        p = head.next  
        while p != tail:  
            lst.append(p.value)  
            p = p.next  
        return f"object LRUCache<{lst}>"  
  
    def get(self, key):  
        if key not in self._cache_map:  
            return None  
        # 存在 将 key 移动到尾部  
        node = self._cache_map[key]  
  
        # 需要移动到末尾  
        self.move_to_tail(node)  
        return node.value  
  
    def put(self, key, value):  
        if key in self._cache_map:  
            node = self._cache_map[key]  
            node.value = value  
            self.move_to_tail(node)  
        else:  
            node = DLinkedListNode(key, value)  
            self.add_to_tail(node)  
            self._cache_map[key] = node  
            self._size += 1  
  
            if self._size > self._capacity:  
                rm_node = self.remove_head()  
                self._size -= 1  
                self._cache_map.pop(rm_node.key)  
  
    def move_to_tail(self, node):  
        if node.next != self._tail:  
            # 如果不是最后一个结点，才需要移动  
            self.remove_node(node)  
            self.add_to_tail(node)  
  
    def move_to_head(self, node):  
        if node.prev != self._head:  
            # 如果不是第一个结点，才需要移动  
            self.remove_node(node)  
            self.add_to_head(node)  
  
    def add_to_head(self, node):  
        if node.next or node.prev:  
            raise NodeNotIndependentException(  
                f'结点DLinkedListNode<{node.key}, {node.value}>的 next 指针或 prev 指针非空')  
        node.next = self._head.next  
        node.prev = self._head  
        node.next.prev = node  
        self._head.next = node  
  
    def add_to_tail(self, node):  
        if node.next or node.prev:  
            raise NodeNotIndependentException(  
                f'结点DLinkedListNode<{node.key}, {node.value}>的 next 指针或 prev 指针非空')  
        node.next = self._tail  
        node.prev = self._tail.prev  
        node.prev.next = node  
        self._tail.prev = node  
  
    def remove_node(self, node):  
        if node == self._tail or node == self._head:  
            raise ValueRemoveException('Can not remove head or tail node.')  
        node.prev.next = node.next  
        node.next.prev = node.prev  
        node.next = None  
        node.prev = None  
  
    def remove_head(self):  
        node = self._head.next  
        if node == self._tail:  
            raise ValueRemoveException('Can not remove tail node.')  
        self._head.next = node.next  
        node.next.prev = self._head  
        node.next = None  
        node.prev = None  
        return node  
  
    def remove_tail(self):  
        node = self._tail.prev  
        if node == self._head:  
            raise ValueRemoveException('Can not remove head node.')  
        node.prev.next = self._tail  
        self._tail.prev = node.prev  
        node.next = None  
        node.prev = None  
        return node  
  
    def _make_key(self, args, kwargs):  
        key = args  
  
        if kwargs:  
            key += tuple(sorted(kwargs.items()))  
        return key  
  
    def __call__(self, func):  
        @wraps(func)  
        def wrapper(*args, **kwargs):  
            key = self._make_key(args, kwargs)  
  
            if key in self._cache_map:  
                node = self._cache_map[key]  
                self.move_to_tail(node)  
                return node.value  
  
            result = func(*args, **kwargs)  
            self.put(key, result)  
  
            return result  
  
        # 将缓存实例挂载到 wrapper 函数上，方便外部访问（可选）  
        wrapper.cache = self  
        return wrapper
        
        
@LRUCache(capacity=3)  
def test_func(x, y):  
    print(f"Calculating {x} + {y}...")  
    return x + y  
  
  
if __name__ == "__main__":  
    print("--- Test 1 ---")  
    print(test_func(1, 2))  # 计算并缓存  
    print(test_func(1, 2))  # 命中缓存，不打印 Calculating  
    print("\n--- Test 2 ---")  
    print(test_func(2, 3))  # 计算  
    print(test_func(3, 4))  # 计算  
    print(test_func(4, 5))  # 计算，此时容量满，(1,2) 应该被移除  
  
    print("\n--- Test 3 (Check eviction) ---")  
    print(test_func(1, 2))  # 应该重新计算，因为之前被挤出去了
    
# 输出结果:
--- Test 1 ---
Calculating 1 + 2...
3
3

--- Test 2 ---
Calculating 2 + 3...
5
Calculating 3 + 4...
7
Calculating 4 + 5...
9

--- Test 3 (Check eviction) ---
Calculating 1 + 2...
3
```

注意:上述代码知识可以用, 但是在健壮性和工程性上有很大欠缺, 例如:

1. 未解决线程安全问题
   Python 的 `dict` 在 Python 3 及以后虽然是原子的，但上述实现中的 `get`、`put` 和 `__call__` 方法内部包含多个步骤（查表、移动节点、删除节点、释放内存），这些步骤不是原子操作。
	1. 链表损坏: 多个线程同时操作 `move_to_tail`, 会导致链表指针错乱, 造成结点丢失或死循环
	2. `KeyError`: 一个线程刚判断 `key in cache` 为 `True`, 还没来得及取值, 另一个线程却已经执行了淘汰逻辑将该 `key` 删除, 导致下一行取值时报错

2. 构造 `key` 的问题
	1. 不可哈希导致整个程序崩溃
	2. `sorted` 要求所有的 `value` 都要可比较, 如果 `value` 是不可比较对象, 会因类型不同无法比较而导致比较失败抛出异常.

3. 装饰器用于类方法上
	1. 内存泄漏风险: `self` 被包含在缓存的 `key` 中, 缓存对象持有 `self` 的引用, 如果 `self` 本身应该被销毁, 但由于缓存还在引用该对象, 于是导致 `self` 无法被垃圾回收.
	2. 缓存失效: 不同的实例调用同一个方法, 由于 `self` 不同, 它们无法共享缓存. 通常这可能不是预期的行为(也许这正是预期行为, 取决于需求).

4. `get` 返回值歧义: 如果缓存合法地存储了 `None`, 那么调用 `get('key')` 时如果返回 `None`, 调用者无法区分是 `缓存未命中 还是 缓存命中但是值为None`.

5. 性能还可优化: `sorted` 在每次 `__call__` 调用中都需进行一次, 如果调用 `__call__` 很频繁会导致性能损耗

针对上述问题的改进版本:

```python
import threading
from functools import wraps

class DLinkedListNode:
    def __init__(self, key=0, value=0):
        self.value = value
        self.key = key
        self.next = None
        self.prev = None

class LRUCache:
    def __init__(self, capacity: int = 128):
        self._capacity = max(0, capacity) # 防止负数
        self._size = 0
        self._cache_map = {}
        self._head = DLinkedListNode()
        self._tail = DLinkedListNode()
        self._head.next = self._tail
        self._tail.prev = self._head
        # 增加锁
        self._lock = threading.Lock()

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node):
        node.prev = self._tail.prev
        node.next = self._tail
        self._tail.prev.next = node
        self._tail.prev = node

    def _move_to_tail(self, node):
        self._remove_node(node)
        self._add_to_tail(node)

    def get(self, key):
        with self._lock:
            if key not in self._cache_map:
                return None # 或者抛出 KeyError
            node = self._cache_map[key]
            self._move_to_tail(node)
            return node.value

    def put(self, key, value):
        with self._lock:
            if key in self._cache_map:
                node = self._cache_map[key]
                node.value = value
                self._move_to_tail(node)
            else:
                # capacity 为 0 时不存储
                if self._capacity == 0:
                    return 
                    
                node = DLinkedListNode(key, value)
                self._cache_map[key] = node
                self._add_to_tail(node)
                self._size += 1

                if self._size > self._capacity:
                    removed = self._head.next
                    self._remove_node(removed)
                    self._cache_map.pop(removed.key, None)
                    self._size -= 1

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 简单的 Key 生成，注意不可哈希对象会报错
            try:
                key = args
                if kwargs:
                    # 这里依旧存在 sorted 的类型比较风险，
                    # 生产环境建议使用 repr() 或 str() 转换
                    key += tuple(sorted(kwargs.items()))
            except TypeError:
                # 降级处理：如果不支持排序或哈希，直接调用函数，不缓存
                return func(*args, **kwargs)
            
            result = self.get(key)
            if result is not None:
                return result
            
            # 双重检查锁（可选），或者直接计算
            # 这里简单处理：计算后 put
            result = func(*args, **kwargs)
            
            # 处理结果不可哈希的情况（虽然 value 不需要做 key，但保持一致性）
            self.put(key, result)
            return result
        
        wrapper.cache = self
        return wrapper
```
