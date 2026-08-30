<h1 align="center">Python 类型提示完全指南（Python 3.9+，部分特性需更高版本）</h1>
# 1. 基础类型
## 1.1 基本类型
```python
age: int = 25
score: float = 98.5
name: str = "Alice"
is_active: bool = True
data: bytes = b"hello"
def say_hello() -> None:
    print("Hello!")
```
## 1.2 Any — 任意类型
```python
from typing import Any
def process(data: Any) -> Any:  # 接受任何类型，返回任何类型
    return data
data: Any = 42
data = "now it's a string"  # ✅ 逃逸类型检查
```
> ⚠️ `Any` 会关闭类型检查，应尽量少用。
## 1.3 Optional / Union — 可选与联合类型
```python
from typing import Optional, Union
# Optional[X] === Union[X, None]，表示"可以是 X，也可以是 None"
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None
# Union 表示多种类型之一
def parse_value(value: Union[int, str, float]) -> str:
    return str(value)
# Python 3.10+ 推荐 | 语法
def find_user_v2(user_id: int) -> str | None: ...
def parse_value_v2(value: int | str | float) -> str: ...
```
# 2. 容器与迭代类型
## 2.1 常用容器
```python
# === Python 3.9+ 推荐写法（PEP 585）===
items: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1}
unique: set[int] = {1, 2, 3}
point: tuple[int, int] = (10, 20)
record: tuple[str, int, float] = ("Alice", 25, 98.5)  # 固定长度、各位置类型可不同
# === Python 3.8 及以下需要从 typing 导入 ===
from typing import List, Dict, Set, Tuple
items: List[int] = [1, 2, 3]
```
## 2.2 抽象容器类型
### 2.2.1 Mapping / MutableMapping
```python
from typing import Mapping, MutableMapping
# Mapping[K, V]：只读映射（dict 的超类型接口）
def get_values(data: Mapping[str, int]) -> list[int]:
    return list(data.values())
get_values({"a": 1})  # ✅ dict、OrderedDict、defaultdict 等均可
# MutableMapping[K, V]：可变映射
def add_item(data: MutableMapping[str, int]) -> None:
    data["new"] = 42
```
> 💡 函数参数优先用 `Mapping`/`Sequence` 而非 `dict`/`list`，更灵活。
### 2.2.2 Sequence / MutableSequence
```python
from typing import Sequence, MutableSequence
# Sequence[T]：只读序列（list、tuple、str 都是 Sequence）
def total(values: Sequence[float]) -> float:
    return sum(values)
total([1.0, 2.0])  # ✅ list
total((1.0, 2.0))  # ✅ tuple
total("abc")       # ✅ str 也是 Sequence[str]
# MutableSequence[T]：可变序列（list 是，tuple 不是）
def append_item(seq: MutableSequence[int]) -> None:
    seq.append(99)
```
### 2.2.3 Iterable / Iterator
```python
from typing import Iterable, Iterator
# Iterable[T]：可迭代对象（有 __iter__）
def process(items: Iterable[int]) -> None:
    for item in items:
        print(item)
process([1, 2, 3])  # ✅ list / tuple / range 均可
# Iterator[T]：迭代器（有 __next__）
def count_up() -> Iterator[int]:
    n = 0
    while True:
        yield n
        n += 1
```
### 2.2.4 Generator 详解
`Generator[YieldType, SendType, ReturnType]` 三个类型参数的含义：
```text
Generator[YieldType, SendType, ReturnType]
                │            │         │
                │            │         └─ 函数 return 时返回值的类型
                │            └─ yield 接收外部 send() 传入值的类型
                └─ yield 产出值的类型
```
```python
from typing import Generator
def example() -> Generator[str, int, float]:
    received = yield "hello"   # yield 产出 → YieldType = str
    received2 = yield "world"  # received 的类型 → SendType = int
    return 3.14                # return → ReturnType = float
gen = example()
print(next(gen))        # hello
print(gen.send(42))     # send(42) 赋给 received，产出 world
try:
    gen.send(99)
except StopIteration as e:
    print(e.value)      # 3.14（return 值通过 StopIteration.value 获取）
```
最常见的简化形式（`SendType`、`ReturnType` 均为 `None`）：
```python
def __iter__(self) -> Generator[T, None, None]:
    for i in range(self._size):
        yield self._data[i]
# 完全等价于 Iterator[T]
```
更多示例：
```python
def fib_gen() -> Generator[int, None, None]:
    """生成 Fibonacci 数"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
def echo_gen() -> Generator[str, str, None]:
    """带 send 的生成器"""
    while True:
        received = yield "ready"
        if received is not None:
            yield f"echo: {received}"
```
> `Iterator[X]` 等价于 `Generator[X, None, None]`；`Generator` 是 `Iterator` 的超集（多出 send / throw / close 能力）。
## 2.3 特殊容器
### 2.3.1 OrderedDict / defaultdict / Counter / Deque
```python
from typing import OrderedDict, DefaultDict, Counter as CounterType, Deque
from collections import defaultdict, Counter, deque
config: OrderedDict[str, str] = OrderedDict()  # 保留插入顺序
config["host"] = "localhost"
groups: DefaultDict[str, list[int]] = defaultdict(list)  # 带默认值的字典
groups["even"].append(2)
word_count: CounterType[str] = Counter()  # 计数器
word_count["hello"] += 1
queue: Deque[int] = deque()  # 双端队列
queue.append(1)
val: int = queue.popleft()
```
### 2.3.2 ChainMap
```python
from typing import ChainMap
from collections import ChainMap as CM
defaults: dict[str, int] = {"a": 1, "b": 2}
overrides: dict[str, int] = {"b": 99, "c": 3}
combined: ChainMap[str, int] = CM(overrides, defaults)
# combined["b"] == 99, combined["a"] == 1
```
### 2.3.3 MappingProxyType
```python
from typing import MappingProxyType
from types import MappingProxyType as MPT
config: MappingProxyType[str, str] = MPT({"host": "localhost"})  # 只读字典视图
# config["host"] = "127.0.0.1"  # ❌ 运行时 TypeError
```
# 3. 函数与可调用对象
## 3.1 Callable
### 3.1.1 基本语法
`Callable` 用于标注**可调用对象**（函数、方法、lambda、实现了 `__call__` 的类实例等）。
```python
from typing import Callable
# Callable[[参数类型列表], 返回值类型]
```
### 3.1.2 使用示例
```python
# 1. 函数接受一个函数作为参数
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)
apply(lambda x, y: x + y, 1, 2)  # ✅ 返回 3
# 2. 无参无返回值的可调用对象
def run_task(task: Callable[[], None]) -> None:
    task()
run_task(lambda: print("hello"))  # ✅
# 3. 任意参数：... 表示任意参数，返回值必须是 int
def execute_any(func: Callable[..., int]) -> int:
    return func(1, 2, 3)
# 4. 作为返回值类型
def get_logger(name: str) -> Callable[[str], None]:
    def log(msg: str) -> None:
        print(f"[{name}] {msg}")
    return log
logger = get_logger("APP")
logger("started")  # 输出: [APP] started
# 5. 用 Protocol 定义更精细的可调用协议
from typing import Protocol
class DoubleFunc(Protocol):
    def __call__(self, x: int) -> int: ...
def use_double(f: DoubleFunc, n: int) -> int:
    return f(n)
use_double(lambda x: x * 2, 5)  # ✅ 返回 10
```
## 3.2 NoReturn / Never — 不返回类型
```python
from typing import NoReturn
def raise_error(msg: str) -> NoReturn:
    """永远不会有正常返回"""
    raise ValueError(msg)
def fail() -> NoReturn:
    import sys
    sys.exit(1)
def example() -> int:
    raise_error("something wrong")
    # 类型检查器知道这里不会继续执行，后续代码视为不可达
```
`Never`（Python 3.11+，PEP 673）是 `NoReturn` 的泛化版本，任何类型都是它的超类型，常用于穷尽检查：
```python
from typing import Never
def assert_never(x: Never) -> Never:
    raise AssertionError(f"Unhandled type: {type(x)}")
def process(value: int | str) -> str:
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return value.upper()
    else:
        assert_never(value)  # 新类型加入联合类型但未处理时，此处报错
```
## 3.3 Type — 类本身
```python
from typing import Type
class Animal: ...
class Dog(Animal): ...
# Type[X] 表示"X 这个类本身"，而不是 X 的实例
def create_instance(cls: Type[Animal]) -> Animal:
    return cls()
dog = create_instance(Dog)  # ✅ 返回类型推断为 Dog
```
## 3.4 ParamSpec — 参数签名泛型（3.10+）
```python
from typing import ParamSpec, TypeVar, Callable
P = ParamSpec('P')
R = TypeVar('R')
# 装饰器中完整保留被装饰函数的参数签名
def log_and_call(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    print(f"Calling {func.__name__}")
    return func(*args, **kwargs)
result = log_and_call(int, "123")      # ✅ result 是 int
result = log_and_call(len, [1, 2, 3])  # ✅ result 是 int
```
## 3.5 Concatenate — 拼接参数签名（3.10+）
```python
from typing import Concatenate, ParamSpec, TypeVar, Callable
P = ParamSpec('P')
R = TypeVar('R')
# 给函数添加一个前置参数
def add_logging(func: Callable[P, R]) -> Callable[Concatenate[str, P], R]:
    def wrapper(prefix: str, *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"{prefix}: calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
@add_logging
def multiply(a: int, b: int) -> int:
    return a * b
result = multiply("DEBUG", 3, 4)  # multiply 现在需要 (str, int, int) -> int
```
## 3.6 overload — 函数重载
```python
from typing import overload
# 为同一个函数提供多个类型签名
@overload
def process(value: int) -> str: ...
@overload
def process(value: str) -> int: ...
@overload
def process(value: list[int]) -> float: ...
# 实际实现（不带 @overload）
def process(value):
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return len(value)
    elif isinstance(value, list):
        return sum(value) / len(value)
    raise TypeError
result1: str = process(42)           # 类型检查器知道返回 str
result2: int = process("hello")      # 返回 int
result3: float = process([1, 2, 3])  # 返回 float
```
# 4. 泛型编程
## 4.1 TypeVar
### 4.1.1 基本声明
`TypeVar` 用于定义**类型变量**，实现**泛型编程**，让函数/类的类型可以"参数化"。
```python
from typing import TypeVar
T = TypeVar('T')                                      # 任意类型
T_co = TypeVar('T_co', covariant=True)                # 协变（只用于返回值）
T_contra = TypeVar('T_contra', contravariant=True)    # 逆变（只用于参数）
```
### 4.1.2 泛型函数
```python
from typing import TypeVar, List
T = TypeVar('T')
# 输入什么类型，输出什么类型
def first(items: List[T]) -> T:
    return items[0]
x: int = first([1, 2, 3])   # T 被推断为 int
s: str = first(["a", "b"])  # T 被推断为 str
# 多个类型变量
K = TypeVar('K')
V = TypeVar('V')
def pair(key: K, value: V) -> tuple[K, V]:
    return (key, value)
result: tuple[str, int] = pair("age", 30)
```
### 4.1.3 约束
约束：T 只能是列出的类型**之一**。
```python
Num = TypeVar('Num', int, float)
def add(a: Num, b: Num) -> Num:
    return a + b
add(1, 2)      # ✅ 返回 int
add(1.5, 2.5)  # ✅ 返回 float
# add(1, "2")  # ❌ 类型检查器报错
```
`AnyStr` 是 `TypeVar('AnyStr', str, bytes)` 的快捷方式：
```python
from typing import AnyStr
def concat(a: AnyStr, b: AnyStr) -> AnyStr:
    return a + b
concat("hello", "world")    # 返回 str
concat(b"hello", b"world")  # 返回 bytes
# concat("hello", b"world") # ❌ str 和 bytes 不能混用
```
### 4.1.4 有界
有界：T 只要是 bound 类型的**子类**即可，且仍保持原类型（返回类型与输入类型一致）。
```python
class Animal: ...
class Dog(Animal): ...
class Cat(Animal): ...
A = TypeVar('A', bound=Animal)
def feed(animal: A) -> A:
    return animal
d: Dog = feed(Dog())  # ✅ 类型安全
c: Cat = feed(Cat())  # ✅
# 协议作为边界
from typing import Protocol, Any
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
CT = TypeVar('CT', bound=Comparable)
def find_max(items: list[CT]) -> CT:
    return max(items)
```
### 4.1.5 协变与逆变
```python
from typing import TypeVar
# 协变：如果 Dog 是 Animal 的子类，则 Sequence[Dog] 是 Sequence[Animal] 的子类
# 适用于只读容器 / 返回值
T_co = TypeVar('T_co', covariant=True)
# 逆变：如果 Dog 是 Animal 的子类，
# 则 Callable[[Animal], None] 是 Callable[[Dog], None] 的子类
#（接受 Animal 的函数一定能接受 Dog），适用于函数参数
T_contra = TypeVar('T_contra', contravariant=True)
```
## 4.2 Generic — 泛型类
```python
from typing import Generic, TypeVar, Optional
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
stack_int = Stack[int]()    # 只能放 int
stack_int.push(1)
# stack_int.push("hello")   # ❌ 类型检查器报错
stack_str = Stack[str]()    # 只能放 str
stack_str.push("hello")
```
## 4.3 Self — 指代当前类（3.11+）
```python
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
Python 3.11 之前的替代写法：
```python
from typing import TypeVar
T = TypeVar('T', bound='Builder')
class Builder:
    def set_name(self: T, name: str) -> T:
        self.name = name
        return self
