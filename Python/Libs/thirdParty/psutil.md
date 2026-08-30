---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-16 12:08:28 周日"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">psutil</h1>  

----

# 1. `psutil` 核心概念

`psutil` 是一个 Python 库，可以把它理解成：

> 一个跨平台的“系统信息读取器”。

操作系统本身一直在维护 CPU、内存、磁盘、网络、进程等信息。`psutil` 的作用，就是让你用 Python 代码方便地读取这些信息，甚至做一些进程管理操作，比如查看进程、结束进程。

## 1.1 主要解决的问题

- 你不用自己去解析 Linux 的 `/proc` 文件系统；
- 你不用调用 `top`、`free`、`ps` 等命令再解析文本；
- 你写的代码可以在 `Windows`、`Linux`、`macOS` 上尽量保持一致。

## 1.2 示例

先安装: `pip install psutil`

```python
import psutil

# logical 参数默认为 true
print('CPU 逻辑核心数(logical=True):', psutil.cpu_count())
print('CPU 逻辑核心数(logical=False):', psutil.cpu_count(logical=False))
print("CPU 最近 1 秒的平均使用率:", psutil.cpu_percent(interval=1))

memory = psutil.virtual_memory()
print(f'总内存: {memory.total / (1024 ** 3):.2f}GB')
print(f'可用内存: {memory.available / (1024 ** 3):.2f}GB')
print(f'内存使用率: {memory.percent}%')

process = psutil.Process()
print('当前 python 进程的 PID:', process.pid)
print('当前进程名:', process.name())
print(f'当前进程内存占用: {process.memory_info().rss / (1024 ** 2):.2f}MB')
```

输出：

```python
CPU 逻辑核心数(logical=True): 20
CPU 逻辑核心数(logical=False): 14
CPU 最近 1 秒的平均使用率: 11.9
总内存: 31.72GB
可用内存: 17.29GB
内存使用率: 45.5%
当前 python 进程的 PID: 8584
当前进程名: python.exe
当前进程内存占用: 18.22MB
```

## 1.3 代码解释

- `psutil.cpu_count(logical=True)`：返回 CPU 的逻辑核心数。
  - 比如你的电脑是 4 个物理核心，开启了超线程，逻辑核心数是 8。
  - `logical=True` 表示返回逻辑核心数。
  - `logical=False` 通常返回物理核心数。

- `psutil.cpu_percent(interval=1)`：返回最近 1 秒的平均 CPU 使用率。
  这里有一个关键点：
  - `interval=1` 表示它会等待 1 秒，然后计算这一秒内的 CPU 平均使用率。
    如果不传 `interval`，第一次调用通常会返回 `0.0`，这一点后面会在“误解”里解释。

- `mem = psutil.virtual_memory()`：获取系统虚拟内存信息，它返回一个对象，里面有很多字段，常用的有：
  - `total`：总内存大小，单位是字节。
  - `available`：可用内存大小，单位是字节。
  - `percent`：内存使用率，已经是百分比数值。

- `p = psutil.Process()`：获取当前 Python 进程的对象。
  注意：这里不是创建一个新进程，而是“打开”当前正在运行的这个 Python 脚本对应的进程信息。

- `p.memory_info().rss / (1024**2):.2f`
  - `p.memory_info()`：获取这个进程的内存信息。
  - `.rss`：进程实际占用的物理内存大小，单位是字节。
  - `1024**2`：把字节转换成 MB。
  - `:.2f`：保留两位小数。

## 1.4 常见的误解

### 1.4.1 误解一：`cpu_percent()`

```python
import psutil

print(psutil.cpu_percent())  # 0.0
```

**结果得到 `0.0`，以为 CPU 没工作，其实不是！**

`cpu_percent()` 需要两个时间点的数据做差值，才能算出使用率。第一次调用只是建立了一个“起点”，还没有足够信息计算。

**解决办法：**

- 使用 `psutil.cpu_percent(interval=1)`；
- 或者先调用一次，等待一段时间后再调用第二次。

![image-20260816124158891](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260816124159776.png)

![image-20260816124757064](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260816124758417.png)

### 1.4.2 误解二：`available VS. free`

