---
aliases:
  - course of study
  - course
  - json
  - module
tags:
  - tutorial
  - computer-science
  - json
category: knowledge
datetime: " 2026-08-08 11:08:55 周六"
author: wephiles
rating: "5"
---

<h1 style="text-align: center;">json 模块</h1>

# 一、`JSON` 与 `Python json` 模块概述

## 1.1 什么是 `json`

`JSON`（`JavaScript Object Notation`）是一种轻量级数据交换格式，易于人阅读和编写，也易于机器解析和生成。它基于 `JavaScript` 的子集，但现在已成为独立于语言的通用数据格式。

**`JSON` 的优势：**

- 跨语言、跨平台
- 简洁清晰
- 易于解析
- `Web API` 的标准数据格式

## 1.2 `Python json` 模块简介

Python 的 `json` 模块提供了 `JSON` 数据的编码和解码功能，实现了 Python 对象与 JSON 字符串之间的相互转换。

# 二、`json` 模块的核心架构

```python
============================================================
Python json 模块核心架构
============================================================

【核心函数】
  - json.dump()
  - json.dumps()
  - json.load()
  - json.loads()

【核心类】
  - json.JSONEncoder
  - json.JSONDecoder

【数据类型映射关系】
  Python          →       JSON
  ----------------------------------------
  dict            →       object
  list, tuple     →       array
  str             →       string
  int, float      →       number
  True            →       true
  False           →       false
  None            →       null
```

# 三、四大核心函数

## 3.1 `json.dumps()` —— 将 Python 对象转换为 `JSON` 字符串

函数签名：

```python
json.dumps(obj, *, skipkeys=False, ensure_ascii=True, 
            check_circular=True, allow_nan=True, 
            cls=None, indent=None, separators=None, 
            default=None, sort_keys=False, **kw)
```

**通俗理解：** `dumps` = “dump string”，将 Python 对象"倾倒"成 JSON 格式的**字符串**。

```python
======================================================================
json.dumps() - 序列化为字符串
======================================================================

【示例1: 基本数据类型】
原始 Python 对象: {'name': '张三', 'age': 30, 'is_student': False, 'score': 95.5, 'hobbies': ['reading', 'coding', 'gaming'], 'address': None}
JSON 字符串: {"name": "\u5f20\u4e09", "age": 30, "is_student": false, "score": 95.5, "hobbies": ["reading", "coding", "gaming"], "address": null}

【示例2: 使用 indent 美化输出】
格式化后的 JSON:
{
  "name": "\u5f20\u4e09",
  "age": 30,
  "is_student": false,
  "score": 95.5,
  "hobbies": [
    "reading",
    "coding",
    "gaming"
  ],
  "address": null
}

【示例3: ensure_ascii 参数】
默认情况 (ensure_ascii=True):
{"name": "\u5f20\u4e09", "age": 30, "is_student": false, "score": 95.5, "hobbies": ["reading", "coding", "gaming"], "address": null}

设置 ensure_ascii=False (推荐):
{"name": "张三", "age": 30, "is_student": false, "score": 95.5, "hobbies": ["reading", "coding", "gaming"], "address": null}

【示例4: sort_keys 参数 - 按键名排序】
原始: {'z': 1, 'a': 2, 'm': 3}
排序后: {"a": 2, "m": 3, "z": 1}

【示例5: 元组的处理】
包含元组的数据: {'coordinates': (10.5, 20.3), 'list_data': [1, 2, 3]}
JSON 输出 (元组变列表): {"coordinates": [10.5, 20.3], "list_data": [1, 2, 3]}

```

## 3.2 `json.dump()` - 将 Python 对象序列化并写入文件

函数签名：

```python
json.dump(obj, fp, *, skipkeys=False, ensure_ascii=True, 
           check_circular=True, allow_nan=True, 
           cls=None, indent=None, separators=None, 
           default=None, sort_keys=False, **kw)

```

**通俗理解：** `dump` 直接将 Python 对象"倾倒"到**文件**中，不需要先转成字符串再写入。