```
## 4.4 TypeVarTuple / Unpack — 可变长度泛型（3.11+）
```python
from typing import TypeVarTuple, Generic, Unpack
Ts = TypeVarTuple('Ts')
class Array(Generic[*Ts]):
    """可变长度类型的数组，常用于数学库中实现任意维度数组"""
    def __init__(self, *shape: *Ts) -> None:
        self.shape = shape
a: Array[float, int] = Array(3.14, 42)
```
`Unpack` 解包类型：
```python
# 解包 Tuple 为参数类型
def my_func(a: int, b: str, c: float) -> None: ...
args: tuple[int, str, float] = (1, "hello", 3.14)
my_func(*args)  # ✅ 类型检查器可以验证
# 解包 TypedDict
from typing import TypedDict
class Defaults(TypedDict):
    host: str
    port: int
class Config(Defaults, total=False):
    debug: bool
def configure(**kwargs: Unpack[Config]) -> None: ...
configure(host="localhost", port=8080)              # ✅
configure(host="localhost", port=8080, debug=True)  # ✅
# configure(host="localhost", unknown=123)          # ❌
```
# 5. 类型别名与常量
## 5.1 TypeAlias / type 语句
```python
from typing import TypeAlias
# 明确标记这是一个类型别名（而非普通变量）
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]
Matrix3x3: TypeAlias = tuple[Vector, Vector, Vector]
# Python 3.12+ 推荐用 type 语句
type Point = tuple[float, float]
type UserID = int
type Matrix2 = list[list[float]]
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
def distance(p: Point) -> float:
    return (p[0]**2 + p[1]**2) ** 0.5
