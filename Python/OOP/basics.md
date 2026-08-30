---
aliases:
  - course of study
  - course
  - python
  - OOP
tags:
  - tutorial
  - computer-science
  - oop
  - Python
category: knowledge
datetime: " 2026-08-08 12:08:75 周六"
author: wephiles
rating: "0"
---

[TOC]

<h1 style="text-align: center;">Python 面向对象</h1>

# 1. 方法

在 Python 面向对象中，**自定义**方法（即非内置特殊方法）的名字以不同数量的下划线开头，代表着**完全不同的访问级别和底层机制**。它们之间的核心区别如下：

## 1.1 `method`（普通方法/公共方法）

- **定义**：没有任何前导下划线，如 `def info(self):`。
- **性质**：**公开（`Public`）**。这是最常规的方法。
- **访问**：类内部、子类、外部实例均可以直接无障碍访问。
- **设计意图**：对外暴露的正式接口，表示“你可以随便调用我”。

------

## 1.2 `_method`（单前导下划线）

- **定义**：以一个下划线开头，如 `def _internal(self):`。
- **性质**：**“受保护的”（Protected）**，但这**纯属语法约定（君子协定）**，Python 解释器**并不会**做任何强制拦截。
- **访问**：外部依然可以访问（`obj._internal()` 完全合法且能运行），不会报错。
- **特殊行为**：在使用 `from module import *` 时，以单下划线开头的对象不会被导入（除非显式定义了 `__all__`）。
- **设计意图**：强烈暗示“这是内部实现细节，请勿在外部调用”，仅用于提醒协作开发者和未来的自己。

------

## 1.3 `__method`（双前导下划线，且末尾无双下划线）

- **定义**：以两个下划线开头且**不以**两个下划线结尾，如 `def __core(self):`。
- **性质**：**“私有”（Private）**，通过**名称修饰（Name Mangling）**机制实现。
- **访问**：无法直接通过 `obj.__core()` 访问，会报 `AttributeError`。
- **底层原理**：Python 解释器会在编译时，自动将方法名重命名为 `_ClassName__core`（即 `_类名__方法名`）。你可以通过 `obj._ClassName__core()` 强行调用，但**极度不推荐**。
- **设计意图**：**主要目的是防止子类意外重写（覆盖）父类的方法名**，而不是为了“安全加密”。当子类也定义了 `__core` 时，两者互不干扰，因为它们在底层被修饰成了不同的名字。

------

## 1.4 特别补充：`__method__`（双前导+双末尾下划线）

- **请勿**自定义这种名称（如 `__my__`）。
- 这是 Python 内部的**魔术方法（特殊方法）**保留命名规范（如 `__init__`、`__len__`）。随意自定义会与未来 Python 版本的内部方法冲突，且破坏代码可读性。

------

## 1.5 代码演示对照

```
class Parent:
    def public(self):
        print("公共方法")

    def _protected(self):
        print("受保护方法（约定）")

    def __private(self):
        print("私有方法（名称修饰）")

class Child(Parent):
    # 尝试重写父类的“私有”方法
    def __private(self):
        print("子类的私有方法")

    def call_parent_private(self):
        # 无法直接调用父类的 __private，因为被修饰了
        # self.__private()  # 这里调用的是子类自己的，而不是父类的
        # 必须通过修饰后的名字调用父类的：
        self._Parent__private()  # 输出：私有方法（名称修饰）

# --- 外部调用测试 ---
p = Parent()
p.public()           # 正常输出
p._protected()       # 正常输出（虽然 IDE 可能警告）

# p.__private()      # 报错：AttributeError

# 通过修饰后的名字强行调用（可行但不应该这么做）
p._Parent__private() # 输出：私有方法（名称修饰）
```

## 1.6 总结与最佳实践建议

| 命名格式     | 访问级别         | 机制             | 子类行为                             | 实际使用建议                                                 |
| :----------- | :--------------- | :--------------- | :----------------------------------- | :----------------------------------------------------------- |
| `method`     | 公开             | 无               | 可直接继承/重写                      | 公开接口，放心使用。                                         |
| `_method`    | 受保护（约定）   | 仅是命名规范     | 可直接继承/重写（约定上属于内部）    | **推荐使用**：用于类内部逻辑辅助函数，告诉调用者“别碰我”。   |
| `__method`   | 私有（强制修饰） | 名称修饰（改名） | **难以被重写**（子类同名会另起炉灶） | **谨慎使用**：仅在**绝对不想被子类覆盖**时使用（如基类中的核心钩子函数）。在日常业务代码中，很少需要用它，过度使用会提高调试复杂度。 |
| `__method__` | 特殊方法         | 解释器预留       | 按文档覆盖                           | **禁止自定义**此类名字。                                     |

