---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-14 21:08:67 周五"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">docstring</h1>

---

文档字符串是出现在模块、函数、类或方法开头的字符串字面量，用于说明代码的功能、参数、返回值等信息。

# 1. 什么是 `文档字符串`

文档字符串是出现在模块、函数、类或方法定义后的第一个语句的字符串字面量，用于记录代码的功能和用法。

# 2. 主要风格

## 2.1 `Google` 风格

```bash
def calculate_area(length, width):
    """计算矩形面积。

    使用给定的长度和宽度计算矩形的面积。
	
    Args:
        length (float): 矩形的长度，必须为正数。
        width (float): 矩形的宽度，必须为正数。

    Returns:
        float: 矩形的面积。

    Raises:
        ValueError: 如果长度或宽度为负数。

    Example:
        >>> calculate_area(5, 3)
        15.0
    """
    if length < 0 or width < 0:
        raise ValueError("长度和宽度必须为正数")
    return length * width
```

## 2.2 `Numpy` 风格

```bash
def calculate_area(length, width):
    """
    计算矩形面积。

    使用给定的长度和宽度计算矩形的面积。
	
    Parameters
    ----------
    length : float
        矩形的长度，必须为正数。
    width : float
        矩形的宽度，必须为正数。

    Returns
    -------
    float
        矩形的面积。

    Raises
    ------
    ValueError
        如果长度或宽度为负数。

    Examples
    --------
    >>> calculate_area(5, 3)
    15.0
    """
    if length < 0 or width < 0:
        raise ValueError("长度和宽度必须为正数")
    return length * width
```

## 2.3 `Sphinx/reStructuredText` 风格

```bash
def calculate_area(length, width):
    """
    计算矩形面积。

    使用给定的长度和宽度计算矩形的面积。

    :param length: 矩形的长度，必须为正数。
    :type length: float
    :param width: 矩形的宽度，必须为正数。
    :type width: float
    :return: 矩形的面积。
    :rtype: float
    :raises ValueError: 如果长度或宽度为负数。

    :example:

    >>> calculate_area(5, 3)
    15.0
    """
    if length < 0 or width < 0:
        raise ValueError("长度和宽度必须为正数")
    return length * width

```

## 2.4 `Epytext` 风格

```bash
def calculate_area(length, width):
    """
    计算矩形面积。

    使用给定的长度和宽度计算矩形的面积。

    @param length: 矩形的长度，必须为正数。
    @type length: float
    @param width: 矩形的宽度，必须为正数。
    @type width: float
    @return: 矩形的面积。
    @rtype: float
    @raise ValueError: 如果长度或宽度为负数。
    """
    if length < 0 or width < 0:
        raise ValueError("长度和宽度必须为正数")
    return length * width
```

## 2.5 `One-line` 风格 —— 单行文档字符串

```bash
def add(a, b):
    """返回两个数的和。"""
    return a + b
```

# 3. 文档字符串的访问方式

```python
def example():
    """这是一个示例函数。"""
    pass

# 访问文档字符串
print(example.__doc__)  # 输出：这是一个示例函数。

# 使用 help() 函数
help(example)
```

# 4. 各种风格对比

| 风格           | 特点             | 适用场景           | 工具支持             |
| -------------- | ---------------- | ------------------ | -------------------- |
| **`Google`**   | 简洁、易读、流行 | 现代Python项目     | `pydocstyle, Sphinx` |
| **`NumPy`**    | 结构化、详细     | 科学计算项目       | `pydocstyle, Sphinx` |
| **`Sphinx`**   | 功能强大、灵活   | 文档生成、大型项目 | `Sphinx`             |
| **`Epytext`**  | Java风格         | 传统项目           | `Epydoc`             |
| **`One-line`** | 简单直接         | 简单函数           | 所有工具             |

# 5. 示例: 类和方法