```
## 5.2 NewType — 语义化类型别名
```python
from typing import NewType
# 运行时无开销，仅用于类型检查
UserId = NewType('UserId', int)
OrderId = NewType('OrderId', int)
user_id: UserId = UserId(42)
order_id: OrderId = OrderId(42)
def get_user(uid: UserId) -> str:
    return f"user-{uid}"
get_user(user_id)     # ✅
# get_user(order_id)  # ❌ UserId 不是 OrderId
```
## 5.3 Final / final — 不可变
```python
from typing import Final, final
# 常量：不可重新赋值
PI: Final[float] = 3.14159
MAX_SIZE: Final = 100
# MAX_SIZE = 200  # ❌ 类型错误
class Base:
    VERSION: Final[str] = "1.0"  # 类属性不可修改
    def __init__(self) -> None:
        self.id: Final[int] = 0  # 实例 Final 属性只能在 __init__ 中赋值一次
    @final
    def important_method(self) -> None:
        """子类不允许重写此方法"""
class Child(Base):
    # VERSION = "2.0"                  # ❌ 不允许重赋值
    # def important_method(self): ...  # ❌ 不允许重写
    ...
```
> ⚠️ `Final` 标记不可变**容器**时（如 `NAMES: Final = ["Alice"]`），只限制变量重新绑定，不限制容器内容的修改。
## 5.4 ClassVar — 类变量
```python
from typing import ClassVar
class Counter:
    count: ClassVar[int] = 0  # 类级别变量，不是实例变量
    def __init__(self) -> None:
        Counter.count += 1  # 正确
        # self.count = 1    # 类型检查器会警告
