---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-21 22:08:26 周五"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">queue</h1>  

----

# 一、`queue` 概览

## 1.1 `queue` 解决了什么问题

想象一个生活中的场景：**奶茶店排队**。

- 先来的人先拿到奶茶（**先进先出，FIFO**：First In, First Out）
- 后来的人排在队伍后面
- 店员（处理者）永远从队伍**最前面**拿订单

`queue` 模块就是把这个"排队"的概念搬进了 Python。

**那它解决了什么问题呢？**

直接用 `list` 也能模拟排队（`append` 入队、`pop(0)` 出队），但有两个大问题：

1. **不安全**：如果你有多个线程（比如多个店员同时接单），用 `list` 可能出现两个店员拿到同一个订单、或者订单凭空丢失的混乱情况。
2. **不方便**：`list.pop(0)` 每次都要把后面所有元素往前挪一格，队伍越长越慢。

`queue` 模块的核心价值：

- ✅ **线程安全**：多个线程同时读写也不会乱（底层自动加了"锁"，可以理解为每次只有一个线程能操作队列，操作完换下一个）
- ✅ **自带阻塞功能**：队列为空时 `get()` 会安静地等待，队列满时 `put()` 会安静地等待，不用你自己写"等待重试"的逻辑

> **一句话总结**：`queue` 是一个线程安全的、先进先出的数据结构，特别适合"一边生产数据、一边消费数据"的多线程场景。

## 1.2 示例

```python
import queue

q = queue.Queue()          # 创建一个先进先出队列

q.put("任务1")              # 入队：任务从队尾进入
q.put("任务2")
q.put("任务3")

print("当前队列长度:", q.qsize())        # 输出: 3

first = q.get()            # 出队：从队头取出
print("取出的元素:", first)              # 输出: 任务1
print("取出后队列长度:", q.qsize())      # 输出: 2

q.task_done()              # 标记：刚才取出的任务已处理完
print("队列是否为空:", q.empty())        # 输出: False

```

```python showLineNumbers
import queue, threading

q = queue.Queue(maxsize=5)     # 最多同时存 5 个元素

def producer():                # 生产者：负责往队列里放数据
    for i in range(3):
    d
        q.put(f"数据{i}")

def consumer():                # 消费者：负责从队列里取数据处理
    for _ in range(3):
        item = q.get()
        print(f"取到了 {item}")
        q.task_done()

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join()   # 等生产者线程结束
t2.join()   # 等消费者线程结束

```

**生产者-消费者模式**：一个（或多个）线程往队列放任务，另一个（或多个）线程从队列取任务处理。队列就像传送带，把两边解耦（互不直接依赖）。

## 1.3 常用方法和类速查表

| 名称                                    | 作用                                          |
| ------------------------------------- | ------------------------------------------- |
| `Queue(maxsize=0)`                    | 普通先进先出队列                                    |
| `LifoQueue`                           | 后进先出（这就是栈！Last In, First Out）               |
| `PriorityQueue`                       | 优先级队列，元素按优先级（值越小越先出）取出                      |
| `SimpleQueue`                         | 简化版 Queue，更快，但没有任务跟踪（没有 `task_done`/`join`） |
| `put(item, block=True, timeout=None)` | 入队，可设置阻塞和超时                                 |
| `put_nowait(item)`                    | 入队，不等待，满了直接抛 `Full` 异常                      |
| `get(block=True, timeout=None)`       | 出队，队列为空时默认阻塞等待                              |
| `get_nowait()`                        | 出队，不等待，空了直接抛 `Empty` 异常                     |
| `qsize()`                             | 大约的元素个数                                     |
| `empty()` / `full()`                  | 是否为空 / 是否已满                                 |
| `task_done()` / `join()`              | 任务完成标记 / 等待所有任务处理完                          |

## 1.4 适用性

**✅ 适合用 queue：**

- 多线程之间传数据（最典型场景）
- 生产者-消费者模型（爬虫分发 URL、日志写入、任务调度）
- 需要阻塞等待语义的场景（队列空了就等，有了再取）
- 需要优先级调度（`PriorityQueue`）