```python
class Rectangle:
    """表示矩形的类。

    这个类提供了计算矩形面积和周长的方法。

    Attributes:
        length (float): 矩形的长度。
        width (float): 矩形的宽度。

    Example:
        >>> rect = Rectangle(5, 3)
        >>> rect.area()
        15.0
    """

    def __init__(self, length, width):
        """初始化矩形实例。

        Args:
            length (float): 矩形的长度。
            width (float): 矩形的宽度。

        Raises:
            ValueError: 如果长度或宽度为负数。
        """
        if length < 0 or width < 0:
            raise ValueError("长度和宽度必须为正数")
        self.length = length
        self.width = width

    def area(self):
        """计算矩形的面积。

        Returns:
            float: 矩形的面积。
        """
        return self.length * self.width

    def perimeter(self):
        """计算矩形的周长。

        Returns:
            float: 矩形的周长。
        """
        return 2 * (self.length + self.width)
```

# 6. 文档字符串检查工具

## 6.1 `pydocstyle`

安装:

```python
pip install pydocstyle
```

使用:

```python
# 检查单个文件
pydocstyle your_file.py

# 检查整个项目
pydocstyle your_project/

# 指定风格
pydocstyle --convention=google your_file.py
pydocstyle --convention=numpy your_file.py
pydocstyle --convention=pep257 your_file.py
```

配置文件: `.pydocstyle.ini`

```python
[pydocstyle]
convention = google
match = (?!test_).*\.py
match_dir = [^\.].*
```

## 6.2 `flake8-docstrings`

安装

```python
pip install flake8-docstrings
```

使用

```python
flake8 --docstring-convention=google your_file.py
flake8 --docstring-convention=numpy your_file.py
```

## 6.3 `interrogate`

检查代码覆盖率:

```python
pip install interrogate

# 检查文档字符串覆盖率
interrogate your_project/

# 生成报告
interrogate -v your_project/
```

## 6.4 `pylint`

```python
pip install pylint

# 检查代码包括文档字符串
pylint your_file.py
```

# 7. 最佳实践建议

模块级别:

```python
"""模块的简短描述。

详细描述模块的功能和用途。

Example:
    使用示例
"""

import os
```

函数级别:

```python
def function_name(param1, param2):
    """简短描述。

    详细描述（可选）。

    Args:
        param1 (type): 参数描述。
        param2 (type): 参数描述。

    Returns:
        type: 返回值描述。

    Raises:
        ExceptionType: 异常描述。
    """
    pass
```

类级别:

```python
class User:
    """表示一个系统用户。

    该类用于存储用户的基本信息，并提供权限验证功能。
	
    Args:
        username (str): 用户的唯一标识名。
        email (str): 用户的电子邮件地址。
        role (str, optional): 用户角色，默认为 'guest'。
            可选值: 'admin', 'member', 'guest'。

    Attributes:
        username (str): 用户的名称。
        email (str): 用户的邮箱。
        role (str): 用户当前角色。
        is_active (bool): 用户是否处于激活状态。

    Raises:
        ValueError: 如果 username 为空。

    Example:
        >>> user = User('john_doe', 'john@example.com', 'admin')
        >>> user.has_permission('write')
        True
    """

    def __init__(self, username, email, role='guest'):
        if not username:
            raise ValueError("用户名不能为空")
        self.username = username
        self.email = email
        self.role = role
        self.is_active = True  # 公有属性，建议在 Attributes 中说明

    def has_permission(self, action):
        """检查用户是否有权限执行某操作。

        Args:
            action (str): 操作名称。

        Returns:
            bool: 如果有权限返回 True，否则返回 False。
        """
        return self.role == 'admin' and action in ['read', 'write', 'delete']
```

选择建议:

- **现代项目推荐：`Google 风格`**（简洁易读）
- **科学计算项目推荐：`NumPy` 风格**（结构化强）
- **需要生成文档：`Sphinx` 风格**（功能强大）

# 8. 配置建议

创建 `setup.cfg` 文件:

```python
[pydocstyle]
convention = google
add-ignore = D100,D104

[flake8]
docstring-convention = google
max-line-length = 100
```