```
## 5.5 Literal — 字面量类型（3.8+）
```python
from typing import Literal
Direction = Literal["north", "south", "east", "west"]
Status = Literal[0, 1, 2]
def move(direction: Direction) -> None:
    print(f"Moving {direction}")
move("north")  # ✅
# move("up")   # ❌ 类型错误
def set_status(code: Status) -> None: ...
set_status(0)  # ✅
# set_status(99)  # ❌ 类型错误
```
## 5.6 LiteralString — 安全的字符串字面量（3.11+）
```python
from typing import LiteralString
# 只能是字符串字面量，不能是运行时拼接的字符串，防止 SQL 注入
def run_query(sql: LiteralString) -> None:
    execute(sql)
run_query("SELECT * FROM users")  # ✅
table = "users"
# run_query(f"SELECT * FROM {table}")  # ❌ 不是字面量
```
## 5.7 Annotated — 附加元数据（3.9+）
```python
from typing import Annotated
# Annotated[T, metadata...] 不改变基础类型，但可以携带元数据
def process(
    name: Annotated[str, "用户名，最大50字符"],
    age: Annotated[int, "必须大于0", "单位：岁"]
) -> None: ...
# 常见框架用法（如 FastAPI）
from fastapi import Query
def search(q: Annotated[str, Query(max_length=50)]) -> str:
    return q
