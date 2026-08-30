---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-15 09:08:36 周六"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">overview</h1>
# 1. 示例 1

```python
import time
import threading

text_to_write = """帝高阳之苗裔兮，朕皇考曰伯庸。摄提贞于孟陬兮，惟庚寅吾以降。皇览揆余初度兮，肇锡余以嘉名。名余曰正则兮，字余曰灵均。纷吾既有此内美兮，又重之以修能。扈江离与辟芷兮，纫秋兰以为佩。汩余若将不及兮，恐年岁之不吾与。朝搴阰之木兰兮，夕揽洲之宿莽。日月忽其不淹兮，春与秋其代序。惟草木之零落兮，恐美人之迟暮。(惟 通：唯)不抚壮而弃秽兮，何不改此度？(改此度 一作：改乎此度)乘骐骥以驰骋兮，来吾道夫先路！昔三后之纯粹兮，固众芳之所在。杂申椒与菌桂兮，岂惟纫夫蕙茝！彼尧舜之耿介兮，既遵道而得路。何桀纣之猖披兮，夫唯捷径以窘步。惟夫党人之偷乐兮，路幽昧以险隘。岂余身之惮殃兮，恐皇舆之败绩！忽奔走以先后兮，及前王之踵武。荃不察余之中情兮，反信谗而齌怒。余固知謇謇之为患兮，忍而不能舍也。指九天以为正兮，夫唯灵修之故也。曰黄昏以为期兮，羌中道而改路！初既与余成言兮，后悔遁而有他。余既不难夫离别兮，伤灵修之数化。余既滋兰之九畹兮，又树蕙之百亩。畦留夷与揭车兮，杂杜衡与芳芷。冀枝叶之峻茂兮，愿俟时乎吾将刈。虽萎绝其亦何伤兮，哀众芳之芜秽。众皆竞进以贪婪兮，凭不厌乎求索。羌内恕己以量人兮，各兴心而嫉妒。忽驰骛以追逐兮，非余心之所急。老冉冉其将至兮，恐修名之不立。朝饮木兰之坠露兮，夕餐秋菊之落英。苟余情其信姱以练要兮，长顑颔亦何伤。掔木根以结茝兮，贯薜荔之落蕊。(掔木 一作：揽木)矫菌桂以纫蕙兮，索胡绳之纚纚。謇吾法夫前修兮，非世俗之所服。虽不周于今之人兮，愿依彭咸之遗则。长太息以掩涕兮，哀民生之多艰。余虽好修姱以鞿羁兮，謇朝谇而夕替。既替余以蕙纕兮，又申之以揽茝。亦余心之所善兮，虽九死其犹未悔。怨灵修之浩荡兮，终不察夫民心。众女嫉余之蛾眉兮，谣诼谓余以善淫。固时俗之工巧兮，偭规矩而改错。背绳墨以追曲兮，竞周容以为度。忳郁邑余侘傺兮，吾独穷困乎此时也。宁溘死以流亡兮，余不忍为此态也。"""


def read_and_write(file_path: str, text: str, number: int = 0):
    with open(file_path, 'w', encoding='utf-8') as fp:
        for i in range(number):
            fp.write(text + '\n')


start = time.time()

read_and_write('./data/data_1.txt', text_to_write, number=5000)
read_and_write('./data/data_2.txt', text_to_write, number=5000)
read_and_write('./data/data_3.txt', text_to_write, number=5000)

print('单线程耗时:', time.time() - start)

start_multi = time.time()

text_list = [
    ('./data/mul_data_1.txt', text_to_write),
    ('./data/mul_data_2.txt', text_to_write),
    ('./data/mul_data_3.txt', text_to_write)
]

for path, text in text_list:
    t = threading.Thread(target=read_and_write, args=(path, text, 5000,))
    t.start()
    t.join()

print('多线程(伪)耗时:', time.time() - start_multi)

start_multi_real = time.time()

text_list = [
    ('./data/real_mul_data_1.txt', text_to_write),
    ('./data/real_mul_data_2.txt', text_to_write),
    ('./data/real_mul_data_3.txt', text_to_write)
]

threads = []

for path, text in text_list:
    t = threading.Thread(target=read_and_write, args=(path, text, 5000,))
    threads.append(t)
    t.start()

for td in threads:
    td.join()

print('多线程(真正)耗时:', time.time() - start_multi_real)
```