在 Linux 上，`free` 可能看起来很小，但系统可用内存其实不少。因为 Linux 会把空闲内存用来做缓存，这些缓存可以在需要时释放给程序使用。所以判断“现在还能用多少内存”，通常应该看：

```python
psutil.virtual_memory().available
```

而不是只看 `free`。

### 1.4.3 误解三：`psutil.Process()`

`psutil.Process()` 只是获取一个已经存在的进程的信息对象。

如果你想启动一个新进程，应该用：

```python
psutil.Popen(["python", "script.py"])
```

而不是 `psutil.Process()`。

### 1.4.4 误解四：以为所有字段在所有操作系统上都能使用

`psutil` 尽量统一接口，但有些信息是平台相关的。

例如某些进程字段在 Windows 上有，在 Linux 上可能没有，或者含义略有不同。所以写跨平台代码时，不要假设所有属性都存在，必要时做异常处理或条件判断。

### 1.4.5 误解五：以为 `psutil` 是系统优化、杀毒或监控服务

`psutil` 只是一个库，它读取系统信息，或者帮你管理进程。它不会主动优化系统、清理内存、杀毒，也不会在后台一直运行。它适合写脚本、采集数据、做工具，不适合做纳秒级性能监控或修改内核参数。

## 1.5 适用场景

- 写监控脚本，采集 CPU、内存、磁盘、网络信息。
- 批量查看或管理进程。
- 做跨平台运维工具。
- 自定义系统仪表盘。

不适用场景：

- 需要修改系统配置、内核参数。
- 需要极高频率、极低延迟的性能监控。
- 需要非常精细的线程级分析，通常有更专业的工具，比如 Linux 下的 `perf`、`eBPF` 等。

和 `Linux` 的 `ps` 命令的区别：

- `ps` 是一个命令行工具，主要给人看。
- `psutil` 是一个 `Python` 库，主要给程序用。

- `psutil` 通常更快，因为它直接调用系统接口读取数据。
- `ps` 命令虽然本身也很快，但如果你在 `Python` 里反复调用 `subprocess` 去执行 `ps`，再解析文本，开销会更大。
- 如果只是偶尔看一次，两者差别不大；如果是在循环里大量调用，`psutil` 优势更明显。

## 1.6 对于 `psutil` 的理解

### 1.6.1 问题 1

> 为什么 `psutil.cpu_percent(interval=1)` 需要等待 1 秒才能给出一个有意义的值？
> 如果直接调用 `psutil.cpu_percent()`，第一次为什么通常会得到 `0.0`？
> 这反映了 psutil 在计算 CPU 使用率时采用了什么基本思路？

回答上述问题：

> `psutil.cpu_percent()` 并不是在“等待 1 秒然后看 CPU 忙不忙”，而是做了两件事：
>
> - 记录当前 CPU 已经工作了多少时间，比如 `cpu_time_1`；
> - 过了一段时间，再记录一次 `cpu_time_2`；
> - 用 `(cpu_time_2 - cpu_time_1) / 时间差` 算出这段时间内 CPU 忙碌时间的占比。
>
> > 所以，它依赖的是**两个采样点之间的差值**。
> >
> > 第一次调用 `cpu_percent()` 时，因为还没有上一次的采样点，所以只能返回 `0.0` 作为占位。
> > 这也解释了为什么 `psutil.cpu_percent(interval=1)`会阻塞 1 秒 —— 因为系统需要在这一秒内完成两次采样。
> >
> > > CPU 使用率需要两个不同时间点的采样才能计算，单个时间点只有累计工作时间，没有“使用率”这个概念。

### 1.6.2 问题 2

> 在 `psutil.virtual_memory()` 的结果里，有 `free` 和 `available` 两个字段。
> 为什么在判断“系统现在还能给新程序用多少内存”时，通常应该看 `available`，而不是只看 `free`？
> 请结合操作系统的内存管理思路来说明。

回答上述问题：