# 带约束
PositiveInt = Annotated[int, lambda x: x > 0]
```
# 6. 结构化类型
## 6.1 Protocol — 结构化子类型（3.8+）
### 6.1.1 定义与使用
任何**结构匹配**的类都自动满足协议，无需继承（鸭子类型的静态检查）。
```python
from typing import Protocol
class Drawable(Protocol):
    def draw(self) -> str: ...
class Circle:
    def draw(self) -> str:
        return "○"
class Rectangle:
    def draw(self) -> str:
        return "□"
def render(obj: Drawable) -> None:
    print(obj.draw())
render(Circle())     # ✅ 无需继承！只要结构匹配
render(Rectangle())  # ✅
# render(42)         # ❌ int 没有 draw() 方法
```
### 6.1.2 runtime_checkable
```python
from typing import Protocol, runtime_checkable
@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...
class File:
    def close(self) -> None:
        print("file closed")
isinstance(File(), Closeable)    # True
isinstance(object(), Closeable)  # False
# ⚠️ 只检查方法是否存在，不检查签名！
```
### 6.1.3 预定义协议
```python
from typing import SupportsInt, SupportsFloat, SupportsAbs, SupportsRound
def to_int(val: SupportsInt) -> int:
    return int(val)
to_int(3.14)    # ✅
to_int("42")    # ✅ str 支持 __int__
# to_int([1,2]) # ❌ list 不支持 __int__
# 类似的预定义协议还有：
# SupportsBytes, SupportsComplex, SupportsIndex, SupportsRound
```
## 6.2 TypedDict — 带类型的字典（3.8+）
```python
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
# user["age"] = "30"     # ❌ 必须是 int
# user["phone"] = "123"  # ❌ 没有 phone 这个键
# 函数式写法
UserDict = TypedDict('UserDict', {'name': str, 'age': int, 'email': str})
# total=False：所有键可选
class PartialUser(TypedDict, total=False):
    name: str
    age: int
# 必选 + 可选混合
class FullUser(TypedDict):
    name: str
    age: int
class UpdateUser(FullUser, total=False):
    email: str  # 可选
    phone: str  # 可选
# Python 3.11+ 也可用 Required / NotRequired
from typing import Required, NotRequired
class UserV2(TypedDict):
    name: Required[str]    # 必须提供
    age: NotRequired[int]  # 可以不提供