**核心结论**：大部分情况下，用 `_method` 表示“内部使用”就足够了，**双下划线 `__method` 主要是为了规避继承中的命名冲突**，而非实现传统编程语言中的“访问权限控制”。

# 2. 变量

## 2.1 下划线前缀的区别（变量版）

无论是实例变量还是类变量，前缀下划线的含义完全一致：

| 命名格式     | 访问级别               | 底层机制                     | 实际效果                                                     |
| :----------- | :--------------------- | :--------------------------- | :----------------------------------------------------------- |
| `variable`   | **公开 (Public)**      | 无                           | 类内外、子类均可直接访问和修改。                             |
| `_variable`  | **受保护 (Protected)** | **纯约定**                   | 解释器不拦截，外部可以访问（`obj._variable`），但强烈暗示“内部细节，别动我”。`from module import *` 时不会被导入。 |
| `__variable` | **私有 (Private)**     | **名称修饰 (Name Mangling)** | 编译时重命名为 `_ClassName__variable`。外部无法直接通过原名访问，**主要是为了防止子类意外重写父类的变量名**。 |

------

## 2.2 实例变量 vs 类变量（核心本质区别）

抛开下划线不看，实例变量和类变量有**5个决定性区别**：

| 对比维度       | **实例变量 (Instance Variable)**                             | **类变量 (Class Variable)**                            |
| :------------- | :----------------------------------------------------------- | :----------------------------------------------------- |
| **定义位置**   | 在 `__init__` 或实例方法内，通过 `self.xxx` 定义             | 直接在类缩进下定义（不在任何方法内）                   |
| **归属者**     | **属于具体的实例对象**（每个对象独有一份）                   | **属于类本身**（全局只有一份，所有实例共享）           |
| **存储空间**   | 存在每个实例的 `__dict__` 字典中                             | 存在类的 `__dict__` 字典中                             |
| **修改影响**   | 只影响调用该方法的那个对象                                   | 影响所有实例（除非实例有同名变量覆盖了它）             |
| **访问优先级** | **实例变量 > 类变量**（通过 `self.xxx` 或 `obj.xxx` 访问时，优先找实例自己的，找不到再找类的） | 直接通过 `类名.xxx` 访问，或作为实例查找不到时的“备胎” |

------

## 2.3 组合起来的 6 种写法详解（含代码）

我们把这两层维度交叉，得到以下 6 种情况：

### 2.3.1. 类变量（公开、受保护、私有）

```
class Parent:
    class_public = "公开类变量"
    _class_protected = "约定受保护类变量"
    __class_private = "私有类变量"  # 实际名字被改成 _Parent__class_private

class Child(Parent):
    __class_private = "子类的私有类变量"  # 实际名字被改成 _Child__class_private，父类的没被覆盖

# 访问演示
print(Parent.class_public)          # ✅ 正常
print(Parent._class_protected)      # ✅ 能访问（但别这么干）
# print(Parent.__class_private)     # ❌ AttributeError
print(Parent._Parent__class_private) # ✅ 能强行访问（但极不推荐）

print(Child.__class_private)        # ❌ 报错（因为子类自己的也被修饰成了 _Child__class_private）
print(Child._Parent__class_private) # ✅ 输出父类的值（说明子类并没有覆盖掉父类的私有变量）
```

### 2.3.2. 实例变量（公开、受保护、私有）

```
class Parent:
    def __init__(self, name):
        self.public = name           # 公开实例变量
        self._protected = f"内部_{name}"  # 受保护约定
        self.__private = f"私有_{name}"   # 实例变量同样发生名称修饰

    def show(self):
        # 在类内部，可以直接通过 self.__private 访问（解释器自动转换）
        print(self.__private)  

class Child(Parent):
    def __init__(self, name):
        super().__init__(name)
        self.__private = "子类私有"  # 底层变成 _Child__private，和父类的 _Parent__private 互不干扰

p = Parent("Alex")
print(p.public)          # ✅ Alex
print(p._protected)      # ✅ 内部_Alex（约定警告）
# print(p.__private)     # ❌ AttributeError
print(p._Parent__private) # ✅ 私有_Alex（强行访问）

c = Child("Bob")
c.show()                 # 输出：私有_Bob（父类方法访问的是父类的私有变量）
```