> 1. free 到底是什么
>    `free` 表示：
>
>    > 系统完全没有被任何东西占用的内存。
>
>    它不包括缓存，也不包括正在被程序使用的内存。
>
>    你可以把它理解成：
>
>    > “这块内存现在完全空着，谁都没用。”
>
> 2. `available` 不是“真实内存剩余量”
>    `available` 更准确的意思是：
>
>    > 系统估计：如果现在要启动一个新程序，在不触发交换分区的前提下，大概还能拿出多少内存给程序用。
>
>    它会把一部分“可以回收的缓存”也算进去。
>
>    因为 Linux 喜欢用空闲内存来做文件缓存，但这些缓存并不是必须一直占着的。
>    如果程序需要内存，系统可以快速释放一部分缓存给程序用。
>
>    所以 `available` 可以理解为：
>
>    > `free` + 一部分可回收的缓存。
>
>    它不是精确的“真实剩余量”，而是一个“估计可用量”。

### 1.6.3 问题 3

> 假设你想用 Python 查看 PID 为 `1234` 的进程占用了多少内存。
>
> 有两种做法：
>
> 1. 使用 `psutil.Process(1234).memory_info().rss`
> 2. 使用 `subprocess` 执行 `ps -p 1234 -o rss`，然后解析命令输出
>
> 请你从“程序获取系统信息的方式”这个角度，用自己的话说说：
>
> > 这两种做法在本质上有什么不同？
> > 为什么 `psutil` 这种做法通常更适合在 Python 代码中使用？

回答上述问题：

> `psutil.Process(1234).memory_info().rss` 在本质上是调用操作系统底层 `API` 直接获取相关数据后封装成一个Python对象，能够在Python 中很方便地进行访问； 
>
> 而 subprocess 执行 `ps -p 1234 -o rss` 是利用 Python 的库发送命令到系统，拿到系统返回的文本信息，还需要对命令进行解析。 
>
> 正如上述分析，`psutil.Process(1234).memory_info().rss` 直接返回 Python 对象，即非常适合在 Python 代码中使用；而 subprocess 执行 `ps -p 1234 -o rss` 是拿到了文本数据，还需要进行解析才能够在 Python 中使用，所以此方法相较于`psutil.Process(1234).memory_info().rss` 并不是很适合在 Python 代码中使用。
>
> 补充：
>
> 1. `psutil` 跨平台
>
> `psutil.Process(1234).memory_info().rss` 在 Windows、Linux、macOS 上都能用，接口基本一致。
>
> 而 `ps -p 1234 -o rss` 是 Linux/Unix 命令，在 Windows 上不存在。
> 所以如果你想写跨平台脚本，`psutil` 是更好的选择。
>
> 2. 不依赖命令输出格式
>
> `ps` 命令的输出格式可能因系统版本、语言环境不同而变化。
> 如果你用 `subprocess` 去解析文本，代码会变得很脆弱，容易因为一个空格或列宽变化而报错。
>
> `psutil` 返回的是结构化数据，不需要你去“猜”命令输出长什么样。

### 1.6.4 一句话总结 `psutil`

> `psutil` 是 Python 里的一个工具库，就像系统的管家。你写几行代码问它内存用了多少、CPU 忙不忙，它就直接把数字给你，不用你敲命令、看一堆文本。而且你可以写个脚本让它自动定时查，把结果记录到文件里，很适合做监控。

## 1.7 练习题

### 1.7.1 第一题

```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
每隔 3 秒记录一次 CPU 使用率和内存使用率，写入一个 monitor.log 文件。
"""

import time
from datetime import datetime

import psutil

head = f"{' '*19}\tCPU使用率\t内存使用率\n"

with open("./monitor.log", "w", encoding="utf-8") as f:
    f.write(head)

while True:
    cur_dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    cpu_userage = psutil.cpu_percent()
    mem_userage = psutil.virtual_memory().percent
    w_text = f"{cur_dt} \t {cpu_userage}% \t {mem_userage}%\n"
    with open("./monitor.log", "a", encoding="utf-8") as f:
        f.write(w_text)
    time.sleep(3)

```

上述代码有一些性能逻辑和性能问题：

