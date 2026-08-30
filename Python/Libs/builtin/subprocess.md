---
aliases:
  - course of study
  - course
  - libraries
  - subprocess tutorial
tags:
  - tutorial
  - computer-science
  - subprocess
  - Python
category: knowledge
datetime: " 2026-08-08 12:08:29 周六"
author: wephiles
rating: "2"
---

<h1 style="text-align: center;">subprocess</h1>

# 1. `subprocess` 模块简介

## 1.1 什么是 `subprocess`

**subprocess** 是 Python 标准库中用于**生成子进程**、**连接它们的输入/输出/错误管道**以及**获取它们的返回码**的模块。

简单来说，它让你可以在 Python 程序中**执行外部命令**（如 shell 命令、系统程序、其他脚本等），就像在终端中输入命令一样。

## 1.2 为什么需要 `subprocess`

| 场景         | 传统方法    | subprocess 优势                  |
| ------------ | ----------- | -------------------------------- |
| 执行系统命令 | os.system() | 更安全、功能更强大               |
| 获取命令输出 | os.popen()  | 可以同时处理 stdin/stdout/stderr |
| 管道操作     | 手动处理    | 内置管道支持                     |
| 异步执行     | 困难        | Popen 类支持非阻塞调用           |

## 1.3 基本使用原则

```python
# 🎯 黄金法则：永远优先使用 subprocess.run()
# 简单、安全、满足 90% 的需求
```

# 2. 核心函数详解

## 2.1 `subprocess.run()` -- 推荐首选 🔥

函数签名:

```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, 
               shell=False, cwd=None, timeout=None, check=False, 
               encoding=None, errors=None, text=None, env=None, 
               universal_newlines=None)
```

参数详解:

| 参数                        | 类型      | 说明                | 默认值 |
| --------------------------- | --------- | ------------------- | ------ |
| `args`                      | str/list  | 要执行的命令        | 必需   |
| `stdin`                     | file/PIPE | 标准输入            | None   |
| `stdout`                    | file/PIPE | 标准输出            | None   |
| `stderr`                    | file/PIPE | 标准错误            | None   |
| `shell`                     | bool      | 是否通过 shell 执行 | False  |
| `cwd`                       | str       | 工作目录            | None   |
| `timeout`                   | float     | 超时时间(秒)        | None   |
| `check`                     | bool      | 非零退出码时抛异常  | False  |
| `text`/`universal_newlines` | bool      | 以文本模式返回      | False  |
| `encoding`                  | str       | 文本编码            | None   |
| `env`                       | dict      | 环境变量            | None   |
| `input`                     | str/bytes | 传递给 stdin 的数据 | None   |

返回值：`CompletedProcess` 对象

```python
class CompletedProcess:
    args          # 传入的参数
    returncode    # 返回码，0 表示成功
    stdout        # 标准输出（如果捕获）
    stderr        # 标准错误（如果捕获）
```

示例代码:

```python
import subprocess
import sys

print("=" * 60)
print("subprocess.run() 示例集合")
print("=" * 60)

# ====== 基础用法 ======
print("\n【1】最简单的用法 - 执行命令")
result = subprocess.run(["ls", "-l"])
print(f"返回码: {result.returncode}")

# ====== 捕获输出 ======
print("\n【2】捕获标准输出")
result = subprocess.run(["echo", "Hello World"], capture_output=True, text=True)
print(f"输出内容: {result.stdout}")
print(f"返回码: {result.returncode}")

# ====== shell=True 的使用 ======
print("\n【3】使用 shell 模式（注意安全风险！）")
result = subprocess.run("echo 'Hello from shell' && date", shell=True, 
                       capture_output=True, text=True)
print(f"输出: {result.stdout.strip()}")

# ====== 检查返回码 ======
print("\n【4】使用 check=True 自动检查失败")
try:
    # 这会失败，因为不存在的命令
    subprocess.run(["ls", "/nonexistent"], check=True, 
                   capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    print(f"捕获到异常！返回码: {e.returncode}")
    print(f"错误输出: {e.stderr}")

# ====== 超时控制 ======
print("\n【5】设置超时")
try:
    subprocess.run(["sleep", "5"], timeout=2)
except subprocess.TimeoutExpired as e:
    print(f"命令超时！执行时间: {e.timeout}秒")

# ====== 工作目录 ======
print("\n【6】指定工作目录")
result = subprocess.run(["pwd"], cwd="/tmp", capture_output=True, text=True)
print(f"在 /tmp 目录下执行 pwd: {result.stdout.strip()}")

# ====== 环境变量 ======
print("\n【7】设置自定义环境变量")
custom_env = {"MY_VAR": "Custom Value", "PATH": "/usr/bin:/bin"}
# 注意：在 Windows 上可能需要完整的环境变量
if sys.platform != "win32":
    result = subprocess.run(["bash", "-c", "echo $MY_VAR"], 
                           env=custom_env, capture_output=True, text=True)
    print(f"自定义环境变量输出: {result.stdout.strip()}")

# ====== 输入数据 ======
print("\n【8】向子进程输入数据")
result = subprocess.run(["cat"], input="Hello via stdin!\nLine 2\n", 
                       capture_output=True, text=True)
print(f"cat 输出: {result.stdout}")

# ====== 错误输出合并 ======
print("\n【9】合并 stdout 和 stderr")
result = subprocess.run(
    ["bash", "-c", "echo stdout; echo stderr >&2"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,  # 重定向 stderr 到 stdout
    text=True
)
print(f"合并输出: {result.stdout}")

# ====== 实际应用：调用 git ======
print("\n【10】实际应用 - 获取 git 信息")
result = subprocess.run(["git", "--version"], capture_output=True, text=True)
if result.returncode == 0:
    print(f"Git 版本: {result.stdout.strip()}")
else:
    print("Git 未安装")

print("\n" + "=" * 60)

```

示例:

```python
import subprocess

subprocess.run(["ls", '-lah'])
```

