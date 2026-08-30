<h1 align="center">Python 程序性能优化指南</h1>
# 1. 为什么切片比 for 循环快
**一句话总结**：切片是在 C 语言层面用 `memcpy` 一次性搬数据，for 循环是 Python 解释器逐个元素搬运。
## 1.1 性能对比
```python
import time
data = list(range(1_000_000))
# for 循环
start = time.perf_counter()
new_data = [None] * len(data)
for i in range(len(data)):
    new_data[i] = data[i]
print(f"for 循环耗时: {time.perf_counter() - start:.4f} 秒")   # 0.0452 秒
# 切片
start = time.perf_counter()
new_data = data[:]
print(f"切片耗时: {time.perf_counter() - start:.4f} 秒")       # 0.0003 秒
```
**切片比 for 循环快约 150 倍。**
## 1.2 切片的底层实现
切片最终调用 CPython 底层的 `list_ass_slice` 函数：
```
用户代码: self._data[2:5] = [10, 20]
        │
        ▼
Python 解释器（字节码: STORE_SUBSCR）
解析出: 源列表、起始位置(2)、结束位置(5)
        │
        ▼
C 层: list_ass_slice()
  1. 计算需要移动的元素个数
  2. 调用 memmove() 腾出/压缩空间
  3. 调用 memcpy() 写入新数据
```
关键在 `memmove` / `memcpy` 两个 C 标准库函数：
- 操作系统/CPU 级别操作，直接对内存地址批量搬移
- CPU 有专门指令（如 `rep movsb`）加速连续内存拷贝
- 中间无 Python 对象创建、引用计数增减、类型检查等开销
## 1.3 for 循环的底层实现
每次循环，解释器都要重复执行全部步骤：
1. 从 range 对象取出当前 i 值
2. `data.__getitem__(i)`：越界检查、查找内存地址、引用计数 +1
3. `new_data.__setitem__(i, val)`：越界检查、旧值引用计数 -1（可能触发 GC）、写入新值
4. 更新循环变量 i，检查是否循环结束
每一步都经过：Python 字节码 → 帧求值 → C 函数调用 → 返回。
## 1.4 核心差距
| 对比项            | for 循环              | 切片             |
| ----------------- | --------------------- | ---------------- |
| Python/C 切换次数 | **N 次**              | **1 次**         |
| 边界检查次数      | 2N 次                 | 1 次             |
| 引用计数操作      | 2N 次                 | 底层批量处理     |
| 执行层面          | Python 字节码解释执行 | CPU 直接操作内存 |
> **比喻**：for 循环是一粒一粒用筷子搬沙子，每搬一粒还要登记；切片是一辆挖掘机，一铲子搬完。
# 2. 核心优化原则
**尽量把工作交给 C 层去做，减少 Python 解释器的介入。**
口诀：能用 C 做的就不要用 Python 做，能用 O(1) 的就不要用 O(N)，能一次分配的就不要反复分配。
# 3. 循环与迭代优化
## 3.1 推导式替代 for + append
```python
# ❌ 慢：解释器循环
result = []
for x in range(1000000):
    result.append(x * 2)
# ✅ 快：C 层预分配 + 批量执行
result = [x * 2 for x in range(1000000)]
```
原因：推导式有专门字节码 `LIST_APPEND`，绕过 `list.append()` 方法查找开销；大小可预先计算，一次性分配内存，避免反复扩容。
## 3.2 内置函数替代手写循环
```python
# ❌ 慢                     # ✅ 快
total = 0                   total = sum(data)
for x in data:
    total += x
max_val = data[0]           max_val = max(data)
for x in data:
    if x > max_val:
        max_val = x
found = False               found = target in data
for x in data:
    if x == target:
        found = True
        break
```
`sum`、`max`、`min`、`any`、`all`、`map`、`filter` 均为纯 C 实现，迭代开销远小于 Python 层 for 循环。
## 3.3 缓存方法引用到局部变量
```python
# ❌ 每次循环都查找 append 方法
for x in data:
    result.append(x)
# ✅ 把方法引用缓存为局部变量，减少属性查找
result_append = result.append
for x in data:
    result_append(x)
```
极热路径（百万次循环以上）可提升约 10%~20%。
# 4. 字符串处理
## 4.1 join() 替代 += 拼接
```python
# ❌ 慢：每次 += 都创建新字符串对象 O(N²)
result = ""
for word in words:
    result += word
# ✅ 快：一次计算总长度、分配一次内存 O(N)
result = "".join(words)
```
## 4.2 f-string 是最快的格式化方式
```python
name, age = "Alice", 25
"%s is %d" % (name, age)         # 最老，较慢
"{} is {}".format(name, age)     # 中等
f"{name} is {age}"               # 最快
```
f-string 在**编译阶段**完成表达式解析，运行时直接求值拼接，无额外格式化解析开销。
## 4.3 startswith/endswith 替代切片比较
```python
# ❌ 先切片（创建新字符串）再比较
if url[:8] == "https://": ...
# ✅ 底层 C 直接比较，不创建新字符串
if url.startswith("https://"): ...
```
# 5. 数据结构选择
## 5.1 set/dict 替代 list 做查找
```python
# ❌ O(N)                  # ✅ O(1)
if item in my_list: ...     if item in my_set: ...
```
| 操作       | list  | set      | dict     |
| ---------- | ----- | -------- | -------- |
| `x in ...` | O(N)  | **O(1)** | **O(1)** |
| 插入       | O(1)* | O(1)     | O(1)     |
| 删除       | O(N)  | O(1)     | O(1)     |
> *list 尾部插入 O(1)，中间插入 O(N)
## 5.2 deque 替代 list 做队列
```python
from collections import deque
my_list.pop(0)                 # ❌ O(N)，后面所有元素前移
my_deque = deque([1, 2, 3])    # ✅ 双向链表
my_deque.popleft()             # O(1)
my_deque.appendleft(0)         # O(1)
```
## 5.3 tuple 替代 list（数据不可变时）
```python
point = [10, 20, 30]   # ❌ 可变，额外维护动态数组结构
point = (10, 20, 30)   # ✅ 不可变，更紧凑
import sys
print(sys.getsizeof([1, 2, 3]))  # 88 字节
print(sys.getsizeof((1, 2, 3)))  # 72 字节
```
优势：内存更小（无动态扩容机制）、创建更快、可哈希（可作 dict key）；Python 内部大量使用元组（`*args`、多返回值）。
**原则**：数据创建后不需要修改，就用 tuple。
## 5.4 array.array 替代 list（大量同类型数值）
```python
import array
# ❌ list：每个元素都是完整 Python 对象，100 万 int 约 28 MB
nums_list = [i for i in range(1_000_000)]
# ✅ array：底层 C 连续数组，100 万 int 约 4 MB
nums_array = array.array('i', range(1_000_000))
# 'i' = signed int (4字节)，'d' = double (8字节)，'f' = float (4字节)
```
| 存储内容       | list   | array | 节省    |
| -------------- | ------ | ----- | ------- |
| 100 万个 int   | ~28 MB | ~4 MB | **85%** |
| 100 万个 float | ~28 MB | ~8 MB | **71%** |
## 5.5 frozenset 替代 set（作 key 或嵌套）
```python
# ❌ set 可变，不能嵌套、不能作 dict key
{ {1, 2}, {3, 4} }          # TypeError!
{ {1,2}: "value" }          # TypeError!
# ✅ frozenset 不可变
a, b = frozenset([1, 2]), frozenset([3, 4])
nested = {a, b}                              # 嵌套集合
mapping = {a: "group_a", b: "group_b"}       # 当字典 key
```
## 5.6 bisect 有序列表二分查找
```python
import bisect
# ❌ 线性查找 O(N)
def find_insert_pos(sorted_list, value):
    for i, v in enumerate(sorted_list):
        if v >= value:
            return i
    return len(sorted_list)
# ✅ 二分查找 O(log N)
pos = bisect.bisect_left(sorted_list, value)   # 返回应插入的位置
bisect.insort(sorted_list, value)              # 插入并保持有序
```
| 数据规模      | 线性查找 | 二分查找 |
| ------------- | -------- | -------- |
| 1,000         | 微秒级   | 微秒级   |
| 1,000,000     | 毫秒级   | 微秒级   |
| 1,000,000,000 | 秒级     | 微秒级   |
# 6. 变量作用域优化
局部变量访问**远快于**全局变量：局部变量通过数组下标访问（`LOAD_FAST`），全局变量需字典查找（`LOAD_GLOBAL`）。
```python
import math
# ❌ 每次循环走 LOAD_GLOBAL（字典查找）
def compute_slow(n):
    result = 0
    for i in range(n):
        result += math.sqrt(i)
    return result
# ✅ 提前缓存为局部变量，走 LOAD_FAST
def compute_fast(n):
    result = 0
    sqrt = math.sqrt   # 只做一次全局查找
    for i in range(n):
        result += sqrt(i)
    return result
```
字节码对比：
```python
# 慢版本每次循环:
LOAD_GLOBAL 0 (math)    # 全局字典查找
LOAD_ATTR 1 (sqrt)      # 属性查找
LOAD_FAST 2 (i)
CALL_FUNCTION 1
# 快版本每次循环:
LOAD_FAST 3 (sqrt)      # 直接取局部变量，一步到位
LOAD_FAST 2 (i)
CALL_FUNCTION 1
```
可提升约 30%~40%。
# 7. 对象与内存优化
## 7.1 \_\_slots\_\_ 减少实例内存
默认每个实例都有 `__dict__` 动态存储属性，内存开销大：
```python
# ❌ 每个实例带一个 __dict__
class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
# ✅ 固定属性列表，不创建 __dict__
class Point:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
import sys
p1 = Point(1, 2, 3)                # 无 __slots__
p2 = Point(1, 2, 3)                # 有 __slots__
print(sys.getsizeof(p1.__dict__))  # 104 字节（__dict__ 本身）
print(sys.getsizeof(p2))           # 48 字节
```
| 对比                                                         | 无 `__slots__` | 有 `__slots__`   |
| ------------------------------------------------------------ | -------------- | ---------------- |
| 单个对象                                                     | ~152 字节      | **~48 字节**     |
| 100 万个对象                                                 | ~152 MB        | **~48 MB**       |
| 属性访问速度                                                 | 慢（字典查找） | 快（固定偏移量） |
| 动态添加属性                                                 | ✅ 可以         | ❌ 不可以         |
| **适用场景**：需要创建大量小对象时（粒子、图节点、数据库行等）。 |                |                  |
## 7.2 生成器节省内存
```python
# ❌ 一次性生成 100 万元素的列表
def get_all_numbers(n):
    return [x * x for x in range(n)]
# ✅ 惰性求值，每次只产生一个值，内存占用 O(1)
def get_all_numbers(n):
    for x in range(n):
        yield x * x
```
> 此优化**不提速甚至略降速**，但能把内存占用从 GB 级降到 KB 级，避免程序因内存不足被系统杀死。
# 8. 缓存与记忆化
## 8.1 functools.lru_cache
对**纯函数**（相同输入永远返回相同输出）用缓存避免重复计算：
```python
from functools import lru_cache
# ❌ fibonacci(35) → 2.8 秒；fibonacci(40) → 34 秒（指数爆炸）
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
# ✅ fibonacci(35) → 0.00003 秒；fibonacci(1000) → 0.001 秒
@lru_cache(maxsize=None)   # maxsize=None 表示缓存无上限
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
# 也可缓存耗时 I/O 或复杂计算结果
@lru_cache(maxsize=1024)
def get_user_info(user_id: int):
    return database.query(user_id)
```
**原理**：内部维护字典，以函数参数为 key、返回值为 value，调用先查字典，命中直接返回。
# 9. 并发与并行
## 9.1 GIL 限制与 multiprocessing
Python 的 **GIL（全局解释器锁）** 使多线程无法利用多核 CPU 做并行计算：
```
多线程: T1 / T2 / T3 ──→ 只有一个线程持有 GIL，其余等待（本质交替执行，非真正并行）
多进程: P1 / P2 / P3 ──→ 每个进程有独立 GIL，互不干扰，真正并行（核1 / 核2 / 核3）
```
```python
from multiprocessing import Pool
# ❌ 单进程
def process_single(data):
    return [heavy_compute(x) for x in data]
# ✅ 多进程：自动分配到多个 CPU 核心
def process_parallel(data):
    with Pool(processes=4) as pool:   # 4 个进程 = 4 核并行
        return pool.map(heavy_compute, data)
```
## 9.2 任务类型选择
| 任务类型                         | 推荐方案                | 原因                  |
| -------------------------------- | ----------------------- | --------------------- |
| CPU 密集型（计算、图像处理）     | **multiprocessing**     | 绕过 GIL，真正并行    |
| I/O 密集型（网络请求、文件读写） | **threading / asyncio** | 等待 I/O 时会释放 GIL |
# 10. NumPy 向量化
处理大量数值运算时，NumPy 可带来 **100 倍甚至 1000 倍**提升：
```python
import numpy as np
data = list(range(1_000_000))
# ❌ Python 原生循环：320 ms
result = []
for x in data:
    result.append(x ** 2 + x * 3 + 1)
# ✅ NumPy 向量化（一行搞定）：3 ms
arr = np.array(data, dtype=np.int64)
result = arr ** 2 + arr * 3 + 1
```
**为什么快**：
```
Python 循环:   x=0 → 计算 → append ；x=1 → 计算 → append ；...
              （Python 层循环 100 万次，每次跨越 Python/C 边界）
NumPy:        Python 一次跨界，整块数据交给 C 层
              → C 层对连续内存批量运算（CPU SIMD 指令同时处理一批数据，一条指令算 4~8 个数）
              → 结果一次返回
```
# 11. 速查与总结
## 11.1 性能优化金字塔
```
              ▲
             / \   4. 算法与数据结构选择（O(N) vs O(N²)）
            /───\
           /     \  3. 用对数据结构（set 做查找，deque 做队列）
          /───────\
         /         \ 2. 用对操作（切片/join/内置函数/推导式）
        /───────────\
       /             \ 1. 避免低级错误（循环中拼接字符串等）
      /───────────────\
```
## 11.2 优化技巧速查表
| 类别       | 优化技巧                                                     |
| ---------- | ------------------------------------------------------------ |
| 循环与迭代 | 切片代替 for 搬运元素；推导式代替 for+append；内置函数代替手写循环；局部变量缓存全局变量/方法引用 |
| 字符串     | `"".join()` 代替 `+=`；f-string 代替 % 和 format；startswith/endswith 代替切片比较 |
| 数据结构   | set/dict 代替 list 做查找 O(N)→O(1)；deque 代替 list 做队列；tuple 代替 list（不可变时）；array.array 存大量同类型数值；bisect 二分查找 O(N)→O(log N) |
| 对象与内存 | `__slots__` 减少实例内存；生成器节省内存；frozenset 用于嵌套集合/字典 key |
| 缓存       | `@lru_cache` 缓存纯函数结果                                  |
| 并发       | multiprocessing 处理 CPU 密集型；asyncio/threading 处理 I/O 密集型 |
| 终极武器   | NumPy 向量化（数值计算提速 100x+）；Cython / C 扩展（极致性能） |
## 11.3 注意事项
**"过早优化是万恶之源"**。实际开发中先保证代码正确和可读，遇到真正的性能瓶颈时，再针对性使用这些技巧。