输出结果如下：
```
单线程耗时: 0.0373835563659668
多线程(伪)耗时: 0.0352938175201416
多线程(真正)耗时: 0.027052640914916992
```

计算一下单线程耗时是多线程的多少倍：
```
>>> python
>>> 0.0373835563659668 / 0.027052640914916992
1.3818819568685168
```

> **⚠️ 注意: 下面这样写是无法真正实现多线程的**:
>
> ```python
> for path, text in text_list:
>     t = threading.Thread(target=read_and_write, args=(path, text, 5000,))
>     t.start()
>     t.join()
> ```
>
> 因为在循环中 `t.start()` 后立马跟着 `t.join()`, `join` 的作用的等待线程运行完毕, 如果每个子线程启动后主线程都需要等待启动的子线程运行完再进行下一步操作,这样的话会导致多线程完全退化成单线程,无法实现真正的加速.

计算结果：

可以看出，IO密集型任务使用多线程有很好的提速效果。

# 2. 线程名称的设置和获取

```python
import threading


def task():
    name = threading.current_thread().name
    print(f'当前运行的子线程名: {name}.')


for i in range(3):
    t = threading.Thread(target=task)
    t.start()
```

输出结果:

```python
当前运行的子线程名: Thread-1 (task).
当前运行的子线程名: Thread-2 (task).
当前运行的子线程名: Thread-3 (task).
```

---

```python
import threading


def task():
    name = threading.current_thread().name
    print(f'当前运行的子线程名: {name}.')


for i in range(3):
    t = threading.Thread(target=task)
    t.name = f'test-thread-{i + 1}'
    t.start()
```

输出结果:

```python
当前运行的子线程名: test-thread-1.
当前运行的子线程名: test-thread-2.
当前运行的子线程名: test-thread-3.
```

# 3. 自定义线程类

直接将线程需要做的事放到 `run` 方法中。

```python
import threading


class MyThread(threading.Thread):
    def run(self):
        print(f'执行线程, 参数: {self._args}, 名称: {threading.current_thread().name}')


t1 = MyThread(args=(10, 20,))
t2 = MyThread(args=(100, 200,))
t3 = MyThread(args=(-10, -20,))
t1.start()
t2.start()
t3.start()
```

输出结果:

```python
执行线程, 参数: (10, 20), 名称: Thread-1
执行线程, 参数: (100, 200), 名称: Thread-2
执行线程, 参数: (-10, -20), 名称: Thread-3
```

---

示例:

```python
import threading
import requests


class DownloadVideoExampleThread(threading.Thread):
    def run(self):
        file_name, url = self._args
        res = requests.get(url)
        with open(file_name, 'wb') as fp:
            fp.write(res.content)


url_list = [
    ('xxx.mp4', 'https://www.baidu.com'),
    ('yyy.mp4', 'https://www.sougou.com'),
    ('zzz.mp4', 'https://www.cnblogs.com/'),
]

for item in url_list:
    t = DownloadVideoExampleThread(args=item)
    t.start()
```

# 4. 线程安全

## 4.1 锁

一个进程中可以有多个线程，且线程共享所有进程中的资源

多个线程同时去操作一个"东西"，可能会存在数据混乱的情况，例如：

```python
import threading

number = 0
loop = 165456


def _add(count):
    global number
    for i in range(count):
        number += 1


def _sub(count):
    global number
    for i in range(count):
        number -= 1


t1 = threading.Thread(target=_add, args=(loop,))
t2 = threading.Thread(target=_sub, args=(loop,))

t1.start()
t2.start()

print(number)  # 这个 number 是多少是不确定的 -- 因为 number 的 +1操作 和 -1操作 没有原子化
```

如何解决上述问题: 加锁

```python
...
lock = threading.Lock()

def _add(count):
    global number
    for i in range(count):
        lock.acquire()
        number += 1
        lock.release()
...
```