## 2.4 最易踩坑的“赋值陷阱”（实例 vs 类变量）

这是面试常考点。当通过 `self` 修改类变量时，**读**和**写**逻辑完全不同：

```
class MyClass:
    items = []  # 类变量（共享）
    count = 0   # 类变量（不可变）

obj1 = MyClass()
obj2 = MyClass()

# 场景1：修改可变对象（不会新建实例变量）
obj1.items.append(1)  
print(obj2.items)  # 输出 [1] —— 因为是同一个列表，obj2 受到了影响！

# 场景2：对不可变对象赋值（会新建实例变量，遮蔽类变量）
obj1.count = 10  
print(obj1.count)  # 输出 10（实例变量，独有）
print(obj2.count)  # 输出 0（类变量，未变）
print(MyClass.count) # 输出 0（类变量，未变）

# 场景3：想要修改类变量，必须通过类名
MyClass.count = 100  
print(obj2.count)  # 输出 100（所有实例都能看到类变量的修改）
```

## 2.5 总结与最佳实践

1. **日常业务中**，用 `_variable` 表示“内部属性”就足够了，**强烈不建议**在实例变量上滥用 `__variable`，因为名称修饰会让调试变得极其痛苦（`IDE`无法智能提示，调试时看到一堆 `_ClassName__var`）。
2. **`__variable` 的唯一合理用途**：在框架或基类中，定义一个**绝对不允许子类重名的核心属性**（比如底层缓存键）。
3. **类变量**：只用来存放所有实例**共享的固定数据**（如配置常量、默认选项）或**共享的可变容器**（但要小心上述的 `append` 和 `=` 的区别）。
4. **访问口诀**：通过 `self.xxx` 访问时，**自己兜里有（实例变量）先用自己，自己兜里没有再去类里找（类变量）**；通过 `类名.xxx` 访问时，永远只操作类变量。

# 3. 组合

```python
class School(object):
    
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def speak(self):
        pass
        
obj1 = School('xxx', 'aaa/bbb/ccc')
obj2 = School('yyy', 'ddd/eee/fff')
obj3 = School('zzz', 'ggg/hhh/iii')

class Teacher(object):
    
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.__salary = salary
        self.school = None
        
t1 = Teacher('a', 25, 188888)
t2 = Teacher('b', 26, 155555)
t3 = Teacher('c', 24, 166668)

# 为老师分配学校
t1.school = obj1
t2.school = obj1
t3.school = obj2

# 查看t1老师所在学校的学校名称
print(t1.school.name)
# t1老师进行讲课
t1.school.speak()
```

# 4. 类 / 对象 能否做字典的 `key`

**能，但有严格的前提条件。**

Python 字典的键只有一个硬性要求：**该对象必须是“可哈希的”（Hashable）**。

类和对象是否可哈希，取决于它们是否实现了 `__hash__()` 方法，并且该方法的返回值在其生命周期内保持不变。下面分三种常见场景给你拆解，附带一个**极易踩坑**的致命误区。

------

### 4.1 类对象（Class Object）本身做 Key —— ✅ 完全可以

在 Python 中，类本身也是对象（元类 `type` 的实例）。**类默认是可哈希的**，因为它们的哈希值基于内存地址（`id`），且生命周期内不变。

```
class Dog:
    pass

class Cat:
    pass

# 直接用类名作为字典的键
registry = {
    Dog: "这是狗狗类",
    Cat: "这是猫咪类"
}

print(registry[Dog])  # 输出：这是狗狗类
```

这种写法在**工厂模式**、**策略模式**或**注册表**中非常常见。

------

### 4.2 常规的实例对象（未重写 `__eq__`）做 Key —— ✅ 完全可以

如果你自定义的类**没有**重写 `__eq__` 和 `__hash__` 方法，那么实例对象默认是可哈希的。哈希值基于对象的内存地址（`id`），不同对象即使内容完全一样，也被视为不同的键。

```
class Person:
    def __init__(self, name):
        self.name = name

p1 = Person("Alex")
p2 = Person("Alex")  # 内容一样，但是两个独立对象

d = {}
d[p1] = "第一次"
d[p2] = "第二次"

print(d)  # 输出：{<__main__.Person object at 0x...>: '第一次', <__main__.Person object at 0x...>: '第二次'}
print(len(d))  # 输出：2（因为内存地址不同，视为不同键）
```