**❌ 不适合用 queue：**

- **单线程中单纯存数据**：没有多线程竞争，用 `list` 或 `collections.deque` 更轻快
- **需要随机访问/中间插入删除**：队列只能从两端操作，这种情况用 `list`
- **需要遍历查看所有元素**：queue 不支持索引和迭代，强行取出会破坏队列
- **需要持久化存储**：队列在内存里，程序结束就没了，考虑数据库或文件

## 1.5 常见的坑

1. **`empty()` 判断不可靠（检查-再操作）**

   ```python
   if not q.empty():       # ❌ 危险！判断完到 get 之间，别的线程可能把元素取走了
      item = q.get()
   ```

    正确做法：用 `get(timeout=...)` 或 `get_nowait()` + 捕获 `queue.Empty` 异常。

1. **忘了调用 `task_done()` 导致 `join()` 永远卡死**
   `q.join()` 会一直等到每个被 `get()` 出来的元素都调用了 `task_done()`。漏掉一个，程序就永久阻塞。
2. **`get()` 会真的把元素拿走**
   queue 没有 `peek()`（只看不取）方法。如果你想"看一眼队头但不拿出来"，标准库没有直接支持（可以用 `get()` 后再 `put()` 回去，但要小心顺序）。
3. **`qsize()`/`empty()` 在多线程下只是"近似值**
   拿到结果的瞬间可能已经变了，别用它做关键逻辑判断。
4. **queue 不能迭代、不能 len()**
   `for x in q` 和 `len(q)` 都会报错，这是它和 `deque`、`list` 的显著区别。

## 1.6 Python 中实现队列和栈的其他方式

| 方式                    | 栈                     | 队列                       | 特点                                                   |
| ----------------------- | ---------------------- | -------------------------- | ------------------------------------------------------ |
| `list`                  | ✅ `append()` + `pop()` | ⚠️ `pop(0)` 很慢            | 简单，但队列操作慢，且非线程安全                       |
| `collections.deque`     | ✅ `append()` + `pop()` | ✅ `append()` + `popleft()` | **单线程首选**，两端操作都是 O(1)                      |
| `queue.LifoQueue`       | ✅                      | ❌                          | 线程安全的栈                                           |
| `queue.Queue`           | ❌                      | ✅                          | 线程安全的队列                                         |
| `multiprocessing.Queue` | ❌                      | ✅                          | **进程**间通信（多进程要用这个，不能用 `queue.Queue`） |
| `heapq`                 | ❌                      | 优先级队列                 | 自己实现优先队列，单线程高效                           |

> **记忆口诀**：单线程用 `deque`，多线程用 `queue.Queue`，多进程用 `multiprocessing.Queue`。

## 1.7 初学者的误解

**误解 1：“`queue` 和 `list`、`deque` 差不多，随便选一个就行”**
❌ 它们解决的是**不同的问题**。`queue` 的核心卖点是**线程安全 + 阻塞等待**。单线程里用它纯属浪费（还有额外开销）；多线程里用 `list` 则是事故现场。

**误解 2：“`get()` 之后数据还在队列里，只是被标记取出了”**
❌ 恰恰相反：`get()` 是**真正移除**元素，取出来就没了。很多人以为 `task_done()` 是"删除元素"，其实它只是打了个"已完成"的标记，用于配合 `join()` 计数。

**误解 3：“队列先进先出，栈后进先出，所以两者毫无关系”**
❌ 它们其实是同一棵树上的两根枝：`queue` 模块里就有 `LifoQueue`（栈）。栈 = 只从同一端进出（后进的先出），队列 = 从两端进出（先进的先出）。理解了这一点，看到 `LifoQueue` 就不会陌生了。

## 1.8 检查理解

### 1.8.1 **第 1 题（概念辨析）**

你的同事说：“我写了一个单线程的脚本，只是想按顺序处理一批发票数据，所以我用了 `queue.Queue`，因为队列就是用来按顺序处理数据的。”
请指出他理解上偏差在哪里，以及你会推荐他用什么替代。