但是如上述这样做在循环中加锁会导致每一次循环都需要加锁释放锁, 耗时更长.

```python
...
lock = threading.Lock()

def _add(count):
    global number
    lock.acquire()
    for i in range(count):
        number += 1
    lock.release()
...
```

虽然这样规避了在循环中加锁和释放锁的开销, 但是如果这样写的话会导致多线程变成单线程了, 毫无意义。所以建议不要这么写。

---

## 4.2 Python 中默认线程安全的操作（数据结构）

![image-20260815103451244](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260815103459469.png)

- `queue` 模块
  这些队列内部使用锁（`threading.Lock`）保护所有操作，支持多生产者/多消费者场景，是线程安全的。
  - `queue.Queue`
  - `queue.LifoQueue`
  - `queue.PriorityQueue`

- `logging` 模块
  `logging` 模块是线程安全的，多个线程可以同时写日志而不会导致消息交错或丢失。
- 线程同步原语
  `threading` 模块提供的同步对象本身就是线程安全的（它们存在的目的就是为了协调线程）：
  - `Lock`
  - `RLock`
  - `Semaphore`
  - `Event`
  - `Condition`
  - `Barrier`
- `collections.deque` 的追加和弹出操作
  官方文档明确指出：**`deque` 的 `append`、`appendleft`、`pop`、`popleft` 是线程安全的**，可以安全地在多线程环境中使用而无需额外加锁。
  但**其他操作**（如索引、`len()`、迭代、`rotate()` 等）并不是线程安全的，需要外部同步。
-  因 GIL 而“看似”线程安全的操作（但不可依赖）
  在 `CPython` 中，由于 GIL 的存在，**单个字节码指令**的执行是原子的，因此以下**单个操作**通常不会被线程切换打断：
  这些操作在 `CPython` 中**实际表现**是原子的，因此很多人误以为它们是线程安全的。但官方文档**没有**保证这种原子性。
  - 变量赋值（`x = value`）
  - 变量读取（`y = x`）
  - 列表的 `append` / `pop` 等单个方法调用
  - 字典的单个键赋值/读取（`d[key] = value`, `value = d[key]`）

补充：

- 复合操作（如 `x += 1`、`if x in d: ...`）涉及多个字节码，线程切换可能发生在中间，导致数据竞争。
- 其他 Python 实现（如 `PyPy、Jython`）或未来的 `CPython` 版本（如 Python 3.13 的 **自由线程模式 / no-GIL**）可能不再提供这种隐式的原子性。

## 4.3 常见的非线程安全操作(需要手动加锁)

以下操作/数据结构**不是线程安全的**，多个线程同时操作时可能导致数据损坏、异常或未定义行为：

- 普通的 `list`、`dict`、`set` 的复合操作，例如：

  ```
  if x not in my_dict:
      my_dict[x] = value   # 检查-设置，可能被打断
  ```

- 简单的计数器自增/自减：

  ```
  counter += 1   # 读-改-写，非原子
  ```

- 遍历容器时修改容器（可能引发 `RuntimeError`）

- 多个线程同时写同一个文件（数据可能交错）

- 多个线程同时操作同一个数据库连接或网络套接字

对于这些情况，必须使用锁或其他同步机制来保护共享资源。

## 4.4 总结

| 对象/操作                                              | 是否线程安全 | 备注                                   |
| :----------------------------------------------------- | :----------- | :------------------------------------- |
| `queue.Queue` 系列                                     | ✅ 是         | 专门设计，内部加锁                     |
| `logging` 模块                                         | ✅ 是         | 内部处理了线程同步                     |
| `threading.Lock/RLock/Semaphore/Event/Condition` 等    | ✅ 是         | 本身就是同步工具                       |
| `collections.deque` 的 `append/pop/appendleft/popleft` | ✅ 是         | 官方明确声明                           |
| 普通变量的赋值/读取                                    | ❌ 非官方保证 | 在 CPython 中因 GIL 看似原子，不可依赖 |
| `list/dict/set` 的单个方法调用                         | ❌ 非官方保证 | 同样依赖 GIL，不可依赖                 |
| 复合操作（`+=`、`check-then-act`）                     | ❌ 否         | 明显存在数据竞争                       |
| 直接写文件、操作网络套接字                             | ❌ 否         | 需要外部锁或使用线程安全封装           |