输出:

```python
drwxrwxr-x 8 jinyu jinyu 4.0K  8月  2 12:19 .
drwxrwxr-x 3 jinyu jinyu 4.0K  7月  8 22:44 ..
-rw-r--r-- 1 jinyu jinyu    0  6月 13 15:38 db.sqlite3
drwxrwxr-x 3 jinyu jinyu 4.0K  6月 13 15:38 demo
drwxrwxr-x 7 jinyu jinyu 4.0K  6月 13 15:28 .git
-rw-rw-r-- 1 jinyu jinyu  109  6月 13 15:28 .gitignore
-rw-rw-r-- 1 jinyu jinyu   82  6月 13 15:28 main.py
-rwxrwxr-x 1 jinyu jinyu  660  6月 13 15:35 manage.py
-rw-rw-r-- 1 jinyu jinyu  172  6月 13 15:29 pyproject.toml
-rw-rw-r-- 1 jinyu jinyu    5  6月 13 15:28 .python-version
-rw-rw-r-- 1 jinyu jinyu    0  6月 13 15:28 README.md
-rw-rw-r-- 1 jinyu jinyu   50  8月  8 12:36 run.py
drwxrwxr-x 2 jinyu jinyu 4.0K  6月 13 15:37 static
drwxrwxr-x 2 jinyu jinyu 4.0K  6月 13 15:40 templates
-rw-rw-r-- 1 jinyu jinyu 3.1K  6月 13 15:29 uv.lock
drwxrwxr-x 5 jinyu jinyu 4.0K  6月 13 15:29 .venv
drwxrwxr-x 4 jinyu jinyu 4.0K  6月 13 15:39 website
```

## 2.2 `subprocess.call()` -- 简单执行

函数签名:

```python
subprocess.call(args, *, stdin=None, stdout=None, stderr=None, 
                shell=False, cwd=None, timeout=None)
```

**特点：** 只返回退出码，不捕获输出

```python
import subprocess

print("=" * 60)
print("subprocess.call() 示例")
print("=" * 60)

# 返回退出码
exit_code = subprocess.call(["ls", "-l"])
print(f"ls 命令退出码: {exit_code}")

# 失败的情况
exit_code = subprocess.call(["ls", "/nonexistent"])
print(f"失败命令退出码: {exit_code}")  # 非 0

# 保存输出到文件
with open('output.txt', 'w') as f:
    exit_code = subprocess.call(["echo", "Hello"], stdout=f)
print(f"输出已写入文件，退出码: {exit_code}")

print("=" * 60)

```

## 2.3 subprocess.check_call() - 失败抛异常

函数签名:

```python
subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None,
                      shell=False, cwd=None, timeout=None)
```

特点: 退出码非 0 时自动抛出 `CallProcessError`

```python
import subprocess

print("=" * 60)
print("subprocess.check_call() 示例")
print("=" * 60)

try:
    # 成功的情况
    subprocess.check_call(["echo", "Success"])
    print("命令执行成功")
except subprocess.CalledProcessError as e:
    print(f"命令失败: {e}")

try:
    # 失败的情况
    subprocess.check_call(["ls", "/nonexistent"])
except subprocess.CalledProcessError as e:
    print(f"捕获异常！命令: {e.cmd}, 返回码: {e.returncode}")

print("=" * 60)

```

## 2.4 `subprocess.check_output()` -- 获取输出

函数签名:

```python
subprocess.check_output(args, *, stdin=None, stderr=None, shell=False,
                        cwd=None, encoding=None, errors=None, 
                        universal_newlines=False, timeout=None, text=False)
```

特点: 返回标准输出（bytes 或 str），失败时抛出异常

```python
import subprocess

print("=" * 60)
print("subprocess.check_output() 示例")
print("=" * 60)

# 获取输出（bytes）
output = subprocess.check_output(["echo", "Hello World"])
print(f"Bytes 输出: {output}")
print(f"解码后: {output.decode().strip()}")

# 获取输出（直接返回字符串）
output = subprocess.check_output(["echo", "Hello World"], text=True)
print(f"字符串输出: {output.strip()}")

# 错误处理
try:
    subprocess.check_output(["ls", "/nonexistent"])
except subprocess.CalledProcessError as e:
    print(f"输出失败！错误码: {e.returncode}")
    if hasattr(e, 'output') and e.output:
        print(f"错误输出: {e.output.decode()}")

print("=" * 60)

```

## 2.5 `subprocess.getoutput()` 和 `getstatusoutput()`

这两个是便捷函数，**内部使用 shell=True**（⚠️ 安全注意）

```python
subprocess.getoutput(cmd)      # 返回输出字符串
subprocess.getstatusoutput(cmd)  # 返回 (exit_code, output)

```

```python
import subprocess

print("=" * 60)
print("getoutput() 和 getstatusoutput() 示例")
print("=" * 60)

# getoutput - 只获取输出
output = subprocess.getoutput("ls -l | head -5")
print(f"前5行文件:\n{output}")

# getstatusoutput - 获取状态和输出
status, output = subprocess.getstatusoutput("date")
print(f"状态码: {status}, 输出: {output.strip()}")

status, output = subprocess.getstatusoutput("ls /nonexistent")
print(f"失败命令 - 状态码: {status}")

print("=" * 60)

```

# 3. `Popen` 类

`Popen` 是最强大的类，提供对子进程的完全控制。

## 3.1 `Popen` 构造函数

函数签名:

```python
class subprocess.Popen(args, bufsize=-1, executable=None, 
                       stdin=None, stdout=None, stderr=None,
                       preexec_fn=None, close_fds=True,
                       shell=False, cwd=None, env=None,
                       universal_newlines=False, 
                       startupinfo=None, creationflags=0,
                       restore_signals=True, start_new_session=False,
                       pass_fds=(), encoding=None, errors=None, text=None)

```

## 3.2 `Popen` 主要属性和方法

