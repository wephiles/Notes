# Python 类型提示完全指南

## 一、`Callable` 的使用

`Callable` 用于标注**可调用对象**（函数、方法、lambda、实现了 `__call__` 的类实例等）。

### 基本语法

```
from typing import Callable

# Callable[[参数类型列表], 返回值类型]
```

### 示例

```
from typing import Callable

# ---- 1. 最基础的用法：函数接受一个函数作为参数 ----
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    """接受一个两参数函数，返回 int"""
    return func(a, b)

apply(lambda x, y: x + y, 1, 2)   # ✅ 返回 3
apply(lambda x, y: x * y, 3, 4)   # ✅ 返回 12

# ---- 2. 参数为空的可调用对象 ----
def run_task(task: Callable[[], None]) -> None:
    """接受一个无参无返回值的函数"""
    task()

run_task(lambda: print("hello"))   # ✅

# ---- 3. 任意参数的可调用对象 ----
from collections.abc import Callable as AbcCallable

def execute_any(func: AbcCallable[..., int]) -> int:
    """... 表示任意参数，返回值必须是 int"""
    return func(1, 2, 3)

# ---- 4. 作为返回值类型 ----
def get_logger(name: str) -> Callable[[str], None]:
    """返回一个打印函数"""
    def log(msg: str) -> None:
        print(f"[{name}] {msg}")
    return log

logger = get_logger("APP")
logger("started")  # 输出: [APP] started

# ---- 5. 用 Protocol 定义更精细的可调用协议 ----
from typing import Protocol

class DoubleFunc(Protocol):
    def __call__(self, x: int) -> int: ...

def use_double(f: DoubleFunc, n: int) -> int:
    return f(n)

use_double(lambda x: x * 2, 5)   # ✅ 返回 10
```

## 二、`TypeVar` 的使用

`TypeVar` 用于定义**类型变量**，实现**泛型编程**，让函数/类的类型可以"参数化"。

### 基本语法

```
from typing import TypeVar

T = TypeVar('T')                    # 任意类型
T_co = TypeVar('T_co', covariant=True)    # 协变（只用于返回值）
T_contra = TypeVar('T_contra', contravariant=True)  # 逆变（只用于参数）

# 约束类型变量 —— 只能是 str 或 bytes
StrOrBytes = TypeVar('StrOrBytes', str, bytes)
```

### 示例

```
from typing import TypeVar, List

T = TypeVar('T')

# ---- 1. 泛型函数：输入什么类型，输出什么类型 ----
def first(items: List[T]) -> T:
    return items[0]

x: int = first([1, 2, 3])           # T 被推断为 int
s: str = first(["a", "b"])          # T 被推断为 str

# ---- 2. 多个类型变量 ----
K = TypeVar('K')
V = TypeVar('V')

def pair(key: K, value: V) -> tuple[K, V]:
    return (key, value)

result: tuple[str, int] = pair("age", 30)

# ---- 3. 有界类型变量 ----
Num = TypeVar('Num', int, float)  # Num 只能是 int 或 float

def add(a: Num, b: Num) -> Num:
    return a + b

add(1, 2)        # ✅  返回 int
add(1.5, 2.5)    # ✅  返回 float
# add(1, "2")     # ❌ 类型检查器报错

# ---- 4. 泛型类 ----
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def top(self) -> T:
        return self._items[-1]

stack_int = Stack[int]()       # 只能放 int
stack_int.push(1)
# stack_int.push("hello")      # ❌ 类型检查器报错

stack_str = Stack[str]()       # 只能放 str
stack_str.push("hello")

# ---- 5. Self 类型（Python 3.11+）----
from typing import Self

class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self

    def set_age(self, age: int) -> Self:
        self.age = age
        return self

# 链式调用时返回值类型正确
b: Builder = Builder().set_name("Alice").set_age(30)
```

### TypeVar 的约束 vs 有界

```
# 有界—— 只能是列出的类型之一
OnlyStrOrInt = TypeVar('OnlyStrOrInt', str, int)

# 约束—— 只要是这些类型的子类就可以，但仍然是同一个类型
class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

A = TypeVar('A', bound=Animal)  # A 可以是 Animal 或其任何子类

def feed(animal: A) -> A:
    return animal
```

## 三、其他常用类型提示

### 1. 基本类型

```
a: int = 1
b: float = 1.0
c: str = "hello"
d: bool = True
e: bytes = b"data"
f: None = None
```

### 2. 容器类型（Python 3.9+ 可直接用内置类型）

```
# === Python 3.9+ 推荐写法（PEP 585）===
items: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1}
unique: set[int] = {1, 2, 3}
pair: tuple[str, int] = ("a", 1)

# === Python 3.8 及以下需要从 typing 导入 ===
from typing import List, Dict, Set, Tuple
items: List[int] = [1, 2, 3]
mapping: Dict[str, int] = {"a": 1}
```

### 3. 特殊容器类型

```
from typing import Optional, Union, Literal, Any

# Optional[X]  ===  X | None  （值可以是 X 或 None）
name: Optional[str] = None
name: str | None = None          # Python 3.10+ 推荐写法

# Union[X, Y]   ===  X | Y     （值可以是多种类型之一）
value: Union[int, str] = 42
value: int | str = "hello"       # Python 3.10+ 推荐写法

# Literal[]      —— 值只能是字面量之一
direction: Literal["north", "south", "east", "west"] = "north"
status: Literal[0, 1, 2] = 1

# Any            —— 任意类型（等同于没有类型检查，慎用）
data: Any = 42
data = "now it's a string"       # ✅ 不报错（逃逸类型检查）
```

### 4. `Final` 和 `ClassVar`

```
from typing import Final, ClassVar

class Config:
    # ClassVar: 类变量，不属于实例
    MAX_SIZE: ClassVar[int] = 100

    # Final: 运行时不可重新赋值
    VERSION: Final[str] = "1.0.0"

    def __init__(self) -> None:
        # 实例的 Final 属性（只能在 __init__ 中赋值一次）
        self.id: Final[int] = 0

# Config.VERSION = "2.0"  # ❌ 类型检查器报错
```

