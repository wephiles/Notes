---
aliases:
  - course of study
  - course
  - dotenv
  - Python
  - tutorial
  - third party lib
tags:
  - tutorial
  - computer-science
  - dotenv
  - third-party-lib
  - Python
category: knowledge
datetime: " 2026-08-08 14:08:49 周六"
author: wephiles
rating: "1"
---

[TOC]

<h1 style="text-align: center;">python-dotenv</h1>

# 1. 什么是 `python-dotenv`

`python-dotenv` 是一个用于从 `.env` 文件中读取环境变量到 Python 程序中的库。它的核心价值在于：

- 将配置与代码分离
- 敏感信息安全存储
- 多环境配置管理
- 简化开发流程

# 2. 安装方法

```python
pip install python-dotenv
```

# 3. 核心 `API` 详解

## 3.1 `load_dotenv`

```python
"""
函数签名：
load_dotenv(
    dotenv_path=None,      # .env 文件路径
    override=False,        # 是否覆盖已存在的环境变量
    verbose=False,         # 是否显示详细输出
    encoding=None          # 文件编码
)

返回值：True（成功）或 False（失败）
"""
from dotenv import load_dotenv
import os

# 基本用法
load_dotenv()  # 自动查找当前目录下的 .env 文件

# 指定路径
load_dotenv('/path/to/.env')

# 覆盖已存在的环境变量
load_dotenv(override=True)

# 示例
load_dotenv()
database_url = os.getenv('DATABASE_URL')
print(f"数据库URL: {database_url}")

```

## 3.2 `dotenv_values()` - 返回字典而非设置环境变量

```python
"""
函数签名：
dotenv_values(
    dotenv_path=None,
    encoding='UTF-8',
    verbose=True
)

返回值：OrderedDict 字典
"""
from dotenv import dotenv_values

# 获取配置但不设置到环境变量
config = dotenv_values('.env')
print(config['DATABASE_URL'])  # 直接通过字典访问

# 与 load_dotenv 的区别：
# load_dotenv() → 设置到 os.environ
# dotenv_values() → 只返回字典，不修改环境变量

# 适用场景：临时使用配置，不想污染全局环境变量

```

## 3.3 `set_key()` - 设置键值

```python
"""
函数签名：
set_key(
    dotenv_path,           # .env 文件路径
    key_to_set,            # 键名
    value_to_set,          # 值
    encoding=None,
    quote_mode='always'    # 引号模式：'always', 'auto', 'never'
)

返回值：(True/False, 'key' 或 None)
"""
from dotenv import set_key

# 添加或修改配置
set_key('.env', 'NEW_KEY', 'new_value')

# 带引号处理
set_key('.env', 'PASSWORD', 'my pass with spaces', quote_mode='always')

# 示例
set_key('.env', 'API_KEY', 'sk-xxxxx')

```

## 3.4 `unset_key()` - 删除键值

```python
"""
函数签名：
unset_key(
    dotenv_path,
    key_to_unset,
    encoding=None
)

返回值：(True/False, 'key' 或 None)
"""
from dotenv import unset_key

# 删除配置项
result = unset_key('.env', 'UNUSED_KEY')
print(f"删除结果: {result}")

```

## 3.5 `get_key()` - 获取单个键值

```python
"""
函数签名：
get_key(
    dotenv_path,
    key_to_get,
    encoding=None
)

返回值：键对应的值（字符串）或 None
"""
from dotenv import get_key

# 只获取单个值，不加载全部
api_key = get_key('.env', 'API_KEY')
print(f"API Key: {api_key}")

```

## 3.6 `find_dotenv()` - 自动查找 `.env` 文件

```python
"""
函数签名：
find_dotenv(
    filename='.env',
    raise_error_if_not_found=False,
    usecwd=False  # 是否从当前工作目录开始查找
)

返回值：文件路径（字符串）
"""
from dotenv import find_dotenv

# 查找 .env 文件
env_path = find_dotenv()
print(f"找到 .env 文件: {env_path}")

# 自定义文件名
env_path = find_dotenv('.env.production')

# 与 load_dotenv 配合使用
load_dotenv(find_dotenv())

```

# 4. 完整使用示例

## 4.1 基础配置管理

```python
# .env 文件内容
"""
DATABASE_URL=postgresql://localhost:5432/mydb
DATABASE_USER=admin
DATABASE_PASSWORD=secret123
API_KEY=sk-test-123456789
DEBUG=True
PORT=8000
"""

# app.py
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 使用环境变量
db_url = os.getenv('DATABASE_URL')
db_user = os.getenv('DATABASE_USER')
api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG', 'False').lower() == 'true'
port = int(os.getenv('PORT', '8000'))

print(f"数据库: {db_url}")
print(f"用户: {db_user}")
print(f"调试模式: {debug}")
print(f"端口: {port}")
```

