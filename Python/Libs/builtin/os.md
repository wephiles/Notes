---
aliases:
  - course of study
  - course
  - os
tags:
  - tutorial
  - computer-science
  - os-tutorial
  - Python
category: knowledge
datetime: " 2026-08-08 10:08:07 周六"
author: wephiles
rating: "2"
---
<h1 style="text-align: center;">os</h1>

os 模块是 Python 与操作系统交互的桥梁。

# 一、初识 os 模块

简单说，`os` 模块让我们在 Python 里使用操作系统的功能，比如：

- 读取/修改文件、目录
- 获取环境变量
- 执行系统命令
- 查看进程信息

并且它**自动适配 Windows、macOS、Linux**，一套代码多平台运行。

# 二、常用系统信息常量

这些常量告诉你当前运行的环境是什么，避免写死路径分隔符。

| 常量         | 含义                     | 示例输出 (Linux/macOS) | 示例输出 (Windows) |
| :----------- | :----------------------- | :--------------------- | :----------------- |
| `os.name`    | 操作系统类型             | `'posix'`              | `'nt'`             |
| `os.sep`     | 路径分隔符               | `'/'`                  | `'\\'`             |
| `os.linesep` | 行终止符                 | `'\n'`                 | `'\r\n'`           |
| `os.pathsep` | 环境变量分隔符 (如 PATH) | `':'`                  | `';'`              |

Windows：

```
import os

print(f'系统类型：{os.name}')
print(f'路径分隔符：{os.sep}')
print(f'行终止符：{os.linesep!r}')
print(f'环境变量分割符：{os.pathsep}')
```

输出：

```
系统类型：nt
路径分隔符：\
行终止符：'\r\n'
环境变量分割符：;
```

Linux：

```
import os

print(f'系统类型：{os.name}')
print(f'路径分隔符：{os.sep}')
print(f'行终止符：{os.linesep!r}')
print(f'环境变量分割符：{os.pathsep}')
```

输出：

```
系统类型：posix
路径分隔符：/
行终止符：'\n'
环境变量分割符：:
```

使用示例：

```
if os.name == 'nt':
    print("这是 Windows，开启多进程需要用 if __name__ == '__main__'")
else:
    print("这是 Unix-like 系统，可以用 os.fork()")
```

```
Windows：
这是 Windows, 开启多进程需要用 if __name__ == '__main__'

Linux：
系统类型：posix
路径分隔符：/
行终止符：'\n'
环境变量分割符：:
这是 Unix-like 系统，可以用 os.fork()
```

# 三、环境变量

环境变量常用来存密码、API 密钥、环境名称等，**千万别写死在代码里**。

## 3.1 `os.environ` —— 类似字典的环境变量对象

Windows：

```
import os

# 查看所有环境变量
for i, (key, value) in enumerate(os.environ.items()):
    # 太多 取前 10 个即可
    if i >= 10:
        break

# 读取某个变量 —— 不存在会抛出 KeyError
try:
    home = os.environ['HOME'] if os.name == 'nt' else os.environ['USERPROFILE']
    print('用户主目录:', home)
except KeyError as e:
    print(e)
except Exception as e:
    print(e)

# 更加安全的方式: os.getenv()
os.environ['API_KEY'] = 'This is an api key.'
api_key = os.getenv('API_KEY', 'Default value.')
print(api_key)
```

```
'HOME'
This is an api key.
```

![image-20260808105058140](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260808105330172.png)

Linux：

```
import os

# 查看所有环境变量
for i, (key, value) in enumerate(os.environ.items()):
    # 太多 取前 10 个即可
    if i >= 10:
        break
    print(i, '--->', key, '--->', value)

# 读取某个变量 —— 不存在会抛出 KeyError
try:
    home = os.environ['HOME'] if os.name == 'nt' else os.environ['USERPROFILE']
    print('用户主目录:', home)
except KeyError as e:
    print(e)
except Exception as e:
    print(e)

# 更加安全的方式: os.getenv()
os.environ['API_KEY'] = 'This is an api key.'
api_key = os.getenv('API_KEY', 'Default value.')
print(api_key)
```

