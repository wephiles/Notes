## 一、为什么切片比 for 循环快？

一句话总结：**切片是在 C 语言层面用 `memcpy`（内存拷贝）一次性搬数据的，而 for 循环是 Python 解释器逐个元素搬运的。**

我们来看一个直观的性能对比：

```
import time

data = list(range(1_000_000))

# ========== for 循环 ==========
start = time.perf_counter()
new_data = [None] * len(data)
for i in range(len(data)):
    new_data[i] = data[i]
print(f"for 循环耗时: {time.perf_counter() - start:.4f} 秒")

# ========== 切片 ==========
start = time.perf_counter()
new_data = data[:]
print(f"切片耗时:   {time.perf_counter() - start:.4f} 秒")
for 循环耗时: 0.0452 秒
切片耗时:   0.0003 秒
```

**切片比 for 循环快了约 150 倍。** 原因如下：

### 切片的底层实现（CPython 源码解析）

Python 的切片操作最终会调用 CPython 底层的 `list_ass_slice` 函数。它的大致执行流程是：

```
用户代码: self._data[2:5] = [10, 20]
        │
        ▼
┌─────────────────────────────────────────┐
│  Python 解释器 (字节码: STORE_SUBSCR)    │
│  解析出: 源列表、起始位置(2)、结束位置(5)   │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  C 层: list_ass_slice()                 │
│                                         │
│  1. 计算需要移动的元素个数               │
│  2. 调用 memmove() 腾出/压缩空间         │
│     ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐              │
│     │ │ │x│x│x│ │ │ │ │ │  ← 原数组     │
│     └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘              │
│              ↓ memmove (CPU指令级搬移)    │
│     ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐              │
│     │ │ │?│?│?│←│←│←│ │ │  ← 腾出空间    │
│     └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘              │
│  3. 调用 memcpy() 写入新数据              │
│     ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐              │
│     │ │ │10│20│←│←│←│ │ │ │  ← 写入完成  │
│     └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘              │
└─────────────────────────────────────────┘
```

关键在于 **`memmove` / `memcpy`** 这两个 C 标准库函数：

- 它们是操作系统/CPU 级别的操作，直接对内存地址进行批量搬移
- CPU 有专门的指令（如 `rep movsb`）来加速连续内存的拷贝
- 中间**没有任何 Python 对象的创建、引用计数的增减、类型检查等开销**

### for 循环的底层实现

```
用户代码:
for i in range(len(data)):
    new_data[i] = data[i]

        │
        ▼
每一次循环，解释器都要重复执行以下全部步骤:
        │
        ▼
┌──────────────────────────────────────────┐
│  第 N 次迭代 (共执行 N 次！):              │
│                                          │
│  ① 从 range 对象取出当前 i 值             │
│  ② 对 data 进行 __getitem__(i) 调用       │
│     - 检查 i 是否越界                     │
│     - 查找 data[i] 的内存地址             │
│     - 将该元素的引用计数 +1               │
│  ③ 对 new_data 进行 __setitem__(i, val)  │
│     - 检查 i 是否越界                     │
│     - 将旧值的引用计数 -1 (可能触发GC)    │
│     - 写入新值，引用计数 +1               │
│  ④ 更新循环变量 i                         │
│  ⑤ 检查是否循环结束                       │
│                                          │
│  以上每一步都需要经过:                     │
│  Python字节码 → 帧求值 → C函数调用 → 返回  │
└──────────────────────────────────────────┘
```

**核心差距就是一个数字：**



| 对比项            | for 循环                        | 切片                     |
| ----------------- | ------------------------------- | ------------------------ |
| Python/C 切换次数 | **N 次**（每个元素一次）        | **1 次**（整个操作一次） |
| 边界检查次数      | **2N 次**（get+set 各检查一次） | **1 次**                 |
| 引用计数操作      | **2N 次**                       | 底层批量处理             |
| 执行层面          | Python 字节码解释执行           | CPU 直接操作内存         |