```python
# 属性
Popen.pid          # 子进程 PID
Popen.returncode   # 返回码（进程结束后）
Popen.stdin        # 标准输入流
Popen.stdout       # 标准输出流
Popen.stderr       # 标准错误流

# 方法
Popen.poll()       # 检查进程是否结束，返回 None 或 returncode
Popen.wait(timeout=None)  # 等待进程结束
Popen.communicate(input=None, timeout=None)  # 与进程交互
Popen.send_signal(signal)  # 发送信号
Popen.terminate()   # 发送 SIGTERM
Popen.kill()        # 发送 SIGKILL
```

## 3.3 `Popen` 完整示例

```python
import subprocess
import time
import signal

print("=" * 70)
print("Popen 类完整示例")
print("=" * 70)

# ====== 示例 1：基本使用 ======
print("\n【1】基本 Popen 使用")
proc = subprocess.Popen(["echo", "Hello from Popen"], 
                       stdout=subprocess.PIPE, text=True)
stdout, stderr = proc.communicate()
print(f"输出: {stdout.strip()}")
print(f"返回码: {proc.returncode}")

# ====== 示例 2：实时读取输出 ======
print("\n【2】实时读取输出（逐行）")
proc = subprocess.Popen(
    ["python3", "-c", "import time; [print(f'Line {i}') or time.sleep(0.5) for i in range(5)]"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1  # 行缓冲
)

print("开始逐行读取：")
while True:
    line = proc.stdout.readline()
    if line == '' and proc.poll() is not None:
        break
    if line:
        print(f"  读取: {line.strip()}", end='\n')

print(f"进程结束，返回码: {proc.returncode}")

# ====== 示例 3：进程控制 ======
print("\n【3】进程控制 - 启动、等待、终止")
# 启动一个长时间运行的进程
proc = subprocess.Popen(["sleep", "10"])
print(f"进程启动，PID: {proc.pid}")

# 检查进程状态
status = proc.poll()
print(f"进程状态: {'运行中' if status is None else f'已结束({status})'}")

# 等待一小段时间
time.sleep(1)

# 终止进程
print("发送终止信号...")
proc.terminate()
proc.wait()  # 等待进程结束
print(f"进程已终止，返回码: {proc.returncode}")  # 通常为 -15 (SIGTERM)

# ====== 示例 4：输入交互 ======
print("\n【4】与子进程交互")
proc = subprocess.Popen(
    ["python3", "-c", "import sys; name = input('请输入名字: '); print(f'你好, {name}!')"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 发送输入并获取输出
stdout, stderr = proc.communicate(input="Alice\n")
print(f"程序输出: {stdout}")

# ====== 示例 5：管道连接 ======
print("\n【5】管道连接 - 进程链式调用")
# ps aux | grep python
ps_proc = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
grep_proc = subprocess.Popen(
    ["grep", "python"],
    stdin=ps_proc.stdout,
    stdout=subprocess.PIPE,
    text=True
)
ps_proc.stdout.close()  # 允许 ps_proc 收到 SIGPIPE

output, _ = grep_proc.communicate()
print(f"找到的 Python 进程 (前3行):\n{output.split(chr(10))[:3]}")

# ====== 示例 6：异步非阻塞 ======
print("\n【6】异步非阻塞操作")
proc = subprocess.Popen(
    ["python3", "-c", "import time; [print(f'{i}...') or time.sleep(0.3) for i in range(5)]"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print("主程序可以做其他事情...")
for i in range(3):
    print(f"  主程序计数: {i}")
    time.sleep(0.2)

# 等待子进程完成
print("等待子进程...")
proc.wait()
print(f"子进程完成，返回码: {proc.returncode}")

# ====== 示例 7：超时控制 ======
print("\n【7】communicate() 超时")
proc = subprocess.Popen(
    ["python3", "-c", "import time; time.sleep(10); print('Done')"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

try:
    stdout, stderr = proc.communicate(timeout=2)
except subprocess.TimeoutExpired:
    print("操作超时，终止进程")
    proc.kill()
    stdout, stderr = proc.communicate()  # 清理资源
    print(f"进程已终止")

# ====== 示例 8：同时捕获 stdout 和 stderr ======
print("\n【8】分别捕获 stdout 和 stderr")
proc = subprocess.Popen(
    ["bash", "-c", "echo '这是标准输出' && echo '这是错误输出' >&2"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = proc.communicate()
print(f"stdout: {stdout.strip()}")
print(f"stderr: {stderr.strip()}")

# ====== 示例 9：实际应用 - 调用 ffmpeg ======
print("\n【9】实际应用 - 模拟调用外部工具")
# 检查是否安装了 ffmpeg
try:
    result = subprocess.run(
        ["ffmpeg", "-version"],
        capture_output=True,
        text=True,
        timeout=2
    )
    if result.returncode == 0:
        version_line = result.stdout.split('\n')[0]
        print(f"检测到: {version_line}")
    else:
        print("ffmpeg 未安装")
except (FileNotFoundError, subprocess.TimeoutExpired):
    print("ffmpeg 未安装或响应超时")

# ====== 示例 10：环境变量和目录 ======
print("\n【10】自定义环境变量和工作目录")
proc = subprocess.Popen(
    ["bash", "-c", "echo \"PWD: $PWD\" && echo \"MY_VAR: $MY_VAR\""],
    cwd="/tmp",
    env={"MY_VAR": "CustomValue", "PATH": "/usr/bin:/bin"},
    stdout=subprocess.PIPE,
    text=True
)
output, _ = proc.communicate()
print(output)

print("=" * 70)

```

# 4. 异常类

## 4.1 异常结构层级

```python
Exception
 └── SubprocessError
      ├── CalledProcessError
      └── TimeoutExpired

```

## 4.2 异常详解

### 4.2.1 `CalledProcessError` - 命令执行失败

```
class CalledProcessError(SubprocessError):
    returncode   # 退出码
    cmd          # 执行的命令
    output       # 捕获的输出（如果有）
    stdout       # 捕获的标准输出
    stderr       # 捕获的标准错误
```