## 4.5 建议：

- 优先使用专门设计的线程安全数据结构（如 `queue.Queue`）。
- 对于共享可变状态，使用 `Lock` / `RLock` 保护。
- 避免依赖 GIL 的“伪线程安全”，尤其在未来可能启用 no-GIL 的 Python 版本中，必须显式同步。

# 5. 线程锁

在程序中如果想要自己手动加锁，一般有两种：`Lock`和`RLock`

## 5.1 `Lock` 同步锁 -- 不支持锁的嵌套

```python
import threading

number = 0
lock = threading.Lock()


def task():
    global number

    lock.acquire()
    for _ in range(100000):
        number += 1
    lock.release()

    print(number)


for i in range(2):
    t = threading.Thread(target=task)
    t.start()
```

## 5.2 `RLock` 递归锁 -- 支持锁的嵌套 -- 可重入的锁

```python
import threading

number = 0
lock = threading.RLock()


def task():
    global number

    lock.acquire()
    for _ in range(100000):
        number += 1
    lock.release()

    print(number)


for i in range(2):
    t = threading.Thread(target=task)
    t.start()
```

# 6. 死锁

死锁，由于竞争资源或者由于彼此通信而造成的一种阻塞现象。

```python
import threading
import time

lock = threading.Lock()


def task():
    # 第一个抵达的线程进入并上锁，其他线程就需要在此等待
    lock.acquire() 
    # 第一个抵达的线程又要申请锁，但是此时锁已经被第一个线程拿到了，那么第一个线程就会一直等待有进程能释放(啥也不干，就硬等) -- 导致死锁
    lock.acquire()  
    print(123)
    lock.release()
    lock.release()


for i in range(2):
    t = threading.Thread(target=task)
    t.start()
```

```python
import threading
import time

lock1 = threading.Lock()
lock2 = threading.Lock()


def task1():
    lock1.acquire() 
    time.sleep(1)
    lock2.acquire()
    print(11)
    lock2.release()
    print(111)
    lock1.release()
    print(1111)

    
def task2():
    lock2.acquire() 
    time.sleep(1)
    lock1.acquire()
    print(22)
    lock1.release()
    print(222)
    lock2.release()
    print(2222)

t1 = threading.Thread(target=task1)
t1.start()

t2 = threading.Thread(target=task2)
t2.start()

# 上述代码可能产生死锁
```

# 7. 线程池

`Python3` 中官方才正式提供线程池

线程不是开的越多越好，开的多了可能会导致系统的性能更低了，例如：如下的代码是不推荐在项目开发中编写的:

```python
import threading

def task():
    do something ...

url_list = [f'https://www.baidu.com?page={i}' for i in range(300000)]
for url in url_list:
    t = threading.Thread(target=task, args=(url,))
    t.start()
```

不建议：无限制地创建线程

建议: 使用线程池

---

## 7.1 示例1

```python
import time
import threading
from concurrent.futures import ThreadPoolExecutor

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
}


def task(url, name):
    print('当前执行进程:', threading.current_thread().name)
    print(f'下载 {name}: {url} ...')
    try:
        content = requests.get(url=url, headers=headers)
        with open(f'./crawls/{name}.html', 'w', encoding='utf-8') as fp:
            fp.write(content.text)
    except Exception:
        pass


urls = [
    (f'https://quotes.toscrape.com/page/{i}/', f'quotes_{i}')
    for i in range(1, 11)
]

start = time.time()

pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix='crawl_thread_')

for url in urls:
    pool.submit(task, url[0], url[1])

print('所有任务执行结束, 耗时:', time.time() - start, 's')
```

输出结果:

```python
当前执行进程: crawl_thread__0
下载 quotes_1: https://quotes.toscrape.com/page/1/ ...
当前执行进程: crawl_thread__1
下载 quotes_2: https://quotes.toscrape.com/page/2/ ...
当前执行进程: crawl_thread__2
下载 quotes_3: https://quotes.toscrape.com/page/3/ ...
当前执行进程: crawl_thread__3
当前执行进程:下载 quotes_4: https://quotes.toscrape.com/page/4/ ...
所有任务执行结束, 耗时:  0.0016300678253173828 crawl_thread__4s

下载 quotes_5: https://quotes.toscrape.com/page/5/ ...
当前执行进程: crawl_thread__3
下载 quotes_6: https://quotes.toscrape.com/page/6/ ...
当前执行进程: crawl_thread__4
下载 quotes_7: https://quotes.toscrape.com/page/7/ ...
当前执行进程: crawl_thread__2
下载 quotes_8: https://quotes.toscrape.com/page/8/ ...
当前执行进程: crawl_thread__0
下载 quotes_9: https://quotes.toscrape.com/page/9/ ...
当前执行进程: crawl_thread__1
下载 quotes_10: https://quotes.toscrape.com/page/10/ ...
```

## 7.2 示例 2: 等待所有线程执行完毕

```python
import time
import threading
from concurrent.futures import ThreadPoolExecutor

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
}


def task(url, name):
    print('当前执行进程:', threading.current_thread().name)
    print(f'下载 {name}: {url} ...')
    try:
        content = requests.get(url=url, headers=headers)
        with open(f'./crawls/{name}.html', 'w', encoding='utf-8') as fp:
            fp.write(content.text)
    except Exception:
        pass


urls = [
    (f'https://quotes.toscrape.com/page/{i}/', f'quotes_{i}')
    for i in range(1, 11)
]

start = time.time()

pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix='crawl_thread_')

for url in urls:
    pool.submit(task, url[0], url[1])

pool.shutdown(True)  # 等待线程池中的任务执行完毕后，再继续执行

print('所有任务执行结束, 耗时:', time.time() - start, 's')
```

输出结果：

```python
当前执行进程: crawl_thread__0
下载 quotes_1: https://quotes.toscrape.com/page/1/ ...
当前执行进程: crawl_thread__1
下载 quotes_2: https://quotes.toscrape.com/page/2/ ...
当前执行进程: crawl_thread__2
下载 quotes_3: https://quotes.toscrape.com/page/3/ ...
当前执行进程: crawl_thread__3当前执行进程: crawl_thread__4
下载 quotes_4: https://quotes.toscrape.com/page/4/ ...

下载 quotes_5: https://quotes.toscrape.com/page/5/ ...
当前执行进程: crawl_thread__0
下载 quotes_6: https://quotes.toscrape.com/page/6/ ...
当前执行进程: crawl_thread__3
下载 quotes_7: https://quotes.toscrape.com/page/7/ ...
当前执行进程: crawl_thread__4
下载 quotes_8: https://quotes.toscrape.com/page/8/ ...
当前执行进程: crawl_thread__1
下载 quotes_9: https://quotes.toscrape.com/page/9/ ...
当前执行进程: crawl_thread__2
下载 quotes_10: https://quotes.toscrape.com/page/10/ ...
所有任务执行结束, 耗时: 3.8450326919555664 s
```

## 7.3 示例3： 任务执行完毕后执行其他操作

```python
import time
import threading
from concurrent.futures import ThreadPoolExecutor, Future

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
}


def task(url, name):
    print('当前执行进程:', threading.current_thread().name)
    print(f'下载 {name}: {url} ...')
    try:
        content = requests.get(url=url, headers=headers)
        with open(f'./crawls/{name}.html', 'w', encoding='utf-8') as fp:
            fp.write(content.text)
        return f'./crawls/{name}.html', True
    except Exception:
        return '', False


def done(response):
    """演示处理下载下来的数据..."""
    if response.result()[1]:
        print(f'爬虫成功: {response.result()[0]} ...')
        time.sleep(0.5)
    else:
        print('爬虫失败')


urls = [
    (f'https://quotes.toscrape.com/page/{i}/', f'quotes_{i}')
    for i in range(1, 11)
]

start = time.time()

pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix='crawl_thread_')

for url in urls:
    future: Future = pool.submit(task, url[0], url[1])
    future.add_done_callback(done)

pool.shutdown(True)  # 等待线程池中的任务执行完毕后，再继续执行

print('所有任务执行结束, 耗时:', time.time() - start, 's')
```