### 5. `Protocol` — 结构化子类型（鸭子类型的静态检查）

```
from typing import Protocol

class Speakable(Protocol):
    def speak(self) -> str: ...

class Dog:
    def speak(self) -> str:
        return "Woof!"

class Robot:
    def speak(self) -> str:
        return "Beep!"

def make_sound(thing: Speakable) -> None:
    print(thing.speak())

make_sound(Dog())    # ✅ Dog 有 speak() 方法，符合 Protocol
make_sound(Robot())  # ✅ Robot 有 speak() 方法，符合 Protocol
# make_sound(42)     # ❌ int 没有 speak() 方法
```

### 6. `TypedDict` — 带类型的字典

```
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str

user: User = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}

# user["age"] = "30"  # ❌ 类型检查器报错，必须是 int
```

### 7. `NamedTuple` — 带类型的命名元组

```
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p = Point(1.0, 2.0)
print(p.x)    # 1.0
# p.z         # ❌ 类型检查器报错
```

### 8. `NewType` — 语义化的类型别名

```
from typing import NewType

UserId = NewType('UserId', int)
OrderId = NewType('OrderId', int)

user_id: UserId = UserId(42)
order_id: OrderId = OrderId(42)

# 虽然运行时都是 int，但类型检查器会把它们视为不同类型
def get_user(uid: UserId) -> str:
    return f"user-{uid}"

get_user(user_id)    # ✅
# get_user(order_id)  # ❌ 类型检查器报错
```

### 9. `Type` — 表示类本身

```
from typing import Type

class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

def create(cls: Type[Animal]) -> Animal:
    return cls()

dog = create(Dog)  # ✅ 返回类型推断为 Dog（子类也可以）
```

### 10. `ParamSpec` — 参数签名泛型（Python 3.10+）

```
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec('P')
R = TypeVar('R')

def log_and_call(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    """装饰器：打印日志后调用原函数，完整保留参数签名"""
    print(f"Calling {func.__name__}")
    return func(*args, **kwargs)

result = log_and_call(int, "123")        # ✅ result 是 int
result = log_and_call(len, [1, 2, 3])    # ✅ result 是 int
```

### 11. `Concatenate` — 扩展参数签名（Python 3.10+）

```
from typing import Concatenate, ParamSpec, TypeVar, Callable

P = ParamSpec('P')
R = TypeVar('R')

def with_db(conn: "Connection", func: Callable[Concatenate[str, P], R],
            name: str, *args: P.args, **kwargs: P.kwargs) -> R:
    """给函数额外注入一个连接参数"""
    return func(conn, name, *args, **kwargs)
```

### 12. `overload` — 函数重载

```
from typing import overload

@overload
def process(data: str) -> str: ...
@overload
def process(data: int) -> int: ...
@overload
def process(data: list) -> list: ...

def process(data):
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, int):
        return data * 2
    else:
        return [x * 2 for x in data]

r1: str  = process("hello")   # ✅ 类型推断为 str
r2: int  = process(5)          # ✅ 类型推断为 int
r3: list = process([1, 2])     # ✅ 类型推断为 list
```

### 13. `cast` — 类型转换（仅用于类型检查器提示）

```
from typing import cast, Any

data: Any = get_from_json()            # 没有类型信息
user: User = cast(User, data)          # 告诉检查器"我保证这是 User"
```

### 14. `assert_never` — 穷尽检查

```
from typing import assert_never

def handle(event: Literal["click", "hover", "focus"]) -> str:
    if event == "click":
        return "clicked"
    elif event == "hover":
        return "hovered"
    elif event == "focus":
        return "focused"
    else:
        # 如果添加了新的字面量但忘记处理，这里会报错
        assert_never(event)
```

## 四、类型提示有什么意义？



| 意义               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| **📖 文档化**       | 类型本身就是最好的文档，一眼看出函数期望什么、返回什么       |
| **🐛 提前发现 Bug** | 在代码运行**之前**（写代码时）就发现类型错误，而不是到线上才崩 |
| **🤖 IDE 智能补全** | VSCode / PyCharm 根据类型提示提供精准的自动补全和参数提示    |
| **🔄 重构安全**     | 改了某个函数的签名，类型检查器会帮你找到所有需要同步修改的地方 |
| **👥 团队协作**     | 明确的接口约定，减少"这个参数传什么？"的沟通成本             |
| **🔗 接口契约**     | 类似于 Java/C# 的接口/泛型系统，让 Python 也能做大规模工程   |

### 配合工具使用

```
# mypy — 最流行的 Python 静态类型检查器
pip install mypy
mypy my_project/

# pyright — 微软开发的类型检查器（VSCode 内置）
npm install -g pyright
pyright my_project/

# 在 VSCode 中，安装 Pylance 扩展即可获得实时类型检查
```

> **注意**：Python 的类型提示在运行时**不会强制执行**，它们是给**静态检查器**和 **IDE** 看的。如果想运行时强制检查，可以用 `@dataclass` + `__post_init__`、`pydantic` 等库。



## Generator 详解

### 1. `Generator[YieldType, SendType, ReturnType]` 三个类型参数的含义

```
Generator[YieldType, SendType, ReturnType]
            │         │          │
            │         │          └─ 函数 return 时返回值的类型
            │         └─ yield 接收外部 send() 传入值的类型
            └─ yield 产出值的类型
```

对应生成器函数内部的三种操作：

```
def example() -> Generator[str, int, float]:
    received = yield "hello"      # yield "hello" → YieldType = str
                                   # received 的类型 → SendType = int
    received2 = yield "world"     # 同上
    return 3.14                   # return → ReturnType = float
gen = example()

# 第一次 next()，产出 "hello"
print(next(gen))                # 输出: hello

# send(42) 把 42 发送进生成器，赋给 received，然后产出 "world"
print(gen.send(42))             # 输出: world

# 再次 send(99)，赋给 received2，然后生成器 return 3.14
try:
    gen.send(99)
except StopIteration as e:
    print(e.value)               # 输出: 3.14
```