> 他的理解没有问题，但是有偏差；`queue.Queue()` 当然可以按顺序处理数据，这和队列的先进先出的特性是吻合的，但是问题是，`queue.Queue()` 的个核心在于解决多线程的同步问题，而不是解决顺序处理问题，如果要解决顺序处理问题，用内置的 `list` 即可解决，而且更加轻量级。

批改：✅

**你答对的核心**：

- `queue.Queue` 的灵魂是**线程安全**，不是"按顺序处理" ✓
- 单线程场景用它等于为用不上的功能付出额外开销 ✓
- 推荐更轻量的替代 ✓

**两个可以更好的地方**：

1. **表述**："他的理解没有问题，但是有偏差"这句话有点绕。更清晰的说法是：*他说的功能上没错（队列确实按序处理），但选型判断错了——单线程不需要为"线程安全"买单。*

2. **替代方案可以更精确**：

   - 如果只是**遍历处理**一批发票：`list` 完全够用 ✓（你说的对）
   - 如果需要**模拟队列的进/出**（从头部取）：`list.pop(0)` 是 O(n)，`collections.deque.popleft()` 是 O(1)，此时 `deque` 更好

   面试或博客里能主动区分这两种情况，会显得理解更深。

### 1.8.2 **第 2 题（运行结果推理）**

不看代码运行结果，请写出下面程序的输出，并解释为什么 `join()` 没有导致程序卡死（或者卡死了，为什么）：

```python
import queue, threading

q = queue.Queue()

def worker():
    item = q.get()
    print(f"处理了 {item}")
    q.task_done()

t = threading.Thread(target=worker)
t.start()
q.put("订单A")
q.join()
print("全部完成")

```

> 运行结果：
>处理了 订单A
> 全部完成
>
> `join` 只是等待线程运行结束，而不是阻塞。

批改：❌

**输出完全正确** ✓：`处理了 订单A` → `全部完成`

**但解释是错的**。你写的：

> `join` 只是等待线程运行结束，而不是阻塞。

这里你把**两个不同的 `join`** 搞混了：

|                 | `t.join()`（Thread 的） | `q.join()`（Queue 的）                                       |
| --------------- | ----------------------- | ------------------------------------------------------------ |
| 属于谁          | 线程对象                | 队列对象                                                     |
| 干什么          | 等**线程**结束          | **阻塞**，直到队列里每个被 `get()` 走的元素都收到 `task_done()` 信号 |
| 支持 timeout 吗 | ✅ 支持                  | ❌ 不支持（直接报 `TypeError`）                               |

代码里写的是 **`q.join()`**，它**确实是阻塞的**。它没卡死的原因是：

> 队列内部有一个计数器（`unfinished_tasks`）：`put()` 时 +1，`task_done()` 时 -1。`q.join()` 的逻辑就是"阻塞等这个计数器归零"。worker 里 `get()` 之后调用了 `task_done()`，计数归零，`join()` 放行。

把 `task_done()` 删掉后，worker 线程**早就结束了**，但执行 `q.join()` 的线程 3 秒后依然卡着——如果 `q.join()` 是在"等线程结束"，线程都结束了它早该返回了。它等的是 `task_done` 信号。

把 `q.join()` 换成 `t.join()`，本题输出会变吗？
答：输出一样，但机制完全不同。如果 worker 是 `while True` 死循环消费，`q.join()` 在队列清空后能返回，`t.join()` 则永远等不到——这就是两种 join 的本质区别。

### 1.8.3 **第 3 题（机制理解）**

小明说：“`empty()` 返回 `False` 说明队列里有东西，所以紧接着调用 `q.get()` 一定能取到元素，不会卡住。”
请判断这个说法是否正确，并从"多线程环境下两次调用之间可能发生什么"的角度解释原因。

> 这个说法是错误的，因为调用 `empty()` 后也能队列中的数据被其他进程取走，所以不一定能取到元素，可能会卡住。
>
> 多线程环境下，A 线程调用 `empty()` 后可能切换到 B 线程，如果A 线程调用时候队列只有一个元素，此时 `empty` 当然是 `False`，切换到 B 线程是，B 线程也可以获取 `empty()`，此时也为 `False`，于是 B取走队列中唯一的元素处理，此时切换回 A 进程，A 线程调用 `get` 发现没有队列为空会一直阻塞，就会出现问题。

