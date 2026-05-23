## 核心原理：GIL 与原子性

Python 的 **GIL（全局解释器锁）** 保证同一时刻只有一个线程执行 Python 字节码。但 GIL **会在每条字节码之间释放**，因此一个 Python 语句如果对应多条字节码，线程可能在中间被挂起，产生竞态条件。

## ✅ 线程安全的操作

### 1. 不可变对象的读取（天然安全）

```
# 以下类型不可变，读取永远线程安全
x = 1            # int
y = 3.14         # float  
s = "hello"      # str
t = (1, 2, 3)    # tuple
f = frozenset()  # frozenset
b = True         # bool
n = None         # NoneType
```

### 2. 简单赋值（单条 `STORE_NAME` 字节码，原子操作）

```
x = 1          # ✅ 原子：STORE_NAME
x = "hello"    # ✅ 原子：STORE_NAME
x = None       # ✅ 原子：STORE_NAME
```

> 字节码仅一条 `STORE_NAME`，GIL 不会在执行中途切换。

### 3. 列表的原子操作（C 语言层面保证）

```
lst = []
lst.append(x)     # ✅ 原子
lst.pop()         # ✅ 原子（从末尾弹出）
lst.pop(-1)       # ✅ 原子
lst[i]            # ✅ 原子（读取）
len(lst)          # ✅ 原子
```

### 4. 字典的原子操作

```
d = {}
d[key] = value    # ✅ 原子（STORE_SUBSCR）
d[key]            # ✅ 原子（读取）
key in d          # ✅ 原子
d.get(key)        # ✅ 原子
len(d)            # ✅ 原子
del d[key]        # ✅ 原子
```

### 5. 集合的原子操作

```
s = set()
s.add(x)          # ✅ 原子
s.discard(x)      # ✅ 原子
x in s            # ✅ 原子
len(s)            # ✅ 原子
```

### 6. `collections.deque` 的原子操作

```
from collections import deque
q = deque()
q.append(x)       # ✅ 原子
q.appendleft(x)   # ✅ 原子
q.pop()           # ✅ 原子
q.popleft()       # ✅ 原子
len(q)            # ✅ 原子
```

### 7. `queue` 模块（专为多线程设计）

```
from queue import Queue, LifoQueue, PriorityQueue

q = Queue()
q.put(item)       # ✅ 线程安全（内部有锁）
q.get()           # ✅ 线程安全
q.qsize()         # ✅ 线程安全
q.empty()         # ✅ 线程安全
```

### 8. `threading` 模块的同步原语（天然线程安全）

```
import threading

lock = threading.Lock()        # ✅ 互斥锁
rlock = threading.RLock()      # ✅ 可重入锁
semaphore = threading.Semaphore(n)  # ✅ 信号量
event = threading.Event()      # ✅ 事件
condition = threading.Condition()  # ✅ 条件变量
barrier = threading.Barrier(n)    # ✅ 栅栏
```

## ❌ 非线程安全的操作

### 1. `+=` / `-=` / `*=` 等复合赋值（读-改-写，非原子）

```
x = 0
x += 1  # ❌ LOAD + INPLACE_ADD + STORE（3条字节码）
# 字节码：
#   LOAD_NAME x
#   LOAD_CONST 1
#   INPLACE_ADD      ← GIL可能在这里切换！
#   STORE_NAME x
```

### 2. 检查后操作（Check-Then-Act）

```
if balance >= 100:    # 检查
    balance -= 100    # 操作 ❌ 之间可能被其他线程打断
```

### 3. 列表的非原子操作

```
lst[i] = x           # ✅ 原子
lst.sort()           # ❌ 非原子（多步操作）
lst.reverse()        # ❌ 非原子
if i < len(lst):     # ❌ 检查和访问之间可被打断
    lst[i]
lst.insert(0, x)     # ❌ 非原子
lst.remove(x)        # ❌ 非原子
```

### 4. 字典的非原子操作

```
for k, v in d.items():   # ❌ 迭代期间修改会出问题
    ...
d.update(other_dict)     # ❌ 非原子
d.setdefault(k, v)       # ❌ 非原子（检查+写入两步）
```

### 5. 集合的非原子操作

```
s.remove(x)          # ❌ 若x不存在会抛KeyError（非原子的查找+删除）
s.pop()              # ❌ 非原子
s.update(other)      # ❌ 非原子
```

## 🔧 如何保证线程安全

### 方法1：使用 `threading.Lock`

```
import threading

counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    with lock:
        counter += 1  # ✅ 现在安全了
```

### 方法2：使用 `queue.Queue`（生产者-消费者模式）

```
from queue import Queue

q = Queue()
# 多个线程安全地 put/get
q.put(item)
item = q.get()
```

### 方法3：使用 `collections.deque`（有限场景）

```
from collections import deque

q = deque()
# append/popleft 是原子的，适合简单的生产者-消费者
q.append(item)
item = q.popleft()
```

### 方法4：使用 `threading.local`（线程本地存储）

```
import threading

local_data = threading.local()
local_data.x = 1  # 每个线程有独立副本，无需加锁
```

## 📊 总结对照表



| 操作              | 线程安全？ | 原因                  |
| ----------------- | ---------- | --------------------- |
| `x = 1`           | ✅          | 单条字节码            |
| `x += 1`          | ❌          | 3条字节码（读-改-写） |
| `lst.append(x)`   | ✅          | C层面原子操作         |
| `lst[i]`          | ✅          | 原子操作              |
| `lst.sort()`      | ❌          | 多步操作              |
| `d[k] = v`        | ✅          | 原子操作              |
| `d[k]`            | ✅          | 原子操作              |
| `d.update()`      | ❌          | 多步操作              |
| `s.add(x)`        | ✅          | 原子操作              |
| `s.pop()`         | ❌          | 非原子                |
| `deque.append()`  | ✅          | 原子操作              |
| `Queue.put/get`   | ✅          | 内置锁保护            |
| `if cond: action` | ❌          | 检查与操作间可被打断  |
| 不可变对象读取    | ✅          | 不可变即安全          |

> ⚠️ **重要提醒**：即使某些操作在 CPython 实现中是原子的，这也属于**实现细节**而非语言规范保证。不同的 Python 实现（如 PyPy、Jython）行为可能不同。**在关键场景下，始终使用显式锁来保证线程安全。**