### 2. 最常见的简化形式

绝大多数情况下，`SendType` 和 `ReturnType` 都是 `None`：

```
def __iter__(self) -> Generator[T, None, None]:
    for i in range(self._size):
        yield self._data[i]

# 完全等价于 Iterator[T]
```

### 3. Generator vs Iterator

```
from collections.abc import Iterator, Generator
# Iterator[X]  等价于  Generator[X, None, None]
# Generator 是 Iterator 的超集（多出 send / throw / close 能力）
```

## TypeVar 详解

### 1. 基本声明

```
from typing import TypeVar

T = TypeVar('T')            # 最灵活，可以是任何类型
```

### 2. 约束类型

```
# T 可以是 int 或 float，但不能是 str 等
NumberT = TypeVar('NumberT', int, float)

def add(a: NumberT, b: NumberT) -> NumberT:
    return a + b

add(1, 2)        # ✅
add(1.5, 2.5)    # ✅
add(1, "hello")  # ❌ 类型检查报错
```

### 3. 约束边界

```
# T 必须是 Comparable 的子类型（协议约束）
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...

CT = TypeVar('CT', bound=Comparable)

def find_max(items: list[CT]) -> CT:
    return max(items)
```

### 4. 完整的泛型类示例

```
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None
```





----

----

----







# 2. `Python TypeHint` 完整详解 -- 看这个就够了

> 适用于 Python 3.9+（部分特性需要更高版本）

## 📌 第一部分：常用 `TypeHint`

### 1. 基础类型

```
# 整数
age: int = 25

# 浮点数
score: float = 98.5

# 字符串
name: str = "Alice"

# 布尔值
is_active: bool = True

# 字节
data: bytes = b"hello"

# 无返回值（函数）
def say_hello() -> None:
    print("Hello!")
```

### 2. `Any` — 任意类型

```
from typing import Any

def process(data: Any) -> Any:
    # 接受任何类型，返回任何类型
    return data
```

> ⚠️ `Any` 会关闭类型检查，应尽量少用。

### 3. `Optional` / `Union` — 可选类型 / 联合类型

```
from typing import Optional, Union

# Optional[X] 等价于 Union[X, None]，表示"可以是 X，也可以是 None"
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None  # 找不到返回 None

# Union 表示"多种类型之一"
def parse_value(value: Union[int, str, float]) -> str:
    return str(value)

# Python 3.10+ 可以用 | 语法（推荐）
def find_user_v2(user_id: int) -> str | None:
    if user_id == 1:
        return "Alice"
    return None

def parse_value_v2(value: int | str | float) -> str:
    return str(value)
```

### 4. 容器类型 — `List`, `Dict`, `Set`, `Tuple`

```
from typing import List, Dict, Set, Tuple

# List[T] — 元素全部为 T 的列表
names: List[str] = ["Alice", "Bob", "Charlie"]
scores: List[int] = [100, 90, 85]

# Python 3.9+ 推荐：直接用内置类型
names: list[str] = ["Alice", "Bob"]

# Dict[K, V] — 键类型 K，值类型 V 的字典
user_map: Dict[str, int] = {"Alice": 25, "Bob": 30}
# Python 3.9+
user_map: dict[str, int] = {"Alice": 25}

# Set[T] — 元素全部为 T 的集合
unique_ids: Set[int] = {1, 2, 3, 4}
# Python 3.9+
unique_ids: set[int] = {1, 2, 3}

# Tuple[T1, T2, ...] — 固定长度、各位置类型可不同的元组
point: Tuple[int, int] = (10, 20)          # 两个 int
record: Tuple[str, int, float] = ("Alice", 25, 98.5)  # 混合类型

# Python 3.9+
point: tuple[int, int] = (10, 20)
```

### 5. `Callable` — 可调用对象（函数类型）

```
from typing import Callable

# Callable[[参数类型们], 返回类型]
def apply(fn: Callable[[int, int], int], a: int, b: int) -> int:
    return fn(a, b)

# 实际使用
result = apply(lambda x, y: x + y, 3, 5)  # 8

# 无参数的 callable
def run_task(task: Callable[[], None]) -> None:
    task()

# 可变参数的 callable（不精确）
def execute(fn: Callable[..., int]) -> int:
    return fn()
```

### 6. `Type` — 类本身（而非实例）

```
from typing import Type

class Animal: pass
class Dog(Animal): pass

# Type[X] 表示"X 这个类本身"，而不是 X 的实例
def create_instance(cls: Type[Animal]) -> Animal:
    return cls()

dog = create_instance(Dog)  # ✅ Dog 是 Animal 的子类
```

### 7. `TypeVar` — 泛型变量

```
from typing import TypeVar, List

# 定义泛型变量
T = TypeVar('T')          # 可以是任意类型
K = TypeVar('K')          # 另一个独立的泛型变量
N = TypeVar('N', int, float)  # 约束为 int 或 float

# 泛型函数：输入什么类型，输出什么类型
def first(items: List[T]) -> T:
    return items[0]

a = first([1, 2, 3])       # 返回 int
b = first(["x", "y"])      # 返回 str

# 约束泛型
def add(a: N, b: N) -> N:
    return a + b

result = add(1, 2)         # int
result = add(1.5, 2.5)     # float
# add("a", "b")            # ❌ 类型错误
```

### 8. `Generic` — 泛型类

```
from typing import Generic, TypeVar, List

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

# 使用
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
val: int = int_stack.pop()   # 类型检查器知道返回 int

str_stack: Stack[str] = Stack()
str_stack.push("hello")
```

### 9. 字面量类型 `Literal` (Python 3.8+)