批改：✅

**全部要点都答到了**：

- 判断说法错误 ✓
- 场景推演完整且严谨：A 检查非空 → 切换到 B → B 取走唯一元素 → 切回 A → `get()` 空队列无限阻塞 ✓
- 这正是经典的"**先检查、再行动**"竞态问题：检查和行动之间隔了一个"其他线程可以插手的空隙" ✓

**两个小笔误**（不影响得分）：

- “A 进程” → 应为 “A **线程**”。进程和线程是两回事：`multiprocessing` 里才是进程，这里都是线程。
- “队列中的数据被其他进程取走**也能**” → “也有可能”。

**补充正确写法**（博客里值得写）：

```python
import queue

try:
    item = q.get(timeout=1)      # 最多等 1 秒
except queue.Empty:
    print("队列空了，先干别的")

```

或者 `q.get_nowait()` + 捕获 `queue.Empty`。核心思想：**把"检查"和"取"合并成一次原子操作，不给其他线程插手的空隙**。

## 1.9 总结与建议

你对 queue 的**场景判断**（第 1 题）和**竞态条件**（第 3 题）掌握得很扎实，第 3 题的推演甚至达到了能给别人讲明白的水平。

唯一的薄弱点：**`q.join()` / `task_done()` 的配对机制**——这恰恰是我上次提到的坑 #2，实战中最容易造成"程序莫名其妙卡死却不报错"的问题。建议：

1. 亲手做个实验：写一个生产者-消费者程序，故意删掉 `task_done()`，观察 `join()` 卡死；再加回来，观察恢复——做过一次就终身难忘；
2. 写博客时，把"**`Thread.join` 和 `Queue.join` 同名不同义**"单独作为一个小节，这是很多教程都没讲清的点，也是你这次的真实踩坑记录，很有价值。

# 二、深入了解

## 2.1 queue 的深层作用

它不是"容器"，是"协调器"

入门时我们说"queue 是线程安全的队列"。这个说法没错，但它掩盖了本质：**`queue.Queue` 不是一个"装数据的容器"，而是一套"线程之间的协调系统"**。它同时干着四件事：

作用 1：安全传递 —— 数据不丢、不重、不乱

多个线程同时读写时，靠内部那把锁（Lock，可以理解为"卫生间门锁"：进去就锁门，别人排队等）保证每次操作完整。这是你已经掌握的部分，不展开。

作用 2：节奏协调 —— 背压（这是最容易被忽略的杀手锏）

**背压**：当消费者处理不过来时，压力"反向"传导给生产者，让它自动放慢速度——不需要你写任何"队列太长了就 sleep 一下"的代码。

作用 3：解耦缓冲 —— 两边互不认识

生产者和消费者不需要知道对方是谁、有几个、速度多快。队列像工厂流水线之间的**暂存区**：

- 生产快、消费慢 → 队列先攒着（削峰填谷）
- 生产慢、消费快 → 消费者自动等待（就是 `get()` 的阻塞）
- 想从 1 个消费者扩到 5 个 → 生产者代码**一行都不用改**（后面项目实战会演示）

作用 4：完成通知 —— "活干完了"本身也是信息

`join()/task_done()` 解决的问题是：主线程怎么知道"所有任务都处理完了"？自己数数？加锁查计数器？queue 把这件事做成了标准原语。

内部解剖：Queue 到底是什么？

```
q = queue.Queue()
print(type(q.queue))      # <class 'collections.deque'>   ← 存数据的是 deque！
print(type(q.mutex))      # <class '_thread.lock'>        ← 一把锁
print(type(q.not_empty))  # <class 'threading.Condition'> ← "非空"信号
print(type(q.not_full))   # <class 'threading.Condition'> ← "未满"信号
```

所以一个 `Queue` = **deque（干活的）+ Lock（保安全的）+ 两个 Condition（管等待的）**。

> **条件变量**：一种"睡觉 + 叫醒"机制。线程没活干时调用 `wait()` 去**睡觉（不耗 CPU）**，条件满足时别人调用 `notify()` 把它叫醒。