### 4.2.2 `TimeoutExpired` - 命令超时

```
class TimeoutExpired(SubprocessError):
    cmd          # 执行的命令
    timeout      # 超时时间
    output       # 捕获的输出
    stdout       # 捕获的标准输出
    stderr       # 捕获的标准错误
```

## 4.3 异常处理示例

```
import subprocess

print("=" * 70)
print("异常处理示例")
print("=" * 70)

# ====== CalledProcessError ======
print("\n【1】CalledProcessError 处理")
try:
    subprocess.run(
        ["ls", "/nonexistent"],
        check=True,
        capture_output=True,
        text=True
    )
except subprocess.CalledProcessError as e:
    print(f"❌ 命令执行失败")
    print(f"   命令: {' '.join(e.cmd)}")
    print(f"   返回码: {e.returncode}")
    print(f"   标准输出: {e.stdout if e.stdout else '(无)'}")
    print(f"   标准错误: {e.stderr if e.stderr else '(无)'}")

# ====== TimeoutExpired ======
print("\n【2】TimeoutExpired 处理")
try:
    subprocess.run(["sleep", "5"], timeout=2)
except subprocess.TimeoutExpired as e:
    print(f"⏰ 命令超时")
    print(f"   超时时间: {e.timeout} 秒")
    print(f"   命令: {' '.join(e.cmd)}")
    
    # 超时后清理进程
    if e.output:
        print(f"   已捕获输出: {e.output}")

# ====== 通用 SubprocessError ======
print("\n【3】通用异常处理")
try:
    proc = subprocess.Popen(["nonexistent_command"])
except FileNotFoundError as e:
    print(f"📁 文件未找到: {e.filename}")
except subprocess.SubprocessError as e:
    print(f"🔧 子进程错误: {type(e).__name__}: {e}")
except Exception as e:
    print(f"❓ 其他异常: {type(e).__name__}: {e}")

# ====== 带资源清理的异常处理 ======
print("\n【4】带资源清理的异常处理")
proc = subprocess.Popen(["sleep", "10"])
try:
    proc.wait(timeout=2)
except subprocess.TimeoutExpired:
    print("超时，清理资源...")
    proc.terminate()
    try:
        proc.wait(timeout=1)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    print("资源已清理")

print("=" * 70)
```

# 5. 常量

```python
import subprocess

print("=" * 70)
print("subprocess 常量")
print("=" * 70)

# ====== PIPE ======
print("\n【1】subprocess.PIPE")
print(f"   值: {subprocess.PIPE}")
print(f"   作用: 创建管道，用于捕获输入/输出")
proc = subprocess.Popen(["echo", "test"], stdout=subprocess.PIPE)
output, _ = proc.communicate()
print(f"   示例: {output.decode().strip()}")

# ====== DEVNULL ======
print("\n【2】subprocess.DEVNULL")
print(f"   值: {subprocess.DEVNULL}")
print(f"   作用: 丢弃输出（相当于 /dev/null）")
proc = subprocess.Popen(
    ["echo", "这条消息会被丢弃"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
proc.wait()
print("   消息已丢弃，无输出")

# ====== STDOUT ======
print("\n【3】subprocess.STDOUT")
print(f"   值: {subprocess.STDOUT}")
print(f"   作用: 将 stderr 重定向到 stdout")
proc = subprocess.Popen(
    ["bash", "-c", "echo stdout; echo stderr >&2"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)
output, _ = proc.communicate()
print(f"   合并后的输出:\n{output}")

print("=" * 70)

```

# 6. 实际工程应用场景

## 6.1 系统管理脚本

```python
#!/usr/bin/env python3
"""
系统监控脚本示例
"""

import subprocess
import json
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.results = {}
    
    def get_disk_usage(self, path="/"):
        """获取磁盘使用情况"""
        try:
            result = subprocess.run(
                ["df", "-h", path],
                capture_output=True,
                text=True,
                check=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                return {
                    "filesystem": parts[0],
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "percent": parts[4],
                    "mount": parts[5]
                }
        except subprocess.CalledProcessError as e:
            print(f"获取磁盘信息失败: {e}")
        return None
    
    def get_memory_info(self):
        """获取内存信息"""
        try:
            result = subprocess.run(
                ["free", "-h"],
                capture_output=True,
                text=True,
                check=True
            )
            # 解析输出
            lines = result.stdout.strip().split('\n')
            mem_line = lines[1].split()
            return {
                "total": mem_line[1],
                "used": mem_line[2],
                "free": mem_line[3],
                "available": mem_line[6]
            }
        except subprocess.CalledProcessError as e:
            print(f"获取内存信息失败: {e}")
        return None
    
    def get_cpu_load(self):
        """获取 CPU 负载"""
        try:
            result = subprocess.run(
                ["uptime"],
                capture_output=True,
                text=True,
                check=True
            )
            # uptime 输出: "load average: 0.05, 0.04, 0.05"
            output = result.stdout
            if "load average:" in output:
                load_part = output.split("load average:")[1].strip()
                loads = [float(x.strip(',')) for x in load_part.split()]
                return {
                    "1min": loads[0],
                    "5min": loads[1],
                    "15min": loads[2]
                }
        except subprocess.CalledProcessError as e:
            print(f"获取 CPU 负载失败: {e}")
        return None
    
    def check_service_status(self, service_name):
        """检查服务状态 (systemd)"""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {
                "name": service_name,
                "status": result.stdout.strip(),
                "active": result.returncode == 0
            }
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return {
                "name": service_name,
                "status": "unknown",
                "active": False
            }
    
    def generate_report(self):
        """生成报告"""
        self.results["timestamp"] = datetime.now().isoformat()
        self.results["disk"] = self.get_disk_usage()
        self.results["memory"] = self.get_memory_info()
        self.results["cpu"] = self.get_cpu_load()
        
        # 检查关键服务
        services = ["ssh", "nginx", "mysql"]
        self.results["services"] = {
            svc: self.check_service_status(svc) for svc in services
        }
        
        return self.results

# 使用示例
if __name__ == "__main__":
    monitor = SystemMonitor()
    report = monitor.generate_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
```

