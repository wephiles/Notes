```text
假设代码层级结构是这样的:
/root
	· main.py
	· base.py
```

----

---

```python
# base.py

def func_in_all():
    print("this is function func_in_all!")


def func_not_in_all():
    print("this is function func_not_in_all_1!")


def _func_in_all():
    print("this is function _func_in_all")


def _func_not_in_all():
    print("this is function _func_not_in_all")


def __func_in_all():
    print("this is function __func_in_all")


def __func_not_in_all():
    print("this is function __func_not_in_all")


variable_in_all = "This is variable variable_in_all"
variable_not_in_all = "This is a variable variable_not_in_all"


_variable_in_all = "This is a variable _variable_in_all"
_variable_not_in_all = "This is a variable _variable_not_in_all"

__variable_in_all = "This is a variable __variable_in_all"
__variable_not_in_all = "This is a variable __variable_not_in_all"	
```

```python
# main.py

from base import *

print(dir())  
# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'func_in_all', 'func_not_in_all', 'variable_in_all', 'variable_not_in_all']
```

以上在 `base.py` 没有定义 `__all__` 的情况下 `import *` 的状态

下面看看定义 `__all__` 的情况下 `import *` 的状态

```python
# base.py
__all__ = [
    "func_in_all",
    "_func_in_all",
    "__func_in_all",
    "variable_in_all",
    "_variable_in_all",
    "__variable_in_all",
]


def func_in_all():
    print("this is function func_in_all!")


def func_not_in_all():
    print("this is function func_not_in_all_1!")


def _func_in_all():
    print("this is function _func_in_all")


def _func_not_in_all():
    print("this is function _func_not_in_all")


def __func_in_all():
    print("this is function __func_in_all")


def __func_not_in_all():
    print("this is function __func_not_in_all")


variable_in_all = "This is variable variable_in_all"
variable_not_in_all = "This is a variable variable_not_in_all"


_variable_in_all = "This is a variable _variable_in_all"
_variable_not_in_all = "This is a variable _variable_not_in_all"

__variable_in_all = "This is a variable __variable_in_all"
__variable_not_in_all = "This is a variable __variable_not_in_all"

```

```python
# main.py

from base import *

print(dir())
# ['__builtins__', '__cached__', '__doc__', '__file__', '__func_in_all', '__loader__', '__name__', '__package__', '__spec__', '__variable_in_all', '_func_in_all', '_variable_in_all', 'func_in_all', 'variable_in_all']
```

上面是我们用 `import *` 来导入所有模块, 下面我们另外使用 `import xxx`

```python
# base.py
__all__ = [
    "func_in_all",
    "_func_in_all",
    "__func_in_all",
    "variable_in_all",
    "_variable_in_all",
    "__variable_in_all",
]


def func_in_all():
    print("this is function func_in_all!")


def func_not_in_all():
    print("this is function func_not_in_all_1!")


def _func_in_all():
    print("this is function _func_in_all")


def _func_not_in_all():
    print("this is function _func_not_in_all")


def __func_in_all():
    print("this is function __func_in_all")


def __func_not_in_all():
    print("this is function __func_not_in_all")


variable_in_all = "This is variable variable_in_all"
variable_not_in_all = "This is a variable variable_not_in_all"


_variable_in_all = "This is a variable _variable_in_all"
_variable_not_in_all = "This is a variable _variable_not_in_all"

__variable_in_all = "This is a variable __variable_in_all"
__variable_not_in_all = "This is a variable __variable_not_in_all"
```

```python
# main.py

from base import *
from base import func_not_in_all

print(dir())
# ['__builtins__', '__cached__', '__doc__', '__file__', '__func_in_all', '__loader__', '__name__', '__package__', '__spec__', '__variable_in_all', '_func_in_all', '_variable_in_all', 'func_in_all', 'func_not_in_all', 'variable_in_all']
```

我们发现 `__all__` 只会对 `from xxx import *` 生效, 对 `from xxx import yyy` 是不生效的.

----

---

---

上述演示只是针对于模块内的 `__all__`, 下面看 `__init__.py` 中的 `__all__`

```text
文件层级结构如下:
/root
    · main.py
    · /packages
        · __init__.py
        · base.py
        · module_get.py
        · module_put.py
```



