```
from typing import Literal

# 限定为几个固定值之一
Direction = Literal["north", "south", "east", "west"]
Status = Literal[0, 1, 2]

def move(direction: Direction) -> None:
    print(f"Moving {direction}")

move("north")   # ✅
move("up")      # ❌ 类型错误

def set_status(code: Status) -> None:
    pass

set_status(0)   # ✅
set_status(99)  # ❌ 类型错误

# Python 3.11+ 也可以用 type 语句（见后文）
```

### 10. `final` — 不可覆盖 / 不可重赋值 (Python 3.8+)

```
from typing import final

class Base:
    @final
    def important_method(self) -> None:
        """子类不允许重写此方法"""
        pass

class Child(Base):
    def important_method(self) -> None:  # ❌ 类型错误
        pass

# 常量赋值
MAX_SIZE: final = 100
MAX_SIZE = 200  # ❌ 类型错误
```

### 11. `ClassVar` — 类变量（非实例变量） (Python 3.5.3+)

```
from typing import ClassVar

class Counter:
    count: ClassVar[int] = 0  # 类级别变量，不是实例变量

    def __init__(self) -> None:
        Counter.count += 1    # 正确
        # self.count = 1      # 类型检查器会警告

c1 = Counter()  # count = 1
c2 = Counter()  # count = 2
```

### 12. `NewType` — 创建语义不同的类型别名

```
from typing import NewType

# 创建"新类型"（运行时无开销，仅用于类型检查）
UserId = NewType('UserId', int)
OrderId = NewType('OrderId', int)

def get_user(user_id: UserId) -> str:
    return f"User_{user_id}"

def get_order(order_id: OrderId) -> str:
    return f"Order_{order_id}"

uid = UserId(42)
get_user(uid)    # ✅
# get_user(42)   # ⚠️ 类型检查器可能警告（建议用 UserId 包装）
# get_order(uid) # ❌ UserId 不是 OrderId
```

### 13. `Protocol` — 结构化子类型 / 鸭子类型 (Python 3.8+)

```
from typing import Protocol

# 定义协议（接口）
class Drawable(Protocol):
    def draw(self) -> str:
        ...

# 任何有 draw() -> str 的类都自动满足 Drawable 协议
class Circle:
    def draw(self) -> str:
        return "○"

class Rectangle:
    def draw(self) -> str:
        return "□"

# 无需继承！只要结构匹配就行
def render(obj: Drawable) -> None:
    print(obj.draw())

render(Circle())      # ✅
render(Rectangle())   # ✅

# RuntimeCheckable 可以在运行时检查
from typing import runtime_checkable

@runtime_checkable
class Sized(Protocol):
    def size(self) -> int: ...

isinstance(Circle(), Sized)  # True 或 False
```

### 14. `TypedDict` — 带键类型提示的字典 (Python 3.8+)

```
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    age: int
    email: str

# 或者用函数式写法
UserDict = TypedDict('UserDict', {'name': str, 'age': int, 'email': str})

# 使用
user: UserDict = {
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com"
}

user["name"]  # 类型检查器知道是 str
# user["phone"] = "123"  # ❌ 没有 phone 这个键

# 可选键
class PartialUser(TypedDict, total=False):
    name: str
    age: int
# 两个键都可以不提供

# 必选 + 可选混合
class FullUser(TypedDict):
    name: str
    age: int

class UpdateUser(FullUser, total=False):
    email: str  # 可选
    phone: str  # 可选
```

### 15. `dataclass` 中的类型提示

```
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str | None = None  # 带默认值的可选字段

p = Person(name="Alice", age=25)
p.name  # str
p.email # str | None
```

### 16. `Final` 大写（用于类型注解的不可变容器）

```
from typing import Final

# 标记一个变量为常量
PI: Final[float] = 3.14159

# 标记不可变的列表内容
NAMES: Final = ["Alice", "Bob"]
NAMES.append("Charlie")  # ⚠️ 类型检查器可能警告
```

### 17. `Self` — 指代当前类 (Python 3.11+)

```
from typing import Self

class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self

    def set_age(self, age: int) -> Self:
        self.age = age
        return self

# 链式调用类型安全
builder = Builder().set_name("Alice").set_age(25)

# 之前需要这样写：
from __future__ import annotations
T = TypeVar('T', bound='Builder')
class Builder:
    def set_name(self: T, name: str) -> T:
        self.name = name
        return self
```

### 18. `reveal_type` — 调试用（mypy/pyright 专用）

```
from typing import reveal_type

x: int = 42
reveal_type(x)  # 类型检查器会报告：Note: Revealed type is "builtins.int"
# 正常运行时会报错，仅用于类型检查
```

### 19. 字符串注解 `Annotated` (Python 3.9+)

```
from typing import Annotated

# Annotated[T, metadata...]  给类型附加额外信息
# 不改变基础类型，但可以携带元数据

def process(
    name: Annotated[str, "用户名，最大50字符"],
    age: Annotated[int, "必须大于0", "单位：岁"]
) -> None:
    pass

# 常见框架用法（如 FastAPI）
from fastapi import Query

def search(
    q: Annotated[str, Query(max_length=50)]
) -> str:
    return q

# 带约束
from typing import Annotated
PositiveInt = Annotated[int, lambda x: x > 0]
```

### 20. `Required` / `NotRequired` (Python 3.11+)

```
from typing import TypedDict, Required, NotRequired

class User(TypedDict):
    name: Required[str]      # 必须提供
    age: NotRequired[int]    # 可以不提供（total=True 模式下的例外）

user1: User = {"name": "Alice"}        # ✅
user2: User = {"name": "Bob", "age": 30}  # ✅
# user3: User = {"age": 25}           # ❌ 缺少必填的 name
```

### 21. `Alias` 与 `type` 语句 (Python 3.12+)

```
# Python 3.12 新增 type 语句，创建类型别名
type Point = tuple[float, float]
type UserID = int
type Matrix = list[list[float]]
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

def distance(p: Point) -> float:
    return (p[0]**2 + p[1]**2) ** 0.5
```

### 22. `NoReturn` — 永远不返回的函数