```
0 ---> SHELL ---> /bin/bash
1 ---> SESSION_MANAGER ---> local/jinyu:@/tmp/.ICE-unix/2832,unix/jinyu:/tmp/.ICE-unix/2832
2 ---> QT_ACCESSIBILITY ---> 1
3 ---> COLORTERM ---> truecolor
4 ---> XDG_CONFIG_DIRS ---> /etc/xdg/xdg-ubuntu:/etc/xdg
5 ---> XDG_MENU_PREFIX ---> gnome-
6 ---> TERM_PROGRAM_VERSION ---> 1.105.17075
7 ---> XDG_CONFIG_DIRS_VSCODE_SNAP_ORIG ---> /etc/xdg/xdg-ubuntu:/etc/xdg
8 ---> GNOME_DESKTOP_SESSION_ID ---> this-is-deprecated
9 ---> GDK_BACKEND_VSCODE_SNAP_ORIG ---> 
'USERPROFILE'
This is an api key.
```

![image-20260808105316088](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260808105324998.png)

## 3.2 写环境变量（只影响当前进程以及子进程）

```
os.environ['MY_APP_MODE'] = 'development'
print(os.getenv('MY_APP_MODE'))  # development
```

## 3.3 工程建议

- 用 `os.getenv('KEY', '默认')` 提供默认值，避免变量缺失报错。
- 敏感信息用环境变量，配合 `.env` 文件（`python-dotenv` 库），不提交到 Git。

# 四、**文件和目录操作

## 4.1 `os.getcwd()` 和 `os.chdir(path)`

获取和改变当前工作目录。相对路径都基于这个目录。

```
import os

print(f"当前目录: {os.getcwd()}")
# 切换到上级目录
os.chdir('..')
print(f"切换后: {os.getcwd()}")
```

```
当前目录: /home/jinyu/Documents/pythonProjects/Demo
切换后: /home/jinyu/Documents/pythonProjects
```

## 4.2 `os.listdir()`  —— 列出目录内容

返回指定目录下的文件及子目录名列表（不含 `.` 和 `..`）。

```python
# 列出当前目录所有内容
contents = os.listdir('.')
print(contents)
```

```
['demo', 'static', 'pyproject.toml', 'uv.lock', 'manage.py', 'website', 'run.py', '.python-version', 'README.md', 'db.sqlite3', '.git', 'main.py', '.venv', 'templates', '.gitignore']
```

## 4.3 `os.scandir(path)` —— 推荐的迭代方式（Python 3.5+）

返回一个 `os.DirEntry` 对象的迭代器，**性能更好**，可以同时获取名称、类型、元数据，减少系统调用。

```python
import os

with os.scandir('.') as entries:
    for entry in entries:
        if entry.is_file():
            print(f"文件: {entry.name}, 大小: {entry.stat().st_size} 字节")
        elif entry.is_dir():
            print(f"目录: {entry.name}")
```

```python
目录: demo
目录: static
文件: pyproject.toml, 大小: 172 字节
文件: uv.lock, 大小: 3155 字节
文件: manage.py, 大小: 660 字节
目录: website
文件: run.py, 大小: 253 字节
文件: .python-version, 大小: 5 字节
文件: README.md, 大小: 0 字节
文件: db.sqlite3, 大小: 0 字节
目录: .git
文件: main.py, 大小: 82 字节
目录: .venv
目录: templates
文件: .gitignore, 大小: 109 字节
```

**`os.DirEntry` 类的主要属性和方法**：

- `entry.name` ：文件名
- `entry.path` ：完整路径
- `entry.is_file()` / `is_dir()` / `is_symlink()`
- `entry.stat()` ：获取文件元信息（返回 `os.stat_result` 对象）

## 4.4 遍历目录树 —— `os.walk(top)`

生成目录树中所有文件和文件夹，常用来批量处理文件。

```python
import os

for root, dirs, files in os.walk('./my_project'):
    for file in files:
        if file.endswith('.py'):
            full_path = os.path.join(root, file)
            print(f"Python 文件: {full_path}")
    # 可以在循环内修改 dirs（比如排除 .git 目录）
    if '.git' in dirs:
        dirs.remove('.git')
```

- `root`：当前目录路径
- `dirs`：当前目录下的子目录列表
- `files`：当前目录下的文件列表

## 4.5 创建目录

- `os.mkdir(path)` ：创建一个目录，父目录必须存在。

- `os.makedirs(path, exist_ok=True)` ：递归创建所有中间目录，`exist_ok=True` 避免报错。

```python
import os

# 创建单层目录
os.mkdir('test_dir')

# 创建多层目录，即使中间目录不存在也能创建
os.makedirs('a/b/c/d', exist_ok=True)
```

## 4.6 删除文件和目录

- `os.remove(path)` (或 `os.unlink`) ：删除文件，不能删目录。
- `os.rmdir(path)` ：删除空目录。
- `os.removedirs(path)` ：递归删除空目录，从叶子删到根，遇到非空就停止。