## 3.3 `json.loads()` - 从 `JSON` 字符串反序列化为 Python 对象

函数签名：

```python
json.loads(s, *, cls=None, object_hook=None, 
            parse_float=None, parse_int=None, 
            parse_constant=None, object_pairs_hook=None, **kw)
```

**通俗理解：** `loads` = “load string”，从 JSON **字符串**中"加载"出 Python 对象。

## 3.4 `json.load()` - 从文件读取并反序列化为 Python 对象

函数签名：

```python
json.load(fp, *, cls=None, object_hook=None, 
           parse_float=None, parse_int=None, 
           parse_constant=None, object_pairs_hook=None, **kw)
```

# 四、核心参数详解

## 4.1 `dumps()` 和 `dump()` 的关键参数

| 参数           | 说明                 | 默认值         | 使用场景              |
| -------------- | -------------------- | -------------- | --------------------- |
| `indent`       | 缩进空格数，美化输出 | `None`         | 配置文件、日志、调试  |
| `ensure_ascii` | 是否转义非ASCII字符  | `True`         | **False**推荐用于中文 |
| `sort_keys`    | 是否按键排序         | `False`        | 配置文件比对、测试    |
| `skipkeys`     | 跳过非字符串键       | `False`        | 处理不规范的字典      |
| `separators`   | 分隔符设置           | `(', ', ': ')` | 压缩JSON大小          |
| `default`      | 处理无法序列化的对象 | `None`         | 自定义对象序列化      |
| `cls`          | 自定义编码器类       | `None`         | 高级自定义序列化      |

## 4.2 `loads()` 和 `load()` 的关键参数

| 参数                | 说明                   | 使用场景                  |
| ------------------- | ---------------------- | ------------------------- |
| `object_hook`       | 解析后的自定义处理     | 将字典转为自定义类        |
| `object_pairs_hook` | 解析键值对的自定义处理 | 保留键顺序、`OrderedDict` |
| `parse_float`       | 自定义浮点数解析       | 用 `Decimal` 处理精度     |
| `parse_int`         | 自定义整数解析         | 指定整数类型              |
| `parse_constant`    | 解析常量               | 处理特殊值                |

# 五、核心类详解

## 5.1 `json.JSONEncoder` —— 自定义编码器

**作用：** 当默认的 `JSON` 序列化无法处理某些 Python 对象时（如日期时间、自定义类），可以通过继承 `JSONEncoder` 实现自定义序列化。

**核心方法：** `default(obj)` - 必须重写此方法处理自定义对象。

```python
import json
from datetime import datetime
from decimal import Decimal

class CustomEncoder(json.JSONEncoder):
    """自定义 JSON 编码器"""
    
    def default(self, obj):
        # 处理日期时间对象
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        
        # 处理 Decimal 对象（高精度数值）
        if isinstance(obj, Decimal):
            return float(obj)
        
        # 处理集合类型
        if isinstance(obj, set):
            return list(obj)
        
        # 处理自定义类（需要有 to_dict 方法）
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        
        # 其他无法处理的类型
        return super().default(obj)  # 抛出 TypeError

# 使用方式
data = {
    "created_at": datetime.now(),
    "price": Decimal("19.99"),
    "tags": {"python", "json", "tutorial"}
}

json_str = json.dumps(data, cls=CustomEncoder, ensure_ascii=False)

```

## 5.2 `json.JSONDecoder` - 自定义解码器

**作用：** 实现 `JSON` 数据到 Python 对象的自定义转换。

```python
import json

class CustomDecoder(json.JSONDecoder):
    """自定义 JSON 解码器"""
    
    def __init__(self, *args, **kwargs):
        # 设置 object_hook
        kwargs['object_hook'] = self.object_hook
        super().__init__(*args, **kwargs)
    
    @staticmethod
    def object_hook(dct):
        """对解析出的每个字典进行处理"""
        # 自动将包含 __class__ 的字典转为对象
        if '__class__' in dct:
            class_name = dct.pop('__class__')
            # 根据类名创建对象（示例）
            obj = type(class_name, (), dct)
            return obj
        return dct

# 使用方式
json_str = '{"__class__": "Person", "name": "张三", "age": 30}'
obj = json.loads(json_str, cls=CustomDecoder)

```