```python
数据库: postgresql://localhost:5432/mydb
用户: admin
调试模式: True
端口: 8000
```

## 4.2 多环境配置

```python
"""
项目结构：
├── .env                  # 默认配置
├── .env.development      # 开发环境
├── .env.production       # 生产环境
└── config.py             # 配置加载
"""

# config.py
import os
from dotenv import load_dotenv, find_dotenv

def get_env_filename():
    """根据运行环境返回对应的 .env 文件名"""
    env = os.getenv('APP_ENV', 'development')  # 默认开发环境
    return f'.env.{env}'

# 加载对应环境的配置
env_file = get_env_filename()
load_dotenv(find_dotenv(env_file))

# 或使用更健壮的方式
def load_config():
    """加载配置的推荐方式"""
    # 先加载默认配置
    load_dotenv('.env')
    
    # 再加载环境特定配置（覆盖默认）
    env = os.getenv('APP_ENV', 'development')
    env_file = f'.env.{env}'
    
    try:
        load_dotenv(env_file, override=True)
    except FileNotFoundError:
        print(f"警告: 未找到 {env_file}")

load_config()

# 使用配置
print(f"当前环境: {os.getenv('ENV')}")
print(f"数据库: {os.getenv('DATABASE_URL')}")
```

## 4.3 类型安全的配置类

```python
# config.py
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    """配置类，提供类型安全和默认值"""
    
    # 数据库配置
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    DATABASE_USER: str = os.getenv('DATABASE_USER', 'root')
    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD', '')
    
    # API 配置
    API_KEY: str = os.getenv('API_KEY', '')
    API_TIMEOUT: int = int(os.getenv('API_TIMEOUT', '30'))
    
    # 应用配置
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT: int = int(os.getenv('PORT', '8000'))
    APP_NAME: str = os.getenv('APP_NAME', 'MyApp')
    
    # 可选配置
    REDIS_URL: Optional[str] = os.getenv('REDIS_URL')
    
    @classmethod
    def validate(cls):
        """验证必要配置"""
        required = ['DATABASE_URL', 'API_KEY']
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"缺少必要配置: {missing}")
        
        return True

# 使用
config = Config()
print(f"数据库: {config.DATABASE_URL}")
print(f"调试: {config.DEBUG}")

# 验证
Config.validate()
```

## 4.4 动态修改配置

```python
from dotenv import set_key, unset_key, get_key, load_dotenv
import os

# 创建新配置
def setup_api_key(api_key):
    """设置 API Key"""
    result = set_key('.env', 'API_KEY', api_key)
    print(f"设置结果: {result}")
    return result

# 更新配置
def update_database_url(new_url):
    """更新数据库 URL"""
    set_key('.env', 'DATABASE_URL', new_url)
    load_dotenv(override=True)  # 重新加载
    print(f"已更新数据库URL")

# 删除配置
def remove_config(key):
    """删除配置项"""
    result = unset_key('.env', key)
    print(f"删除 {key}: {result}")

# 使用示例
setup_api_key('sk-new-api-key-123')
update_database_url('postgresql://newhost:5432/newdb')
remove_config('UNUSED_VAR')

```

## 4.5 `Flask` 项目集成

```python
# Flask 项目示例
# .env
"""
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///dev.db
"""

# app.py
from flask import Flask
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

@app.route('/')
def index():
    return f"App: {os.getenv('APP_NAME')}"

if __name__ == '__main__':
    app.run(
        debug=os.getenv('DEBUG', 'False') == 'true',
        port=int(os.getenv('PORT', 5000))
    )

```

## 4.6 `Django` 项目集成

```python
# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'mydb'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# 邮件配置
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

# 5. 高级用法

## 5.1 变量插值

```python
# .env 文件支持变量引用
"""
BASE_DIR=/app
LOG_DIR=${BASE_DIR}/logs
DATA_DIR=${BASE_DIR}/data
"""

from dotenv import load_dotenv
import os

load_dotenv()
print(f"日志目录: {os.getenv('LOG_DIR')}")  # /app/logs

```

## 5.2 命令行工具

```python
# 在命令行中使用
python -m dotenv run -- python your_script.py

# 或
python -m dotenv run python your_script.py

