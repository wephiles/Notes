---
aliases:
  - course of study
  - course
  - tutorial
  - pathlib tutorial
tags:
  - tutorial
  - Python
  - pathlib
  - libraries
  - built-in
  - computer-science
category:
  - pathlib
  - Python builtin libraries
  - knowledge
datetime: " 2026-08-02 13:08:29 周日"
author: wephiles
rating: "5"
---
`pathlib` 是 Python 3.4 引入的标准库，用面向对象的方式处理文件系统路径。它把路径抽象成对象，告别了 `os.path` 那种函数式、字符串拼接的操作方式，代码更清晰、可读性更强，而且跨平台兼容。

参考文档：

- [`Python官方文档`](https://docs.python.org/3/library/pathlib.html)
- [`GeeksForGeeks`](https://www.geeksforgeeks.org/python/pathlib-module-in-python/)
- [`W3Schools`](https://www.w3schools.com/python/ref_module_pathlib.asp)
- [`realpython`](https://realpython.com/python-pathlib/)
- [`DataCamp`](https://www.datacamp.com/tutorial/comprehensive-tutorial-on-using-pathlib-in-python-for-file-system-manipulation)

# 一、 核心类体系

`pathlib` 的类分为两大体系：`纯路径` 和 `具体路径`。 

| 类名                | 描述                            | 是否访问实际文件系统 |
| ----------------- | ----------------------------- | ---------- |
| `PurePath`        | 纯路径基类, 只做路径计算, 不涉及 `IO`       | ❌ 否        |
| `PurePosixPath`   | `UNIX/POSIX` 风格路径(`/分割`)      | ❌ 否        |
| `PureWindowsPath` | `Windows` 路径风格路径(`\分割`)       | ❌ 否        |
| `Path`            | 具体路径, 继承自 `PurePath`, 可执行文件操作 | ✅ 是        |
| `PosixPath`       | 具体路径                          | ✅ 是        |
| `WindowsPath`     | `Windows` 具体路径                | ✅ 是        |

**日常开发中, 直接使用 `Path` 即可**, 它会根据操作系统自动实例化为 `PosixPath` 或 `WindowsPath`.

```python
from pathlib import Path
```

# 二、 创建路径对象

## 2.1 直接创建

```python
from pathlib import Path


a = Path(".")  # 当前目录
b = Path("foo/bar.txt")  # 相对路径
c = Path("/etc/nginx")  # 绝对路径
d = Path("D:\\data")  # Windows 路径

print(a)
print(b)
print(c)
print(d)
```

运行结果：

```python
.
foo\bar.txt
\etc\nginx
D:\data
```

## 2.2 特殊构造方法

```python
Path.cwd()  # 当前工作目录，类似 os.getcwd()
Path.home()  # 用户主目录，类似 os.path.expanduser('~')
```

示例：

```python
from pathlib import Path


print(Path.cwd())
print(Path.home())
```

输出结果：

```python
E:\Code\PyProjects\Demos\practice
C:\Users\wephiles
```

上述代码在 Linux 环境运行后结果：

![image-20260802120610951](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260802120612356.png)

## 2.3 路径拼接 —— `/` 运算符

这是 `pathlib` 最优雅的特性，只需用 `/` 拼接字符串或另一个 `Path` 对象：

```python
from pathlib import Path


base = Path("/usr")
full = base / "local" / "bin"
print(full)  # \usr\local\bin
```

## 2.4 从其他表示创建

```python
from pathlib import Path


print(Path("foo", "bar", "baz"))  # foo\bar\baz
```

# 三、 纯路径方法

这部分方法不访问磁盘，只做字符串级别的路径计算。

## 3.1 路径属性

| 属性          | 示例 (`Path('/home/user/docs/20250305/file.tar.gz')`) | 说明              |
| :---------- | :-------------------------------------------------- | :-------------- |
| `.name`     | `'file.tar.gz'`                                     | 完整文件名           |
| `.stem`     | `'file.tar'`                                        | 去掉最后一个后缀的文件名    |
| `.suffix`   | `'.gz'`                                             | 最后一个后缀          |
| `.suffixes` | `['.tar', '.gz']`                                   | 所有后缀列表          |
| `.parent`   | `Path('/home/user/docs')`                           | 父目录             |
| `.parents`  | 序列，索引 0 为直接父目录                                      | 所有祖先目录          |
| `.parts`    | `('/', 'home', 'user', 'docs', 'file.tar.gz')`      | 各组成部分元组         |
| `.root`     | `'/'`                                               | 根目录             |
| `.anchor`   | `'/'`                                               | 根 + 盘符（Windows） |
| `.drive`    | `''`（Linux）或 `'C:'`（Win）                            | 盘符              |

示例`（Windows）`：

```python
from pathlib import Path

path = Path("D:\\home\\user\\docs\\20250305\\file.demo.show.txt")


print(path.name)  # file.demo.show.txt
print(path.stem)  # file.demo.show
print(path.suffix)  # .txt
print(path.suffixes)  # ['.demo', '.show', '.txt']
print(path.parent)  # D:\home\user\docs\20250305
print(path.parents)  # <WindowsPath.parents>
print(path.parts)  # ('D:\\', 'home', 'user', 'docs', '20250305', 'file.demo.show.txt')
print(path.root)  # \
print(path.anchor)  # D:\
print(path.drive)  # D:
```

示例`（Linux）`：

```python
from pathlib import Path

path = Path("/home/user/docs/file.20250103.tar.gz")


print(path.name)  # file.20250103.tar.gz
print(path.stem)  # file.20250103.tar
print(path.suffix)  # .gz
print(path.suffixes)  # ['.20250103', '.tar', '.gz']
print(path.parent)  # /home/user/docs
print(path.parents)  # <PosixPath.parents>
print(path.parts)  # ('/', 'home', 'user', 'docs', 'file.20250103.tar.gz')
print(path.root)  # /
print(path.anchor)  # /
print(path.drive)  #
```

## 3.2 路径变换

| 方法                   | 作用                         | 示例                        |
| :--------------------- | :--------------------------- | :-------------------------- |
| `.with_name(name)`     | 替换文件名                   | `p.with_name('new.txt')`    |
| `.with_suffix(suffix)` | 替换后缀                     | `p.with_suffix('.bz2')`     |
| `.with_stem(stem)`     | 替换 stem (3.9+)             | `p.with_stem('archive')`    |
| `.relative_to(other)`  | 计算出相对路径               | `p.relative_to('/home')`    |
| `.joinpath(*args)`     | 拼接子路径（等价于 `/`）     | `p.joinpath('sub', 'file')` |
| `.as_posix()`          | 返回 POSIX 风格字符串（`/`） | `'home/user/docs'`          |
| `.as_uri()`            | 转成 file URI                | `'file:///home/user/docs'`  |
| `str(p)`               | 返回平台原生路径字符串       |                             |

`Windows`：

```python
from pathlib import Path

p = Path(__file__)

print(p)  # E:\Code\PyProjects\Demos\practice\funcs\my_path.py
print(p.with_name('rename.txt'))  # E:\Code\PyProjects\Demos\practice\funcs\rename.txt
print(p.with_suffix('.mp4'))  # E:\Code\PyProjects\Demos\practice\funcs\my_path.mp4
print(p.with_stem('path_666'))  # E:\Code\PyProjects\Demos\practice\funcs\path_666.py
print(p.relative_to('E:\\Code\\PyProjects\\Demos\\practice'))  # funcs\my_path.py
print(p.joinpath('sub', 'good.txt'))  # E:\Code\PyProjects\Demos\practice\funcs\my_path.py\sub\good.txt
print(p.as_posix())  # E:/Code/PyProjects/Demos/practice/funcs/my_path.py
print(p.as_uri())  # file:///E:/Code/PyProjects/Demos/practice/funcs/my_path.py
print(str(p))  # E:\Code\PyProjects\Demos\practice\funcs\my_path.py
```

`Linux`：

```python
from pathlib import Path

p = Path(__file__)

print(p)  
print(p.with_name('rename.txt'))  
print(p.with_suffix('.mp4'))  
print(p.with_stem('path_666')) 
print(p.relative_to('/home')) 
print(p.joinpath('sub', 'good.txt'))  
print(p.as_posix()) 
print(p.as_uri()) 
print(str(p))
```

```python
/home/jinyu/Documents/pythonProjects/Demo/run.py
/home/jinyu/Documents/pythonProjects/Demo/rename.txt
/home/jinyu/Documents/pythonProjects/Demo/run.mp4
/home/jinyu/Documents/pythonProjects/Demo/path_666.py
jinyu/Documents/pythonProjects/Demo/run.py
/home/jinyu/Documents/pythonProjects/Demo/run.py/sub/good.txt
/home/jinyu/Documents/pythonProjects/Demo/run.py
file:///home/jinyu/Documents/pythonProjects/Demo/run.py
/home/jinyu/Documents/pythonProjects/Demo/run.py
```

## 3.3 判断方法

| 方法                     | 作用                         |
| :----------------------- | :--------------------------- |
| `.is_absolute()`         | 是否为绝对路径               |
| `.is_relative_to(other)` | 是否相对于另一个路径 (3.9+)  |
| `.match(pattern)`        | 是否匹配通配符模式（不递归） |

```python
from pathlib import Path

p = Path(__file__)

print(p.is_absolute())  # True

p_1 = Path('./data/dat.txt')
print(p_1.is_absolute())  # False
```

# 四、 具体路径方法（`Path` 独有）

这些方法会**真正访问文件系统**，可能抛出 `OSError` 或 `PermissionError`。

下面所有案例均基于 `Windows`

## 4.1 存在性与类型判断

```python
from pathlib import Path

p = Path('data.txt')

print(p.exists())          # 路径是否存在
print(p.is_file())         # 是否是普通文件
print(p.is_dir())          # 是否是目录
print(p.is_symlink())      # 是否是符号链接
print(p.is_socket())       # 是否是 socket
print(p.is_fifo())         # 是否是管道
print(p.is_block_device()) # 是否是块设备
print(p.is_char_device())  # 是否是字符设备
print(p.is_mount())        # 是否是挂载点 (3.7+)
```

输出结果：

```python
True
True
False
False
False
False
False
False
False
```

## 4.2 文件元信息

```python
from pathlib import Path

p = Path('data.txt')

print(p.stat())  # 返回 os.stat_result，包含大小、权限、时间等
print(p.lstat())  # 若为符号链接，返回链接本身的信息
# p.owner()  # 文件所有者 (Unix)
# p.group()  # 文件所属组 (Unix)
```

输出结果：

```
os.stat_result(st_mode=33206, st_ino=7599824371321814, st_dev=5391008048241521747, st_nlink=1, st_uid=0, st_gid=0, st_size=0, st_atime=1785647011, st_mtime=1785647011, st_ctime=1785647011)
os.stat_result(st_mode=33206, st_ino=7599824371321814, st_dev=5391008048241521747, st_nlink=1, st_uid=0, st_gid=0, st_size=0, st_atime=1785647011, st_mtime=1785647011, st_ctime=1785647011)
```

注意：`stat` 方法返回的对象可以这样用

```
from pathlib import Path

p = Path('data.txt')

stat = p.stat()
print(stat.st_size)  # 文件大小(字节)
print(stat.st_mtime)  # 文件修改时间
```

输出结果：

```
3
1785647328.041
```

## 4.3 路径解析

```python
p.resolve()        # 解析所有符号链接，返回绝对路径
p.absolute()       # 转为绝对路径（不解析符号链接）
p.expanduser()     # 展开 ~ 和 ~user
```

## 4.4 文件读写

这是 `pathlib` 最便利的特性之一，无需手动 `open` 和 `close`。

```python
from pathlib import Path

p = Path('data.txt')

text = p.read_text(encoding='utf-8')  # 读取文本
print('原始文件数据:', text)
p.write_text('Hello, world!\n', encoding='utf-8')  # 写入文本
text = p.read_text(encoding='utf-8')
print("写入文本后文件数据:", text)

data = p.read_bytes()
print("二进制文件数据:", data)
p.write_bytes(b'\x12\x16')
data = p.read_bytes()
print("写入二进制数据后文件数据(二进制):", data)
text = p.read_text(encoding='utf-8')
print("写入二进制后文件文本数据:", text)
```

```python
原始文件数据: 惹我光头强，揍你没商量。
写入文本后文件数据: Hello, world!

二进制文件数据: b'Hello, world!\r\n'
写入二进制数据后文件数据(二进制): b'\x12\x16'
写入二进制后文件文本数据: 
```

![image-20260802132220993](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260802132222057.png)

## 4.5 用传统文件打开

```python
from pathlib import Path

p = Path('data.txt')

with p.open('r', encoding='utf-8') as fp:
    for line in fp:
        print(line)
```

## 4.6 目录遍历与匹配

```python
from pathlib import Path

p = Path(r'E:\Code\PyProjects\Demos\practice')

print('====================================================')

# 遍历直接子项（不含子目录内容）
for child in p.iterdir():
    print(child)

print('====================================================')

# glob 模式匹配（当前目录）
for py_file in p.glob('*.py'):
    print(py_file)

print('====================================================')

# 递归 glob（类似 **/*.py）
for py_file in p.rglob('*.py'):
    print(py_file)
```

```python
====================================================
E:\Code\PyProjects\Demos\practice\.idea
E:\Code\PyProjects\Demos\practice\.venv
E:\Code\PyProjects\Demos\practice\cache_about
E:\Code\PyProjects\Demos\practice\funcs
E:\Code\PyProjects\Demos\practice\main.py
E:\Code\PyProjects\Demos\practice\pyproject.toml
E:\Code\PyProjects\Demos\practice\uv.lock
E:\Code\PyProjects\Demos\practice\__pycache__
====================================================
E:\Code\PyProjects\Demos\practice\main.py
====================================================
E:\Code\PyProjects\Demos\practice\main.py
E:\Code\PyProjects\Demos\practice\cache_about\my_cache.py
E:\Code\PyProjects\Demos\practice\cache_about\stroong_cache.py
E:\Code\PyProjects\Demos\practice\cache_about\__init__.py
E:\Code\PyProjects\Demos\practice\funcs\demonstration.py
E:\Code\PyProjects\Demos\practice\funcs\my_path.py
E:\Code\PyProjects\Demos\practice\funcs\__init__.py
E:\Code\PyProjects\Demos\practice\funcs\闭包01.py
E:\Code\PyProjects\Demos\practice\funcs\闭包02.py
E:\Code\PyProjects\Demos\practice\.venv\Scripts\activate_this.py
E:\Code\PyProjects\Demos\practice\.venv\Lib\site-packages\_virtualenv.py
```

`glob` 和 `rglob` 返回的是生成器，适用于大量文件。

## 4.7 创建与删除

```python
p.mkdir()                 # 创建目录
p.mkdir(parents=True, exist_ok=True)  # 递归创建，存在不报错

p.rmdir()                 # 删除空目录
p.unlink()                # 删除文件或符号链接
p.unlink(missing_ok=True) # 文件不存在不报错 (3.8+)
```

## 4.8 重命名与替换

```python
target = Path('new_name.txt')
p.rename(target)   # 重命名/移动（跨文件系统可能失败）
p.replace(target)  # 重命名/移动，强制覆盖目标（跨文件系统也会替换）
```

示例：

```python
from pathlib import Path

p = Path('./old_data.txt')

p.rename('new_data.txt')
```

> [!Caution]
>
> **注意：** `p.rename()` 重命名时有移动文件功能！

## 4.9 符号链接与硬链接

```python
p.symlink_to('/usr/bin/python3')    # 创建指向 p 的符号链接，p 是链接本身
p.link_to('/some/existing/file')    # 创建硬链接，p 是链接
```

**注意方向**：`symlink_to(target)` 的意思是“将当前路径（`p`）创建为指向 `target` 的符号链接”，即 `p -> target`。

## 4.10 修改权限与时间

```
p.chmod(0o755)              # 更改权限
p.lchmod(0o644)             # 如果是符号链接，改链接自身权限 (Unix)
p.touch(mode=0o600, exist_ok=True)  # 更新访问/修改时间，不存在则创建
```

## 4.11 比较路径

```
p.samefile(other_path)      # 判断是否指向同一文件/目录（即使路径不同）
```

## 4.12 实用操作（Python 3.8+）

```
p = Path('docs/archive.tar.gz')

# 直接获取 home 目录的相对路径
p.relative_to(Path.home())  # 相对于 home

# 读取并写入（链式操作）
Path('output.txt').write_text(
    Path('input.txt').read_text().upper()
)
```

# 五、 与 `os.path` 的常见映射

| os.path 函数         | pathlib 等价                |
| :------------------- | :-------------------------- |
| `os.path.abspath()`  | `Path.resolve()`            |
| `os.path.realpath()` | `Path.resolve()`            |
| `os.path.exists()`   | `Path.exists()`             |
| `os.path.isdir()`    | `Path.is_dir()`             |
| `os.path.isfile()`   | `Path.is_file()`            |
| `os.path.join()`     | `Path / 'sub'`              |
| `os.path.basename()` | `Path.name`                 |
| `os.path.dirname()`  | `Path.parent`               |
| `os.path.splitext()` | `Path.stem` + `Path.suffix` |
| `glob.glob()`        | `Path.glob()`               |
| `open(path, 'r')`    | `Path.open()`               |
| 读取文本             | `Path.read_text()`          |
| 写入文本             | `Path.write_text()`         |

# 六、 综合示例

```python
from pathlib import Path

# 遍历当前目录下所有 .txt 文件，读取并打印非空行
for txt_file in Path.cwd().glob('*.txt'):
    print(f"--- {txt_file.name} ---")
    for line in txt_file.read_text(encoding='utf-8').splitlines():
        if line.strip():
            print(line)
```

```python
# 在桌面创建嵌套目录并写入文件
desktop = Path.home() / 'Desktop'
project = desktop / 'my_project' / 'data'
project.mkdir(parents=True, exist_ok=True)

readme = project / 'README.md'
readme.write_text('# My Project\nData files stored here.')
```

```python
# 批量修改文件后缀
for md in Path('docs').rglob('*.md'):
    md.rename(md.with_suffix('.rst'))
```

# 七、 注意事项

1. **跨平台**：用 `/` 拼接会自动处理分隔符，不要手动拼接 `'/'` 或 `'\\'`。
2. **性能**：`glob` 返回生成器，但 `rglob` 底层是 `os.scandir`，在大目录下效率优于 `os.walk` + 过滤。
3. **路径是对象**：很多接受字符串路径的函数（如 `open()`、`shutil.copy()`）也直接接受 `Path` 对象（Python 3.6+ 的 PEP 519）。
4. **错误处理**：操作文件系统时会抛出 `FileNotFoundError`、`PermissionError` 等，注意捕获。

`pathlib` 提供了从路径计算到文件 IO 的一站式解决方案，是现代 Python 文件操作的首选。一旦习惯了 `Path` 的流畅语法，就很难再回到 `os.path` 的繁琐写法。