```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
每隔 3 秒记录一次 CPU 使用率和内存使用率，写入一个 monitor.log 文件。
"""

import time
from datetime import datetime

import psutil

with open("./monitor.log", "a", encoding="utf-8") as f:
    head = f"{' '*19} \t CPU使用率\t内存使用率\n"
    f.write(head)

    psutil.cpu_percent()
    time.sleep(3)

    while True:
        try:
            cur_dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            cpu_usage = psutil.cpu_percent()
            mem_usage = psutil.virtual_memory().percent
            w_text = f"{cur_dt} \t {cpu_usage}% \t {mem_usage}%\n"
            f.write(w_text)
            f.flush()
            time.sleep(3)
        except KeyboardInterrupt:
            print("监控已停止。")
            break

```

### 1.7.2 第二题

```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
打印当前系统的 CPU 物理核心数 和 逻辑核心数。
打印当前系统的 总内存 和 已使用内存(单位: GB, 保留两位小数)。
打印当前 Python 进程的 PID 和 进程名。
"""

import psutil

print(f"物理核心数: {psutil.cpu_count(logical=False)}")
print(f"逻辑核心数: {psutil.cpu_count()}")

memory = psutil.virtual_memory()
print(f"总内存: {memory.total / (1024 ** 3):.2f} GB")
print(f"已使用内存: {memory.used / (1024 ** 3):.2f} GB")

process = psutil.Process()
print(f"当前进程PID: {process.pid}")
print(f"当前进程名: {process.name()}")

```

### 1.7.3 第三题

```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
输入一个进程名，例如 "python"。
返回一个列表，列表中每个元素是一个字典，包含该进程的 pid、name、内存占用（MB，保留两位小数）。
如果找不到任何同名进程，返回空列表。
"""

import psutil


def find_processes_by_name(name: str):
    res = []
    try:
        for p in psutil.process_iter(["pid", "name", "memory_info"]):
            if name.lower() == p.info["name"].lower():
                memory_mb = round(p.info["memory_info"].rss / 1024 / 1024, 2)
                res.append(
                    {"pid": p.info["pid"], "name": p.info["name"], "mem": memory_mb}
                )
    except PermissionError as e:
        print("没有权限:", e)
    except Exception as e:
        print("未知错误:", e)
    return res


if __name__ == "__main__":
    processes = find_processes_by_name("python")

    if processes:
        print(f"找到 {len(processes)} 个 Python 进程。")
        for data_dict in processes:
            pid, name, mem = data_dict["pid"], data_dict["name"], data_dict["mem"]
            print(f"PID: {pid:<8} | name: {name:<10} | memory: {mem} MB.")
    else:
        print(f"并未找到 Python 进程！")

```

### 1.7.4 第四题

```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
在脚本中设定一个 PID，比如 pid = 1234。
连续采集 5 次，每次间隔 1 秒。
每次采集：
    该进程的 CPU 使用率（使用 psutil.Process(pid).cpu_percent(interval=1)）。
    该进程当前内存占用（MB，保留两位小数）。
打印每次采集的结果，格式类似：
    第 1 次: CPU 12.5% | 内存 45.32 MB
    第 2 次: CPU 10.1% | 内存 45.40 MB
    ...
"""

import psutil

pid = input("请输入你需要监控的进程ID: ")

try:
    pid = int(pid)
except ValueError:
    print("输入的数据不是数字！")
    exit(1)


try:
    process = psutil.Process(pid=pid)
except psutil.NoSuchProcess:
    print(f"PID 为 {pid} 的进程不存在!")
    exit(1)

process.cpu_percent()

for i in range(5):
    try:
        cpu_usage = process.cpu_percent(interval=1)
        mem_usage = round(process.memory_info().rss / 1024 / 1024, 2)
        print(f"第 {i + 1} 次: CPU {cpu_usage:.2f} | 内存: {mem_usage} MB")
    except psutil.NoSuchProcess:
        print("进程在统计的过程中退出了！")
        exit(1)

```

# 2. `psutil` 的常用扩展功能

## 2.1 磁盘信息

磁盘分区和使用率

```python
import psutil

# 查看所有磁盘分区
for part in psutil.disk_partitions():
    print(part.device, part.mountpoint, part.fstype)

# 查看根分区的使用情况
usage = psutil.disk_usage("/")
print(f"总容量: {usage.total / (1024**3):.2f} GB")
print(f"已用: {usage.used / (1024**3):.2f} GB")
print(f"可用: {usage.free / (1024**3):.2f} GB")
print(f"使用率: {usage.percent}%")
```