user1: UserV2 = {"name": "Alice"}  # ✅
# user3: UserV2 = {"age": 25}      # ❌ 缺少必填的 name
```
## 6.3 NamedTuple — 带类型的命名元组
```python
from typing import NamedTuple
# 类式定义（推荐）
class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0  # 可有默认值
p = Point(1.0, 2.0)
print(p.x)  # 1.0
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
## 6.4 dataclass 中的类型提示
```python
from dataclasses import dataclass
@dataclass
class Person:
    name: str
    age: int
    email: str | None = None  # 带默认值的可选字段
p = Person(name="Alice", age=25)
p.name   # str
p.email  # str | None
```
# 7. 异步与上下文管理
## 7.1 AsyncIterable / AsyncIterator / AsyncGenerator
```python
from typing import AsyncIterable, AsyncIterator, AsyncGenerator
import asyncio
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
async def async_numbers() -> AsyncGenerator[int, None]:
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i
```
## 7.2 Awaitable / Coroutine
```python
from typing import Awaitable, Coroutine
import asyncio
async def fetch_data() -> str:
    await asyncio.sleep(1)
    return "data"
def schedule_task() -> Awaitable[str]:
    return fetch_data()  # 可以被 await 的对象
async def my_coro() -> Coroutine[None, None, int]:
    await asyncio.sleep(1)
    return 42
```
## 7.3 ContextManager / AsyncContextManager
```python
from typing import ContextManager, AsyncContextManager
from contextlib import contextmanager
import asyncio
# 同步上下文管理器
@contextmanager
def open_file(path: str) -> ContextManager[None]:
    f = open(path, 'w')
    try:
        yield
    finally:
        f.close()
# 异步上下文管理器（Python 3.7+）
class AsyncSession:
    async def __aenter__(self) -> str:
        await asyncio.sleep(0.1)
        return "session"
    async def __aexit__(self, *args) -> None:
        await asyncio.sleep(0.1)
def get_session() -> AsyncContextManager[str]:
    return AsyncSession()
```
# 8. 类型检查与调试工具
## 8.1 cast — 强制类型转换
```python
from typing import cast, Any
# cast 不会做运行时转换，只告诉类型检查器"相信我，这是这个类型"
def process(data: list) -> list[dict[str, str]]:
    return cast(list[dict[str, str]], data)
json_data: dict = {"name": "Alice", "age": 25}
name: str = cast(dict[str, str], json_data)["name"]
data: Any = get_from_json()   # 没有类型信息
user: User = cast(User, data)
```
## 8.2 TypeGuard / TypeIs — 类型守卫
```python
from typing import TypeGuard
# TypeGuard（3.10+）：返回 True 时，第一个参数被窄化为指定类型
# 允许自定义检查逻辑（isinstance 只能用于运行时检查）
def is_string_list(val: list) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)
def process(items: list) -> None:
    if is_string_list(items):
        for item in items:
            print(item.upper())  # ✅ item 是 str
    else:
        pass  # items 在这里不是 list[str]
```
```python
from typing import TypeIs
# TypeIs（3.13+）：更严格，要求 val 本来就必须是目标类型的子类型
def is_int(val: object) -> TypeIs[int]:
    return isinstance(val, int)
def handle(val: object) -> None:
    if is_int(val):
        print(val + 1)  # ✅ val: int
```
## 8.3 reveal_type — 调试
```python
from typing import reveal_type
x: int = 42
reveal_type(x)  # mypy/pyright 报告: Revealed type is "builtins.int"
# 正常运行时会报错，仅用于类型检查
```
## 8.4 get_type_hints — 运行时获取
```python
from typing import get_type_hints, get_origin, get_args
class MyClass:
    x: int
    y: list[str]
    z: int | None
hints = get_type_hints(MyClass)
# {'x': <class 'int'>, 'y': list[str], 'z': int | None}
get_origin(list[str])       # <class 'list'>
get_args(list[str])         # (<class 'str'>,)
get_origin(dict[str, int])  # <class 'dict'>
get_args(dict[str, int])    # (<class 'str'>, <class 'int'>)
get_origin(int | None)      # typing.Union
get_args(int | None)        # (int, NoneType)
```
## 8.5 TYPE_CHECKING 与前向引用
```python
# TYPE_CHECKING：只在类型检查时执行，运行时跳过，避免循环导入
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import User
    from services import Database
class MyService:
    def get_user(self, db: 'Database') -> 'User':  # 字符串前向引用
        return db.query()
# 前向引用：类内部引用自身
class Node:
    def __init__(self, value: int, next_node: 'Node | None' = None) -> None:
        self.value = value
        self.next = next_node
# Python 3.7+ 推荐：所有注解自动变为字符串（延迟求值），无需再加引号
from __future__ import annotations
class Node2:
    def __init__(self, value: int, next_node: Node2 | None = None) -> None:
        self.value = value
        self.next = next_node
```
## 8.6 \_\_all\_\_ 导出控制
```python
from typing import TYPE_CHECKING
__all__ = ["public_func", "PublicClass"]
if TYPE_CHECKING:
    _InternalClass: type  # 不会出现在 __all__ 中，仅用于类型检查
```
# 9. 其他高级特性
## 9.1 Buffer — 缓冲区协议（3.12+）
```python
from typing import Buffer
# 表示支持缓冲区协议的对象（bytes, bytearray, memoryview 等）
def process_buffer(data: Buffer) -> bytes:
    return bytes(data)
process_buffer(b"hello")           # ✅
process_buffer(bytearray(5))       # ✅
process_buffer(memoryview(b"hi"))  # ✅
```
## 9.2 Traversable 与递归类型
```python
# 尚未成为正式标准，在 typing_extensions 中可用
from typing_extensions import Traversable
# 递归类型：树结构，可用于 JSON AST 等场景（配合 type 语句）
type Tree = dict[str, Tree | str | int]
```
## 9.3 typing_extensions — 实验性/未来特性
```python
# 很多新特性先在 typing_extensions 中发布
from typing_extensions import (
    Unpack,            # Python 3.11
    TypeVarTuple,      # Python 3.11
    Self,              # Python 3.11
    TypeGuard,         # Python 3.10
    ParamSpec,         # Python 3.10
    Literal,           # Python 3.8
    Protocol,          # Python 3.8
    runtime_checkable,
)
# 推荐低版本 Python 使用 typing_extensions 获取新特性
```
# 10. 意义与使用建议
## 10.1 类型提示的意义
| 意义           | 说明                                                      |
| -------------- | --------------------------------------------------------- |
| 📖 文档化       | 类型本身就是最好的文档，一眼看出函数期望什么、返回什么    |
| 🐛 提前发现 Bug | 在代码运行**之前**就发现类型错误，而不是到线上才崩        |
| 🤖 IDE 智能补全 | VSCode / PyCharm 根据类型提示提供精准的自动补全和参数提示 |
| 🔄 重构安全     | 改签名后，类型检查器帮你找到所有需要同步修改的地方        |
| 👥 团队协作     | 明确的接口约定，减少"这个参数传什么？"的沟通成本          |
| 🔗 接口契约     | 类似 Java/C# 的接口/泛型系统，支持大规模工程              |
> **注意**：类型提示在运行时**不会强制执行**，是给静态检查器和 IDE 看的。运行时强制检查可用 `@dataclass` + `__post_init__`、`pydantic` 等库。
## 10.2 配合工具使用
```bash
# mypy — 最流行的 Python 静态类型检查器
pip install mypy
mypy my_project/
# pyright — 微软开发的类型检查器
npm install -g pyright
pyright my_project/
# VSCode 中安装 Pylance 扩展即可获得实时类型检查
```
## 10.3 使用建议
1. 项目起步时：加上基础类型注解
2. 团队协作时：启用 mypy/pyright 严格检查
3. 开发框架/库时：使用 Protocol + TypeVar + overload
4. Python 3.10+ 优先使用 `X | Y` 替代 `Union`
5. Python 3.9+ 优先使用 `list[T]` 替代 `List[T]`
6. 函数参数优先用 `Sequence`/`Mapping` 而非 `list`/`dict`（更灵活）
7. 用 `TYPE_CHECKING` 避免循环导入
8. 用 `from __future__ import annotations` 启用延迟求值
## 10.4 总结速查表
| 类别           | TypeHint                                       | 说明         | Python 版本     |
| -------------- | ---------------------------------------------- | ------------ | --------------- |
| **基础**       | `int`, `float`, `str`, `bool`, `bytes`, `None` | 基本类型     | 全部            |
| **任意**       | `Any`                                          | 关闭检查     | 全部            |
| **联合**       | `Union[A, B]` / `A \| B`                       | 多选一       | 3.10+ 用 `\|`   |
| **可选**       | `Optional[T]` / `T \| None`                    | 可为 None    | 同上            |
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
|                | Bound TypeVar                                  | 带边界泛型   | 全部            |
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