## 6.2 数据处理管道

```python
#!/usr/bin/env python3
"""
数据处理管道示例
"""

import subprocess
import tempfile
import os

class DataPipeline:
    """数据处理管道类"""
    
    def __init__(self):
        self.temp_files = []
    
    def create_temp_file(self, content=""):
        """创建临时文件"""
        fd, path = tempfile.mkstemp()
        self.temp_files.append(path)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    def grep_file(self, pattern, input_file):
        """使用 grep 过滤文件"""
        output_file = self.create_temp_file()
        
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            proc = subprocess.Popen(
                ["grep", pattern],
                stdin=infile,
                stdout=outfile,
                text=True
            )
            proc.wait()
        
        return output_file if proc.returncode == 0 else None
    
    def sort_file(self, input_file, reverse=False):
        """对文件内容排序"""
        output_file = self.create_temp_file()
        cmd = ["sort"]
        if reverse:
            cmd.append("-r")
        
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            proc = subprocess.Popen(cmd, stdin=infile, stdout=outfile, text=True)
            proc.wait()
        
        return output_file
    
    def count_lines(self, input_file):
        """统计文件行数"""
        result = subprocess.run(
            ["wc", "-l", input_file],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return int(result.stdout.strip().split()[0])
        return 0
    
    def unique_lines(self, input_file):
        """去重"""
        output_file = self.create_temp_file()
        
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            proc = subprocess.Popen(
                ["uniq"],
                stdin=infile,
                stdout=outfile,
                text=True
            )
            proc.wait()
        
        return output_file
    
    def cleanup(self):
        """清理临时文件"""
        for f in self.temp_files:
            try:
                os.unlink(f)
            except OSError:
                pass
        self.temp_files = []

# 使用示例
if __name__ == "__main__":
    # 创建测试数据
    test_data = """apple
banana
apple
cherry
banana
date
apple
elderberry
"""
    
    pipeline = DataPipeline()
    
    try:
        # 1. 创建输入文件
        input_file = pipeline.create_temp_file(test_data)
        print(f"原始数据 ({pipeline.count_lines(input_file)} 行):")
        print(open(input_file).read())
        
        # 2. 过滤包含 'a' 的行
        filtered = pipeline.grep_file("a", input_file)
        print(f"\n过滤包含 'a' 的行 ({pipeline.count_lines(filtered)} 行):")
        print(open(filtered).read())
        
        # 3. 排序
        sorted_file = pipeline.sort_file(filtered)
        print(f"\n排序后 ({pipeline.count_lines(sorted_file)} 行):")
        print(open(sorted_file).read())
        
        # 4. 去重
        unique_file = pipeline.unique_lines(sorted_file)
        print(f"\n去重后 ({pipeline.count_lines(unique_file)} 行):")
        print(open(unique_file).read())
        
    finally:
        pipeline.cleanup()
```

## 6.3 `Web` 服务调用外部 `API`

```python
#!/usr/bin/env python3
"""
使用 curl 调用 API 的封装
"""

import subprocess
import json
from typing import Optional, Dict, Any

class APIClient:
    """基于 curl 的 API 客户端"""
    
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    def _build_curl_command(self, method: str, url: str, 
                           headers: Optional[Dict] = None,
                           data: Optional[Dict] = None) -> list:
        """构建 curl 命令"""
        cmd = ["curl", "-s", "-X", method.upper()]
        
        # 添加 headers
        if headers:
            for key, value in headers.items():
                cmd.extend(["-H", f"{key}: {value}"])
        
        # 添加数据
        if data:
            cmd.extend(["-d", json.dumps(data)])
        
        # 添加 URL
        full_url = f"{self.base_url}/{url.lstrip('/')}" if self.base_url else url
        cmd.append(full_url)
        
        return cmd
    
    def request(self, method: str, url: str, 
                headers: Optional[Dict] = None,
                data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送 HTTP 请求
        
        Returns:
            {
                'success': bool,
                'status_code': int,
                'data': Any,
                'error': str
            }
        """
        cmd = self._build_curl_command(method, url, headers, data)
        
        try:
            # 使用 -w 获取 HTTP 状态码
            cmd_with_status = cmd.copy()
            cmd_with_status.extend(["-w", "\n%{http_code}", "-o", "-"])
            
            result = subprocess.run(
                cmd_with_status,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'status_code': 0,
                    'data': None,
                    'error': f'curl failed with code {result.returncode}: {result.stderr}'
                }
            
            # 解析输出（最后一行是状态码）
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                response_body = '\n'.join(lines[:-1])
                status_code = int(lines[-1])
            else:
                response_body = ''
                status_code = 0
            
            # 尝试解析 JSON
            try:
                data = json.loads(response_body) if response_body else None
            except json.JSONDecodeError:
                data = response_body
            
            return {
                'success': 200 <= status_code < 300,
                'status_code': status_code,
                'data': data,
                'error': None
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'status_code': 0,
                'data': None,
                'error': f'Request timeout after {self.timeout} seconds'
            }
        except FileNotFoundError:
            return {
                'success': False,
                'status_code': 0,
                'data': None,
                'error': 'curl command not found'
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': 0,
                'data': None,
                'error': str(e)
            }
    
    def get(self, url: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """GET 请求"""
        return self.request("GET", url, headers)
    
    def post(self, url: str, data: Dict, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """POST 请求"""
        headers = headers or {}
        headers.setdefault("Content-Type", "application/json")
        return self.request("POST", url, headers, data)
    
    def put(self, url: str, data: Dict, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT 请求"""
        headers = headers or {}
        headers.setdefault("Content-Type", "application/json")
        return self.request("PUT", url, headers, data)
    
    def delete(self, url: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """DELETE 请求"""
        return self.request("DELETE", url, headers)

# 使用示例
if __name__ == "__main__":
    client = APIClient()
    
    # 测试 GET 请求
    print("测试 GET 请求:")
    response = client.get("https://httpbin.org/get")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    # 测试 POST 请求
    print("\n测试 POST 请求:")
    response = client.post("https://httpbin.org/post", {"name": "Python", "version": "3.11"})
    print(json.dumps(response, indent=2, ensure_ascii=False))

```