磁盘 IO 统计

```python
io = psutil.disk_io_counters()
print(f"读取字节数: {io.read_bytes}")
print(f"写入字节数: {io.write_bytes}")
```

## 2.2 网络信息

网络 IO 总量

```python
net = psutil.net_io_counters()
print(f"发送字节数: {net.bytes_sent}")
print(f"接收字节数: {net.bytes_recv}")
print(f"发送错误数: {net.errout}")
```

当前网络连接

```python
for conn in psutil.net_connections(kind="tcp"):
    if conn.status == "ESTABLISHED":
        print(f"{conn.laddr} -> {conn.raddr} 状态: {conn.status}")
```

注意：在某些系统上需要管理员权限才能看到所有连接。

## 2.3 进程管理

更常见的场景是：

- 根据 `PID` 查找进程
- 列出所有进程
- 启动子进程
- 等待进程结束
- 终止进程

列出所有进程并排序

```python
processes = []
for p in psutil.process_iter(["pid", "name", "memory_info"]):
    try:
        mem_mb = p.info["memory_info"].rss / 1024 / 1024
        processes.append({
            "pid": p.info["pid"],
            "name": p.info["name"],
            "memory_mb": round(mem_mb, 2)
        })
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

# 按内存从大到小排序
processes.sort(key=lambda x: x["memory_mb"], reverse=True)

for proc in processes[:10]:
    print(f"{proc['pid']:>8} {proc['name']:<20} {proc['memory_mb']:>8.2f} MB")
```

使用 `Popen` 启动子进程

```python
import psutil

p = psutil.Popen(["python", "-c", "import time; time.sleep(5)"])
print(f"启动子进程 PID: {p.pid}")

# 等待子进程结束
p.wait()
print("子进程已结束")
```

终止进程

```python
p = psutil.Process(1234)
p.terminate()  # 发送 SIGTERM
p.wait(timeout=5)  # 等待最多5秒

# 如果还在运行，强制结束
if p.is_running():
    p.kill()  # 发送 SIGKILL
```

## 2.4 系统其他信息

系统启动时间

```python
import psutil, datetime

boot_time = psutil.boot_time()
print(datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S"))
```

登录用户

```python
for user in psutil.users():
    print(user.name, user.terminal, user.host)
```

温度传感器（Linux常见）

```python
temps = psutil.sensors_temperatures()
if temps:
    for name, entries in temps.items():
        for entry in entries:
            print(f"{name} {entry.label}: {entry.current}°C")
else:
    print("当前平台不支持温度读取")
```

# 3. 实际项目示例

**简易服务器监控脚本**