------

### 4.3 重写了 `__eq__` 的实例对象做 Key —— ❌ 默认会报错（大坑！）

**这是面试和实际编码中最容易翻车的地方。**

Python 有一条铁律：**如果你重写了 `__eq__` 方法（用于比较相等性），Python 会自动将 `__hash__` 设置为 `None`**，表示该对象**不可哈希**。此时强行作为 Key，会抛出 `TypeError: unhashable type 'Person'`。

```
class Person:
    def __init__(self, name):
        self.name = name
    
    # 重写了 eq，希望同名的人视为相等
    def __eq__(self, other):
        return self.name == other.name

p1 = Person("Alex")
d = {}
# d[p1] = "test"  # 取消注释会报错：TypeError: unhashable type: 'Person'
```

**如果你想既要重写 `__eq__`，又想拿它当 Key，必须显式实现 `__hash__`**：

```
class Person:
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        return self.name == other.name
    
    # 显式指定哈希值基于不可变的 name 属性
    def __hash__(self):
        return hash(self.name)

p1 = Person("Alex")
p2 = Person("Alex")
d = {}
d[p1] = "第一次"
d[p2] = "第二次"  # 此时 p2 会覆盖 p1，因为两者相等且哈希值相同

print(len(d))  # 输出：1
```

------

### 4.4 终极警告：可变对象做 Key 是“定时炸弹”

即使你的对象是可哈希的（比如上面显式实现了 `__hash__`），但如果它**包含可变属性**，一旦放入字典后修改了属性，它的哈希值就会改变，导致字典再也找不到这个键（内存泄漏）。

python

```
class BadKey:
    def __init__(self, value):
        self.value = value
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        return self.value == other.value

obj = BadKey(10)
d = {obj: "原始数据"}

# 危险操作：修改了作为 Key 的对象的内部状态
obj.value = 20  

# 此时哈希值已变，字典内部去查找 hash(20) 的位置，找不到原来的键
print(d.get(obj))  # 输出：None（丢失了数据！）
```

**最佳实践建议：**

1. **尽量使用不可变类型作为 Key**（如 `str`、`int`、`tuple`）。
2. 如果非要拿自定义对象当 Key，**确保该对象在设计上是不可变的**（即所有属性在 `__init__` 后不再修改）。
3. **绝不要在对象作为字典 Key 期间修改它的哈希依赖属性**。

------

### 总结速查表

| 对象类型                                  | 是否可哈希 | 能否做 Key         | 底层原因                   |
| :---------------------------------------- | :--------- | :----------------- | :------------------------- |
| **类对象** (Class)                        | ✅ 是       | 能                 | 默认基于 `id`，不可变      |
| **普通实例**（未重写 `__eq__`）           | ✅ 是       | 能                 | 默认基于 `id`，不可变      |
| **重写了 `__eq__`，未写 `__hash__`**      | ❌ 否       | **不能**（报错）   | Python 自动禁用哈希        |
| **重写了 `__eq__` 且显式写了 `__hash__`** | ✅ 是       | **能（但需谨慎）** | 必须确保哈希值不随属性变化 |
| **内置不可变类型**（`str/int/tuple`）     | ✅ 是       | 能                 | 原生支持，绝对安全         |
| **内置可变类型**（`list/dict/set`）       | ❌ 否       | 不能               | 原生不可哈希               |

| 情况                                    | 类本身能否作为键 | 实例能否作为键 |
| --------------------------------------- | ---------------- | -------------- |
| 默认情况(不重写 `__eq__` 和 `__hash__`) | ✅                | ✅              |
| 只重写 `__eq__`                         | ✅                | ❌              |
| 同时重写 `__eq__` 和 `__hash__`         | ✅                | ✅              |
| 只重写 `__hash__`                       | ✅                | ✅              |

# 5. 主动调用其他类的成员