```
from typing import NoReturn

def raise_error(msg: str) -> NoReturn:
    """这个函数永远不会有正常返回"""
    raise ValueError(msg)

def fail() -> NoReturn:
    """调用后，后续代码类型检查器视为不可达"""
    import sys
    sys.exit(1)

def example() -> int:
    raise_error("something wrong")  # 类型检查器知道这里不会继续执行
    # x = 1  # 不可达代码，类型检查器会警告
```

### 23. `Never` — 底部类型 (Python 3.11+ / PEP 673)

```
# Never 是 NoReturn 的泛化版本
# 任何类型都是 Never 的超类型
# Never 可用于联合类型的交集

# 常见用法：穷举检查
from typing import Never

def assert_never(x: Never) -> Never:
    raise AssertionError(f"Unhandled type: {type(x)}")

def process(value: int | str) -> str:
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return value.upper()
    else:
        assert_never(value)  # 如果有新类型被加入联合类型，这里会报错
```

### 24. 类型别名 TypeAlias

```
from typing import TypeAlias

# 明确标记这是一个类型别名（而非普通变量）
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]
Matrix3x3: TypeAlias = tuple[Vector, Vector, Vector]

# Python 3.12+ 推荐用 type 语句
# type Vector = list[float]
```

### 25. `ParamSpec` — 保留参数签名的泛型 (Python 3.10+)

```
from typing import ParamSpec, Callable, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

# 装饰器中保留被装饰函数的参数签名
def log_call(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def add(a: int, b: int) -> int:
    return a + b

# 类型检查器知道 add 仍然是 (int, int) -> int
```

### 26. `Concatenate` — 拼接参数签名 (Python 3.10+)

```
from typing import Concatenate, ParamSpec, Callable, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

# 给函数添加一个前置参数
def add_logging(
    func: Callable[P, R]
) -> Callable[Concatenate[str, P], R]:
    def wrapper(prefix: str, *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"{prefix}: calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@add_logging
def multiply(a: int, b: int) -> int:
    return a * b

# multiply 现在需要 (str, int, int) -> int
result = multiply("DEBUG", 3, 4)  # 12
```

## 📌 第二部分：不常用 / 高级 TypeHint

### 27. `Mapping` / `MutableMapping` — 抽象映射类型

```
from typing import Mapping, MutableMapping

# Mapping[K, V]：只读映射（dict 的超类型接口）
def get_values(data: Mapping[str, int]) -> list[int]:
    return list(data.values())

# 可以接受 dict, OrderedDict, defaultdict 等
get_values({"a": 1, "b": 2})          # ✅
get_values({})                         # ✅

# MutableMapping[K, V]：可变映射
def add_item(data: MutableMapping[str, int]) -> None:
    data["new"] = 42
```

> 💡 推荐用 `Mapping` 而非 `dict` 作为函数参数类型，因为更灵活。

### 28. `Sequence` / `MutableSequence` — 抽象序列类型

```
from typing import Sequence, MutableSequence

# Sequence[T]：只读序列（list, tuple, str 等都是 Sequence）
def total(values: Sequence[float]) -> float:
    return sum(values)

total([1.0, 2.0, 3.0])    # ✅ list
total((1.0, 2.0))         # ✅ tuple
total("abc")              # ✅ str 也是 Sequence[str]

# MutableSequence[T]：可变序列（list 是，tuple 不是）
def append_item(seq: MutableSequence[int]) -> None:
    seq.append(99)
```

### 29. `Iterable` / `Iterator` / `Generator`

```
from typing import Iterable, Iterator, Generator

# Iterable[T]：可迭代对象（有 __iter__）
def process(items: Iterable[int]) -> None:
    for item in items:
        print(item)

process([1, 2, 3])    # ✅ list
process((1, 2, 3))    # ✅ tuple
process(range(5))     # ✅ range

# Iterator[T]：迭代器（有 __next__）
def count_up() -> Iterator[int]:
    n = 0
    while True:
        yield n
        n += 1

# Generator[YieldType, SendType, ReturnType]
def fib_gen() -> Generator[int, None, None]:
    """生成 Fibonacci 数"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Generator with send
def echo_gen() -> Generator[str, str, None]:
    while True:
        received = yield "ready"
        if received is not None:
            yield f"echo: {received}"

gen = echo_gen()
next(gen)          # "ready"
gen.send("hello")  # "echo: hello"

# Generator with return value
def compute() -> Generator[int, None, str]:
    yield 1
    yield 2
    yield 3
    return "done"
    # ReturnType "done" 可以通过 StopIteration.value 获取
```

### 30. `AsyncIterable` / `AsyncIterator` / `AsyncGenerator`

```
from typing import AsyncIterable, AsyncIterator, AsyncGenerator
import asyncio

# 异步迭代
class AsyncRange:
    def __init__(self, n: int) -> None:
        self.n = n

    def __aiter__(self) -> AsyncIterator[int]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[int]:
        for i in range(self.n):
            yield i
            await asyncio.sleep(0.1)

async def process_async(items: AsyncIterable[int]) -> None:
    async for item in items:
        print(item)

# 异步生成器
async def async_numbers() -> AsyncGenerator[int, None]:
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i
```

### 31. `Awaitable` / `Coroutine`

```
from typing import Awaitable, Coroutine
import asyncio

# Awaitable[T]：可以被 await 的对象
async def fetch_data() -> str:
    await asyncio.sleep(1)
    return "data"

def schedule_task() -> Awaitable[str]:
    return fetch_data()

# Coroutine[YieldType, SendType, ReturnType]
async def my_coro() -> Coroutine[None, None, int]:
    await asyncio.sleep(1)
    return 42
```

### 32. `ContextManager` / `AsyncContextManager`

```
from typing import ContextManager, AsyncContextManager
from contextlib import contextmanager

# 同步上下文管理器
@contextmanager
def open_file(path: str) -> ContextManager[None]:
    f = open(path, 'w')
    try:
        yield
    finally:
        f.close()

# 异步上下文管理器 (Python 3.7+)
class AsyncSession:
    async def __aenter__(self) -> str:
        await asyncio.sleep(0.1)
        return "session"

    async def __aexit__(self, *args) -> None:
        await asyncio.sleep(0.1)

def get_session() -> AsyncContextManager[str]:
    return AsyncSession()
```