```python
import os

# 删除文件
open('temp.txt', 'w').close()
os.remove('temp.txt')

# 删除空目录
os.mkdir('empty_dir')
os.rmdir('empty_dir')

# 递归删除（如果所有子目录都为空）
os.makedirs('x/y/z')
os.removedirs('x/y/z')  # 会删除 z, y, x（如果都为空）
```

> 工程上更常用 `shutil.rmtree()` 删除非空目录，因为这个是 `os` 模块做不到的。

## 4.7 重命名和移动

- `os.rename(src, dst)` ：重命名文件或目录。
- `os.replace(src, dst)` ：跨平台原子替换，如果目标存在会被覆盖。
- `os.renames(old, new)` ：递归重命名，同时会创建必要的中间目录。

```python
os.rename('old_name.txt', 'new_name.txt')
```

## 4.8 文件元信息 `os.stat(path)`

返回一个 `os.stat_result` 对象，包含大小、权限、修改时间等。

```python
import os, time

info = os.stat('somefile.txt')
print(f"大小: {info.st_size} 字节")
print(f"最后修改: {time.ctime(info.st_mtime)}")
print(f"权限模式: {oct(info.st_mode)}")
```

## 4.9 权限与修改时间

```python
# 更改权限 (Unix 常用，Windows 部分支持)
os.chmod('script.sh', 0o755)

# 修改访问时间和修改时间
os.utime('data.txt', (access_time, modify_time))
```

### 4.10 路径操作

```python
import os

# 拼接路径（智能处理分隔符）
path = os.path.join('folder', 'subfolder', 'file.txt')
print(path)   # folder/subfolder/file.txt (或 Windows 的 \)

# 判断是否存在 / 是文件 / 是目录
print(os.path.exists(path))
print(os.path.isfile(path))
print(os.path.isdir(path))

# 拆分文件名与扩展名
filename, ext = os.path.splitext('archive.tar.gz')
print(filename, ext)  # archive.tar  .gz

# 获取目录部分、文件名部分
print(os.path.dirname('/a/b/c.txt'))  # /a/b
print(os.path.basename('/a/b/c.txt')) # c.txt

# 获取绝对路径
print(os.path.abspath('./data'))
```

# 五、进阶操作

## 5.1 执行系统命令 `os.system(command)`

直接运行 shell 命令，返回退出状态码。**无法捕获输出**，仅适合简单操作。

```python
import os
ret = os.system('echo Hello World')
print(f"返回码: {ret}")
```

输出：

```python
Hello World
返回码: 0
```

## 5.2 获取命令输出 `os.popen(command)`

返回文件对象，可以读取命令输出或写入输入。不过推荐用 `subprocess` 模块代替。

```python
import os
with os.popen('dir' if os.name == 'nt' else 'ls') as f:
    output = f.read()
print(output[:200])  # 只打印前 200 字符
```

## 5.3 进程 ID 和 父进程 ID

```python
import os
print(f"当前进程 PID: {os.getpid()}")
print(f"父进程 PID: {os.getppid()}")
```

## 5.4 创建子进程（Unix 专属）

`os.fork()` 会克隆当前进程，返回 0 表示在子进程中，返回 PID 表示在父进程中。Windows 不支持。

```python
import os, time

if os.name != 'nt':
    pid = os.fork()
    if pid == 0:
        print(f"子进程 PID: {os.getpid()}")
    else:
        print(f"父进程，子进程 PID: {pid}")
```

> 工程上如果要跨平台多进程，请使用 `multiprocessing` 或 `subprocess`。

## 5.5 执行新程序替换当前进程 `os.exec*` 系列

`os.execl`, `os.execvp` 等，会用新程序**完全替换**当前进程的内存空间，代码不会返回到原来的程序。常用于脚本解释器内部。

```python
# 用一个新 Python 脚本替换当前进程
# os.execlp('python', 'python', 'other_script.py')   # 取消注释将替换进程
```

## 5.6 等待子进程结束 `os.wait()`

```python
import os, sys
if os.name != 'nt':
    pid = os.fork()
    if pid == 0:
        print("子进程运行...")
        sys.exit(42)
    else:
        child_pid, status = os.wait()
        print(f"子进程 {child_pid} 退出，状态: {os.WEXITSTATUS(status)}")
```

# 六、文件描述符操作（底层IO）

`os` 模块提供了一系列操作文件描述符的函数，这些是 **底层接口**，上层 `open()` 就是基于它们实现的。

