---
tags:
  - type/tutorial
  - lang/
  - lange/YouLang/
  - domain/computer-science
  - domain/computer-science/basic
  - topic/
  - status/draft
  - source/
aliases:
description:
datetime: " 2026-09-05 17:09:74 周六"
author:
rating:
introduction:
motto: 有志者，事竟成。破釜沉舟，百二秦关终属楚。苦心人，天不负。卧薪尝胆，三千越甲可吞吴。
---
[TOC]

<h1 style="text-align: center;">toml</h1>

----

TOML（Tom's Obvious Minimal Language）是由 GitHub 联合创始人 Tom Preston-Werner 于 2013 年创建的配置文件格式。它的设计目标是语义明显、易于阅读，能够无歧义地映射为哈希表（字典）。

# 1. 基本规则

- **大小写敏感**，文件必须是合法的 UTF-8 编码
- **注释**使用 `#`，从 `#` 开始到行尾均为注释
- **键值对**是基本构成单元，格式为 `key = "value"`

# 2. 键（key）

TOML 有三种键名形式：

**裸键**：只能包含 ASCII 字母、数字、下划线和短横线

```
key = "value"
bare_key = "value"
bare-key = "value"
1234 = "value"
```

**引号键**：可以用双引号或单引号包裹，支持更广泛的字符

```
"127.0.0.1" = "value"
"character encoding" = "value"
'key2' = "value"
```

**点分隔键**：用点将多个键连在一起，相当于嵌套结构

```
"物理属性"."颜色" = "橙色"
site."google.com" = true
```

这等价于 JSON 中的 `{"物理属性": {"颜色": "橙色"}, "site": {"google.com": true}}`。

# 3. 值的数据类型

TOML 支持以下数据类型：

| TOML 类型        | 示例                         | 说明                                                   |
| :--------------- | :--------------------------- | :----------------------------------------------------- |
| **字符串**       | `str = "Hello"`              | 支持转义                                               |
| **多行字符串**   | `str = """多行文本"""`       | 三个引号包裹                                           |
| **字面量字符串** | `path = 'C:\Users'`          | 单引号，不转义                                         |
| **整数**         | `int = 42`                   | 支持十进制、十六进制(`0x`)、八进制(`0o`)、二进制(`0b`) |
| **浮点数**       | `float = 3.14`               | 支持科学计数法 `5e+22`                                 |
| **布尔值**       | `debug = true`               | 必须全小写                                             |
| **日期时间**     | `dob = 1979-05-27T07:32:00Z` | 支持时区偏移                                           |
| **数组**         | `ports = [8000, 8001]`       | 可包含不同类型                                         |
| **表（Table）**  | `[owner]`                    | 相当于字典/对象                                        |
| **内联表**       | `temp = {cpu = 79.5}`        | 一行内定义表                                           |

# 4. 表与嵌套

表用 `[表名]` 定义，其下的键值对都属于该表：

```python
[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [8000, 8001, 8002]
```

**嵌套表**用点分隔：

```python
[servers]
[servers.alpha]
ip = "10.0.0.1"
role = "前端"

[servers.beta]
ip = "10.0.0.2"
role = "后端"
```

这等价于 `servers` 下有两个子表 `alpha` 和 `beta`。

**表数组**：用 `[[表名]]` 定义多个同名的表

```python
[[products]]
name = "Hammer"
sku = 738594937

[[products]]
name = "Nail"
sku = 284758393
```

# 5. 完整示例

```python
# 这是一个 TOML 文档
title = "TOML 示例"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [8000, 8001, 8002]
data = [["delta", "phi"], [3.14]]
temp_targets = { cpu = 79.5, case = 72.0 }

[servers]
[servers.alpha]
ip = "10.0.0.1"
role = "前端"
[servers.beta]
ip = "10.0.0.2"
role = "后端"
```

# 6. Python 操作 toml 数据

Python 生态中有多种方式处理 TOML 数据，根据不同需求选择合适的工具。