## 6.4 **并行执行多个命令

```python
#!/usr/bin/env python3
"""
并行执行多个命令的示例
"""

import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

class ParallelCommandRunner:
    """并行命令执行器"""
    
    @staticmethod
    def run_command(cmd: List[str], timeout: int = 60, name: str = "") -> Dict:
        """执行单个命令"""
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'name': name or ' '.join(cmd),
                'command': cmd,
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': time.time() - start_time,
                'error': None
            }
            
        except subprocess.TimeoutExpired:
            return {
                'name': name or ' '.join(cmd),
                'command': cmd,
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': '',
                'duration': timeout,
                'error': f'Timeout after {timeout} seconds'
            }
        except Exception as e:
            return {
                'name': name or ' '.join(cmd),
                'command': cmd,
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': '',
                'duration': time.time() - start_time,
                'error': str(e)
            }
    
    def run_parallel(self, commands: List[Tuple[List[str], str]], 
                     max_workers: int = 4, timeout: int = 60) -> Dict:
        """
        并行执行多个命令
        
        Args:
            commands: [(cmd_list, name), ...]
            max_workers: 最大并发数
            timeout: 单个命令超时时间
        
        Returns:
            {
                'total': int,
                'success': int,
                'failed': int,
                'results': [result_dict, ...],
                'total_duration': float
            }
        """
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_cmd = {
                executor.submit(self.run_command, cmd, timeout, name): (cmd, name)
                for cmd, name in commands
            }
            
            # 收集结果
            for future in as_completed(future_to_cmd):
                cmd, name = future_to_cmd[future]
                try:
                    result = future.result()
                    results.append(result)
                    status = "✅" if result['success'] else "❌"
                    print(f"{status} {result['name']} - {result['duration']:.2f}s")
                except Exception as e:
                    results.append({
                        'name': name,
                        'command': cmd,
                        'success': False,
                        'error': str(e),
                        'duration': 0
                    })
                    print(f"❌ {name} - Exception: {e}")
        
        # 统计
        total = len(results)
        success = sum(1 for r in results if r['success'])
        failed = total - success
        
        return {
            'total': total,
            'success': success,
            'failed': failed,
            'results': results,
            'total_duration': time.time() - start_time
        }

# 使用示例
if __name__ == "__main__":
    runner = ParallelCommandRunner()
    
    # 定义要执行的命令
    commands = [
        (["echo", "Command 1"], "Echo 1"),
        (["sleep", "2"], "Sleep 2s"),
        (["echo", "Command 2"], "Echo 2"),
        (["sleep", "1"], "Sleep 1s"),
        (["python3", "-c", "print('Python output')"], "Python Script"),
        (["date"], "Current Date"),
    ]
    
    print("开始并行执行命令...\n")
    summary = runner.run_parallel(commands, max_workers=3)
    
    print("\n" + "=" * 60)
    print("执行摘要:")
    print(f"  总命令数: {summary['total']}")
    print(f"  成功: {summary['success']}")
    print(f"  失败: {summary['failed']}")
    print(f"  总耗时: {summary['total_duration']:.2f}s")
    print("=" * 60)
    
    # 打印详细结果
    print("\n详细结果:")
    for result in summary['results']:
        print(f"\n命令: {result['name']}")
        print(f"  成功: {result['success']}")
        print(f"  耗时: {result['duration']:.2f}s")
        if result.get('stdout'):
            print(f"  输出: {result['stdout'].strip()}")
        if result.get('stderr'):
            print(f"  错误: {result['stderr'].strip()}")
        if result.get('error'):
            print(f"  异常: {result['error']}")

```

## 6.5 实时日志监控