> **形象比喻**：for 循环就像是你**一粒一粒地用筷子搬沙子**，每搬一粒还要登记一次；切片就像是叫了一辆**挖掘机**，一铲子就搬完了。

## 二、Python 中还有哪些操作能显著提升效率？

核心原则只有一个：**尽量把工作交给 C 层去做，减少 Python 解释器的介入。**

### 1. 列表/字典推导式 替代 for 循环

```
# ❌ 慢：解释器循环
result = []
for x in range(1000000):
    result.append(x * 2)

# ✅ 快：C 层预分配 + 批量执行
result = [x * 2 for x in range(1000000)]
```

**为什么快？**

- 推导式在 CPython 内部有专门的字节码（`LIST_APPEND`），绕过了 `list.append()` 的方法查找开销
- 列表大小可以预先计算，一次性分配好内存，避免了反复扩容

### 2. 内置函数替代手写逻辑

```
# ❌ 慢：手写求和
total = 0
for x in data:
    total += x

# ✅ 快：内置函数 sum() 是 C 实现的
total = sum(data)

# ❌ 慢：手写找最大值
max_val = data[0]
for x in data:
    if x > max_val:
        max_val = x

# ✅ 快
max_val = max(data)

# ❌ 慢：手写判断是否存在
found = False
for x in data:
    if x == target:
        found = True
        break

# ✅ 快
found = target in data
```

**内置函数**（`sum`, `max`, `min`, `any`, `all`, `map`, `filter`）都是纯 C 实现的，它们迭代数据时的开销远远小于 Python 层的 for 循环。

### 3. 字符串的 `join()` 替代 `+=` 拼接

```
# ❌ 慢：每次 += 都会创建一个新的字符串对象（O(N²)）
result = ""
for word in words:
    result += word

# ✅ 快：一次性计算总长度，分配一次内存（O(N)）
result = "".join(words)
```

这是经典的字符串拼接优化，`join()` 会先遍历一次计算总长度，然后一次分配内存，最后用 `memcpy` 把所有字符串复制过去。

### 4. 集合（set）替代列表做查找

```
# ❌ 慢：列表查找是 O(N)
if item in my_list:      # 最坏情况遍历整个列表
    ...

# ✅ 快：集合查找是 O(1)
if item in my_set:       # 哈希表直接定位
    ...
```



| 操作       | list  | set      | dict     |
| ---------- | ----- | -------- | -------- |
| `x in ...` | O(N)  | **O(1)** | **O(1)** |
| 插入       | O(1)* | **O(1)** | **O(1)** |
| 删除       | O(N)  | **O(1)** | **O(1)** |

> *list 尾部插入是 O(1)，中间插入是 O(N)

### 5. 使用 `collections.deque` 替代列表做 队列操作

```
from collections import deque

# ❌ 慢：list 的 pop(0) 是 O(N)，要把后面所有元素前移
my_list.pop(0)

# ✅ 快：deque 是双向链表，两端的 append/pop 都是 O(1)
my_deque = deque([1, 2, 3])
my_deque.popleft()       # O(1)
my_deque.appendleft(0)   # O(1)
```

### 6. 使用 `locals()` 缓存频繁访问的方法

```
# ❌ 稍慢：每次循环都要查找 append 方法
for x in data:
    result.append(x)

# ✅ 稍快：把方法引用缓存到局部变量，减少属性查找
result_append = result.append
for x in data:
    result_append(x)
```

在极热路径下（百万次循环以上），这个优化能带来约 10%~20% 的提升。

### 7. 生成器（Generator）节省内存

```
# ❌ 一次性生成所有数据，占用大量内存
def get_all_numbers(n):
    return [x * x for x in range(n)]  # 一次性返回 100 万个元素的列表

# ✅ 惰性求值，每次只产生一个值，内存占用 O(1)
def get_all_numbers(n):
    for x in range(n):
        yield x * x                    # 每次只 yield 一个值
```