输出结果：

```python
当前执行进程: crawl_thread__0
下载 quotes_1: https://quotes.toscrape.com/page/1/ ...
当前执行进程: crawl_thread__1
下载 quotes_2: https://quotes.toscrape.com/page/2/ ...当前执行进程:
 crawl_thread__2
下载 quotes_3: https://quotes.toscrape.com/page/3/ ...
当前执行进程: crawl_thread__3
下载 quotes_4: https://quotes.toscrape.com/page/4/ ...
当前执行进程: crawl_thread__4
下载 quotes_5: https://quotes.toscrape.com/page/5/ ...
爬虫成功: ./crawls/quotes_4.html ...
爬虫成功: ./crawls/quotes_5.html ...
爬虫成功: ./crawls/quotes_1.html ...
爬虫成功: ./crawls/quotes_3.html ...
爬虫成功: ./crawls/quotes_2.html ...
当前执行进程: crawl_thread__3
下载 quotes_6: https://quotes.toscrape.com/page/6/ ...
当前执行进程: crawl_thread__4
下载 quotes_7: https://quotes.toscrape.com/page/7/ ...
当前执行进程: crawl_thread__0
下载 quotes_8: https://quotes.toscrape.com/page/8/ ...
当前执行进程: crawl_thread__2
下载 quotes_9: https://quotes.toscrape.com/page/9/ ...
当前执行进程: crawl_thread__1
下载 quotes_10: https://quotes.toscrape.com/page/10/ ...
爬虫成功: ./crawls/quotes_6.html ...
爬虫成功: ./crawls/quotes_8.html ...
爬虫成功: ./crawls/quotes_10.html ...
爬虫成功: ./crawls/quotes_9.html ...
爬虫成功: ./crawls/quotes_7.html ...
所有任务执行结束, 耗时: 4.233995676040649 s
```

---

优化一下上述代码：

```python
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
}

# 确保保存目录存在
os.makedirs('./crawls', exist_ok=True)

def task(url, name):
    print(f'当前线程: {threading.current_thread().name}')
    print(f'下载 {name}: {url} ...')
    try:
        # 设置超时，避免无限等待
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查 HTTP 状态码
        filepath = f'./crawls/{name}.html'
        with open(filepath, 'w', encoding='utf-8') as fp:
            fp.write(response.text)
        return filepath, True
    except Exception as e:
        # 记录具体错误，便于排查
        print(f'任务 {name} 失败: {e}')
        return '', False

def done(future):
    """处理下载完成后的结果"""
    result = future.result()  # 不会抛异常，因为 task 内已捕获
    filepath, success = result
    if success:
        print(f'爬虫成功: {filepath}')
        # 这里可以添加后续处理，但避免长时间阻塞
    else:
        print('爬虫失败')

urls = [
    (f'https://quotes.toscrape.com/page/{i}/', f'quotes_{i}')
    for i in range(1, 11)
]

start = time.time()

# 使用 with 自动管理线程池
with ThreadPoolExecutor(max_workers=5, thread_name_prefix='crawl_thread_') as pool:
    futures = []
    for url, name in urls:
        future = pool.submit(task, url, name)
        future.add_done_callback(done)
        futures.append(future)

print('所有任务执行结束, 耗时:', time.time() - start, 's')
```

## 7.4 最终统一获取结果

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor, Future


def task(video_url):
    print('开始执行任务', video_url)
    time.sleep(2)
    return random.randint(0, 10)


future_list = []

# 创建线程池 里面最多创建 max_workers 个线程
pool = ThreadPoolExecutor(max_workers=10)

url_list = [f'https://www.baidu.com?page={i}' for i in range(20)]

for url in url_list:
    # 在线程池中提交一个任务，线程池如果有空闲进程，则分配一个线程去执行，执行完毕后再将线程交还给线程池，如果没有空闲线程，则等待
    future: Future = pool.submit(task, url)
    future_list.append(future)

pool.shutdown(True)

for fu in future_list:
    print(fu.result())