下面这个脚本综合了 CPU、内存、磁盘、网络和进程监控，适合放在服务器上定时运行。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简易系统监控脚本
每 5 秒采集一次系统状态，并检查指定进程是否存在。
"""

import time
from datetime import datetime
import psutil

# 要监控的关键进程名
WATCH_PROCESS = "nginx"

def get_process_info(name):
    """返回第一个匹配名称的进程信息，若不存在则返回 None"""
    for p in psutil.process_iter(["pid", "name", "memory_info"]):
        try:
            if p.info["name"].lower() == name.lower():
                return {
                    "pid": p.info["pid"],
                    "memory_mb": round(p.info["memory_info"].rss / 1024 / 1024, 2)
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def collect_metrics():
    """采集一次系统指标"""
    # CPU：先建立基线
    psutil.cpu_percent()

    # 内存
    mem = psutil.virtual_memory()

    # 磁盘
    disk = psutil.disk_usage("/")

    # 网络
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()

    cpu_usage = psutil.cpu_percent(interval=1)
    net_sent = net2.bytes_sent - net1.bytes_sent
    net_recv = net2.bytes_recv - net1.bytes_recv

    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": cpu_usage,
        "mem_total": round(mem.total / 1024**3, 2),
        "mem_used": round(mem.used / 1024**3, 2),
        "mem_percent": mem.percent,
        "disk_total": round(disk.total / 1024**3, 2),
        "disk_used_percent": disk.percent,
        "net_sent_kbps": round(net_sent / 1024, 2),
        "net_recv_kbps": round(net_recv / 1024, 2),
        "watch_process": get_process_info(WATCH_PROCESS)
    }

def main():
    print("开始监控，按 Ctrl+C 停止...")
    try:
        while True:
            data = collect_metrics()
            print(f"\n[{data['time']}]")
            print(f"  CPU: {data['cpu']}%")
            print(f"  内存: {data['mem_used']}/{data['mem_total']} GB ({data['mem_percent']}%)")
            print(f"  磁盘: 使用率 {data['disk_used_percent']}%")
            print(f"  网络: 上传 {data['net_sent_kbps']} KB/s, 下载 {data['net_recv_kbps']} KB/s")
            if data["watch_process"]:
                p = data["watch_process"]
                print(f"  进程 {WATCH_PROCESS}: PID {p['pid']}, 内存 {p['memory_mb']} MB")
            else:
                print(f"  警告: 进程 {WATCH_PROCESS} 不存在!")
            time.sleep(4)  # 循环间隔，配合采集中的 sleep 总约5秒
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == "__main__":
    main()
```

这个脚本综合了 CPU、内存、磁盘、网络、进程检查，稍加修改就能用于实际服务器监控，比如把输出写入日志文件或发送到监控平台。

# 4. 推荐的官方文档章节

`psutil` 官方文档写得非常清楚，建议优先阅读下面几个部分：

1. **System related functions**
   https://psutil.readthedocs.io/en/latest/#system-related-functions
   涵盖 CPU、内存、磁盘、网络、传感器等系统级接口。适合你扩展基础能力。
2. **Processes**
   https://psutil.readthedocs.io/en/latest/#processes
   进程管理相关，包括 `Process` 类的所有方法，如 `cpu_percent`、`memory_info`、`terminate`、`wait` 等。
3. **Recipes**
   https://psutil.readthedocs.io/en/latest/#recipes
   官方提供的一些实用示例，比如如何找出占用内存最多的进程、如何监控网络流量等，非常适合照葫芦画瓢。

建议从 **Recipes** 开始，里面有很多可以直接跑的例子，然后配合 **System related functions** 和 **Processes** 查询具体函数的用法。

# 5. 网页版 DeepSeek 笔记记录

```python
psutil 学习笔记
1. psutil 的核心概念
是什么？
psutil 是一个跨平台的 Python 库，可以理解为：

一个“系统信息读取器”，用 Python 代码直接读取 CPU、内存、磁盘、网络、进程等信息。

它主要解决三个问题：

不用手动解析 /proc 文件系统或命令输出文本；

提供统一的 Python 接口，方便在代码中获取结构化数据；

跨平台，同一套代码可以在 Windows、Linux、macOS 上运行。

基本思路
系统级信息：通过 psutil.cpu_percent()、psutil.virtual_memory() 等函数获取。

进程级信息：通过 psutil.Process(pid) 获取某个进程对象，再读取该进程的 CPU、内存、状态等信息。

采样差值计算：CPU 使用率、网络速率等不是瞬时值，需要两个时间点的数据做差值计算。

2. psutil 的最小示例
安装
bash
pip install psutil
基础示例
python
import psutil

# CPU 逻辑核心数
print("逻辑 CPU 核心数:", psutil.cpu_count(logical=True))

# 最近 1 秒的平均 CPU 使用率
print("CPU 使用率:", psutil.cpu_percent(interval=1))

# 内存使用情况
mem = psutil.virtual_memory()
print(f"总内存: {mem.total / (1024**3):.2f} GB")
print(f"可用内存: {mem.available / (1024**3):.2f} GB")
print(f"内存使用率: {mem.percent}%")

# 当前 Python 进程
p = psutil.Process()
print(f"当前进程 PID: {p.pid}")
print(f"当前进程名: {p.name()}")
print(f"当前进程内存占用: {p.memory_info().rss / (1024**2):.2f} MB")
3. psutil 的常用扩展功能
3.1 磁盘信息
python
import psutil

# 所有磁盘分区
for part in psutil.disk_partitions():
    print(part.device, part.mountpoint, part.fstype)

# 指定分区使用情况
usage = psutil.disk_usage("/")
print(f"总容量: {usage.total / (1024**3):.2f} GB")
print(f"已用: {usage.used / (1024**3):.2f} GB")
print(f"可用: {usage.free / (1024**3):.2f} GB")
print(f"使用率: {usage.percent}%")
3.2 网络信息
python
import psutil

# 网络 IO 总量
net = psutil.net_io_counters()
print(f"发送字节数: {net.bytes_sent}")
print(f"接收字节数: {net.bytes_recv}")

# 当前 TCP 连接
for conn in psutil.net_connections(kind="tcp"):
    if conn.status == "ESTABLISHED":
        print(f"{conn.laddr} -> {conn.raddr}")
计算网络速率时，需要取两个时间点的差值，类似 CPU 使用率。

3.3 进程管理
python
import psutil

# 列出所有进程，按内存排序
processes = []
for p in psutil.process_iter(["pid", "name", "memory_info"]):
    try:
        mem_mb = p.info["memory_info"].rss / 1024 / 1024
        processes.append({
            "pid": p.info["pid"],
            "name": p.info["name"],
            "memory_mb": round(mem_mb, 2)
        })
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

processes.sort(key=lambda x: x["memory_mb"], reverse=True)
for proc in processes[:10]:
    print(f"{proc['pid']:>8} {proc['name']:<20} {proc['memory_mb']:>8.2f} MB")
启动子进程：

python
import psutil

p = psutil.Popen(["python", "-c", "import time; time.sleep(5)"])
print(f"子进程 PID: {p.pid}")
p.wait()
print("子进程已结束")
终止进程：

python
p = psutil.Process(1234)
p.terminate()        # 发送 SIGTERM
p.wait(timeout=5)    # 等待最多5秒
if p.is_running():
    p.kill()         # 强制结束
3.4 系统其他信息
python
import psutil, datetime

# 系统启动时间
boot_time = psutil.boot_time()
print(datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S"))

# 当前登录用户
for user in psutil.users():
    print(user.name, user.terminal, user.host)

# 温度传感器（Linux）
temps = psutil.sensors_temperatures()
if temps:
    for name, entries in temps.items():
        for entry in entries:
            print(f"{name} {entry.label}: {entry.current}°C")
4. psutil 的实际项目示例
综合服务器监控脚本
python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简易系统监控脚本
每 5 秒采集一次系统状态，并检查指定进程是否存在。
"""