> 这个优化**不提速，甚至略微降速**，但它能把内存占用从 GB 级降到 KB 级，避免程序因内存不足被系统杀死。

### 总结一张图

```
┌─────────────────────────────────────────────────────┐
│              Python 性能优化层级金字塔                  │
│                                                     │
│                      ▲                               │
│                     / \    4. 算法与数据结构选择        │
│                    /   \   (O(N) vs O(N²))           │
│                   /─────\                            │
│                  /       \  3. 用对数据结构             │
│                 /         \ (set 做查找, deque 做队列)  │
│                /───────────\                         │
│               /             \ 2. 用对操作              │
│              /               \(切片/join/内置函数/推导式)│
│             /─────────────────\                      │
│            /                   \ 1. 避免低级错误        │
│           /                     \(循环中拼接字符串等)   │
│          /───────────────────────\                    │
└─────────────────────────────────────────────────────┘
```

**一句话口诀**：能用 C 做的就不要用 Python 做，能用 O(1) 的就不要用 O(N)，能一次分配的就不要反复分配。



# 还有哪些操作可以提高Python程序的运行速度





## 一、变量作用域优化

### 局部变量访问 远快于 全局变量

Python 在执行函数时，局部变量是通过**数组下标**（偏移量）来访问的，而全局变量需要通过**字典查找**。这在底层字节码中对应 `LOAD_FAST` 和 `LOAD_GLOBAL` 两条指令：

```
import math

# ❌ 慢：每次循环都走 LOAD_GLOBAL（字典查找）
def compute_slow(n):
    result = 0
    for i in range(n):
        result += math.sqrt(i)   # 每次都要去全局命名空间找 math
    return result

# ✅ 快：提前缓存为局部变量，走 LOAD_FAST（数组下标直接取）
def compute_fast(n):
    result = 0
    sqrt = math.sqrt              # 只做一次全局查找
    for i in range(n):
        result += sqrt(i)         # 之后全是局部变量访问
    return result
```

对应字节码对比：

```
# 慢版本每次循环的指令:
  LOAD_GLOBAL    0 (math)        # 1. 在全局字典中查找 math
  LOAD_ATTR      1 (sqrt)        # 2. 在 math 中查找 sqrt
  LOAD_FAST      2 (i)           # 3. 取局部变量 i
  CALL_FUNCTION  1                # 4. 调用

# 快版本每次循环的指令:
  LOAD_FAST      3 (sqrt)        # 1. 直接取局部变量 sqrt（一步到位！）
  LOAD_FAST      2 (i)           # 2. 取局部变量 i
  CALL_FUNCTION  1                # 3. 调用
```

**快了将近 30%~40%**，在极热路径上非常可观。

## 二、数据结构的选择

### 1. `tuple` 替代 `list`（数据不可变时）

```
# ❌ 列表：可变对象，额外维护一个动态数组结构
point = [10, 20, 30]

# ✅ 元组：不可变，内存更紧凑，创建和访问都更快
point = (10, 20, 30)
import sys
print(sys.getsizeof([1, 2, 3]))    # 88 字节
print(sys.getsizeof((1, 2, 3)))    # 72 字节
```

元组的优势：

- **内存占用更小**：不需要维护"动态扩容"的那套机制
- **创建更快**：不需要分配额外的弹性空间
- **可以作为字典的 key**：因为不可变，是可哈希的
- **Python 内部大量使用元组**：函数参数打包 `*args`、多返回值等

> **原则**：只要数据创建后不需要修改，就用 `tuple`。

### 2. `array.array` 替代 `list`（存储大量同类型数值时）