## 6.1  `tomlib`（Python 3.11+ 标准库）

从 Python 3.11 开始，`tomllib` 成为标准库的一部分，**仅支持读取（解析）TOML 文件，不支持写入**。

**读取文件**（必须使用二进制模式）：

```python
import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
print(data)
```

**解析字符串**：

```python
import tomllib

toml_str = """
python-version = "3.11.0"
python-implementation = "CPython"
"""
data = tomllib.loads(toml_str)
print(data)  # {'python-version': '3.11.0', 'python-implementation': 'CPython'}
```

**类型转换表**：

| TOML 类型 | Python 类型                          |
| :-------- | :----------------------------------- |
| 字符串    | `str`                                |
| 整数      | `int`                                |
| 浮点数    | `float`（可用 `parse_float` 自定义） |
| 布尔值    | `bool`                               |
| 日期时间  | `datetime.datetime`                  |

## 6.2 `tomli` （第三方库）

`tomli` 是一个轻量级 TOML 解析库，兼容 TOML v1.0.0 和 v1.1.0。在 Python 3.11 之前，它是解析 TOML 的主流选择。

```python
pip install tomli
```

```python
import tomli

with open("config.toml", "rb") as f:
    data = tomli.load(f)
```

## 6.3 toml（第三方库）

`toml` 库**同时支持读取和写入**，功能更全面。

```python
pip install toml
```

**读取：**

```python
import toml

with open('config.toml', 'r', encoding='utf-8') as f:
    config = toml.load(f)

# 或从字符串解析
config = toml.loads('name = "MyApp"')
```

**写入：**

```python
import toml

new_config = {
    "app": {"name": "MyAwesomeApp", "version": "2.0.0"},
    "features": ["login", "chat", "notifications"]
}

with open('new_config.toml', 'w', encoding='utf-8') as f:
    toml.dump(new_config, f)

# 或转为字符串
toml_str = toml.dumps(new_config)
```

## 6.4 `tomli-w`（TOML 写入器）

`tomli-w` 是一个专门用于写入 TOML 的库，可与 `tomllib` 配合使用。

```
pip install tomli-w
```

## 6.5 `tomlkit`（保留样式的读写）

`tomlkit` 兼具读取和写入功能，并且**保留原文件的格式和注释**，非常适合编辑现有 TOML 文件。

```
pip install tomlkit
```

## 6.6 库选择建议

| 场景                       | 推荐工具                      |
| :------------------------- | :---------------------------- |
| Python 3.11+，只需读取     | `tomllib`（标准库，无需安装） |
| Python 3.11 以下，只需读取 | `tomli`                       |
| 需要读取和写入             | `toml`                        |
| 需要保留格式/注释          | `tomlkit`                     |
| 需要高性能                 | `rtoml`（Rust 实现）          |

# 7. 学习资源

1. **TOML 官方中文文档**（`toml.io/cn/`）：最权威的语法参考，包含完整规范
2. **Python 官方文档 - tomllib**（`docs.python.org/zh-cn/3.13/library/tomllib.html`）：标准库模块的完整 API 文档

另：**优质教程资源**：

| 教程                                                     | 特点                                          | 来源 |
| :------------------------------------------------------- | :-------------------------------------------- | :--- |
| **Python and TOML**（Real Python）                       | 1小时深度教程，涵盖读写配置、`pyproject.toml` | 英文 |
| **Working With TOML and Python**（Real Python 视频课程） | 16节视频课，含练习和问答                      | 英文 |
| **Python toml模块详解**（阿里云开发者）                  | 新手入门，含安装、读写、类型映射              | 中文 |
| **3分钟学会 TOML 配置文件**（腾讯云）                    | 快速上手，对比 JSON/YAML                      | 中文 |
| **TOML 详解**（CSDN）                                    | 全面介绍语法、数据类型、应用场景              | 中文 |
| **配置文件格式 TOML 快速上手**（腾讯云）                 | 语法规则 + 数据结构详解                       | 中文 |