常用有：

- `os.open(path, flags, mode)` ：打开文件并返回文件描述符（整数）
- `os.read(fd, n)` ：从描述符读取 n 个字节
- `os.write(fd, data)` ：写入数据
- `os.close(fd)` ：关闭
- `os.lseek(fd, pos, how)` ：移动读写位置
- `os.fstat(fd)` ：获取文件描述符状态

```python
import os

# 用底层方式写文件
fd = os.open('low_level.txt', os.O_WRONLY | os.O_CREAT, 0o644)
bytes_written = os.write(fd, b'Hello from file descriptor!')
os.close(fd)
print(f"写入了 {bytes_written} 字节")

# 读取
fd = os.open('low_level.txt', os.O_RDONLY)
data = os.read(fd, 100)
print(data.decode())
os.close(fd)
```

工程上很少直接这么用，除非需要精细控制（如管道、非阻塞 I/O）。

# 七、类与异常

`os` 模块中的主要类：

| 类               | 说明                                                         |
| :--------------- | :----------------------------------------------------------- |
| `os.DirEntry`    | 由 `scandir()` 返回，用于高效遍历目录                        |
| `os.stat_result` | `stat()` 返回，文件元信息容器（有 st_size, st_mtime 等属性） |
| `os.environ`     | 环境变量的字典式映射（其实不是类，是 `Mapping` 对象）        |
| `OSError`        | 内置异常，是 `os` 模块里所有 `I/O` 错误的基类                |

## 7.1 异常处理

所有操作系统相关错误都会抛出 `OSError` 或其子类（`FileNotFoundError`, `PermissionError` 等）。处理方式：

```python
import os

try:
    os.remove('不存在的文件.txt')
except FileNotFoundError:
    print("文件不存在，无需删除")
except PermissionError:
    print("没有权限删除")
except OSError as e:
    print(f"其他系统错误: {e}")
```

# 八、工程实战建议 & 最佳实践

1. **路径拼接用 `os.path.join()`**，永远不要手动 `'path' + '/' + 'file'`。

2. **遍历目录用 `os.scandir()`** 代替 `os.listdir()`，速度更快，尤其在海量文件时。

   ```
   import os
   
   obj = os.scandir(r'E:\Code\PyProjects\Demos\practice\funcs')
   for item in obj:
       print(item.name, item.path)
   
   print(type(obj))  # <class 'nt.ScandirIterator'> / <class 'posix.ScandirIterator'>
   ```

3. **创建深层目录用 `os.makedirs(..., exist_ok=True)`**。

4. **获取配置用 `os.getenv()`**，配合默认值保证健壮性。

5. **执行外部命令请用 `subprocess` 模块**，不要用 `os.system()` 或 `os.popen()`，因为它们功能弱、有安全风险（`shell` 注入）。

6. **对于文件复制、移动、删除目录树，结合 `shutil` 模块使用**，`os` 模块提供的是基本原子操作。

7. **跨平台兼容**：检查 `os.name`，或避免使用平台特定功能（如 `os.fork`）；路径操作尽量用 `os.path` 或 `pathlib`。

# 九、附件 —— `os` 模块快速查阅卡片（摘要）

| 分类     | 常用函数/类                                                  | 用途                       |
| :------- | :----------------------------------------------------------- | :------------------------- |
| 系统信息 | `os.name`, `os.sep`, `os.linesep`                            | 判断平台、路径拼接         |
| 环境变量 | `os.environ`, `os.getenv()`                                  | 读取/设置环境变量          |
| 目录操作 | `os.getcwd()`, `os.chdir()`, `os.mkdir()`, `os.makedirs()`, `os.listdir()`, `os.scandir()`, `os.walk()` | 工作目录、创建、遍历       |
| 文件操作 | `os.remove()`, `os.rename()`, `os.replace()`, `os.stat()`, `os.chmod()`, `os.utime()` | 删除、重命名、元信息、权限 |
| 路径操作 | `os.path.join()`, `os.path.exists()`, `os.path.isfile()`, `os.path.isdir()`, `os.path.abspath()` | 路径处理                   |
| 进程     | `os.system()`, `os.popen()`, `os.getpid()`, `os.fork() -- (Unix)` | 命令执行、进程管理         |
| 描述符   | `os.open()`, `os.read()`, `os.write()`, `os.close()`         | 底层文件 I/O               |
| 异常     | `OSError`, `FileNotFoundError` 等                            | 捕获 I/O 错误              |