```
import array

# ❌ list：每个元素都是一个完整的 Python 对象（int 对象头 + 值）
# 存储 100 万个整数大约占用 28MB
nums_list = [i for i in range(1_000_000)]

# ✅ array：底层是 C 连续数组，和 C 的 int[] 一样
# 存储 100 万个整数大约占用 4MB
nums_array = array.array('i', range(1_000_000))
#                       ^
#                  'i' = signed int (4字节)
#                  'd' = double    (8字节)
#                  'f' = float     (4字节)
```



| 存储内容      | list 内存 | array 内存 | 节省    |
| ------------- | --------- | ---------- | ------- |
| 100万个 int   | ~28 MB    | ~4 MB      | **85%** |
| 100万个 float | ~28 MB    | ~8 MB      | **71%** |

### 3. `frozenset` 替代 `set`（用作字典 key 或集合元素时）

```
# ❌ set 是可变的，不能放进另一个 set，也不能做 dict 的 key
my_set = {1, 2, 3}
# {{1,2}, {3,4}}     → TypeError!
# {{1,2}: "value"}   → TypeError!

# ✅ frozenset 是不可变的，可以嵌套、可以当 key
a = frozenset([1, 2])
b = frozenset([3, 4])
nested = {a, b}                 # ✅ 嵌套集合
mapping = {a: "group_a",        # ✅ 当字典 key
           b: "group_b"}
```

## 三、对象与内存优化

### `__slots__` —— 大幅减少对象内存

默认情况下，Python 每个实例都有一个 `__dict__`（字典），用来动态存储属性。字典的内存开销很大：

```
# ❌ 正常写法：每个实例都带一个 __dict__
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# ✅ __slots__：告诉 Python "只有这三个属性，不要 __dict__"
class Point:
    __slots__ = ('x', 'y', 'z')     # 固定属性列表
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
import sys

p1 = Point(1, 2, 3)   # 没有 __slots__
p2 = Point(1, 2, 3)   # 有 __slots__

print(sys.getsizeof(p1.__dict__))   # 104 字节（__dict__ 本身的大小！）
print(sys.getsizeof(p2))            # 48 字节（整个对象就这么大）
```



| 对比              | 无 `__slots__` | 有 `__slots__`       |
| ----------------- | -------------- | -------------------- |
| 单个对象          | ~152 字节      | **~48 字节**         |
| 创建 100 万个对象 | ~152 MB        | **~48 MB**           |
| 属性访问速度      | 慢（字典查找） | **快（固定偏移量）** |
| 能否动态添加属性  | ✅ 可以         | ❌ 不可以             |

> **适用场景**：需要创建大量小对象时（如游戏中的粒子、图中的节点、数据库中的行）。

## 四、缓存与记忆化

### `functools.lru_cache` —— 用空间换时间

对于**纯函数**（相同输入永远返回相同输出），可以用缓存避免重复计算：

```
from functools import lru_cache

# ❌ 慢：每次都重新计算
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# fibonacci(35) → 2.8 秒
# fibonacci(40) → 34 秒（指数级爆炸！）

# ✅ 快：加上缓存装饰器
@lru_cache(maxsize=None)    # maxsize=None 表示缓存无上限
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# fibonacci(35) → 0.00003 秒
# fibonacci(1000) → 0.001 秒（瞬间完成！）
```

**原理**：`lru_cache` 内部维护了一个字典，以函数参数为 key，返回值为 value。调用时先查字典，命中就直接返回。

```
# 也可以用于耗时 I/O 或复杂计算的结果缓存
@lru_cache(maxsize=1024)
def get_user_info(user_id: int):
    """缓存最多 1024 个用户的查询结果"""
    return database.query(user_id)
```

## 五、字符串处理

### 1. `f-string` 是最快的格式化方式

```
name, age = "Alice", 25

# 慢 → 快 排序：
"%s is %d" % (name, age)              # 最老的方式，较慢
"{} is {}".format(name, age)           # format 方法，中等
f"{name} is {age}"                     # f-string，最快！
```