import time
from datetime import datetime
import psutil

WATCH_PROCESS = "nginx"

def get_process_info(name):
    """返回第一个匹配名称的进程信息，若不存在则返回 None"""
    for p in psutil.process_iter(["pid", "name", "memory_info"]):
        try:
            if p.info["name"].lower() == name.lower():
                return {
                    "pid": p.info["pid"],
                    "memory_mb": round(p.info["memory_info"].rss / 1024 / 1024, 2)
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def collect_metrics():
    """采集一次系统指标"""
    psutil.cpu_percent()  # 建立基线

    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()

    cpu_usage = psutil.cpu_percent(interval=1)
    net_sent = net2.bytes_sent - net1.bytes_sent
    net_recv = net2.bytes_recv - net1.bytes_recv

    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": cpu_usage,
        "mem_total": round(mem.total / 1024**3, 2),
        "mem_used": round(mem.used / 1024**3, 2),
        "mem_percent": mem.percent,
        "disk_total": round(disk.total / 1024**3, 2),
        "disk_used_percent": disk.percent,
        "net_sent_kbps": round(net_sent / 1024, 2),
        "net_recv_kbps": round(net_recv / 1024, 2),
        "watch_process": get_process_info(WATCH_PROCESS)
    }

def main():
    print("开始监控，按 Ctrl+C 停止...")
    try:
        while True:
            data = collect_metrics()
            print(f"\n[{data['time']}]")
            print(f"  CPU: {data['cpu']}%")
            print(f"  内存: {data['mem_used']}/{data['mem_total']} GB ({data['mem_percent']}%)")
            print(f"  磁盘: 使用率 {data['disk_used_percent']}%")
            print(f"  网络: 上传 {data['net_sent_kbps']} KB/s, 下载 {data['net_recv_kbps']} KB/s")
            if data["watch_process"]:
                p = data["watch_process"]
                print(f"  进程 {WATCH_PROCESS}: PID {p['pid']}, 内存 {p['memory_mb']} MB")
            else:
                print(f"  警告: 进程 {WATCH_PROCESS} 不存在!")
            time.sleep(4)
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == "__main__":
    main()