# 六、实际工程应用场景

## 6.1 配置文件管理

```python
import json
import os

class ConfigManager:
    """配置文件管理器"""
    
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load()
    
    def load(self):
        """加载配置"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()

# 使用
config = ConfigManager('config.json')
config.set('database.host', 'localhost')
print(config.get('database.host'))

```

## 6.2 `API` 数据交互

```python
import json

# 构造 API 请求体
request_data = {
    "action": "create_user",
    "data": {
        "username": "zhangsan",
        "email": "zhang@example.com",
        "age": 25
    }
}

# 序列化为 JSON 字符串发送
json_payload = json.dumps(request_data, ensure_ascii=False)

# 模拟接收 API 响应
response_json = '''
{
    "code": 200,
    "message": "创建成功",
    "data": {
        "user_id": 10001,
        "created_at": "2024-01-01 10:00:00"
    }
}
'''

# 解析响应
response = json.loads(response_json)
if response['code'] == 200:
    print(f"用户创建成功，ID: {response['data']['user_id']}")

```

## 6.3 数据持久化

```python
import json
from dataclasses import dataclass, asdict

@dataclass
class User:
    """用户数据类"""
    id: int
    name: str
    email: str
    active: bool = True

class UserRepository:
    """用户数据仓库"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.users = self._load_all()
    
    def _load_all(self):
        """加载所有用户"""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [User(**u) for u in data]
        return []
    
    def _save_all(self):
        """保存所有用户"""
        data = [asdict(u) for u in self.users]
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, user):
        self.users.append(user)
        self._save_all()
    
    def find_by_id(self, user_id):
        return next((u for u in self.users if u.id == user_id), None)

```

# 七、异常处理与错误排查

## 7.1 常见异常

```python
import json

# JSONDecodeError - JSON 格式错误
try:
    data = json.loads('{"name": "张三",}')  # 多了逗号
except json.JSONDecodeError as e:
    print(f"JSON 格式错误: {e}")
    print(f"错误位置: 行 {e.lineno}, 列 {e.colno}")

# TypeError - 无法序列化的类型
try:
    data = {"date": datetime.now()}
    json.dumps(data)  # datetime 无法直接序列化
except TypeError as e:
    print(f"无法序列化: {e}")

# 正确处理方式
json.dumps(data, default=lambda x: x.isoformat() if hasattr(x, 'isoformat') else str(x))

```

## 7.2 安全地处理 `JSON`

```python
import json

def safe_json_loads(json_str, default=None):
    """安全的 JSON 解析"""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return default

def safe_json_dumps(obj, **kwargs):
    """安全的 JSON 序列化"""
    kwargs.setdefault('ensure_ascii', False)
    kwargs.setdefault('default', lambda x: str(x))
    
    try:
        return json.dumps(obj, **kwargs)
    except TypeError as e:
        print(f"序列化警告: {e}")
        return json.dumps({}, **kwargs)

```

# 八、最佳实践总结

## 8.1 编码规范

1. **始终指定 `ensure_ascii=False`**：正确处理中文和其他非 ASCII 字符
2. **使用 `indent=2` 美化输出**：方便调试和配置文件阅读
3. **使用 `with` 语句**：确保文件正确关闭
4. **指定 `encoding='utf-8'`**：避免编码问题

## 8.2 性能优化

```python
# 压缩 JSON（减少空格）
json.dumps(data, separators=(',', ':'))

# 使用 ujson（第三方库，更快）
# pip install ujson
import ujson
ujson.dumps(data)
```

## 8.3 工具函数模板

```python
import json
import os

def read_json(filepath, default=None):
    """读取 JSON 文件"""
    if not os.path.exists(filepath):
        return default
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(filepath, data, indent=2):
    """写入 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def pretty_json(data):
    """美化 JSON 输出"""
    return json.dumps(data, ensure_ascii=False, indent=2)

```

