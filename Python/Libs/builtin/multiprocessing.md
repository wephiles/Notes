---
tags:
  - type/tutorial
  - lang/Python
  - lange/Python/multiprocessing
  - domain/computer-science
  - domain/computer-science/basic
  - topic/study/multiprocessing
  - status/draft
  - source/
aliases:
description:
datetime: " 2026-09-05 13:09:64 周六"
author: wephiles
rating: "2"
introduction:
motto: 有志者，事竟成。破釜沉舟，百二秦关终属楚。苦心人，天不负。卧薪尝胆，三千越甲可吞吴。
---
[TOC]

<h1 style="text-align: center;">multiprocessing</h1>

----

# 1. multiprocessing

**multiprocessing** 是 Python 标准库中用于创建和管理多个进程的模块。它提供了一个类似于 `threading` 模块的 `API`，但使用的是**进程（process）**而不是线程（**thread**）。

**核心特点：**

1. **绕过 GIL 限制**：由于 Python 有全局解释器锁（GIL），多线程在 CPU 密集型任务中无法真正并行。`multiprocessing` 通过创建独立进程，每个进程有自己的 Python 解释器和 GIL，从而实现真正的并行计算。
2. **进程隔离**：每个进程有独立的内存空间，进程间不共享变量。
3. **跨平台**：支持 `Windows`、`Linux`、`macOS` 等多种操作系统。

# 2. 如何使用

## 2.1 基本用法

```
import multiprocessing
import time

def worker(name):
    print(f"Worker {name} 开始工作")
    time.sleep(1)
    print(f"Worker {name} 完成工作")

if __name__ == '__main__':
    # 创建进程
    p1 = multiprocessing.Process(target=worker, args=('A',))
    p2 = multiprocessing.Process(target=worker, args=('B',))
    
    # 启动进程
    p1.start()
    p2.start()
    
    # 等待进程结束
    p1.join()
    p2.join()
    
    print("主进程结束")
```

## 2.2 使用 Pool（进程池）

```python
import multiprocessing

def square(x):
    return x * x
	
if __name__ == '__main__':
    # 创建进程池
    with multiprocessing.Pool(processes=4) as pool:
        # map: 并行处理
        results = pool.map(square, [1, 2, 3, 4, 5])
        print("Map 结果:", results)
        
        # apply_async: 异步提交单个任务
        result = pool.apply_async(square, (10,))
        print("Async 结果:", result.get())
        
        # imap: 惰性求值
        for item in pool.imap(square, [6, 7, 8]):
            print("IMap 结果:", item)
```

## 2.3 进程间通信

### 2.3.1 Queue

```python
import multiprocessing

def producer(queue):
    for i in range(5):
        queue.put(f"消息 {i}")

def consumer(queue):
    while True:
        item = queue.get()
        if item == 'STOP':
            break
        print(f"消费: {item}")

if __name__ == '__main__':
    q = multiprocessing.Queue()
    
    p1 = multiprocessing.Process(target=producer, args=(q,))
    p2 = multiprocessing.Process(target=consumer, args=(q,))
    
    p1.start()
    p2.start()
    
    p1.join()
    q.put('STOP')  # 发送停止信号
    p2.join()

```

### 2.3.2 Pipe

```python
import multiprocessing

def send(pipe):
    pipe.send(["Hello", "from", "sender"])
    pipe.close()

if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()
    
    p = multiprocessing.Process(target=send, args=(child_conn,))
    p.start()
    
    print(parent_conn.recv())  # ['Hello', 'from', 'sender']
    p.join()

```

### 2.3.3 Shared Memory

```
import multiprocessing

def modify_value(shared_val, shared_arr):
    shared_val.value = 100
    for i in range(len(shared_arr)):
        shared_arr[i] = i * 2

if __name__ == '__main__':
    value = multiprocessing.Value('i', 0)  # 整数
    array = multiprocessing.Array('i', [0, 0, 0, 0, 0])  # 整数数组
    
    p = multiprocessing.Process(target=modify_value, args=(value, array))
    p.start()
    p.join()
    
    print("Value:", value.value)
    print("Array:", list(array))

```

## 2.4 锁的使用