f-string 快的原因是：它在**编译阶段**就完成了表达式解析，运行时直接求值和拼接，不需要额外的格式化解析开销。

### 2. `str.startswith()` / `str.endswith()` 替代切片判断

```
url = "https://www.example.com"

# ❌ 稍慢：先切片（创建新字符串），再比较
if url[:8] == "https://" :
    ...

# ✅ 更快：底层 C 直接比较，不创建新字符串
if url.startswith("https://") :
    ...
```

## 六、查找与搜索

### `bisect` 模块 —— 有序列表上的二分查找

```
import bisect

# ❌ 线性查找 O(N)
def find_insert_pos(sorted_list, value):
    for i, v in enumerate(sorted_list):
        if v >= value:
            return i
    return len(sorted_list)

# ✅ 二分查找 O(log N)
pos = bisect.bisect_left(sorted_list, value)    # 返回应该插入的位置
bisect.insort(sorted_list, value)               # 插入并保持有序
```



| 数据规模      | 线性查找 | 二分查找 |
| ------------- | -------- | -------- |
| 1,000         | 微秒级   | 微秒级   |
| 1,000,000     | 毫秒级   | 微秒级   |
| 1,000,000,000 | 秒级     | 微秒级   |

## 七、并发与并行

### CPU 密集型任务 —— `multiprocessing`

由于 Python 的 **GIL（全局解释器锁）**，多线程无法利用多核 CPU 做并行计算：

```
┌─────────────────────────────────────────────────┐
│  Python GIL 限制示意                              │
│                                                  │
│  多线程 (threading):                              │
│  ┌───┐ ┌───┐ ┌───┐                               │
│  │ T1│ │ T2│ │ T3│  ──→  只有一个线程能持有 GIL   │
│  └─┬─┘ └─┬─┘ └─┬─┘     其他线程全部等待！         │
│    │     │     │          本质还是"交替执行"        │
│    ▼     ▼     ▼          不是真正的并行           │
│  ┌────────────────┐                              │
│  │   单核 CPU     │                              │
│  └────────────────┘                              │
│                                                  │
│  多进程 (multiprocessing):                        │
│  ┌───┐ ┌───┐ ┌───┐                               │
│  │ P1│ │ P2│ │ P3│  ──→  每个进程有独立的 GIL     │
│  └─┬─┘ └─┬─┘ └─┬─┘     互不干扰，真正并行！       │
│    │     │     │                                   │
│    ▼     ▼     ▼                                   │
│  ┌───┐ ┌───┐ ┌───┐                               │
│  │核1│ │核2│ │核3│                                │
│  └───┘ └───┘ └───┘                               │
└─────────────────────────────────────────────────┘
from multiprocessing import Pool

# ❌ 单进程：处理 1000 万条数据
def process_single(data):
    return [heavy_compute(x) for x in data]

# ✅ 多进程：自动分配到多个 CPU 核心
def process_parallel(data):
    with Pool(processes=4) as pool:       # 4 个进程 = 4 核并行
        return pool.map(heavy_compute, data)
```



| 任务类型                         | 推荐方案                     | 原因                  |
| -------------------------------- | ---------------------------- | --------------------- |
| CPU 密集型（计算、图像处理）     | **multiprocessing**          | 绕过 GIL，真正并行    |
| I/O 密集型（网络请求、文件读写） | **threading** 或 **asyncio** | 等待 I/O 时会释放 GIL |

## 八、终极武器

### NumPy 向量化 —— 数值计算的降维打击

当你需要处理大量数值运算时，NumPy 能带来 **100 倍甚至 1000 倍** 的性能提升：

```
import numpy as np

data = list(range(1_000_000))

# ❌ Python 原生循环
result = []
for x in data:
    result.append(x ** 2 + x * 3 + 1)

# ✅ NumPy 向量化（一行搞定）
arr = np.array(data, dtype=np.int64)
result = arr ** 2 + arr * 3 + 1
Python 循环：  320 ms
NumPy 向量化：   3 ms    ← 快了 100 倍
```

