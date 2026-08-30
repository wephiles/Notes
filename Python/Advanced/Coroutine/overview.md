---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-15 13:08:74 周六"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">overview</h1>

# 1. 简单介绍

> 协程参考： https://zhuanlan.zhihu.com/p/137057192
>
> [asyncio到底是个啥？【python async await】](https://www.bilibili.com/video/BV1NA411g7yf)
>
> 刚开始学习爬虫时的协程相关的笔记：[单线程+异步协程](##单线程+异步协程)

暂时以了解为主。

计算机中提供了：线程、进程用于实现并发编程（真实存在）。

协程（Coroutine）：是程序员通过代码搞出来的一个东西（非真实存在）。

```python
协程也可以被称为微线程，是医用用户态内的上下文切换技术。
简而言之，其实就是通过一个线程实现代码快相互切换执行（来回跳着执行）。
```

例如：

```python
def func1():
    print(1)
    ...
    print(2)
    

def func2():
	print(3)
	...
    print(4)


func1()
func2()
```

上述代码是普通的函数定义和执行，按流程分别执行两个函数中的代码，并先后输出`1 2 3 4`

但如果介入协程技术那么就可以实现函数代码切换执行，最终输出：`1 3 2 4`

在python中有多种方式实现协程, 例如：

- `greenlet`

  ```python
  pip install greenlet
  ```

  ```python
  from greenlet import greenlet
  
  
  def func1():
      print(1)  # 第二步：输出 1
      gr2.switch()  # 第三步：切换到 func2 函数
      print(2)  # 第六步：输出 2
      gr2.switch()  # 第七步：切换到 func2 函数 从上次执行的位置继续向后执行
      
      
  def func2():
      print(3)  # 第四步： 输出3
      gr1.switch()  # 第五步：切换到 func1 函数从上次执行的位置继续向下执行
      print(4)  # 第八步： 输出 4 
      
      
  gr1 = greenlet(func1)
  gr2 = greenlet(func2)
  gr1.switch()  # 第一步 去执行 func1 函数
  ```

- `yield`

  ```python
  def func1():
      yield 1
      yield from func2()
      yield 2
      
  
  def func2():
  	yield 3
      yield 4
  
  
  f1 = func1()
  for item in f1:
      print(item)
  ```

虽然上述两种都实现了协程，但是这种编写代码的方式没什么意义。

这种来回切换执行，可能反倒让程序执行速度变慢（相较于串行）。

协程如何才能有意义？

> 不要让用户去手动切换，而是应该在遇到IO操作的时候能自动切换
>
> Python在3.4之后推出了`asyncio` 模块 + Python 3.5 推出 `async`、`await`语法，内部基于协程并且遇到IO请求自动化切换。

```python
import asyncio


async def func1():
    print(1)
    await asyncio.sleep(2)
    print(2)


async def func2():
    print(3)
    await asyncio.sleep(2)
    print(4)


tasks = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2()),
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```

案例： 协程用于 爬虫

![image-20260815134241438](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260815134242500.png)

通过上述内容发现，在处理IO请求时，协程通过一个线程就可以实现并发操作。

# 2. 总结

![image-20260815134307818](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260815134309015.png)

# 3. 单线程+异步协程

**补充 - 最开始学爬虫时候协程相关**

event_loop:事件循环，相当于一个无限循环，可以把一些函数注册到这个事件循环上，当满足某些条件时，函数就会被循环执行。

coroutine:协程对象，我们可以将协程对象注册到时间循环中，他会被事件循环调用，我们可以使用async关键字来定义一个方法，这个方法不会立即执行，而是返回一个协程对象，只有当这个协程对象注册到事件循环总，事件循环启动后，这个协程对象对应的函数内部的语句才会被执行。

task:任务,他是对协程对象的进一步封装，包含了任务的各个状态

future:代表将来执行或者还没有执行的任务，实际上和task没有本质区别

async定义一个协程

await用于挂起阻塞方法的执行

下面代码展示了协程的测试：

```python
import asyncio


async def request(url):
    print("正在请求...", url)
    print("请求成功", url)
    return url


# 返回一个协程对象
x = request("http://httpbin.org/get")


# # 创建一个事件循环对象
# loop = asyncio.get_event_loop()
#
# # 将协程对象注册到loop，并启动loop
# loop.run_until_complete(x)

# # task的使用
# loop = asyncio.get_event_loop()
# # 基于loop创建了一个task对象
# task = loop.create_task(x)
# print(task)
# # 将任务对象注册到事件循环中并启动
# loop.run_until_complete(task)
# print(task)

# # future的使用
# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(x)
# print(future)
# loop.run_until_complete(future)
# print(future)


# 回调函数 当任务对象执行成功之后 将任务对象回调执行call_back这个函数
def callback_func(task):
    # 可以用result()函数返回协程对象的返回值 -- 即上面定义的request函数(注册后成为协程对象)的返回值
    # result返回的就是任务对象中封装的协程对象对应函数的返回值
    print(task.result())


# 绑定回调
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(x)
# 将回调函数绑定到任务对象中
future.add_done_callback(callback_func)
loop.run_until_complete(future)
```

下面展示了多任务协程：

```python
import asyncio
import time


async def request(url):
    print("downloading...")
    # # 在异步协程中 如果出现同步模块相关代码 那么就无法实现异步
    # time.sleep(2)

    # 当在asyncio中遇到阻塞操作必须进行手动挂起
    await asyncio.sleep(2)

    print('over')
    return url + '-message'


urls = ['www.baidu.com',
        'www.sougou.com',
        'www.runoob.com',
        'www.firefox.com']

start = time.time()

# 任务列表 存放多个任务对象
future_list = []
for url in urls:
    c = request(url)
    future = asyncio.ensure_future(c)
    future_list.append(future)

loop = asyncio.get_event_loop()
# 必须将任务列表封装到wait方法中
loop.run_until_complete(asyncio.wait(future_list))

end = time.time()

print('time: ', end - start)
```

```python
import asyncio
import requests
import time
import aiohttp

# from website import index_bobo, index_jay, index_tom

urls = [
    'http://127.0.0.1:5000/bobo',
    'http://127.0.0.1:5000/jay',
    'http://127.0.0.1:5000/tom',
]

start = time.time()


async def get_page(url):
    print('downloading...', url)

    # # request发起的请求是基于同步的
    # response = requests.get(url)

    # 基于异步的网络请求模块发起请求 -- aiohttp
    async with aiohttp.ClientSession() as session:
        # 可能阻塞的操作必须await手动挂起
        # post get方法 headers params/data同requests
        async with await session.get(url) as response:
            # text()返回字符串形式的响应数据
            # read()返回二进制数据
            # json()返回json对象数据
            # 获取数据的时候也要挂起
            page_text = await response.text()
    print('over.', page_text)
    return url


futures = []

for url in urls:
    c = get_page(url)
    future = asyncio.ensure_future(c)
    futures.append(future)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))

end = time.time()


print('time: ', end-start)
```