```python
class Foo(object):

    def f1(self):
        super().f1()  # 按照继承顺序找下一个类的相关成员
        print('Foo.f1 3个功能')


class Bar(object):

    def f1(self):
        print('Bar.f1 6个功能')


class Info(Foo, Bar):
    pass


obj = Info()
obj.f1()

"""
Bar.f1 6个功能
Foo.f1 3个功能

！！！
Info没有f1，先去Foo里面找(先找左边)，找到了，执行Foo.f1函数
在执行Foo.f1函数的时候，这个函数的第一条语句需要按照继承关系找函数，
但是是按照哪个类的继承关系找呢？是按照Info类还是Foo类呢？答案是：按照Info的
继承关系去找。因为最开始是按照Info的继承关系找f1函数，那么传入的self参数肯定就只是
Info 的对象 (obj) 这个对象了。
==========================================================================
总结一下，如果要执行/找到一个对象的成员，那么从始至终必须要按照这个对象的继承关系去
找。不能找到一半又去不是下一个继承关系的类里面找。并不是简单的找父类。 -- 易错点
！！！
"""
```

# 6. 特殊成员

```python
class Foo(object):

    def __new__(cls, *args, **kwargs):  # 构造方法
        print('__new__方法', cls)
        # __new__的时候创建一个空对象。
        # 将object.__new__(cls)返回后就回去调用__init__方法，初始化对象

        # 必须要有返回值且返回值必须是object.__new__(cls)
        # 所有的对象都是由object创建的
        return object.__new__(cls)

    def __init__(self, a1, a2):  # 初始化方法
        self.a1 = a1
        self.a2 = a2
        print('__init__方法')

    def __call__(self, *args, **kwargs):
        print(111, args, kwargs)
        return 123

    def __getitem__(self, name):
        return 8

    def __setitem__(self, name, value):  # 无返回值
        print('key', 'value', name, value)

    def __delitem__(self, name):  # 无返回值
        print('del', name)


# 1. 类名() -- 自动执行__init__方法
obj = Foo(1, 2)

# 2. 对象() -- 自动执行 __call__方法
obj(1, 2, k1=10, k2=20)

# 3. 对象[] -- 自动执行 __getitem__方法
print(obj['xx'])

# 4. 对象[a] = b -- 自动执行 __setitem__方法
obj['abc'] = 123

# 5. del 对象[a] -- 自动执行 __delitem__方法
del obj['123']

# 6. __new__方法 -- 真正的构造方法
```

```python
# __str__

class Foo(object):
    def __init__(self):
        pass
    
    def func(self):
        pass
    
obj = Foo()
print(obj)  # <__main__.Foo object at 0x0000019D9ED13FA0>

# ##################### 分割线 #####################
class Foo(object):
    def __init__(self):
        pass
    
    def func(self):
        pass
    
    def __str__(self):
        return "A object from Foo class."
    
obj = Foo()
print(obj)  # A object from Foo class.
```

```python
class Foo(object):
    """This is a class docstring."""
    def __init__(self):
        pass

    def func(self):
        pass

    def __str__(self):
        return "A object from Foo class."


obj = Foo()
print(obj)
print(obj.__doc__)  # This is a class docstring.
```

```python
class Foo(object):
    """This is a class docstring."""
    def __init__(self, name, age):
        self.name = name
        self.age = age


obj = Foo('aaa', 123)
print(obj.__dict__)  # {'name': 'aaa', 'age': 123}
```

```python
class Foo(object):
    """This is a class docstring."""

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.detail = [(1, 5), (2, 6), (3, 7)]

    def __iter__(self):
        return iter(self.detail)


obj = Foo('aaa', 123)

for item in obj:
    print(item)
"""
(1, 5)
(2, 6)
(3, 7)
"""
```

```python
class Foo(object):
    """This is a class docstring."""

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.detail = [(1, 5), (2, 6), (3, 7)]

    def __iter__(self):
        return self.detail


obj = Foo('aaa', 123)

for item in obj:
    print(item)

"""
Traceback (most recent call last):
  File "E:\Code\PyProjects\Demos\practice\main.py", line 32, in <module>
    for item in obj:
                ^^^
TypeError: iter() returned non-iterator of type 'list'
"""
```

## 6.1 📌 `__iter__` 方法的作用

`__iter__` 方法是Python迭代器协议的核心，它让对象变得**可迭代**。实现后，对象可以用于：

- `for` 循环
- `list()`, `tuple()`, `set()` 等转换函数
- 解包操作（如 `a, b, c = obj`）

## 6.2 📌 核心规则（非常重要！）

**`__iter__` 方法必须返回一个迭代器对象，而不能直接返回列表/元组/集合！**

### 6.2.1 ❌ 错误示例：