```python
#!/usr/bin/env python3
"""
实时日志监控和过滤
"""

import subprocess
import re
from datetime import datetime
from typing import Callable, Optional

class LogMonitor:
    """实时日志监控器"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.running = False
        self.filters = []
        self.callbacks = []
    
    def add_filter(self, pattern: str, flags: int = 0):
        """添加过滤正则表达式"""
        regex = re.compile(pattern, flags)
        self.filters.append(regex)
    
    def add_callback(self, callback: Callable[[str], None]):
        """添加回调函数"""
        self.callbacks.append(callback)
    
    def _should_process(self, line: str) -> bool:
        """检查行是否应该被处理"""
        if not self.filters:
            return True
        return any(f.search(line) for f in self.filters)
    
    def _notify_callbacks(self, line: str):
        """通知所有回调函数"""
        for callback in self.callbacks:
            try:
                callback(line)
            except Exception as e:
                print(f"回调错误: {e}")
    
    def start(self, follow: bool = True):
        """开始监控"""
        self.running = True
        cmd = ["tail"]
        if follow:
            cmd.append("-f")
        cmd.append(self.log_file)
        
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # 行缓冲
            )
            
            print(f"开始监控: {self.log_file}")
            print(f"过滤器数量: {len(self.filters)}")
            print(f"回调数量: {len(self.callbacks)}")
            print("-" * 50)
            
            while self.running:
                line = proc.stdout.readline()
                if not line:
                    if proc.poll() is not None:
                        break
                    continue
                
                if self._should_process(line):
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] {line.rstrip()}")
                    self._notify_callbacks(line)
                    
        except KeyboardInterrupt:
            print("\n停止监控...")
        finally:
            self.running = False
            if 'proc' in locals():
                proc.terminate()
                proc.wait()
    
    def stop(self):
        """停止监控"""
        self.running = False

# 示例回调函数
def error_alert(line: str):
    """错误警报回调"""
    if "ERROR" in line.upper():
        print(f"  ⚠️  发现错误: {line.strip()}")

def warning_counter(line: str):
    """警告计数回调"""
    if "WARNING" in line.upper():
        # 这里可以添加计数逻辑
        pass

# 使用示例
if __name__ == "__main__":
    # 创建测试日志文件
    import os
    test_log = "/tmp/test_monitor.log"
    
    # 清空或创建测试日志
    with open(test_log, 'w') as f:
        f.write("")
    
    print("创建日志监控器...")
    monitor = LogMonitor(test_log)
    
    # 添加过滤器
    monitor.add_filter(r"(ERROR|WARNING|INFO)")
    
    # 添加回调
    monitor.add_callback(error_alert)
    monitor.add_callback(warning_counter)
    
    # 在另一个进程中写入日志（模拟）
    def write_log_entries():
        import time
        import threading
        
        def writer():
            entries = [
                "2024-01-01 INFO  Application started",
                "2024-01-01 DEBUG Processing request",
                "2024-01-01 WARNING Low memory detected",
                "2024-01-01 INFO  Request processed",
                "2024-01-01 ERROR Failed to connect to database",
                "2024-01-01 WARNING Retry attempt 1",
                "2024-01-01 ERROR Timeout occurred",
            ]
            for entry in entries:
                with open(test_log, 'a') as f:
                    f.write(entry + "\n")
                    f.flush()
                time.sleep(1)
        
        thread = threading.Thread(target=writer)
        thread.daemon = True
        thread.start()
    
    # 启动日志写入
    write_log_entries()
    
    # 启动监控（5秒后自动停止）
    import threading
    def stop_after_delay():
        import time
        time.sleep(8)
        monitor.stop()
    
    stopper = threading.Thread(target=stop_after_delay)
    stopper.daemon = True
    stopper.start()
    
    # 开始监控
    monitor.start(follow=True)
    
    print("\n监控结束")
    
    # 清理
    try:
        os.unlink(test_log)
    except:
        pass

```

# 7. 最佳实践

## 7.1 安全实践

```python
import subprocess

print("=" * 70)
print("安全最佳实践")
print("=" * 70)

# ====== ❌ 错误：使用 shell=True + 用户输入 ======
print("\n【错误示例 1】Shell 注入风险")
user_input = "file.txt; rm -rf /"
# 危险！
# subprocess.run(f"cat {user_input}", shell=True)  # 不要这样做！

# ====== ✅ 正确：使用列表形式 ======
print("\n【正确示例 1】使用列表形式")
user_input = "file.txt"
subprocess.run(["cat", user_input])  # 安全！

# ====== ✅ 正确：使用 shlex.quote() ======
print("\n【正确示例 2】使用 shlex.quote()")
import shlex
user_input = "file with spaces.txt; rm -rf /"
safe_arg = shlex.quote(user_input)
# subprocess.run(f"cat {safe_arg}", shell=True)  # 相对安全
print(f"转义后: {safe_arg}")

# ====== ✅ 最佳：完全避免 shell=True ======
print("\n【最佳实践】完全避免 shell=True")
subprocess.run(["cat", "file with spaces.txt"])

# ====== 白名单验证 ======
print("\n【安全模式】命令白名单")
ALLOWED_COMMANDS = {
    'ls': '/bin/ls',
    'cat': '/bin/cat',
    'grep': '/bin/grep',
}

def safe_run(command_name, args):
    """安全运行白名单命令"""
    if command_name not in ALLOWED_COMMANDS:
        raise ValueError(f"命令 {command_name} 不在允许列表中")
    
    cmd = [ALLOWED_COMMANDS[command_name]] + args
    return subprocess.run(cmd, capture_output=True, text=True)

# safe_run('ls', ['-l'])  # 安全
# safe_run('rm', ['-rf', '/'])  # 抛出异常

print("=" * 70)
```

## 7.2 资源管理

```python
import subprocess
import contextlib

print("=" * 70)
print("资源管理最佳实践")
print("=" * 70)

# ====== 使用 contextmanager 自动清理 ======
print("\n【1】使用上下文管理器")

@contextlib.contextmanager
def managed_process(*args, **kwargs):
    """自动清理的进程上下文管理器"""
    proc = subprocess.Popen(*args, **kwargs)
    try:
        yield proc
    finally:
        # 确保进程被清理
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()

# 使用
with managed_process(["sleep", "10"]) as proc:
    print(f"进程 PID: {proc.pid}")
    # 做一些事情...
print("进程已自动清理")

# ====== Popen 使用 close_fds ======
print("\n【2】正确设置 close_fds")
# 避免文件描述符泄漏
proc = subprocess.Popen(
    ["echo", "test"],
    stdout=subprocess.PIPE,
    close_fds=True  # 关闭所有不需要的文件描述符
)

# ====== 处理管道缓冲 ======
print("\n【3】避免管道死锁")
def safe_communicate(proc, input_data=None):
    """安全的 communicate，避免死锁"""
    try:
        return proc.communicate(input=input_data, timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        return proc.communicate()

# ====== 及时关闭管道 ======
print("\n【4】及时关闭管道")
proc1 = subprocess.Popen(["cat"], stdout=subprocess.PIPE)
proc2 = subprocess.Popen(["grep", "test"], stdin=proc1.stdout)

# 重要：关闭 proc1 的 stdout，避免缓冲区满导致死锁
proc1.stdout.close()

output, _ = proc2.communicate()
print(f"输出: {output.decode()}")

print("=" * 70)
```

## 7.3 错误处理