**为什么 NumPy 这么快？**

```
Python 循环执行过程:
┌──────┐     ┌──────────┐     ┌──────────┐
│ x=0  │ ──→ │ 0²+0*3+1 │ ──→ │ append(1)│  ← Python 层循环 100 万次
│ x=1  │ ──→ │ 1²+1*3+1 │ ──→ │ append(5)│
│ x=2  │ ──→ │ 2²+2*3+1 │ ──→ │ append(11)│
│ ...  │ ──→ │   ...    │ ──→ │   ...   │
└──────┘     └──────────┘     └──────────┘

NumPy 向量化执行过程:
┌──────────────────────────────────────────────────────┐
│  Python → 把整块数据交给 NumPy (只跨越一次 Python/C 边界) │
│       │                                              │
│       ▼                                              │
│  ┌────────────────────────────────────────────┐      │
│  │  C 层：                                    │      │
│  │  ┌─────┬─────┬─────┬─────┬─────┬───┐       │      │
│  │  │  0  │  1  │  2  │ ... │999K │   │       │      │
│  │  └──┬──┴──┬──┴──┬──┴─────┴──┬──┴───┘       │      │
│  │     │     │     │         │               │      │
│  │     ▼     ▼     ▼         ▼               │      │
│  │  CPU SIMD 指令同时处理一批数据               │      │
│  │  (一条指令算 4~8 个数)                       │      │
│  └────────────────────────────────────────────┘      │
│       │                                              │
│       ▼                                              │
│  返回结果给 Python（一次）                              │
└──────────────────────────────────────────────────────┘
```

## 全部优化技巧速查表

```
┌──────────────────────────────────────────────────────────────┐
│                   Python 性能优化速查表                        │
├──────────────┬───────────────────────────────────────────────┤
│  类别         │  优化技巧                                     │
├──────────────┼───────────────────────────────────────────────┤
│ 循环与迭代    │ 切片代替 for 循环搬运元素                       │
│              │ 列表推导式代替 for + append                     │
│              │ 内置函数 (sum/max/min/any/all) 代替手写循环     │
│              │ 局部变量缓存全局变量/方法引用                    │
├──────────────┼───────────────────────────────────────────────┤
│ 字符串       │ "".join() 代替 += 拼接                        │
│              │ f-string 代替 % 和 .format()                  │
│              │ startswith/endswith 代替切片比较               │
├──────────────┼───────────────────────────────────────────────┤
│ 数据结构     │ set/dict 代替 list 做"查找/去重"  O(N)→O(1)   │
│              │ deque 代替 list 做"队列"     O(N)→O(1)        │
│              │ tuple 代替 list (数据不可变时)                  │
│              │ array.array 代替 list (大量同类型数值)          │
│              │ bisect 二分查找代替线性查找   O(N)→O(log N)    │
├──────────────┼───────────────────────────────────────────────┤
│ 对象与内存    │ __slots__ 减少实例内存                         │
│              │ 生成器节省内存 (yield)                         │
│              │ frozenset 用于嵌套集合 / 字典 key               │
├──────────────┼───────────────────────────────────────────────┤
│ 缓存         │ @lru_cache 缓存纯函数结果                      │
├──────────────┼───────────────────────────────────────────────┤
│ 并发         │ multiprocessing 处理 CPU 密集型任务            │
│              │ asyncio / threading 处理 I/O 密集型任务        │
├──────────────┼───────────────────────────────────────────────┤
│ 终极武器     │ NumPy 向量化 (数值计算提速 100x+)               │
│              │ Cython / C 扩展 (极致性能)                     │
└──────────────┴───────────────────────────────────────────────┘
```

但最后一定要强调一点：**“过早优化是万恶之源”**。在实际开发中，先保证代码正确和可读，遇到真正的性能瓶颈时，再针对性使用这些技巧。