```
class Wrong:
    def __iter__(self):
        return [1, 2, 3]  # 错误！列表不是迭代器
```

### 6.2.2 ✓ 正确做法：

```
class Right:
    def __iter__(self):
        return iter([1, 2, 3])  # 返回列表的迭代器
```

## 6.3 📌 迭代器 vs 可迭代对象



| 类型           | 特征                         | 示例                     |
| -------------- | ---------------------------- | ------------------------ |
| **可迭代对象** | 实现 `__iter__`              | 列表、元组、集合、字符串 |
| **迭代器**     | 实现 `__iter__` + `__next__` | 列表的迭代器、生成器     |

- 列表/元组/集合是**可迭代对象**，但**不是迭代器**
- 必须用 `iter()` 获取它们的迭代器

## 6.4 📌 四种正确的实现方式

### 6.4.1：返回生成器（推荐，最简洁）

```
class MyRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __iter__(self):
        current = self.start
        while current < self.end:
            yield current
            current += 1
```

### 6.4.2：返回内置容器的迭代器

```
class Colors:
    def __init__(self):
        self.colors = ['red', 'green', 'blue']
    
    def __iter__(self):
        return iter(self.colors)  # 返回列表的迭代器
```

### 6.4.3：返回生成器表达式

```
class Squares:
    def __init__(self, n):
        self.n = n
    
    def __iter__(self):
        return (i**2 for i in range(self.n))
```

### 6.4.4：返回自定义迭代器对象

```
class Countdown:
    def __iter__(self):
        return CountdownIterator(10)

class CountdownIterator:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
```

## 6.5 📌 总结

1. **`__iter__` 必须返回迭代器对象**，不能直接返回列表/元组/集合
2. **如果想返回列表/元组/集合的元素**，使用 `iter(容器)` 获取其迭代器
3. **最推荐的方式是使用生成器**（`yield`），简洁高效
4. **迭代器必须实现两个方法**：`__iter__` 和 `__next__`

# 7.  `issubclass`/`type`/`isinstance`

- `issubclass` -- 获取前面那个类是否是后面那个类的子子孙孙
- `type` -- 获取当前对象是哪个类创建的
- `isinstance`  - 判断第一个参数（一般是对象）是否是第二个参数（一般是类）的实例

# 8. ***反射

```python
getattr(handler, 'f1')  # 会自动去handler模块中找名字叫f1的成员
```

```python
"""
反射 -- 通过面向对象实现
"""


class Foo(object):
    country = 'a'

    def func(self):
        pass


v = getattr(Foo, 'country')
print(v)

v = getattr(Foo, 'func')
print(v)

obj = Foo()
v = getattr(obj, 'func')
print(v)

"""
a
<function Foo.func at 0x00000200233C1750>
<bound method Foo.func of <__main__.Foo object at 0x0000020025013FA0>>
"""
```

```python
def function():
    name = 'abc'


v = getattr(function, 'name')
print(v)  # 报错 AttributeError: 'function' object has no attribute 'name'
```

```python
def function():
    name = 'abc'
    function.name = name


v = getattr(function, 'name')
print(v)  # 报错 AttributeError: 'function' object has no attribute 'name'
```

```python
def function():
    name = 'abc'

function.name = 'abcdef'


v = getattr(function, 'name')
print(v)  # abcdef
```

```python
class Operate(object):
    func_list = [
        'login', 'logout', 'register'
    ]

    def login(self):
        print('login')

    def logout(self):
        print('logout')

    def register(self):
        print('register')

    def run(self):
        print('''
        请输入要执行的功能:
        1. 登录
        2. 注销
        3. 注册
        ''')
        in_val = input('请输入要执行的操作序号1/2/3 >>> ')
        fun_str = self.func_list[int(in_val) - 1]
        getattr(self, fun_str)()


obj = Operate()
obj.run()
```

```python
getattr()  # 根据字符串的形式去对象中找成员 - 内存级别
hasattr()  # 根据字符串的形式判断对象中是否有该成员 - 内存级别
setattr()  # 根据字符串的形式在对象中动态地设置一个成员 - 内存级别
delattr()  # 根据字符串的形式去对象中动态地删除一个成员 - 内存级别
```

# 9. 类的约束