```python
import subprocess
import logging

print("=" * 70)
print("错误处理最佳实践")
print("=" * 70)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommandError(Exception):
    """自定义命令错误"""
    def __init__(self, message, returncode=None, stdout=None, stderr=None):
        super().__init__(message)
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

def run_command_safely(cmd, check=True, timeout=None, **kwargs):
    """
    安全执行命令，返回结构化结果
    
    Args:
        cmd: 命令列表
        check: 是否检查返回码
        timeout: 超时时间
        **kwargs: 其他 subprocess.run 参数
    
    Returns:
        dict: {
            'success': bool,
            'returncode': int,
            'stdout': str,
            'stderr': str,
            'error': str
        }
    """
    try:
        result = subprocess.run(
            cmd,
            check=check,
            timeout=timeout,
            capture_output=True,
            text=True,
            **kwargs
        )
        
        return {
            'success': True,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'error': None
        }
        
    except subprocess.CalledProcessError as e:
        logger.error(f"命令失败: {' '.join(cmd)}, 返回码: {e.returncode}")
        return {
            'success': False,
            'returncode': e.returncode,
            'stdout': e.stdout if hasattr(e, 'stdout') else None,
            'stderr': e.stderr if hasattr(e, 'stderr') else None,
            'error': f"Command failed with return code {e.returncode}"
        }
        
    except subprocess.TimeoutExpired as e:
        logger.error(f"命令超时: {' '.join(cmd)}")
        return {
            'success': False,
            'returncode': -1,
            'stdout': e.output if hasattr(e, 'output') else None,
            'stderr': None,
            'error': f"Command timed out after {timeout} seconds"
        }
        
    except FileNotFoundError as e:
        logger.error(f"命令不存在: {cmd[0]}")
        return {
            'success': False,
            'returncode': -1,
            'stdout': None,
            'stderr': None,
            'error': f"Command not found: {cmd[0]}"
        }
        
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return {
            'success': False,
            'returncode': -1,
            'stdout': None,
            'stderr': None,
            'error': str(e)
        }

# 使用示例
print("\n【1】成功命令")
result = run_command_safely(["echo", "Hello"])
print(f"结果: {result}")

print("\n【2】失败命令")
result = run_command_safely(["ls", "/nonexistent"], check=False)
print(f"结果: success={result['success']}, error={result['error']}")

print("\n【3】超时命令")
result = run_command_safely(["sleep", "10"], timeout=2)
print(f"结果: success={result['success']}, error={result['error']}")

print("=" * 70)
```

## 7.4 性能优化

```python
import subprocess
import time

print("=" * 70)
print("性能优化建议")
print("=" * 70)

# ====== 避免不必要的文本解码 ======
print("\n【1】仅在需要时使用 text=True")

# 如果只需要检查是否成功，不要捕获输出
start = time.time()
for _ in range(100):
    subprocess.run(["true"])  # 快
print(f"无输出捕获: {time.time() - start:.3f}s")

start = time.time()
for _ in range(100):
    subprocess.run(["true"], capture_output=True, text=True)  # 慢
print(f"捕获输出+文本: {time.time() - start:.3f}s")

# ====== 批量操作 ======
print("\n【2】使用管道代替多次调用")

# 慢：多次调用
start = time.time()
result1 = subprocess.run(["cat", "file.txt"], capture_output=True)
result2 = subprocess.run(["grep", "pattern"], input=result1.stdout, capture_output=True)
result3 = subprocess.run(["wc", "-l"], input=result2.stdout, capture_output=True, text=True)
print(f"多次调用: {time.time() - start:.3f}s")

# 快：单次管道调用
start = time.time()
proc = subprocess.Popen("cat file.txt | grep pattern | wc -l", shell=True, capture_output=True, text=True)
print(f"管道调用: {time.time() - start:.3f}s")

# =====️ 并行执行 ======
print("\n【3】并行执行独立命令")

from concurrent.futures import ThreadPoolExecutor

commands = [["sleep", "1"] for _ in range(5)]

# 串行
start = time.time()
for cmd in commands:
    subprocess.run(cmd)
print(f"串行执行: {time.time() - start:.3f}s")

# 并行
start = time.time()
with ThreadPoolExecutor(max_workers=5) as executor:
    list(executor.map(subprocess.run, commands))
print(f"并行执行: {time.time() - start:.3f}s")

# ====== 缓存结果 ======
print("\n【4】缓存命令结果")
from functools import lru_cache

@lru_cache(maxsize=32)
def get_git_branch():
    """获取 git 分支（缓存结果）"""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None

start = time.time()
for _ in range(10):
    branch = get_git_branch()
print(f"10次调用（缓存）: {time.time() - start:.3f}s")

print("=" * 70)
```

# 8. 总结速查表

| 函数/类                     | 用途                 | 推荐度         |
| --------------------------- | -------------------- | -------------- |
| `subprocess.run()`          | 执行命令并等待完成   | ⭐⭐⭐⭐⭐ 首选     |
| `subprocess.call()`         | 执行命令，返回退出码 | ⭐⭐⭐ 简单场景   |
| `subprocess.check_call()`   | 执行命令，失败抛异常 | ⭐⭐⭐ 简单场景   |
| `subprocess.check_output()` | 获取命令输出         | ⭐⭐⭐⭐ 常用      |
| `subprocess.Popen`          | 高级进程控制         | ⭐⭐⭐⭐⭐ 复杂场景 |
| `subprocess.PIPE`           | 创建管道             | ⭐⭐⭐⭐⭐ 常用     |
| `subprocess.DEVNULL`        | 丢弃输出             | ⭐⭐⭐⭐ 常用      |

# 9. 快速决策树

```python
需要执行外部命令？
├─ 是否需要实时输出？
│  └─ 是 → 使用 Popen + 逐行读取
│  └─ 否 → 继续
├─ 是否需要进程间通信/管道？
│  └─ 是 → 使用 Popen
│  └─ 否 → 继续
├─ 是否需要超时控制？
│  └─ 是 → subprocess.run(timeout=...) 或 Popen + communicate(timeout=...)
│  └─ 否 → 继续
├─ 默认选择 → subprocess.run()
```