```
import multiprocessing

def worker(lock, shared_val):
    with lock:
        for _ in range(100000):
            shared_val.value += 1

if __name__ == '__main__':
    lock = multiprocessing.Lock()
    value = multiprocessing.Value('i', 0)
    
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=worker, args=(lock, value))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print("最终值:", value.value)  # 应该是 400000

```

# 3. 使用过程注意事项

| 注意事项                        | 说明                                                 |
| ------------------------------- | ---------------------------------------------------- |
| **`if __name__ == '__main__'`** | Windows 下必须使用，否则会无限创建子进程             |
| **全局变量不共享**              | 每个进程有独立的内存空间，全局变量修改不影响其他进程 |
| **可 pickle 的对象**            | 传递给子进程的对象必须能被序列化                     |
| **资源清理**                    | 使用完 Queue、Pipe 等要正确关闭                      |
| **进程数量限制**                | 不要创建过多进程，一般设置为 CPU 核心数              |

# 4. 常见陷阱

忘记将进程代码写到  `if __name__ == '__main__'` 块中。

```
# ❌ 错误写法（Windows 下会崩溃）
import multiprocessing

def worker():
    print("Working")

p = multiprocessing.Process(target=worker)
p.start()  # Windows 下会报错或无限循环
p.join()
```

共享全局变量的陷阱

```
# ❌ 这样不会按预期工作
import multiprocessing

counter = 0

def increment():
    global counter
    counter += 1
    print(f"子进程中的 counter: {counter}")

if __name__ == '__main__':
    processes = []
    for _ in range(3):
        p = multiprocessing.Process(target=increment)
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"主进程中的 counter: {counter}")  # 仍然是 0

```

不可 pickle 的对象

```python
# ❌ Lambda 函数无法 pickle
with multiprocessing.Pool() as pool:
    pool.map(lambda x: x**2, [1, 2, 3])  # 报错

# ✅ 正确写法
def square(x):
    return x ** 2

with multiprocessing.Pool() as pool:
    pool.map(square, [1, 2, 3])
```

死锁问题

```python
# ❌ 可能死锁的写法
import multiprocessing

def worker(lock, queue):
    lock.acquire()
    queue.put(1)
    # 如果这里出异常，锁不会释放！
    lock.release()

# ✅ 使用 with 语句
def worker(lock, queue):
    with lock:
        queue.put(1)
```

Pool 的 map 参数问题

```
# ❌ 多个参数需要用 starmap
def func(a, b):
    return a + b

with multiprocessing.Pool() as pool:
    # pool.map(func, [(1,2), (3,4)])  # 报错！
    results = pool.starmap(func, [(1,2), (3,4)])  # ✅ 正确
```

没有正确处理异常

```
# 子进程中的异常不会传播到主进程
def worker(x):
    return 1 / x  # x=0 会报错

with multiprocessing.Pool() as pool:
    # 这个错误会被静默吞掉！
    results = pool.map(worker, [1, 2, 0, 4])
    print(results)  # 输出不完整，没有错误提示
```

# 5. 资源推荐

官方文档

| 资源                                 | 链接                                                      |
| ------------------------------------ | --------------------------------------------------------- |
| Python 官方文档 - multiprocessing    | https://docs.python.org/3/library/multiprocessing.html    |
| Python 官方文档 - concurrent.futures | https://docs.python.org/3/library/concurrent.futures.html |

进阶资源

| 资源                                                    | 说明                 |
| ------------------------------------------------------- | -------------------- |
| Real Python - Multiprocessing                           | 实战教程，有大量示例 |
| Python Cookbook - 并发编程                              | 经典书籍的并发章节   |
| Effective Python - 第55章 “考虑使用 concurrent.futures” | 介绍更现代的并发 API |

# 6. 总结

| 方面     | 要点                                                 |
| -------- | ---------------------------------------------------- |
| 核心概念 | 绕过 GIL，实现真正的并行计算                         |
| 基本用法 | Process、Pool、Queue、Pipe、Value/Array              |
| 关键注意 | `if __name__ == '__main__'`、变量不共享、pickle 限制 |
| 常见坑   | 全局变量、死锁、异常处理、参数传递                   |
| 进阶学习 | concurrent.futures、joblib、dask                     |