### 33. `ChainMap` (Python 3.9+)

```
from typing import ChainMap
from collections import ChainMap as CM

# ChainMap[K, V]：多个字典的链式视图
defaults: dict[str, int] = {"a": 1, "b": 2}
overrides: dict[str, int] = {"b": 99, "c": 3}

combined: ChainMap[str, int] = CM(overrides, defaults)
# combined["b"] == 99, combined["a"] == 1
```

### 34. `OrderedDict` 注解

```
from typing import OrderedDict

# 保留插入顺序的字典
config: OrderedDict[str, str] = OrderedDict()
config["host"] = "localhost"
config["port"] = "8080"
```

### 35. `defaultdict` 注解

```
from collections import defaultdict
from typing import DefaultDict

# DefaultDict[K, V]：带默认值的字典
groups: DefaultDict[str, list[int]] = defaultdict(list)
groups["even"].append(2)
groups["even"].append(4)
groups["odd"].append(1)
# groups == {"even": [2, 4], "odd": [1]}
```

### 36. `Counter` 注解

```
from collections import Counter
from typing import Counter as CounterType

word_count: CounterType[str] = Counter()
word_count["hello"] += 1
word_count["world"] += 2
```

### 37. `Deque` 注解

```
from collections import deque
from typing import Deque

queue: Deque[int] = deque()
queue.append(1)
queue.append(2)
val: int = queue.popleft()  # 1
```

### 38. `NamedTuple` — 命名元组

```
from typing import NamedTuple

# 类式定义（推荐）
class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0  # 可有默认值

p = Point(1.0, 2.0)
p.x  # float
p.z  # float，默认 0.0

# 函数式定义
Point2D = NamedTuple('Point2D', [('x', float), ('y', float)])

# 带方法
class Employee(NamedTuple):
    name: str
    id: int

    @property
    def display_name(self) -> str:
        return f"[{self.id}] {self.name}"
```

### 39. `cast` — 强制类型转换（仅类型检查，运行时无操作）

```
from typing import cast

# cast 不会做运行时转换，只是告诉类型检查器"相信我，这是这个类型"
def process(data: list) -> list[dict[str, str]]:
    # 类型检查器不知道 data 的元素类型
    # 用 cast 告诉它
    return cast(list[dict[str, str]], data)

# 另一个常见场景
json_data: dict = {"name": "Alice", "age": 25}
name: str = cast(dict[str, str], json_data)["name"]
```

### 40. `overload` — 函数重载

```
from typing import overload

# 为同一个函数提供多个类型签名
@overload
def process(value: int) -> str: ...
@overload
def process(value: str) -> int: ...
@overload
def process(value: list[int]) -> float: ...

# 实际实现
def process(value):
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return len(value)
    elif isinstance(value, list):
        return sum(value) / len(value)
    raise TypeError

result1: str = process(42)         # 类型检查器知道返回 str
result2: int = process("hello")    # 返回 int
result3: float = process([1,2,3])  # 返回 float
```

### 41. `runtime_checkable` — 运行时协议检查

```
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

class File:
    def close(self) -> None:
        print("file closed")

class NotCloseable:
    pass

isinstance(File(), Closeable)       # True
isinstance(NotCloseable(), Closeable)  # False

# ⚠️ 注意：只检查方法是否存在，不检查签名！
```

### 42. `Final` 修饰类属性与方法 (Python 3.8+)

```
from typing import final

class Base:
    # 标记类属性为不可修改
    VERSION: final = "1.0"

    @final
    def method(self) -> None:
        """不可被子类重写"""
        pass

class Derived(Base):
    VERSION = "2.0"       # ❌ 不允许重赋值
    def method(self) -> None:  # ❌ 不允许重写
        pass
```

### 43. `Bound` TypeVar — 带边界的泛型

```
from typing import TypeVar

class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

# T 必须是 Animal 或其子类
T = TypeVar('T', bound=Animal)

def make_speak(animal: T) -> T:
    animal.speak()
    return animal  # 返回类型与输入类型一致

d: Dog = make_speak(Dog())  # ✅ 类型安全
c: Cat = make_speak(Cat())  # ✅ 类型安全
```

### 44. `covariant` / `contravariant` — 协变与逆变

```
from typing import TypeVar

class Animal: pass
class Dog(Animal): pass

# 协变：如果 Dog 是 Animal 的子类，
#        则 Sequence[Dog] 是 Sequence[Animal] 的子类
T_co = TypeVar('T_co', covariant=True)

# 逆变：如果 Dog 是 Animal 的子类，
#        则 Comparable[Animal] 是 Comparable[Dog] 的子类
T_contra = TypeVar('T_contra', contravariant=True)

# 示例：只读容器（协变）
class ReadOnlyBox:
    def __init__(self, value): ...
    def get(self): return self._value

# 示例：函数参数（逆变）
# Callable[[Animal], None] 可以接受 Callable[[Dog], None]
# 因为接受 Animal 的函数一定能接受 Dog
```

### 45. `Callable[..., T] 与 Callable[P, T]`

```
from typing import Callable

# 精确签名
def apply(fn: Callable[[int, str], bool], x: int, y: str) -> bool:
    return fn(x, y)

# 任意参数
def do_something(fn: Callable[..., int]) -> int:
    return fn()

# ParamSpec 精确传递
from typing import ParamSpec
P = ParamSpec('P')

def decorator(func: Callable[P, int]) -> Callable[P, int]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> int:
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper
```

### 46. `reveal_type` 与 `TYPE_CHECKING` 条件导入

```
# TYPE_CHECKING：只在类型检查时执行，运行时跳过
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # 这些 import 只用于类型检查，不会在运行时加载
    from models import User
    from services import Database

class MyService:
    def get_user(self, db: 'Database') -> 'User':  # 字符串前向引用
        return db.query()

# 避免循环导入的经典方案
```