`put()` 和 `get()` 的核心逻辑简化后只有几行：

```python
# put() 的简化逻辑
with 锁:
    while 队列已满:
        not_full.wait()        # 释放锁，睡觉，等"有空位"的信号
    deque.append(item)         # 真正存数据
    not_empty.notify()         # 叫醒一个在等"有数据"的线程

# get() 的简化逻辑
with 锁:
    while 队列为空:
        not_empty.wait()       # 释放锁，睡觉，等"有数据"的信号
    item = deque.popleft()     # 真正取数据
    not_full.notify()          # 叫醒一个在等"有空位"的线程

```

大局观：queue.Queue 是消息队列的"单机教具版"

**缓冲、背压、解耦、削峰填谷**——这四个词正是 Kafka、RabbitMQ、Celery 这些分布式消息队列的核心思想。`queue.Queue` 是它们的单机迷你版。学会它，将来接触任何消息中间件，你会发现**概念完全是同一套，只是规模变了**。这也是它值得深学的根本原因。

## 2.2 queue vs deque

不是竞争关系，是上下游关系

**`Queue` 的轮子里装的正是 `deque`**。所以它们的对比不是"谁更好"，而是"裸发动机 vs 装好安全系统的整车"。

性能实测：

| 方式                | 总耗时                      | 平均单次  | 复杂度   |
| ------------------- | --------------------------- | --------- | -------- |
| `collections.deque` | 8.93 ms                     | 0.089 µs  | O(1)     |
| `queue.Queue`       | 248.79 ms                   | 2.488 µs  | O(1)     |
| `list.pop(0)`       | N=5k: 1.7ms → N=20k: 27.1ms | 随 N 恶化 | **O(n)** |

三个结论：

- `deque` 比 `Queue` 快约 **28 倍**——代价是每次操作都要加锁、发信号（安全不免费）
- `list` 做队列是陷阱：N 翻 4 倍，耗时翻 **16 倍**（1.7ms → 27.1ms），标准的平方级恶化
- 但 2.5 µs/次的 `Queue` 绝对不算慢——瓶颈通常在任务本身（网络、磁盘），不在队列

功能对比表

| 维度               | `queue.Queue`                  | `collections.deque`                        |
| ------------------ | ------------------------------ | ------------------------------------------ |
| **定位**           | 并发协调工具                   | 纯数据结构（双端队列）                     |
| **线程安全**       | ✅ 官方文档保证                 | ❌ 不保证（见下方深坑）                     |
| **队列空时取**     | 阻塞等待 / 抛异常，任你选      | 直接抛 `IndexError`                        |
| **队列满时放**     | 阻塞等待（背压）               | 没有满的概念，无限增长                     |
| **完成通知**       | ✅ `join()/task_done()`         | ❌ 无                                       |
| **遍历 / `len()`** | ❌ 都不行                       | ✅ 可迭代、可 `len()`                       |
| **双端操作**       | ❌ 只能一头进另一头出           | ✅ 两头都能进出（所以它既能当栈又能当队列） |
| **性能**           | 慢（加锁成本）                 | 极快                                       |
| **跨进程**         | ❌ 要用 `multiprocessing.Queue` | ❌                                          |

一个高级深坑：`deque` 碰巧"看起来"线程安全

有人说：“CPython 里 `deque.append()` 和 `popleft()` 都是**原子操作**（不可分割、其他线程无法插队打断的操作），所以我用 deque 做线程通信也没出过错。”

在传统 CPython 里这话**碰巧成立**——因为 **GIL**（全局解释器锁：Python 同一时刻只允许一个线程执行字节码）恰好让单个 `append`/`popleft` 不可分割。但即便如此，也不能用 deque 替代 Queue 做线程通信，理由有四：

1. **单个操作原子 ≠ 组合逻辑原子**。“队列为空就等待”= 判断 + 行动两步，中间就能被插队（你上次第 3 题答对的那种竞态）
2. **没有阻塞语义**：空了只能抛异常，你得自己写重试循环
3. **没有 `maxsize` 背压**：内存保护要自己造
4. **没有 `join/task_done`**：完成检测要自己造