```

## 5.3 使用流式输入

```python
from dotenv import load_dotenv
from io import StringIO

# 从字符串加载配置
config_content = """
API_KEY=test123
DEBUG=True
"""

# 使用 StringIO
config_stream = StringIO(config_content)
from dotenv.main import load_stream
load_stream(config_stream)

import os
print(os.getenv('API_KEY'))  # test123

```

# 6. `.env` 文件格式规则

```python
# 注释使用 # 号
# 这是注释

# 基本键值对
KEY=value

# 值可以包含空格（推荐用引号）
KEY_WITH_SPACES="value with spaces"
KEY_WITH_SPACES='value with spaces'

# 多行值
MULTILINE="line1\nline2\nline3"

# 空值
EMPTY_VALUE=

# 等号在值中
URL=https://example.com?param=value&other=test

# 变量引用
BASE_PATH=/home/user
LOG_PATH=${BASE_PATH}/logs

# 导出风格（两种写法等价）
export SHELL_STYLE=value
```

# 7. 最佳实践

## 7.1 项目结构

```python
my_project/
├── .env                    # 本地开发配置（不提交到 git）
├── .env.example            # 示例配置（提交到 git）
├── .env.test               # 测试环境
├── .env.production         # 生产环境（不提交）
├── .gitignore              # 忽略 .env 文件
└── src/
    └── config.py
```

## 7.2 `.gitignore` 配置

```python
# 环境变量文件
.env
.env.local
.env.*.local

# 但保留示例文件
!.env.example

```

## 7.3 配置示例文件

```python
# .env.example - 提交到版本控制
DATABASE_URL=postgresql://localhost:5432/dbname
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
API_KEY=your_api_key_here
DEBUG=True
PORT=8000
```

## 7.4 推荐的加载模式

```python
# 推荐做法：在项目入口文件顶部加载
# main.py 或 __init__.py

from dotenv import load_dotenv
import os

# 尽早加载
load_dotenv()

# 或者使用 Python 3.11+ 的 tomllib 自动加载
```

## 7.5 类型转换辅助函数

```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_bool(key: str, default: bool = False) -> bool:
    """获取布尔值"""
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ('true', '1', 'yes', 'on')

def get_int(key: str, default: int = 0) -> int:
    """获取整数"""
    try:
        return int(os.getenv(key, default))
    except ValueError:
        return default

def get_list(key: str, separator: str = ',') -> list:
    """获取列表"""
    value = os.getenv(key, '')
    return [item.strip() for item in value.split(separator) if item.strip()]

# 使用
debug = get_bool('DEBUG', False)
port = get_int('PORT', 8000)
allowed_hosts = get_list('ALLOWED_HOSTS')
```

# 8. 常见问题与解决方案

## 8.1 环境变量未加载

```python
# 问题：os.getenv() 返回 None

# 解决方案 1：检查文件路径
from dotenv import find_dotenv, load_dotenv
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path)
else:
    print("未找到 .env 文件")

# 解决方案 2：指定绝对路径
import os
from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# 解决方案 3：使用 verbose 模式
load_dotenv(verbose=True)

```

## 8.2 特殊字符处理

```python
# 问题：密码或值中包含特殊字符

# .env 文件
# 使用引号包裹
PASSWORD="p@ss!#$%^&*()"
URL="https://api.example.com?key=value&foo=bar"

# Python 中正确获取
import os
password = os.getenv('PASSWORD')  # 自动去除引号

```

## 8.3 与 `Docker` 集成

```python
# docker-compose.yml
version: '3'
services:
  web:
    build: .
    env_file:
      - .env
    environment:
      - NODE_ENV=production

```

```python
# Dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

# 9. 总结

**`python-dotenv` 核心函数对照表：**

| 函数              | 作用                        | 返回值        |
| ----------------- | --------------------------- | ------------- |
| `load_dotenv()`   | 加载环境变量到 `os.environ` | `True/False`  |
| `dotenv_values()` | 返回配置字典                | `OrderedDict` |
| `set_key()`       | 设置键值                    | `(bool, key)` |
| `unset_key()`     | 删除键值                    | `(bool, key)` |
| `get_key()`       | 获取单个值                  | `str 或 None` |
| `find_dotenv()`   | 查找文件路径                | `str`         |

**适用场景：**

- ✅ 敏感配置管理（密码、密钥）
- ✅ 多环境配置切换
- ✅ 本地开发环境配置
- ✅ 第三方服务密钥管理
- ❌ 频繁变化的运行时配置
- ❌ 超大规模配置管理（考虑使用配置中心）