```python
class BaseMessage(object):
    """BaseMessage类用于约束，约束其派生类，保证派生类中必须编写send方法，不然程序可能会报错"""
    def send():
        # 如果有下面这行语句，只要继承这个基类就必须要重写这个send方法用于完成具体的业务逻辑 否则会报错
        raise NotImplementedError('.send() method must be overridden!')
```

```python
from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    """抽象类"""

    def f1(self):
        # 普通实例方法
        pass

    @abstractmethod
    def f2(self):
        # 抽象方法
        pass


class Foo(Base):
    pass


obj = Foo()
obj.f1()  # 实例化时的报错：TypeError: Can't instantiate abstract class Foo with abstract method f2
```

```python
import hashlib

def md5(pwd):
    # 初始化对象并加盐 -- 盐别乱动 要么放到全局变量 要么放在这儿不要乱动
    obj = hashlib.md5(b'nnCdheFDuwCSAjnwksSDDCAoDdsajkDSAdADSDmfjDdoD')

    # md5加密必须要用字节
    obj.update(pwd.encode('utf-8'))

    # 获取密文
    res = obj.hexdigest()
    
    return res
```

```python
import logging
import traceback

logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def fun():
    try:
        a = a + 1
    except Exception as e:
        # 获取错误的堆栈信息 -- traceback.format_exc()
        logging.error(traceback.format_exc())


fun()
```

```python
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(
    level=logging.DEBUG,
    filename='app1.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 像以上这样写的话，只会生效第一个配置的东西 -- 那么怎么两个地方向两个文件中写日志？看下面
import logging

file_1 = logging.FileHandler('log1.log', mode='w', encoding='utf-8')
fmt1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_1.setFormatter(fmt1)

logger1 = logging.Logger('logger1', level=logging.ERROR)
logger1.addHandler(file_1)

# 另外一个
file_2 = logging.FileHandler('log2.log', mode='w', encoding='utf-8')
fmt2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_2.setFormatter(fmt2)

logger2 = logging.Logger('logger2', level=logging.ERROR)
logger2.addHandler(file_2)

logger1.error('error 1')
logger2.error('error 2')
```

# 10. 多继承

```python
class A(object):
    pass

class B(A):
    pass

class C(B):
    pass

class D(object):
    pass

class E(D, C):
    pass

class F(object):
    pass

class G(F):
    pass

class H(C, G):
    pass

class Foo(E, H):
    pass
```

![image-20260809163535288](https://wephiles-image-bed-1322748259.cos.ap-nanjing.myqcloud.com/assets/20260809163536524.png)

`c3 算法`:



首先要找`Foo`类的继承关系：如果要找`Foo`的继承关系，那么首先找到`E`和`H`的继承关系

```python
L(Foo + L(E) + L(H))
L(E) = L(D) + L(C)
	 = (D, object) + (C, B, A, object)
    
继承关系: E
拿第一个的表头，和后面的除了表头以外的其他类比较，（这里拿出来D和后面的B,A,object对比），如果全都不相等，那么就可以将第一个的表头拿出来(这时候第一个表的表头就可以删除了):
继承关系: ED

再继续拿第一个的表头，继续和后面的除了头以外的对比，如果有相等的，那么不动:
L(E) = L(D) + L(C)
	 = (object) + (C, B, A, object)
再拿第二个表的表头和其他的表尾比较，如果没有，拿出来:
继承关系: EDC

拿出来后变成了:
L(E) = L(D) + L(C)
	 = (object) + (B, A, object)

再继续拿第一个的表头和其他表的表尾比较，如果有相等的，不动，那么拿下一个表的表头和其他表进行对比:
继承关系: EDCB

L(E) = L(D) + L(C)
	 = (object) + (A, object)
继承关系: EDCBA

L(E) = L(D) + L(C)
	 = (object) + (object)
继承关系:E,D,C,B,A,object


# ##########################
H 的查找关系
L(H) = L(C) + L(G)
	 = (C, B, A, object) + (G, F, object)
...
H,C,B,A,G,F,object

所以:
    L(Foo) = L(E) + L(H)
    L(E) = E,D,C,B,A,object
    L(H) = H,C,B,A,G,F,object
    
=> L(Foo) = (E,D,C,B,A,object) + (H,C,B,A,G,F,object)
		  = E,D,H,C,B,A,G,F,object
    
-> 最终结果:Foo,E,D,H,C,B,A,G,F,object
```

注意:

使用`__mro__`寻找继承关系 -- 而`super`就是遵循`__mro__`所指出的继承顺序寻找的.