而且 GIL 依赖是实现细节——Python 3.13 起官方提供了**无 GIL 的 free-threaded 版本**，那种环境下 deque 的"碰巧安全"就不成立了。**官方保证的才算数**，`queue.Queue` 的线程安全是文档承诺，deque 的只是巧合。

选择法则：

> [!Important]
>
> **单线程用 `deque`，多线程用 `queue.Queue`，多进程用 `multiprocessing.Queue`。**

## 2.3 实际项目应用场景

多线程批量任务处理器

场景：批量压缩 20 张图片。单张压缩耗时不同、可能失败重试，用 3 个 worker 并行处理。这是**爬虫 URL 调度、日志批处理、Excel 导入**等场景的通用骨架。

```
import queue, threading, time, random

task_q = queue.Queue(maxsize=5)   # ① 有界队列：缓冲区最多积压 5 个任务
NUM_WORKERS = 3
SENTINEL = object()               # ② 哨兵：一个特殊值，约定含义为"没任务了，下班"
done_count = 0
counter_lock = threading.Lock()   # ③ 保护共享计数器

def worker(name):
    global done_count
    while True:
        task = task_q.get()                     # 队列空则睡觉等待，不空转烧 CPU
        if task is SENTINEL:                    # 收到下班信号
            task_q.task_done()
            break
        time.sleep(random.uniform(0.03, 0.1))   # 模拟压缩耗时
        with counter_lock:                      # 多个 worker 同时写计数器，必须加锁
            done_count += 1
            n = done_count
        print(f"  {name} 完成 {task}（进度 {n}/20）")
        task_q.task_done()                      # 汇报：这个任务处理完了

# 启动 3 个 worker
workers = [threading.Thread(target=worker, args=(f"worker-{i+1}",), daemon=True)
           for i in range(NUM_WORKERS)]
for w in workers:
    w.start()

# 生产端：投递 20 个任务
for i in range(20):
    task_q.put(f"图片{i:02d}.jpg")              # 队列满时自动阻塞 → 内存不会被撑爆

task_q.join()                                   # 等所有任务 task_done（你上次踩的坑，这里用对了）

for _ in range(NUM_WORKERS):                    # 每人发一个哨兵，优雅关闭
    task_q.put(SENTINEL)
task_q.join()
for w in workers:
    w.join()                                    # 确认线程真的退出了
print(">>> 程序正常退出")

```

五个设计要点：

| 设计                        | 体现的作用/知识点                                            |
| --------------------------- | ------------------------------------------------------------ |
| ① `maxsize=5`               | **背压**：就算生产端瞬间来 10 万个任务，内存也只占 5 个的量  |
| ② 哨兵 `SENTINEL`           | **优雅关闭**的经典手法：用特殊值通知 worker 退出。比 `daemon=True` 强杀优雅，worker 能善后 |
| ③ `counter_lock`            | queue 管队列安全，**共享计数器还得你自己加锁**——queue 不是万能保险箱 |
| `while True` + 阻塞 `get()` | worker 没活时**睡觉**而不是轮询（空转查队列会烧 CPU）        |
| 两次 `join()`               | 第一次等任务完成，第二次等哨兵消费完——正是上次你混淆的 `q.join()` 机制的正确应用 |

这个骨架在真实项目里是什么

- 把"图片"换成"URL" → **多线程爬虫**的任务分发器
- 把 worker 换成"攒一批就写数据库" → **日志采集系统**
- 把队列搬到另一台机器 → 这就是 **Kafka 消费者** 的雏形
- 加上任务持久化和重试 → 这就是 **Celery**（Python 著名任务队列库）的核心思想

## 2.4 官方推荐文档

第 1 站：queue 模块文档（主推，必读）

📖 `https://docs.python.org/3/library/queue.html`

页面不长，重点精读三处：