```

# 8. 扩展 - 单例模式

面向对象 + 多线程相关的一个面试题:以后项目和源码中可能会用到

之前写一个类,每次执行 `类名()` 都会实例化一个类的对象

```python
class Foo:
    pass


obj1 = Foo()
obj2 = Foo()

print(obj1, obj2)  # <__main__.Foo object at 0x000001CBB22B4980> <__main__.Foo object at 0x000001CBB2142C10>
```

- 简单的实现单例模式

  ```python
  class Singleton:
      instance = None
  
      def __init__(self, name):
          self.name = name
  
      def __new__(cls, *args, **kwargs):
          # 返回空对象
          if cls.instance:
              return cls.instance
          cls.instance = object.__new__(cls)
          return cls.instance
  
  
  obj1 = Singleton('computer')
  obj2 = Singleton('science')
  
  print(obj1, obj2)  # <__main__.Singleton object at 0x0000020663F54980> <__main__.Singleton object at 0x0000020663F54980>
  ```

- 单例模式在多线程的情况下会出问题

  ```python
  import threading
  import time
  
  
  class Singleton:
      instance = None
  
      def __init__(self, name):
          self.name = name
  
      def __new__(cls, *args, **kwargs):
          # 返回空对象
          if cls.instance:
              return cls.instance
          time.sleep(0.1)
          cls.instance = object.__new__(cls)
          return cls.instance
  
  
  def task():
      obj = Singleton('x')
      print(obj)
  ```

  运行结果: 我们会发现这样的话单例模式会失效 -- 可以加锁

  ```python
  <__main__.Singleton object at 0x00000240EB1C5BE0>
  <__main__.Singleton object at 0x00000240EB052C10><__main__.Singleton object at 0x00000240EB16EC10><__main__.Singleton object at 0x00000240EB12BA80>
  
  <__main__.Singleton object at 0x00000240EB017E10><__main__.Singleton object at 0x00000240BFEA60F0>
  
  <__main__.Singleton object at 0x00000240EB0FCD10>
  
  <__main__.Singleton object at 0x00000240EB0FCF30><__main__.Singleton object at 0x00000240C02A1250>
  <__main__.Singleton object at 0x00000240EB0F0A50>
  ```

  加锁:

  ```python
  import threading
  import time
  
  lock = threading.RLock()
  
  
  class Singleton:
      instance = None
  
      def __init__(self, name):
          self.name = name
  
      def __new__(cls, *args, **kwargs):
          with lock:
              # 返回空对象
              if cls.instance:
                  return cls.instance
              time.sleep(0.1)
              cls.instance = object.__new__(cls)
              return cls.instance
  
  
  def task():
      obj = Singleton('x')
      print(obj)
  
  
  for i in range(10):
      t = threading.Thread(target=task)
      t.start()
  ```

- 还可以优化:  

  ```python
  import threading
  
  
  class Singleton:
      instance = None
      lock = threading.RLock()
  
      def __init__(self, name):
          self.name = name
  
      def __new__(cls, *args, **kwargs):
          with cls.lock:
              # 返回空对象
              if cls.instance:
                  return cls.instance
              cls.instance = object.__new__(cls)
              return cls.instance
  
  
  def task():
      obj = Singleton('x')
      print(obj)
  
  
  for i in range(10):
      t = threading.Thread(target=task)
      t.start()
  ```

- 还可以稍微优化一下性能

  ```python
  import threading
  
  
  class Singleton:
      instance = None
      lock = threading.RLock()
  
      def __init__(self, name):
          self.name = name
  
      def __new__(cls, *args, **kwargs):
          # 可以稍微提高性能 -- 如果在多线程以后想要再次使用这个单例,就可以减少一些加锁和释放锁的开销
          if cls.instance:
              return cls.instance
          with cls.lock:
              # 返回空对象
              if cls.instance:
                  return cls.instance
              cls.instance = object.__new__(cls)
              return cls.instance
  
  
  def task():
      obj = Singleton('x')
      print(obj)
  
  
  for i in range(10):
      t = threading.Thread(target=task)
      t.start()
  
  # 1000 行代码
  
  obj = Singleton('y')
  print(obj)
  ```













