5. psutil 的常见错误
错误 1：第一次调用 cpu_percent() 得到 0.0
python
print(psutil.cpu_percent())  # 往往输出 0.0
原因：CPU 使用率需要两个时间点的差值。第一次调用只建立了基线，没有上一次数据。

解决：

python
psutil.cpu_percent(interval=1)  # 等待 1 秒并返回平均使用率
或先调用一次建立基线，再调用第二次。

错误 2：把 free 和 available 混为一谈
free 是完全空闲的内存，不包括缓存；
available 是系统估计可以给新程序使用的内存，包含可回收缓存。

判断“还能用多少内存”应使用 available。

错误 3：内存换算错误
rss 单位是字节（bytes）。

常见错误：

python
memory_mb = round(p.info["memory_info"].rss / 1202 / 1024, 2)  # 1202 是笔误
正确做法：

python
memory_mb = round(p.info["memory_info"].rss / 1024 / 1024, 2)
错误 4：在 process_iter 循环中因权限不足导致整个循环终止
python
try:
    for p in psutil.process_iter(["pid", "name", "memory_info"]):
        # 某个进程可能因权限不足抛出 AccessDenied
except PermissionError:
    print("没有权限")
这样会让整个循环提前结束。

解决：把 try 放在 for 内部，单个进程失败则跳过。

python
for p in psutil.process_iter(["pid", "name", "memory_info"]):
    try:
        # 读取进程信息
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
错误 5：处理非数字输入或进程不存在时使用 raise
例如：

python
pid = input("请输入 PID: ")
pid = int(pid)  # 如果输入 abc 会抛 ValueError，程序崩溃
或：

python
try:
    process = psutil.Process(pid=pid)
except psutil.NoSuchProcess:
    raise psutil.NoSuchProcess(pid=pid)  # 又让程序崩溃
解决：打印友好提示并退出。

python
try:
    pid = int(pid)
except ValueError:
    print("输入的不是数字！")
    exit(1)
6. psutil 中容易混淆的地方
6.1 物理核心 vs 逻辑核心
psutil.cpu_count(logical=False)：物理核心数。

psutil.cpu_count(logical=True) 或 psutil.cpu_count()：逻辑核心数（含超线程）。

6.2 cpu_percent() 是平均值，不是瞬时值
它需要两个采样点之间的差值。
单次调用第一次往往返回 0.0，因为还没有上一次采样。

6.3 Process() 不是创建进程
psutil.Process(pid) 只是获取一个已经存在的进程的信息对象。
创建新进程应该使用 psutil.Popen([...])。

6.4 磁盘、内存、网络单位都是字节
内存 virtual_memory().total 单位是字节；

磁盘 disk_usage("/").total 单位是字节；

网络 net_io_counters().bytes_sent 单位是字节。

换算时需要注意：

KB = / 1024

MB = / 1024 / 1024

GB = / 1024 / 1024 / 1024

6.5 进程名匹配：完全匹配 vs 模糊匹配
如果使用 if name.lower() in p.info["name"].lower()，可能会匹配到 python3、python2 等。
如果需要精确匹配，应使用 ==。

6.6 psutil 与 ps 命令的区别
ps 是命令行工具，输出文本，需要自己解析。

psutil 是 Python 库，直接返回结构化数据。

大量重复调用时，psutil 通常比在 Python 里反复调用 subprocess 执行 ps 更高效，也更跨平台。

7. 推荐的官方文档
Recipes（实用示例）
https://psutil.readthedocs.io/en/latest/#recipes
官方提供的实用代码片段，适合照葫芦画瓢。

System related functions（系统级函数）
https://psutil.readthedocs.io/en/latest/#system-related-functions
涵盖 CPU、内存、磁盘、网络、传感器等接口。

Processes（进程管理）
https://psutil.readthedocs.io/en/latest/#processes
Process 类的所有方法，如 cpu_percent、memory_info、terminate、wait 等。

建议优先阅读 Recipes，然后根据需要查阅另外两个章节。
```