### 47. `LiteralString` — 安全的字符串字面量 (Python 3.11+)

```
from typing import LiteralString

# LiteralString：必须是字符串字面量，不能是运行时拼接的字符串
def run_query(sql: LiteralString) -> None:
    # 防止 SQL 注入：只接受编译时常量字符串
    execute(sql)

run_query("SELECT * FROM users")  # ✅
table = "users"
# run_query(f"SELECT * FROM {table}")  # ❌ 不是字面量
# query = "SELECT * FROM users"
# run_query(query)  # ❌ 不是字面量（有些检查器可能放行）
```

### 48. `Unpack` / `*` — 解包类型 (Python 3.11+)

```
from typing import Unpack

# 解包 Tuple 为参数类型
def my_func(a: int, b: str, c: float) -> None:
    pass

args: tuple[int, str, float] = (1, "hello", 3.14)
my_func(*args)  # Python 3.11+ 类型检查器可以验证

# 函数签名中使用 Unpack
from typing import Unpack, TypeVarTuple, Any

Ts = TypeVarTuple('Ts')

def func(*args: Unpack[Ts]) -> None:
    pass

# 解包 TypedDict
class Defaults(TypedDict):
    host: str
    port: int

class Config(Defaults, total=False):
    debug: bool

def configure(**kwargs: Unpack[Config]) -> None:
    pass

configure(host="localhost", port=8080)         # ✅
configure(host="localhost", port=8080, debug=True)  # ✅
# configure(host="localhost", unknown=123)     # ❌
```

### 49. `TypeVarTuple` — 可变长度泛型 (Python 3.11+)

```
from typing import TypeVarTuple, Generic

Ts = TypeVarTuple('Ts')

class Array(Generic[*Ts]):
    """可变长度类型的数组"""
    def __init__(self, *shape: *Ts) -> None:
        self.shape = shape

# 支持 float, int, str 等任意数量类型
a: Array[float, int] = Array(3.14, 42)

# 常见用途：数学库中实现任意维度数组
```

### 50. `TypeGuard` — 自定义类型守卫 (Python 3.10+)

```
from typing import TypeGuard

# 类型守卫：返回 True 时，类型检查器将第一个参数视为指定类型
def is_string_list(val: list) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(items: list) -> None:
    if is_string_list(items):
        # items 在这里是 list[str]
        for item in items:
            print(item.upper())  # ✅ item 是 str
    else:
        # items 在这里不是 list[str]
        pass

# TypeGuard vs isinstance 的区别：
# isinstance 只能用于运行时检查
# TypeGuard 允许自定义检查逻辑，且可以窄化为更具体的类型
```

### 51. `TypeIs` — 更严格的类型守卫 (Python 3.13+)

```
from typing import TypeIs

# TypeIs 比 TypeGuard 更严格：
# TypeGuard[str] 返回 True 时，val 被视为 str（即使原来不是 str 的子类型）
# TypeIs[str] 要求 val 本来就必须是 str 的子类型之一

def is_int(val: object) -> TypeIs[int]:
    """返回 True 时，val 一定是 int"""
    return isinstance(val, int)

def handle(val: object) -> None:
    if is_int(val):
        # val: int
        print(val + 1)  # ✅
```

### 52. `MappingProxyType` 注解

```
from typing import MappingProxyType
from types import MappingProxyType as MPT

# 只读字典视图
config: MappingProxyType[str, str] = MPT({"host": "localhost"})
# config["host"] = "127.0.0.1"  # ❌ 运行时 TypeError
```

### 53. `AnyStr` — 约束为 str 或 bytes 的 TypeVar

```
from typing import AnyStr

# AnyStr = TypeVar('AnyStr', str, bytes) 的快捷方式
def concat(a: AnyStr, b: AnyStr) -> AnyStr:
    return a + b

concat("hello", "world")   # 返回 str
concat(b"hello", b"world") # 返回 bytes
# concat("hello", b"world") # ❌ str 和 bytes 不能混用
```

### 54. `get_type_hints` — 运行时获取类型提示

```
from typing import get_type_hints, get_origin, get_args

class MyClass:
    x: int
    y: list[str]
    z: int | None

# 获取类的类型提示
hints = get_type_hints(MyClass)
# {'x': <class 'int'>, 'y': list[str], 'z': int | None}

# 获取泛型参数
origin = get_origin(list[str])     # <class 'list'>
args = get_args(list[str])         # (<class 'str'>,)

origin = get_origin(dict[str, int])  # <class 'dict'>
args = get_args(dict[str, int])      # (<class 'str'>, <class 'int'>)

# 对于 Optional
origin = get_origin(int | None)   # typing.Union
args = get_args(int | None)       # (int, NoneType)
```

### 55. `__all__` 导出控制（配合类型）

```
from typing import TYPE_CHECKING

__all__ = ["public_func", "PublicClass"]

if TYPE_CHECKING:
    # 这些不会出现在 __all__ 中，仅用于类型检查
    _InternalClass: type
```

### 56. 前向引用（Forward References）

```
class Node:
    def __init__(self, value: int, next_node: 'Node | None' = None) -> None:
        self.value = value
        self.next = next_node

    def set_next(self, node: 'Node') -> None:
        self.next = node

# Python 3.7+ 推荐：
from __future__ import annotations  # 所有注解自动变为字符串（延迟求值）

class Node:
    def __init__(self, value: int, next_node: Node | None = None) -> None:
        self.value = value
        self.next = next_node
```

### 57. `SupportsInt`, `SupportsFloat`, `SupportsAbs` 等协议

```
from typing import SupportsInt, SupportsFloat, SupportsAbs, SupportsRound

# 这些是预定义的 Protocol，表示支持特定魔术方法的对象
def to_int(val: SupportsInt) -> int:
    return int(val)

def to_float(val: SupportsFloat) -> float:
    return float(val)

def absolute(val: SupportsAbs[float]) -> float:
    return abs(val)

to_int(3.14)    # ✅
to_int("42")    # ✅ str 支持 __int__
to_int([1,2])   # ❌ list 不支持 __int__

# 其他类似的预定义协议：
# SupportsBytes, SupportsComplex, SupportsIndex
# SupportsRound
```