1. **`put()` 和 `get()` 的参数说明**——`block` 和 `timeout` 的每一种组合会发生什么、抛什么异常，这是阻塞语义的权威定义
2. **`SimpleQueue` 与 `Queue` 的差异段落**——什么时候可以放弃 `task_done` 换性能
3. **优先级队列的示例**——注意元组 `(priority, data)` 中"同优先级时按第二个元素排序"的坑（数据不可比较会报错）

第 2 站：threading 文档的 Condition Objects 小节

📖 `https://docs.python.org/3/library/threading.html#condition-objects`

你已经知道 `Queue` 内部靠 Condition 实现等待/唤醒（实验 A 证明过）。读这一节能彻底看懂 `wait()/notify()`——读完再回看第一部分那两段伪代码，会有"原来如此"的体验。**为什么用 `while` 而不是 `if` 来检查条件**（答案关键词：虚假唤醒）是这一节最值钱的知识点。

第 3 站：源码 `Lib/queue.py`（终极推荐）

Python 标准库源码里最友好的一份：**纯 Python、约 300 行**。核心的 `put()/get()/task_done()/join()` 加起来不到 100 行，且每行你都已具备理解它的知识。读源码时重点找三样东西：锁在哪里获取、两个 Condition 在哪里 `wait`/`notify`、`unfinished_tasks` 计数器如何被 `join` 使用。读完后你对 queue 的理解会超过绝大多数教程作者——这正好达到你"能教别人"的目标。

延伸站：multiprocessing 的队列文档

📖 `https://docs.python.org/3/library/multiprocessing.html#exchanging-objects-between-processes`

多进程版队列，接口几乎一样但底层完全不同（靠管道+序列化传数据）。知道"多进程不能直接用 `queue.Queue`"的原因即可，暂时不必深入。

给你的下一步建议

1. **动手改造实战项目**：给上面的 worker 加上"任务失败自动重试 3 次"的逻辑（提示：失败时 `task_q.put(task)` 放回去，注意重试计数放哪）
2. **写博客**：这次内容正好构成一篇高质量文章《queue.Queue 深度解析：它不是容器，是协调器》——"内部解剖实验 + 性能对比数据 + `deque` 原子性误区"这三块都是网上教程少见的干货
3. 学有余力可以了解 `concurrent.futures.ThreadPoolExecutor`——它是"queue + worker 线程池"的官方封装，理解了今天的原理后再看它会非常轻松

# 三、生产者-消费者模型

```python
import threading
import queue
import time
import random

# 创建有界队列：maxsize 限制缓冲区大小，防止生产过快撑爆内存
q = queue.Queue(maxsize=5)

# 哨兵对象：用于通知消费者"没有更多任务了"
SENTINEL = object()

def producer(name, count):
    """生产者：生产 count 个任务放入队列"""
    for i in range(count):
        item = f"{name}-任务{i}"
        q.put(item)          # 队列满时自动阻塞，直到消费者腾出空间
        print(f"[生产者 {name}] 放入: {item}，队列长度 {q.qsize()}")
        time.sleep(random.uniform(0.05, 0.2))  # 模拟生产耗时
    print(f"[生产者 {name}] 完成生产，退出")

def consumer(name):
    """消费者：循环取任务处理，收到哨兵后退出"""
    while True:
        item = q.get()       # 队列空时自动阻塞，直到有新数据
        if item is SENTINEL:
            q.put(SENTINEL)  # 把哨兵传给下一个消费者
            print(f"[消费者 {name}] 收到结束信号，退出")
            break
        print(f"[消费者 {name}] 处理: {item}")
        time.sleep(random.uniform(0.1, 0.3))  # 模拟处理耗时
        q.task_done()        # 标记任务已处理完成

if __name__ == "__main__":
    producers = [threading.Thread(target=producer, args=("P1", 5)),
                 threading.Thread(target=producer, args=("P2", 5))]
    consumers = [threading.Thread(target=consumer, args=(f"C{i}",), daemon=True)
                 for i in range(1, 4)]

    for t in producers + consumers:
        t.start()

    for p in producers:
        p.join()        # 1. 等所有生产者结束

    q.put(SENTINEL)     # 2. 发出结束信号
    q.join()            # 3. 等队列中所有任务处理完毕
    print("=== 全部完成 ===")

```





