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
datetime: " 2026-09-05 16:09:07 周六"
author:
rating:
introduction:
motto: 有志者，事竟成。破釜沉舟，百二秦关终属楚。苦心人，天不负。卧薪尝胆，三千越甲可吞吴。
---
[TOC]

<h1 style="text-align: center;">yaml</h1>

----

YAML（YAML Ain't Markup Language）是一种人类可读的数据序列化格式，广泛用于配置文件（如 Docker Compose、Kubernetes）和数据交换场景。

# 1. 基本语法规则

| 规则               | 说明                                             |
| :----------------- | :----------------------------------------------- |
| **大小写敏感**     | `Name` 和 `name` 是不同的键                      |
| **缩进表示层级**   | 只能使用**空格**，禁止使用 Tab 键                |
| **缩进空格数不限** | 同层级的元素左对齐即可，推荐 2 个空格            |
| **注释**           | 使用 `#` 表示注释，从 `#` 到行尾的内容都会被忽略 |
| **键值分隔**       | 冒号后面**必须**加一个空格（`key: value`）       |
| **文档分隔**       | `---` 表示文档开始，`...` 表示文档结束           |

# 2. 数据类型

## 2.1 对象（映射/字典）

键值对的集合，使用冒号分隔：

```yaml
person:
  name: Alice
  age: 30
```

行内写法：`person: {name: Alice, age: 30}`

## 2.2 数组（序列/列表）

以 `-` 开头表示列表项：

```yaml
fruits:
  - Apple
  - Banana
  - Orange
```

行内写法：`fruits: [Apple, Banana, Orange]`

## 2.3 复合结构（嵌套）

对象和数组可以任意嵌套：

```yaml
company:
  name: TechCorp
  employees:
    - name: John
      role: Developer
    - name: Sarah
      role: Designer
```

## 2.4 基本型

| 类型      | 示例                                                     |
| :-------- | :------------------------------------------------------- |
| 字符串    | `name: Kalyan`（可加引号：`"Hello"` 或 `'Hello'`）       |
| 整数      | `age: 23`                                                |
| 浮点数    | `score: 98.5`                                            |
| 布尔值    | `is_student: true` / `is_married: false`（大小写不敏感） |
| 空值      | `spouse: null` 或 `spouse: ~`                            |
| 时间/日期 | ISO 8601 格式：`2025-07-09T14:30:00+08:00`               |

## 2.5 多行字符串

**`|`（保留换行符）**：

```yaml
description: |
  这是第一行
  这是第二行
  这是第三行
```

- **`>`（折叠为空格）**：

```yaml
summary: >
  这是一个很长的句子，
  会被折叠成一行，
  换行符变成空格。
```

# 3. 高级特性

## 3.1 锚点与别名

使用 `&` 定义锚点，`*` 引用锚点，避免重复定义：

```yaml
defaults: &config
  host: localhost
  port: 8080

development:
  <<: *config
  database: dev_db

test:
  <<: *config
  database: test_db
```

`<<: *config` 表示将 `config` 锚点的所有键值对合并进来。

## 3.2 强制类型转换

使用 `!!` 指定类型：

```yaml
str_int: !!str 123      # 转为字符串 "123"
str_bool: !!str true    # 转为字符串 "true"
is_float: !!float 42    # 转为浮点数 42.0
```

# 4. Python 操作 `yaml`

Python 标准库不包含 YAML 处理功能，需要使用第三方库。最常用的是 **PyYAML**，如需保留原始格式（注释、缩进等）可使用 **`ruamel.yaml`**。

## 4.1 安装

```yaml
pip install pyyaml
```

## 4.2 读取 `yaml` 文件

```python
import yaml

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# 访问数据，就像操作普通字典一样
print(data['database']['host'])
```

**⚠️ 重要安全提示**：始终使用 `yaml.safe_load()` 而非 `yaml.load()`，因为 `yaml.load()` 可能执行任意代码，存在安全风险。

## 4.3 从字符串读取 `yaml`

```python
import yaml

yaml_str = """
name: Alice
age: 30
hobbies:
  - reading
  - coding
"""

data = yaml.safe_load(yaml_str)
print(data['name'])  # 输出: Alice
```

## 4.4 写入 yaml 文件

使用 `yaml.dump()` 将 Python 对象写入 YAML 文件：

```python
import yaml

config = {
    'database': {
        'host': 'localhost',
        'port': 5432,
        'credentials': {
            'username': 'admin',
            'password': 'secret123'
        }
    },
    'debug': True
}

with open('generated_config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

**常用参数**：

- `default_flow_style=False`：使用块风格（更易读），而不是行内风格
- `allow_unicode=True`：支持中文字符
- `indent=2`：指定缩进空格数

## 4.5 多文档处理

一个 YAML 文件可以包含多个文档（用 `---` 分隔）：

```python
import yaml

# 读取多个文档
with open('multi.yaml', 'r') as f:
    documents = list(yaml.safe_load_all(f))
    for doc in documents:
        print(doc)