### 58. `Buffer` — 缓冲区协议 (Python 3.12+)

```
from typing import Buffer

# Buffer 表示支持缓冲区协议的对象（bytes, bytearray, memoryview 等）
def process_buffer(data: Buffer) -> bytes:
    return bytes(data)

process_buffer(b"hello")     # ✅
process_buffer(bytearray(5)) # ✅
process_buffer(memoryview(b"hi"))  # ✅
```

### 59. `Traversable` — 可遍历类型（未正式发布，预览）

```
# 尚未成为正式标准，在部分 typing_extensions 中可用
from typing_extensions import Traversable

# 递归类型：树结构
type Tree = dict[str, Tree | str | int]

# 可用于 JSON AST 等场景
```

### 60. `typing_extensions` — 实验性/未来特性

```
# 很多新特性先在 typing_extensions 中发布
from typing_extensions import (
    Unpack,        # Python 3.11
    TypeVarTuple,  # Python 3.11
    Self,          # Python 3.11
    TypeGuard,     # Python 3.10
    ParamSpec,     # Python 3.10
    Literal,       # Python 3.8
    Final,         # Python 3.8
    Protocol,      # Python 3.8
    runtime_checkable,
    # ...更多
)

# 推荐低版本 Python 使用 typing_extensions 获取新特性
```

## 📊 总结速查表



| 类别           | TypeHint                                       | 说明         | Python版本      |
| -------------- | ---------------------------------------------- | ------------ | --------------- |
| **基础**       | `int`, `float`, `str`, `bool`, `bytes`, `None` | 基本类型     | 全部            |
| **任意**       | `Any`                                          | 关闭检查     | 全部            |
| **联合**       | `Union[A, B]` / `A | B`                        | 多选一       | 3.10+ 用 `|`    |
| **可选**       | `Optional[T]` / `T | None`                     | 可为None     | 同上            |
| **容器**       | `List[T]` / `list[T]`                          | 列表         | 3.9+ 用内置     |
|                | `Dict[K, V]` / `dict[K, V]`                    | 字典         | 3.9+            |
|                | `Set[T]` / `set[T]`                            | 集合         | 3.9+            |
|                | `Tuple[A, B]` / `tuple[A, B]`                  | 元组         | 3.9+            |
| **函数**       | `Callable[[args], R]`                          | 函数类型     | 全部            |
|                | `NoReturn`                                     | 不返回       | 全部            |
|                | `ParamSpec`                                    | 参数签名泛型 | 3.10+           |
|                | `Concatenate`                                  | 拼接参数     | 3.10+           |
| **泛型**       | `TypeVar`                                      | 泛型变量     | 全部            |
|                | `Generic[T]`                                   | 泛型类       | 全部            |
|                | `TypeVarTuple`                                 | 可变长泛型   | 3.11+           |
|                | `Bound TypeVar`                                | 带边界泛型   | 全部            |
| **别名**       | `TypeAlias` / `type` 语句                      | 类型别名     | 3.12+ type      |
|                | `NewType`                                      | 语义别名     | 全部            |
| **类相关**     | `Type[C]`                                      | 类本身       | 全部            |
|                | `ClassVar[T]`                                  | 类变量       | 3.5.3+          |
|                | `Final`                                        | 不可变       | 3.8+            |
|                | `Self`                                         | 当前类型     | 3.11+           |
| **协议**       | `Protocol`                                     | 结构子类型   | 3.8+            |
|                | `runtime_checkable`                            | 运行时检查   | 3.8+            |
| **字典**       | `TypedDict`                                    | 带类型字典   | 3.8+            |
|                | `Required` / `NotRequired`                     | 必选/可选键  | 3.11+           |
| **字面量**     | `Literal[...]`                                 | 固定值       | 3.8+            |
|                | `LiteralString`                                | 字符串字面量 | 3.11+           |
| **抽象**       | `Mapping`, `Sequence`                          | 抽象接口     | 全部            |
|                | `Iterable`, `Iterator`, `Generator`            | 迭代器       | 全部            |
|                | `AsyncIterable`, `AsyncGenerator`              | 异步         | 全部            |
|                | `ContextManager`, `AsyncContextManager`        | 上下文       | 全部            |
| **守卫**       | `TypeGuard[T]`                                 | 类型守卫     | 3.10+           |
|                | `TypeIs[T]`                                    | 严格守卫     | 3.13+           |
| **工具**       | `cast()`                                       | 强制转换     | 全部            |
|                | `overload`                                     | 函数重载     | 全部            |
|                | `Annotated[T, meta]`                           | 附带元数据   | 3.9+            |
|                | `reveal_type`                                  | 调试         | mypy            |
|                | `Unpack`                                       | 解包类型     | 3.11+           |
|                | `get_type_hints()`                             | 运行时获取   | 全部            |
| **底部**       | `Never`                                        | 底部类型     | 3.11+ (PEP 673) |
| **缓冲**       | `Buffer`                                       | 缓冲区协议   | 3.12+           |
| **预定义协议** | `SupportsInt`, `SupportsAbs` 等                | 鸭子类型协议 | 全部            |

## 🔑 使用建议

```
1. 项目起步时：加上基础类型注解（int, str, Optional 等）
2. 团队协作时：启用 mypy/pyright 严格检查
3. 开发框架/库时：使用 Protocol + TypeVar + overlaod
4. Python 3.10+ 优先使用 | 语法替代 Union
5. Python 3.9+ 优先使用 list[T] 替代 List[T]
6. 函数参数优先用 Sequence/Mapping 而非 list/dict（更灵活）
7. 用 TYPE_CHECKING 避免循环导入
8. 用 from __future__ import annotations 启用延迟求值
```





















