# 写入多个文档
doc1 = {'name': 'Alice'}
doc2 = {'name': 'Bob'}
with open('output.yaml', 'w') as f:
    yaml.dump_all([doc1, doc2], f)
```

## 4.6 完整示例

假设有一个 `config.yaml` 文件：

```python
# 应用配置
app:
  name: MyApp
  version: 1.0.0

database:
  host: localhost
  port: 3306
  user: root
  password: pass123

features:
  - logging
  - monitoring
  - analytics
```

Python 操作代码：

```python
import yaml

# 1. 读取配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

print(f"App: {config['app']['name']} v{config['app']['version']}")
print(f"DB: {config['database']['host']}:{config['database']['port']}")

# 2. 修改配置
config['database']['port'] = 3307
config['features'].append('caching')

# 3. 写回文件
with open('config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

## 4.7 关于 `ruamel.yaml`

如果需要**保留原文件的注释、格式和缩进**（例如修改后仍保持人类可读性），推荐使用 `ruamel.yaml`：

```python
pip install ruamel.yaml
```

```python
from ruamel.yaml import YAML

yaml = YAML()
with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.load(f)

# 修改数据
data['database']['port'] = 3307

# 写回（保留原始格式和注释）
with open('config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f)
```

## 4.8 Python 中两种操作 yaml 方式的对比

| 特性                 | PyYAML | ruamel.yaml |
| :------------------- | :----- | :---------- |
| YAML 版本            | 1.1    | 1.2         |
| 保留注释/格式        | ❌      | ✅           |
| 使用简单             | ✅      | ✅           |
| 性能（配合 LibYAML） | 快     | 中等        |

对于大多数配置管理场景，PyYAML 已经足够；如果需要频繁修改并保持文件的可读性，建议使用 ruamel.yaml。

# 5. 学习资源

- **YAML 官方规范**：最权威的文档，适合深度阅读以理解 YAML 的设计哲学和全部细节。你可以访问 [yaml.org](https://yaml.org/) 查看最新版 **YAML 1.2.2** 规范。
- **PyYAML 官方文档**：PyYAML 是 Python 中最流行的 YAML 库。官方维基 [pyyaml.org/wiki/PyYAMLDocumentation](http://pyyaml.org/wiki/PyYAMLDocumentation) 提供了教程和参考，但官方也提醒内容可能“粗糙且不完整”。
- **ruamel.yaml 官方文档**：如果需要保留注释和格式，ruamel.yaml 是更好的选择。其文档在 [yaml.dev/doc/ruamel.yaml](https://yaml.dev/doc/ruamel.yaml)。
- **PyYAML GitHub 仓库**：在 [github.com/yaml/pyyaml](https://github.com/yaml/pyyaml) 可以获取源码、提交 issue 和参与讨论。
- **Learn X in Y Minutes**：一个非常受欢迎的快速语法速查手册。页面 [learnxinyminutes.com/docs/yaml/](https://learnxinyminutes.com/docs/yaml/) 能让你在极短时间内了解 YAML 的核心语法。

- **Real Python 教程**：一篇非常详尽的中级教程，标题为《YAML: The Missing Battery in Python》。它系统地讲解了在 Python 中使用 YAML 的各个方面。
- **Kubernetes 相关教程**：如果你想学习 YAML 在 Kubernetes 中的应用，这个教程很合适。它在 GitHub 上的地址是 [github.com/peachest/kubernetes-hands-on-course](https://github.com/peachest/kubernetes-hands-on-course)。
- **中文社区教程**：腾讯云开发者社区等平台有很多优质的中文教程，例如《YAML 从入门到应用》、《一文读懂 YAML》等，对新手非常友好。
- **特定场景指南**：YAML 在不同工具中有特定用法，可参考 **Ansible** 、**Kubernetes** 、**Docker Compose** 和 **GitHub Actions** 的官方文档。
- **YAML Tutorial for Beginners**：一个约 30 分钟的入门视频，全面介绍 YAML 语法。
- **YAML in DevOps**：一个约 45 分钟的视频，侧重于 YAML 在 CI/CD 和配置管理中的实际应用。
- **Advanced YAML Techniques**：一个约 25 分钟的视频，深入讲解锚点、别名等高级特性。
- **《YAML Cookbook》**：提供了大量 YAML 的实用“菜谱”和解决方案。
- **《Infrastructure as Code》**：这本书将 YAML 置于更宏大的基础设施即代码（IaC）背景下，有助于理解其重要性。
- **YAML Lint**：一个在线 YAML 校验器和格式化工具，网址是 [yamllint.com](http://www.yamllint.com/)。可以用来检查自己编写的 YAML 文件语法是否正确。
- **在线 Playground**：你可以在各种在线 YAML 解析器中粘贴代码，实时查看解析结果，这是理解语法的好方法。
- **Matrix 与 IRC**：PyYAML 的维护者在 Matrix (`#pyyaml:yaml.io`) 和 IRC (`#pyyaml` on [irc.libera.chat](https://irc.libera.chat/)) 上有活跃的频道，可以在此提问和交流。
- **Stack Overflow**：遇到具体问题时，在 Stack Overflow 上搜索或提问，通常能得到很快的回复。
