---
aliases:
  - course of study
  - course
tags:
  - tutorial
  - computer-science
category: knowledge
datetime: " 2026-08-15 15:08:33 周六"
author: wephiles
rating: "0"
---
<h1 style="text-align: center;">logging</h1>

---

`logging` 是 Python 标准库的日志模块，相比 `print`，它支持：

- 多级别日志：DEBUG / INFO / WARNING / ERROR / CRITICAL
- 多输出目标：控制台、文件、网络、邮件等
- 统一格式：时间、模块、行号、进程、线程等
- 按大小/时间自动切割日志文件
- 日志过滤、传播、上下文信息注入等

# 1. 设计思路

`logging` 的核心由 4 个组件组成：

| 组件            | 作用                                 |
| :-------------- | :----------------------------------- |
| **`Logger`**    | 日志入口，负责产生日志记录           |
| **`Handler`**   | 输出目标，比如控制台、文件、`Socket` |
| **`Formatter`** | 定义日志字符串格式                   |
| **`Filter`**    | 对日志做进一步过滤                   |

它们的关系:

```python
Logger.debug()
    -> 生成 LogRecord
    -> Logger 判断级别
    -> 经过 Logger Filter
    -> 交给当前 Logger 的 Handler
    -> 如果 propagate=True，继续向父 Logger 传播
    -> 每个 Handler 再次判断级别
    -> Handler Filter
    -> Formatter 格式化
    -> 输出
```

Logger 名称是层级结构：

```python
logging.getLogger("app")
logging.getLogger("app.api")
logging.getLogger("app.api.user")
```

`app.api.user` 的父 Logger 是 `app.api`，再上层是 `app`，最顶层是 `root Logger`。

日志级别数值：

| 级别     | 数值 |
| :------- | :--- |
| NOTSET   | 0    |
| DEBUG    | 10   |
| INFO     | 20   |
| WARNING  | 30   |
| ERROR    | 40   |
| CRITICAL | 50   |

# 2. 基本使用方法

最简单的用法是使用 `basicConfig` 配置 `root Logger`：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

logger.debug("这是 debug 日志，默认不会输出")
logger.info("这是 info 日志")
logger.warning("这是 warning 日志")
logger.error("这是 error 日志")
logger.critical("这是 critical 日志")
```

输出:

```python
2026-08-15 12:00:00,123 - __main__ - INFO - 这是 info 日志
2026-08-15 12:00:00,124 - __main__ - WARNING - 这是 warning 日志
...
```

---

`basicConfig` 参数详解:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,                    # 日志级别
    filename='app.log',                     # 日志文件名（不指定则输出到控制台）
    filemode='a',                           # 文件模式：'a'追加, 'w'覆盖
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 格式
    datefmt='%Y-%m-%d %H:%M:%S',            # 时间格式
    style='%',                              # 格式化风格：'%' 或 '{' 或 '$'
    handlers=None,                          # 自定义处理器
    force=False,                            # 强制重新配置
)

```

注意：

- `basicConfig` 配置的是 `root Logger`。
- 只有第一次调用 `basicConfig` 会生效，后续调用会被忽略。
- 建议每个模块使用 `logging.getLogger(__name__)`，这样日志能按模块名过滤。

# 3. 进阶用法

## 3.1 创建自定义 Logger

```python
import logging

# 创建 logger
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# 创建控制台 handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建文件 handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# 创建 formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 给 handler 设置 formatter
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 给 logger 添加 handler
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 使用
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')

```

## 3.2 使用字典配置(推荐用于大型项目)

```python
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # 不禁用已存在的 logger
    
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        },
    },
    
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'app.log',
            'maxBytes': 1024*1024,  # 1MB
            'backupCount': 5,
            'encoding': 'utf-8'
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'error.log',
            'encoding': 'utf-8'
        }
    },
    
    'loggers': {
        'my_app': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False  # 不传播给父 logger
        },
        'my_app.module1': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        }
    },
    
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_app')

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')

```

## 3.3 使用配置文件

创建 `logging.conf` 文件:

```python
[loggers]
keys=root,sampleLogger

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=sampleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_sampleLogger]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=sampleLogger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=sampleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=sampleFormatter
args=('app.log', 'a')

[formatter_sampleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S

```

`Python` 代码:

```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('sampleLogger')

logger.debug('debug message')
logger.info('info message')

```

# 4. 不同层级日志输出到不同位置

## 4.1 不同级别输出到不同的文件

```python
import logging
import logging.handlers


class LevelFilter:
    """自定义级别过滤器"""
    def __init__(self, level):
        self.level = level
    
    def filter(self, record):
        return record.levelno == self.level


def setup_logger():
    """配置日志系统：不同级别输出到不同文件"""
    
    logger = logging.getLogger('my_app')
    logger.setLevel(logging.DEBUG)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    # 控制台处理器 - INFO及以上
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # DEBUG日志文件 - 只记录DEBUG
    debug_handler = logging.FileHandler('debug.log')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.addFilter(LevelFilter(logging.DEBUG))
    debug_handler.setFormatter(formatter)
    
    # INFO日志文件 - 只记录INFO
    info_handler = logging.FileHandler('info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(LevelFilter(logging.INFO))
    info_handler.setFormatter(formatter)
    
    # WARNING日志文件 - 只记录WARNING
    warning_handler = logging.FileHandler('warning.log')
    warning_handler.setLevel(logging.WARNING)
    warning_handler.addFilter(LevelFilter(logging.WARNING))
    warning_handler.setFormatter(formatter)
    
    # ERROR日志文件 - ERROR及以上
    error_handler = logging.FileHandler('error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # 添加所有处理器
    logger.addHandler(console_handler)
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)
    
    return logger


# 使用示例
logger = setup_logger()

logger.debug('这是调试信息，只写入debug.log')
logger.info('这是信息日志，显示在控制台和info.log')
logger.warning('这是警告日志，显示在控制台和warning.log')
logger.error('这是错误日志，显示在控制台和error.log')
logger.critical('这是严重错误，显示在控制台和error.log')

```

## 4.2 按模块划分日志输出

```python
import logging
import logging.config


def setup_module_logging():
    """按模块划分：不同模块的日志输出到不同文件"""
    
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            # 模块A的日志文件
            'module_a_file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': 'module_a.log',
                'encoding': 'utf-8'
            },
            # 模块B的日志文件
            'module_b_file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': 'module_b.log',
                'encoding': 'utf-8'
            },
            # 业务逻辑日志文件
            'business_file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'filename': 'business.log',
                'encoding': 'utf-8'
            }
        },
        
        'loggers': {
            # 模块A：控制台 + 专属文件
            'my_app.module_a': {
                'level': 'DEBUG',
                'handlers': ['console', 'module_a_file'],
                'propagate': False
            },
            # 模块B：控制台 + 专属文件
            'my_app.module_b': {
                'level': 'DEBUG',
                'handlers': ['console', 'module_b_file'],
                'propagate': False
            },
            # 业务层：只写文件，不输出控制台
            'my_app.business': {
                'level': 'INFO',
                'handlers': ['business_file'],
                'propagate': False
            }
        }
    }
    
    logging.config.dictConfig(config)


# 在模块A中
# module_a.py
logger_a = logging.getLogger('my_app.module_a')
logger_a.info('模块A的信息')
logger_a.debug('模块A的调试信息')

# 在模块B中
# module_b.py
logger_b = logging.getLogger('my_app.module_b')
logger_b.info('模块B的信息')

# 在业务逻辑中
# business.py
logger_business = logging.getLogger('my_app.business')
logger_business.info('业务逻辑执行')

```

## 4.3 控制台显示 `INFO`, 文件记录 `DEBUG`

```python
import logging
import logging.handlers


def setup_dual_output_logger():
    """控制台只显示INFO及以上，文件记录DEBUG及以上"""
    
    logger = logging.getLogger('my_app')
    logger.setLevel(logging.DEBUG)
    
    # 详细格式 - 用于文件
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - '
        '%(filename)s:%(funcName)s:%(lineno)d - %(message)s'
    )
    
    # 简洁格式 - 用于控制台
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # 控制台处理器 - INFO及以上
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # 文件处理器 - DEBUG及以上（记录更详细）
    file_handler = logging.handlers.RotatingFileHandler(
        'app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# 使用
logger = setup_dual_output_logger()

logger.debug('这条只在文件中')
logger.info('这条在控制台和文件中')
logger.warning('警告信息')

```

# 5. 日志文件轮转(`Rotating` 和 `Timed`)

## 5.1 按文件大小轮转

```python
import logging
import logging.handlers
import os


def setup_rotating_logger():
    """按文件大小轮转日志"""
    
    logger = logging.getLogger('rotating_app')
    logger.setLevel(logging.DEBUG)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 按大小轮转的文件处理器
    # maxBytes: 单个日志文件最大字节数
    # backupCount: 保留的备份文件数量
    rotating_handler = logging.handlers.RotatingFileHandler(
        filename='app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,          # 保留5个备份
        encoding='utf-8',
        mode='a'                # 追加模式
    )
    rotating_handler.setLevel(logging.DEBUG)
    rotating_handler.setFormatter(formatter)
    
    logger.addHandler(rotating_handler)
    
    return logger


# 测试：写入大量日志触发轮转
logger = setup_rotating_logger()

# 写入大量数据触发轮转
for i in range(10000):
    logger.info(f'这是第 {i} 条日志消息，用于测试日志轮转功能')


# 查看生成的文件
# app.log        - 当前日志文件
# app.log.1      - 第1个备份
# app.log.2      - 第2个备份
# ...
# app.log.5      - 第5个备份

```

## 5.2 按时间轮转

```python
import logging
import logging.handlers


def setup_timed_rotating_logger():
    """按时间轮转日志"""
    
    logger = logging.getLogger('timed_app')
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 按时间轮转的文件处理器
    # when: 轮转时间间隔类型
    #   'S' - 秒
    #   'M' - 分钟
    #   'H' - 小时
    #   'D' - 天
    #   'W0'-'W6' - 周几（W0=周一）
    #   'midnight' - 每天午夜
    # interval: 间隔数量
    # backupCount: 保留的备份数量
    # encoding: 文件编码
    
    timed_handler = logging.handlers.TimedRotatingFileHandler(
        filename='app.log',
        when='midnight',       # 每天午夜轮转
        interval=1,            # 每1天
        backupCount=7,         # 保留7天
        encoding='utf-8',
        delay=False,           # 立即打开文件
        utc=False              # 使用本地时间
    )
    timed_handler.setLevel(logging.DEBUG)
    timed_handler.setFormatter(formatter)
    
    # 自定义文件名格式
    # 默认: app.log.2023-12-01
    timed_handler.namer = lambda name: name.replace('.log', '') + '.log'
    
    logger.addHandler(timed_handler)
    
    return logger


# 每小时轮转示例
def setup_hourly_rotating_logger():
    """每小时轮转一次"""
    logger = logging.getLogger('hourly_app')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    handler = logging.handlers.TimedRotatingFileHandler(
        filename='hourly.log',
        when='H',              # 小时
        interval=1,            # 每1小时
        backupCount=24,        # 保留24小时
        encoding='utf-8'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


# 每周轮转示例
def setup_weekly_rotating_logger():
    """每周一轮转"""
    logger = logging.getLogger('weekly_app')
    
    handler = logging.handlers.TimedRotatingFileHandler(
        filename='weekly.log',
        when='W0',             # W0=周一, W1=周二, ...
        interval=1,
        backupCount=4,         # 保留4周
        encoding='utf-8'
    )
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger

```

## 5.3 组合使用: 大小 + 时间 轮转

```python
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class MixedRotatingHandler:
    """组合大小和时间轮转（需要自定义实现）"""
    
    def __init__(self, filename, maxBytes, backupCount, when='midnight'):
        # 使用 RotatingFileHandler 处理大小限制
        self.size_handler = RotatingFileHandler(
            filename,
            maxBytes=maxBytes,
            backupCount=backupCount
        )


def setup_mixed_logger():
    """推荐方案：使用第三方库或分层设计"""
    
    logger = logging.getLogger('mixed_app')
    logger.setLevel(logging.DEBUG)
    
    # 方案：同时使用两个handler
    # 1. 按大小轮转 - 用于开发环境
    size_handler = logging.handlers.RotatingFileHandler(
        'dev.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    
    # 2. 按时间轮转 - 用于生产环境
    time_handler = logging.handlers.TimedRotatingFileHandler(
        'prod.log',
        when='midnight',
        backupCount=30
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    size_handler.setFormatter(formatter)
    time_handler.setFormatter(formatter)
    
    logger.addHandler(size_handler)
    logger.addHandler(time_handler)
    
    return logger

```

# 6. 日志格式变量

## 6.1 所有可用的 `Format` 变量

```python
import logging
import sys

# 打印所有可用的 LogRecord 属性
def print_all_logrecord_attrs():
    """展示 LogRecord 的所有属性"""
    logger = logging.getLogger('demo')
    handler = logging.StreamHandler()
    
    # 创建一个临时的 formatter 获取属性列表
    record = logging.LogRecord(
        name='demo',
        level=logging.INFO,
        pathname='test.py',
        lineno=1,
        msg='test',
        args=(),
        exc_info=None
    )
    
    print("LogRecord 所有属性:")
    print("-" * 60)
    
    attrs = [
        ('asctime', '日志时间的字符串格式'),
        ('created', '日志创建时间（时间戳）'),
        ('filename', '文件名（不含路径）'),
        ('funcName', '函数名'),
        ('levelname', '日志级别名称'),
        ('levelno', '日志级别数字'),
        ('lineno', '调用日志的行号'),
        ('module', '模块名（不含后缀）'),
        ('msecs', '毫秒部分'),
        ('message', '日志消息'),
        ('msg', '原始日志消息模板'),
        ('name', 'Logger名称'),
        ('pathname', '完整文件路径'),
        ('process', '进程ID'),
        ('processName', '进程名'),
        ('relativeCreated', '相对时间（毫秒，自模块加载）'),
        ('stack_info', '堆栈信息'),
        ('thread', '线程ID'),
        ('threadName', '线程名'),
        ('exc_info', '异常信息元组'),
        ('exc_text', '异常文本'),
    ]
    
    for attr, desc in attrs:
        print(f'{attr:20s} - {desc}')


print_all_logrecord_attrs()

```

## 6.2 常用格式组合

```python
import logging


def demo_format_patterns():
    """展示常用的日志格式"""
    
    formats = {
        'simple': '%(message)s',
        
        'standard': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        
        'detailed': '%(asctime)s - %(name)s - %(levelname)s - '
                    '%(filename)s:%(funcName)s:%(lineno)d - %(message)s',
        
        'with_process_thread': '%(asctime)s - %(name)s - %(levelname)s - '
                               '[%(processName)s:%(threadName)s] - %(message)s',
        
        'json_like': '{"time": "%(asctime)s", "level": "%(levelname)s", '
                     '"logger": "%(name)s", "message": "%(message)s", '
                     '"file": "%(filename)s", "line": %(lineno)d}',
        
        'syslog_style': '%(name)s[%(process)d]: %(levelname)s - %(message)s',
        
        'minimal': '%(levelname)s: %(message)s',
        
        'debug_focused': '[%(filename)20s:%(lineno)4d] %(levelname)-8s %(message)s'
    }
    
    logger = logging.getLogger('format_demo')
    logger.setLevel(logging.DEBUG)
    
    print("\n" + "="*70)
    print("不同格式的日志输出示例：")
    print("="*70 + "\n")
    
    for name, fmt in formats.items():
        print(f"\n--- {name} 格式 ---")
        print(f"格式字符串: {fmt}")
        print(f"输出效果:")
        
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S'))
        
        # 清除之前的 handlers
        logger.handlers.clear()
        logger.addHandler(handler)
        
        logger.info('这是一条信息日志')


demo_format_patterns()

```

## 6.3 自定义 `Format` 字段

```python
import logging
import os


class ContextFilter(logging.Filter):
    """添加自定义字段到日志记录"""
    
    def __init__(self, app_name, environment):
        super().__init__()
        self.app_name = app_name
        self.environment = environment
    
    def filter(self, record):
        # 添加自定义字段
        record.app_name = self.app_name
        record.environment = self.environment
        record.user = os.environ.get('USER', 'unknown')
        return True


def setup_custom_format_logger():
    """使用自定义字段的日志格式"""
    
    logger = logging.getLogger('custom_app')
    logger.setLevel(logging.DEBUG)
    
    # 创建自定义格式
    # 注意：自定义字段需要在 Formatter 中使用，需要先通过 Filter 注入
    formatter = logging.Formatter(
        '%(asctime)s - [%(app_name)s] - [%(environment)s] - '
        '%(levelname)s - [%(user)s] - %(message)s'
    )
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    # 添加自定义字段过滤器
    handler.addFilter(ContextFilter(
        app_name='MyApp',
        environment='production'
    ))
    
    logger.addHandler(handler)
    
    return logger


# 使用
logger = setup_custom_format_logger()
logger.info('用户登录成功')
logger.error('数据库连接失败')

```

# 7. 标准日志写法

## 7.1 标准项目日志配置

```python
"""
标准日志配置模块
文件名: logging_config.py
"""
import logging
import logging.handlers
import os
from pathlib import Path


class AppLogger:
    """应用日志管理器"""
    
    _initialized = False
    
    @classmethod
    def setup(
        cls,
        app_name: str = 'app',
        log_dir: str = 'logs',
        level: str = 'INFO',
        max_bytes: int = 10*1024*1024,  # 10MB
        backup_count: int = 5,
        console_output: bool = True,
        json_format: bool = False
    ):
        """
        配置应用日志系统
        
        Args:
            app_name: 应用名称，用于logger命名
            log_dir: 日志目录
            level: 日志级别
            max_bytes: 单文件最大字节数
            backup_count: 备份文件数量
            console_output: 是否输出到控制台
            json_format: 是否使用JSON格式
        """
        if cls._initialized:
            return
        
        # 创建日志目录
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # 获取根logger
        logger = logging.getLogger(app_name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # 格式化器
        if json_format:
            formatter = cls._get_json_formatter()
        else:
            formatter = cls._get_standard_formatter()
        
        # 文件处理器 - 所有日志
        all_logs_handler = logging.handlers.RotatingFileHandler(
            log_path / f'{app_name}.log',
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        all_logs_handler.setLevel(logging.DEBUG)
        all_logs_handler.setFormatter(formatter)
        logger.addHandler(all_logs_handler)
        
        # 错误日志单独文件
        error_handler = logging.handlers.RotatingFileHandler(
            log_path / f'{app_name}_error.log',
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
        
        # 控制台输出
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        cls._initialized = True
        
        return logger
    
    @staticmethod
    def _get_standard_formatter():
        """标准格式化器"""
        return logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | '
            '%(filename)s:%(lineno)d | %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    @staticmethod
    def _get_json_formatter():
        """JSON格式化器（用于日志收集系统）"""
        import json
        from datetime import datetime
        
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_obj = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'level': record.levelname,
                    'logger': record.name,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno,
                    'file': record.filename
                }
                
                # 添加异常信息
                if record.exc_info:
                    log_obj['exception'] = self.formatException(record.exc_info)
                
                # 添加额外字段
                if hasattr(record, 'extra_data'):
                    log_obj['extra'] = record.extra_data
                
                return json.dumps(log_obj)
        
        return JsonFormatter()
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """获取logger实例"""
        return logging.getLogger(name)


# 初始化函数
def init_logging(app_name: str = 'my_app', **kwargs):
    """初始化日志系统"""
    return AppLogger.setup(app_name=app_name, **kwargs)


def get_logger(name: str = None) -> logging.Logger:
    """获取logger"""
    if name:
        return logging.getLogger(name)
    return logging.getLogger()

```

## 7.2 业务代码中使用

```python
"""
业务模块使用示例
"""
import logging
from logging_config import init_logging, get_logger


# 初始化日志系统（通常在应用启动时调用）
init_logging(
    app_name='order_system',
    log_dir='logs',
    level='DEBUG',
    console_output=True
)


# 在各个模块中获取logger
logger = get_logger('order_system.order_service')


class OrderService:
    """订单服务"""
    
    def __init__(self):
        self.logger = logging.getLogger('order_system.order_service')
    
    def create_order(self, user_id: int, product_ids: list):
        """创建订单"""
        
        # 记录开始信息
        self.logger.info(
            f"开始创建订单",
            extra={
                'user_id': user_id,
                'product_count': len(product_ids)
            }
        )
        
        try:
            # 业务逻辑
            order_id = self._generate_order_id()
            
            # 记录关键步骤
            self.logger.debug(
                f"订单ID生成成功: {order_id}",
                extra={'order_id': order_id}
            )
            
            # 执行数据库操作
            self._save_order(order_id, user_id, product_ids)
            
            # 记录成功
            self.logger.info(
                f"订单创建成功",
                extra={
                    'order_id': order_id,
                    'user_id': user_id
                }
            )
            
            return order_id
            
        except ValueError as e:
            # 业务异常 - 使用 WARNING
            self.logger.warning(
                f"订单创建失败，参数错误: {e}",
                extra={'user_id': user_id},
                exc_info=True
            )
            raise
            
        except Exception as e:
            # 系统异常 - 使用 ERROR
            self.logger.error(
                f"订单创建异常",
                extra={
                    'user_id': user_id,
                    'error_type': type(e).__name__
                },
                exc_info=True
            )
            raise
    
    def _generate_order_id(self):
        return 'ORD123456'
    
    def _save_order(self, order_id, user_id, product_ids):
        pass


def process_payment_example():
    """支付处理示例 - 展示异常日志"""
    logger = get_logger('order_system.payment')
    
    try:
        # 模拟支付处理
        result = call_payment_api()
        logger.info(f"支付成功: {result}")
        
    except ConnectionError as e:
        logger.error(
            "支付接口连接失败",
            exc_info=True,  # 包含堆栈信息
            extra={'api_url': 'https://payment.example.com'}
        )
        raise
    
    except Exception as e:
        logger.exception("支付处理发生未知异常")  # 等同于 error + exc_info=True
        raise


def call_payment_api():
    raise ConnectionError("无法连接到支付服务器")


# 运行示例
if __name__ == '__main__':
    service = OrderService()
    
    # 正常流程
    service.create_order(user_id=1001, product_ids=[1, 2, 3])
    
    # 异常流程
    try:
        process_payment_example()
    except:
        pass

```

## 7.3 WEB 应用日志示例(`Flask/Django`)

```python
"""
Flask 应用日志配置示例
"""
import logging
import logging.handlers
from flask import Flask, request, g
import time
from functools import wraps


def setup_flask_logging(app: Flask):
    """配置 Flask 应用的日志"""
    
    # 创建日志目录
    import os
    os.makedirs('logs', exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | '
        '%(remote_addr)s | %(method)s %(path)s | %(message)s'
    )
    
    # 请求日志
    request_handler = logging.handlers.RotatingFileHandler(
        'logs/requests.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    request_handler.setFormatter(formatter)
    
    # 错误日志
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # 配置 logger
    logger = logging.getLogger('flask_app')
    logger.setLevel(logging.INFO)
    logger.addHandler(request_handler)
    logger.addHandler(error_handler)
    
    return logger


def request_logging_middleware(app):
    """请求日志中间件"""
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
        
        # 为日志格式添加请求信息
        old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.remote_addr = request.remote_addr or '-'
            record.method = request.method or '-'
            record.path = request.path or '-'
            return record
        
        logging.setLogRecordFactory(record_factory)
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            logger = logging.getLogger('flask_app')
            logger.info(
                f"请求完成",
                extra={
                    'status_code': response.status_code,
                    'duration_ms': round(duration * 1000, 2)
                }
            )
        
        return response


# 使用示例
def create_app():
    app = Flask(__name__)
    
    # 配置日志
    logger = setup_flask_logging(app)
    
    # 添加请求日志中间件
    request_logging_middleware(app)
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        logger = logging.getLogger('flask_app.user')
        logger.info("获取用户列表")
        
        # 业务逻辑
        users = ['user1', 'user2']
        
        logger.debug(f"返回用户: {users}")
        return {'users': users}
    
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        logger = logging.getLogger('flask_app.user')
        
        try:
            logger.info(f"查询用户: {user_id}")
            
            # 模拟业务逻辑
            if user_id > 100:
                raise ValueError("用户不存在")
            
            return {'user_id': user_id}
            
        except ValueError as e:
            logger.warning(f"用户查询失败: {e}")
            return {'error': str(e)}, 404
            
        except Exception as e:
            logger.exception(f"查询用户发生异常: user_id={user_id}")
            return {'error': '内部错误'}, 500
    
    return app


# 装饰器方式记录函数日志
def log_execution(func):
    """函数执行日志装饰器"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        
        func_name = func.__name__
        logger.debug(f"开始执行: {func_name}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"执行成功: {func_name}")
            return result
            
        except Exception as e:
            logger.error(
                f"执行失败: {func_name}",
                exc_info=True,
                extra={'args': str(args), 'kwargs': str(kwargs)}
            )
            raise
    
    return wrapper


# 使用装饰器
@log_execution
def calculate_total(items: list) -> float:
    """计算总价"""
    return sum(item['price'] for item in items)

```

## 7.4 多进程环境下日志配置

```python
"""
多进程环境日志配置
"""
import logging
import logging.handlers
import multiprocessing
from multiprocessing.queues import Queue
import time


class QueueHandler(logging.Handler):
    """队列处理器 - 用于多进程"""
    
    def __init__(self, log_queue: Queue):
        super().__init__()
        self.log_queue = log_queue
    
    def emit(self, record):
        try:
            self.log_queue.put_nowait(record)
        except Exception:
            self.handleError(record)


class QueueListener:
    """队列监听器 - 在单独进程中处理日志"""
    
    def __init__(self, log_queue: Queue, handlers: list):
        self.log_queue = log_queue
        self.handlers = handlers
        self._process = None
    
    def start(self):
        """启动监听进程"""
        self._process = multiprocessing.Process(target=self._listen)
        self._process.start()
    
    def stop(self):
        """停止监听进程"""
        self.log_queue.put(None)  # 发送停止信号
        self._process.join()
    
    def _listen(self):
        """监听队列并处理日志"""
        while True:
            record = self.log_queue.get()
            if record is None:  # 停止信号
                break
            
            for handler in self.handlers:
                handler.handle(record)


def setup_multiprocess_logging():
    """多进程日志配置"""
    
    # 创建队列
    log_queue = multiprocessing.Queue()
    
    # 文件处理器
    file_handler = logging.handlers.RotatingFileHandler(
        'multiprocess.log',
        maxBytes=5*1024*1024,
        backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(processName)s - %(levelname)s - %(message)s'
    ))
    
    # 创建并启动监听器
    listener = QueueListener(log_queue, [file_handler])
    listener.start()
    
    # 配置根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(QueueHandler(log_queue))
    
    return listener


def worker_process(worker_id: int, log_queue: Queue):
    """工作进程"""
    # 配置当前进程的 logger
    logger = logging.getLogger(f'worker_{worker_id}')
    logger.handlers = []
    logger.addHandler(QueueHandler(log_queue))
    logger.setLevel(logging.INFO)
    
    # 模拟工作
    for i in range(5):
        logger.info(f"工作进程 {worker_id} 正在处理任务 {i}")
        time.sleep(0.1)
    
    logger.info(f"工作进程 {worker_id} 完成")


def multiprocess_example():
    """多进程示例"""
    
    log_queue = multiprocessing.Queue()
    
    # 设置监听器
    listener = setup_multiprocess_logging()
    
    # 创建多个进程
    processes = []
    for i in range(3):
        p = multiprocessing.Process(
            target=worker_process,
            args=(i, log_queue)
        )
        processes.append(p)
        p.start()
    
    # 等待所有进程完成
    for p in processes:
        p.join()
    
    # 停止监听器
    listener.stop()


if __name__ == '__main__':
    # Windows 多进程需要在 main 中执行
    multiprocessing.freeze_support()
    multiprocess_example()

```

# 8. 常见坑和注意事项

## 8.1 Handler 重复添加问题

```python
import logging


def pitfall_duplicate_handlers():
    """坑：Handler 重复添加"""
    
    # 错误示例
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    
    # 多次调用会导致日志重复输出
    for i in range(3):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
    
    # 输出会重复3次！
    logger.info("这条消息会输出3次")
    
    # 正确做法1：检查是否已有 handler
    logger2 = logging.getLogger('test2')
    logger2.setLevel(logging.DEBUG)
    
    if not logger2.handlers:  # 只有在没有 handlers 时才添加
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger2.addHandler(handler)
    
    logger2.info("这条只输出一次")
    
    # 正确做法2：清除现有 handlers
    logger3 = logging.getLogger('test3')
    logger3.setLevel(logging.DEBUG)
    logger3.handlers.clear()  # 清除现有 handlers
    
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger3.addHandler(handler)
    
    logger3.info("这条也只输出一次")


pitfall_duplicate_handlers()

```

## 8.2 日志级别传播问题

```python
import logging


def pitfall_propagate():
    """坑：日志级别传播"""
    
    # 创建子 logger
    child_logger = logging.getLogger('parent.child')
    child_logger.setLevel(logging.DEBUG)
    
    # 创建父 logger
    parent_logger = logging.getLogger('parent')
    parent_logger.setLevel(logging.WARNING)
    
    # 添加 handler 到父 logger
    parent_handler = logging.StreamHandler()
    parent_handler.setFormatter(logging.Formatter('PARENT: %(message)s'))
    parent_logger.addHandler(parent_handler)
    
    # 问题：子 logger 的日志会传播到父 logger
    # 即使子 logger 设置为 DEBUG，由于父 logger 是 WARNING，
    # 通过父 logger 输出的日志只会是 WARNING 及以上
    
    child_logger.debug("这条不会输出（父logger是WARNING级别）")
    child_logger.warning("这条会输出（WARNING >= WARNING）")
    
    # 解决方案：设置 propagate=False
    child_logger.propagate = False
    child_handler = logging.StreamHandler()
    child_handler.setFormatter(logging.Formatter('CHILD: %(message)s'))
    child_logger.addHandler(child_handler)
    
    child_logger.debug("现在这条会输出（不传播给父logger）")


pitfall_propagate()

```

## 8.3 getLogger() 的单例模式

```python
import logging


def pitfall_getlogger_singleton():
    """坑：getLogger 返回的是同一个对象"""
    
    # 多次调用 getLogger 相同名称，返回同一个对象
    logger1 = logging.getLogger('my_app')
    logger2 = logging.getLogger('my_app')
    
    print(f"logger1 is logger2: {logger1 is logger2}")  # True
    
    # 这意味着在一个地方添加 handler，所有使用该名称的地方都会有
    logger1.addHandler(logging.StreamHandler())
    print(f"logger2 handlers count: {len(logger2.handlers)}")  # 1
    
    # 正确用法：在统一的配置模块中配置一次
    # 在其他模块中只获取使用，不配置


pitfall_getlogger_singleton()

```

## 8.4 日志配置顺序问题

```python
import logging


def pitfall_config_order():
    """坑：basicConfig 必须在第一次日志输出前调用"""
    
    # 错误示例
    # logging.warning("先输出日志")  # 这会自动创建默认配置
    # logging.basicConfig(level=logging.DEBUG)  # 这句将无效！
    
    # 正确做法：先配置，后使用
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True  # Python 3.8+，强制重新配置
    )
    
    logging.debug("现在可以输出 DEBUG 了")


def pitfall_root_logger_level():
    """坑：root logger 默认级别是 WARNING"""
    
    # Root logger 默认级别是 WARNING
    # 即使添加了 DEBUG 级别的 handler，也不会输出 DEBUG 日志
    
    logger = logging.getLogger()  # 获取 root logger
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)  # Handler 设置为 DEBUG
    
    logger.addHandler(handler)
    
    # 但 logger 的级别还是默认的 WARNING
    logger.debug("这条不会输出")  # 因为 logger 的级别是 WARNING
    logger.warning("这条会输出")
    
    # 解决方案：同时设置 logger 和 handler 的级别
    logger.setLevel(logging.DEBUG)
    logger.debug("现在可以输出了")


pitfall_config_order()
pitfall_root_logger_level()

```

## 8.5 异常信息记录方式

```python
import logging


def pitfall_exception_logging():
    """正确记录异常的方式"""
    
    logger = logging.getLogger('exception_demo')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.handlers = [handler]
    
    try:
        result = 1 / 0
    except ZeroDivisionError:
        # 方式1：使用 exc_info=True
        logger.error("发生除零错误", exc_info=True)
        
        # 方式2：使用 exception() 方法（自动包含 exc_info=True）
        logger.exception("发生除零错误（使用exception方法）")
        
        # 方式3：手动传递异常对象
        import sys
        logger.error("发生除零错误", exc_info=sys.exc_info())


pitfall_exception_logging()

```

## 8.6 性能问题: 字符串格式化

```python
import logging
import time


def pitfall_string_formatting():
    """性能坑：字符串格式化"""
    
    logger = logging.getLogger('performance')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    
    expensive_data = "data" * 1000
    
    # 性能差：无论是否输出，都会执行字符串格式化
    start = time.time()
    for i in range(100000):
        logger.debug(f"Processing: {expensive_data} {i}")
    print(f"使用 f-string: {time.time() - start:.3f}s")
    
    # 性能好：使用 % 格式化，只有需要输出时才格式化
    start = time.time()
    for i in range(100000):
        logger.debug("Processing: %s %d", expensive_data, i)
    print(f"使用 % 格式化: {time.time() - start:.3f}s")
    
    # 或者使用懒加载
    start = time.time()
    if logger.isEnabledFor(logging.DEBUG):
        for i in range(100000):
            logger.debug(f"Processing: {expensive_data} {i}")
    print(f"使用懒加载: {time.time() - start:.3f}s")


pitfall_string_formatting()

```

## 8.7 编码问题

```python
import logging


def pitfall_encoding():
    """编码问题：Windows 控制台中文乱码"""
    
    # 方案1：文件 Handler 指定编码
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    
    # 方案2：控制台 Handler 处理编码
    import sys
    import io
    
    # Windows 控制台可能需要这个
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding='utf-8',
            errors='replace'
        )
    
    # 方案3：使用配置
    logging.basicConfig(
        filename='app.log',
        encoding='utf-8',  # Python 3.9+
        format='%(asctime)s - %(message)s'
    )
    
    logger = logging.getLogger('encoding_test')
    logger.info("测试中文日志 - 中文字符")
    logger.info("Testing English - ASCII characters")


pitfall_encoding()

```

# 9. 完整的企业级日志配置模板

```python
"""
企业级日志配置模板
可以直接复制使用
"""
import logging
import logging.config
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime
import json


class LoggingConfig:
    """日志配置类"""
    
    @staticmethod
    def get_default_config(
        app_name: str = 'app',
        log_dir: str = 'logs',
        console_level: str = 'INFO',
        file_level: str = 'DEBUG',
        max_bytes: int = 10*1024*1024,  # 10MB
        backup_count: int = 10,
        json_format: bool = False
    ) -> dict:
        """
        获取默认日志配置
        
        Args:
            app_name: 应用名称
            log_dir: 日志目录
            console_level: 控制台日志级别
            file_level: 文件日志级别
            max_bytes: 单文件最大字节数
            backup_count: 备份文件数量
            json_format: 是否使用JSON格式
        """
        
        # 确保日志目录存在
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        if json_format:
            standard_format = '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'
            detailed_format = '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","file":"%(filename)s","line":%(lineno)d,"func":"%(funcName)s","message":"%(message)s"}'
        else:
            standard_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
            detailed_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d:%(funcName)s | %(message)s'
        
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            
            'formatters': {
                'standard': {
                    'format': standard_format,
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'detailed': {
                    'format': detailed_format,
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                }
            },
            
            'handlers': {
                # 控制台
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': console_level,
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                
                # 所有日志文件
                'all_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': file_level,
                    'formatter': 'detailed',
                    'filename': f'{log_dir}/{app_name}.log',
                    'maxBytes': max_bytes,
                    'backupCount': backup_count,
                    'encoding': 'utf-8'
                },
                
                # 错误日志文件
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                    'filename': f'{log_dir}/{app_name}_error.log',
                    'maxBytes': max_bytes,
                    'backupCount': backup_count,
                    'encoding': 'utf-8'
                },
                
                # 按天轮转的日志（长期保存）
                'daily_file': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'detailed',
                    'filename': f'{log_dir}/{app_name}_daily.log',
                    'when': 'midnight',
                    'backupCount': 30,  # 保留30天
                    'encoding': 'utf-8'
                }
            },
            
            'loggers': {
                # 应用主 logger
                app_name: {
                    'level': 'DEBUG',
                    'handlers': ['console', 'all_file', 'error_file', 'daily_file'],
                    'propagate': False
                },
                
                # 第三方库日志（减少干扰）
                'urllib3': {
                    'level': 'WARNING',
                    'propagate': True
                },
                'requests': {
                    'level': 'WARNING',
                    'propagate': True
                },
                'werkzeug': {
                    'level': 'WARNING',
                    'propagate': True
                }
            },
            
            # Root logger
            'root': {
                'level': 'WARNING',
                'handlers': ['console']
            }
        }
        
        return config
    
    @staticmethod
    def setup(config: dict = None, **kwargs):
        """设置日志配置"""
        if config is None:
            config = LoggingConfig.get_default_config(**kwargs)
        
        logging.config.dictConfig(config)
        return logging.getLogger(kwargs.get('app_name', 'app'))


# 使用示例
def example_usage():
    """企业级配置使用示例"""
    
    # 方式1：使用默认配置
    logger = LoggingConfig.setup(
        app_name='my_enterprise_app',
        log_dir='logs',
        console_level='INFO',
        file_level='DEBUG'
    )
    
    # 方式2：自定义配置
    custom_config = LoggingConfig.get_default_config(
        app_name='custom_app',
        json_format=True  # JSON 格式，方便日志收集
    )
    logger = LoggingConfig.setup(custom_config)
    
    # 在各个模块中使用
    # module1.py
    logger = logging.getLogger('my_enterprise_app.module1')
    logger.debug("模块1的调试信息")
    
    # module2.py  
    logger = logging.getLogger('my_enterprise_app.module2')
    logger.info("模块2的信息")
    
    # business.py
    logger = logging.getLogger('my_enterprise_app.business')
    
    try:
        # 业务逻辑
        process_order(123)
        logger.info("订单处理成功", extra={'order_id': 123})
    except Exception as e:
        logger.exception("订单处理失败")
        raise


def process_order(order_id: int):
    """模拟业务函数"""
    pass


if __name__ == '__main__':
    example_usage()
    
    logger = logging.getLogger('my_enterprise_app')
    
    print("\n" + "="*70)
    print("日志输出示例：")
    print("="*70 + "\n")
    
    logger.debug("调试信息 - 只在文件中")
    logger.info("普通信息 - 控制台和文件都有")
    logger.warning("警告信息")
    logger.error("错误信息 - 同时记录到 error.log")
    
    try:
        1 / 0
    except:
        logger.exception("捕获到异常")
    
    print("\n" + "="*70)
    print("日志文件位置：")
    print("  - logs/my_enterprise_app.log      (所有日志)")
    print("  - logs/my_enterprise_app_error.log (错误日志)")
    print("  - logs/my_enterprise_app_daily.log (按天轮转)")
    print("="*70)

```

# 10. 总结

推荐日志规范:

| 项目         | 建议                                                         |
| ------------ | ------------------------------------------------------------ |
| **日志级别** | DEBUG: 详细调试信息 INFO: 关键业务节点 WARNING: 潜在问题 ERROR: 需要关注的错误 CRITICAL: 严重错误 |
| **日志内容** | 包含足够的上下文信息（用户ID、请求ID、订单ID等）             |
| **日志格式** | 时间 + 级别 + Logger名 + 文件位置 + 消息 + 上下文            |
| **异常日志** | 使用 `logger.exception()` 或 `exc_info=True`                 |
| **敏感信息** | 不要记录密码、token、完整信用卡号等敏感信息                  |
| **性能考虑** | 使用 `%s` 格式化而非 f-string，避免不必要的字符串拼接        |
| **日志轮转** | 生产环境必须配置日志轮转，避免磁盘写满                       |

常用命令速查:

```python
# 快速配置
logging.basicConfig(level=logging.INFO, filename='app.log')

# 获取 logger
logger = logging.getLogger(__name__)  # 使用模块名

# 记录日志
logger.debug("调试信息")
logger.info("信息")
logger.warning("警告")
logger.error("错误")
logger.exception("异常")  # 自动包含堆栈

# 记录额外信息
logger.info("用户登录", extra={'user_id': 123, 'ip': '1.2.3.4'})

# 检查日志级别是否启用（性能优化）
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"复杂计算结果: {expensive_function()}")

```

# 11. 工程中如何使用 logging

目录层级结构:

```python
exercise/
├─ main.py                    # 入口文件，集中配置日志
├─ logs/                      # 日志文件目录（自动创建）
│  ├─ main.log               # 主日志文件（所有模块）
│  ├─ api.log                # API模块日志
│  └─ utils.log              # Utils模块日志
└─ src/
   └─ exercise/
       ├─ api/
       │  ├─ __init__.py
       │  ├─ user.py         # 用户API
       │  └─ part.py         # 零件API
       └─ utils/
          ├─ __init__.py
          ├─ file_util.py    # 文件工具
          └─ op_util.py      # 操作工具
```

`main.py` -- 项目入口，集中配置日志

```python
"""
main.py - 项目入口文件
负责集中配置所有模块的日志设置
"""

import logging
import logging.config
import os
from datetime import datetime


def setup_logging():
    """集中配置所有模块的日志设置"""
    
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 日志配置字典
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,  # 不禁用已存在的logger
        
        # 日志格式配置
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        
        # 处理器配置（控制台+文件）
        'handlers': {
            # 控制台处理器
            'console_handler': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            
            # 主日志文件处理器（记录所有日志）
            'main_file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'main.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf-8'
            },
            
            # API模块日志文件处理器
            'api_file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'api.log'),
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf-8'
            },
            
            # Utils模块日志文件处理器
            'utils_file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'utils.log'),
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf-8'
            }
        },
        
        # 日志记录器配置
        'loggers': {
            # API模块的logger
            'exercise.api': {
                'level': 'DEBUG',
                'handlers': ['console_handler', 'api_file_handler', 'main_file_handler'],
                'propagate': False  # 不向上传播，避免重复打印
            },
            'exercise.api.user': {
                'level': 'DEBUG',
                'handlers': ['console_handler', 'api_file_handler'],
                'propagate': False
            },
            'exercise.api.part': {
                'level': 'DEBUG',
                'handlers': ['console_handler', 'api_file_handler'],
                'propagate': False
            },
            
            # Utils模块的logger
            'exercise.utils': {
                'level': 'DEBUG',
                'handlers': ['console_handler', 'utils_file_handler', 'main_file_handler'],
                'propagate': False
            },
            'exercise.utils.file_util': {
                'level': 'DEBUG',
                'handlers': ['console_handler', 'utils_file_handler'],
                'propagate': False
            },
            'exercise.utils.op_util': {
                'level': 'DEBUG',
                'handlers': ['console_handler', 'utils_file_handler'],
                'propagate': False
            }
        },
        
        # 根日志记录器配置
        'root': {
            'level': 'INFO',
            'handlers': ['console_handler', 'main_file_handler']
        }
    }
    
    # 应用日志配置
    logging.config.dictConfig(LOGGING_CONFIG)
    
    return logging.getLogger(__name__)


# ==================== 主程序入口 ====================
if __name__ == '__main__':
    # 配置日志
    logger = setup_logging()
    
    # 记录程序启动日志
    logger.info("=" * 60)
    logger.info("程序启动")
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 导入各个模块进行测试
        from src.exercise.api import user, part
        from src.exercise.utils import file_util, op_util
        
        # 调用各模块功能
        logger.info("开始调用各模块功能...")
        
        # 测试API模块
        user.get_user_info(1001)
        part.get_part_detail("PART-001")
        
        # 测试Utils模块
        file_util.read_file("/tmp/test.txt")
        op_util.execute_command("ls -la")
        
        logger.info("所有模块调用完成")
        
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("=" * 60)
        logger.info("程序结束")
        logger.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)

```

`src/exercise/api/user.py`

```python
"""
user.py - 用户API模块
"""

import logging

# 获取当前模块的logger
logger = logging.getLogger(__name__)


def get_user_info(user_id):
    """获取用户信息"""
    logger.info(f"开始获取用户信息, user_id={user_id}")
    
    try:
        # 模拟业务逻辑
        logger.debug(f"查询数据库: SELECT * FROM users WHERE id={user_id}")
        
        # 模拟返回数据
        user_data = {
            'id': user_id,
            'name': '张三',
            'email': 'zhangsan@example.com'
        }
        
        logger.info(f"成功获取用户信息: {user_data}")
        return user_data
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}", exc_info=True)
        raise


def create_user(user_data):
    """创建用户"""
    logger.info(f"开始创建用户, data={user_data}")
    
    try:
        # 模拟用户创建逻辑
        logger.debug("验证用户数据...")
        
        if not user_data.get('name'):
            logger.warning("用户名为空")
            raise ValueError("用户名不能为空")
        
        logger.info(f"用户创建成功: {user_data['name']}")
        return {'status': 'success', 'user_id': 1002}
        
    except Exception as e:
        logger.error(f"创建用户失败: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    # 模块单独测试时配置简单日志
    logging.basicConfig(level=logging.DEBUG)
    get_user_info(1001)

```

`src/exercise/api/part.py`

```python
"""
part.py - 零件API模块
"""
import logging

# 获取当前模块的logger
logger = logging.getLogger(__name__)


def get_part_detail(part_id):
    """获取零件详情"""
    logger.info(f"开始获取零件详情, part_id={part_id}")
    
    try:
        # 模拟查询逻辑
        logger.debug(f"查询零件数据: part_id={part_id}")
        
        part_data = {
            'id': part_id,
            'name': '螺丝钉M6',
            'stock': 1000,
            'price': 0.5
        }
        
        logger.info(f"成功获取零件详情: {part_data}")
        return part_data
        
    except Exception as e:
        logger.error(f"获取零件详情失败: {e}", exc_info=True)
        raise


def update_part_stock(part_id, quantity):
    """更新零件库存"""
    logger.info(f"更新零件库存: part_id={part_id}, quantity={quantity}")
    
    try:
        if quantity < 0:
            logger.warning(f"库存数量为负数: {quantity}")
        
        logger.debug(f"执行更新: UPDATE parts SET stock={quantity} WHERE id={part_id}")
        logger.info(f"库存更新成功")
        
        return {'status': 'success'}
        
    except Exception as e:
        logger.error(f"更新库存失败: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_part_detail("PART-001")

```

`src/exercise/utils/file_util.py`

```python
"""
file_util.py - 文件操作工具模块
"""
import os
import logging

# 获取当前模块的logger
logger = logging.getLogger(__name__)


def read_file(file_path):
    """读取文件内容"""
    logger.info(f"开始读取文件: {file_path}")
    
    try:
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            return None
        
        logger.debug(f"打开文件: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"文件读取成功，内容长度: {len(content)} 字符")
        return content
        
    except UnicodeDecodeError as e:
        logger.error(f"文件编码错误: {e}")
        raise
    except Exception as e:
        logger.error(f"读取文件失败: {e}", exc_info=True)
        raise


def write_file(file_path, content):
    """写入文件"""
    logger.info(f"开始写入文件: {file_path}")
    
    try:
        # 确保目录存在
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            logger.debug(f"创建目录: {dir_path}")
            os.makedirs(dir_path)
        
        logger.debug(f"写入内容长度: {len(content)} 字符")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"文件写入成功: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"写入文件失败: {e}", exc_info=True)
        raise


def delete_file(file_path):
    """删除文件"""
    logger.info(f"开始删除文件: {file_path}")
    
    try:
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在，无需删除: {file_path}")
            return True
        
        os.remove(file_path)
        logger.info(f"文件删除成功: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"删除文件失败: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    read_file("/tmp/test.txt")

```

`src/exercise/utils/op_util.py`

```python
"""
op_util.py - 操作工具模块
"""
import logging

# 获取当前模块的logger
logger = logging.getLogger(__name__)


def execute_command(command):
    """执行系统命令"""
    logger.info(f"准备执行命令: {command}")
    
    try:
        # 这里只是模拟，实际可以使用subprocess
        logger.debug(f"命令详情: {command}")
        
        # 模拟执行结果
        result = f"执行结果: {command} - 成功"
        
        logger.info(f"命令执行成功")
        logger.debug(f"执行输出: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"命令执行失败: {e}", exc_info=True)
        raise


def process_data(data):
    """处理数据"""
    logger.info(f"开始处理数据，数据类型: {type(data)}")
    
    try:
        if not data:
            logger.warning("数据为空")
            return None
        
        logger.debug(f"数据处理中...")
        
        # 模拟数据处理
        result = data if isinstance(data, str) else str(data)
        
        logger.info(f"数据处理完成，结果长度: {len(result)}")
        return result
        
    except Exception as e:
        logger.error(f"数据处理失败: {e}", exc_info=True)
        raise


def check_status(status_code):
    """检查状态"""
    logger.info(f"检查状态码: {status_code}")
    
    if status_code == 200:
        logger.info("状态正常")
        return True
    elif status_code == 404:
        logger.warning("资源未找到")
        return False
    elif status_code >= 500:
        logger.error(f"服务器错误: {status_code}")
        return False
    else:
        logger.debug(f"状态码: {status_code}")
        return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    execute_command("ls -la")

```

**日志文件：**

- `logs/main.log` - 所有模块的日志汇总
- `logs/api.log` - user.py 和 part.py 的日志
- `logs/utils.log` - file_util.py 和 op_util.py 的日志

配置说明：

| 配置项       | 说明                               |
| ------------ | ---------------------------------- |
| **日志级别** | DEBUG（文件）/ INFO（控制台）      |
| **日志格式** | 包含时间、级别、模块名、行号、消息 |
| **文件轮转** | 10MB 轮转，保留5个备份             |
| **编码**     | UTF-8，支持中文                    |
| **输出**     | 控制台 + 文件双重输出              |

这样设计的好处是：

1. ✅ 在 main.py 中集中管理所有日志配置
2. ✅ 各模块只需 `logger = logging.getLogger(__name__)` 即可使用
3. ✅ 支持按模块分离日志文件
4. ✅ 控制台和文件同时输出

# 12. 日志配置

## 12.1 字典配置

```python
import logging.config

# 使用字典配置日志
logging.config.dictConfig(LOGGING_CONFIG)
```

```python
LOGGING_CONFIG = {
    # ==================== 必需字段 ====================
    'version': 1,                    # 配置版本，目前固定为1
    
    # ==================== 可选字段 ====================
    'disable_existing_loggers': False,  # 是否禁用已存在的logger
    
    # ==================== 核心组件 ====================
    'formatters': {...},    # 格式化器：定义日志输出格式
    'filters': {...},       # 过滤器：过滤日志记录
    'handlers': {...},      # 处理器：定义日志输出目的地
    'loggers': {...},       # 日志记录器：应用程序使用的接口
    'root': {...},          # 根日志记录器
}
```

### 12.1.1 Formatters（格式化器）

定义日志的输出格式：

```python
'formatters': {
    # 简单格式
    'simple': {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',  # 日期格式
    },
    
    # 详细格式
    'detailed': {
        'format': '[%(asctime)s] %(levelname)s %(name)s:%(lineno)d - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
    
    # JSON格式（适合日志收集系统）
    'json': {
        'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',  # 需要安装 python-json-logger
        'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
    }
}
```

常用格式占位符：

| 占位符           | 说明       | 示例                          |
| ---------------- | ---------- | ----------------------------- |
| `%(asctime)s`    | 时间       | 2024-01-15 10:30:00           |
| `%(name)s`       | logger名称 | exercise.api.user             |
| `%(levelname)s`  | 日志级别   | INFO                          |
| `%(message)s`    | 日志消息   | 用户登录成功                  |
| `%(filename)s`   | 文件名     | user.py                       |
| `%(lineno)d`     | 行号       | 42                            |
| `%(funcName)s`   | 函数名     | get_user_info                 |
| `%(module)s`     | 模块名     | user                          |
| `%(pathname)s`   | 完整路径   | /app/src/exercise/api/user.py |
| `%(process)d`    | 进程ID     | 12345                         |
| `%(thread)d`     | 线程ID     | 67890                         |
| `%(threadName)s` | 线程名     | MainThread                    |

### 12.1.2 Filters（过滤器）

用于过滤日志记录：

```python
'filters': {
    # 只允许特定级别的日志
    'require_debug_true': {
        '()': 'django.utils.log.RequireDebugTrue',  # Django示例
    },
    
    # 自定义过滤器
    'custom_filter': {
        '()': 'myapp.logging.CustomFilter',
        'param': 'value'
    },
    
    # 级别范围过滤器
    'level_range': {
        '()': 'logging.Filter',
        'name': 'exercise.api',  # 只允许该logger
    }
}

```

自定义过滤器示例：

```python
import logging

class LevelRangeFilter(logging.Filter):
    """只允许指定级别范围的日志"""
    def __init__(self, low_level='DEBUG', high_level='WARNING'):
        super().__init__()
        self.low_level = getattr(logging, low_level)
        self.high_level = getattr(logging, high_level)
    
    def filter(self, record):
        return self.low_level <= record.levelno <= self.high_level


# 配置中使用
'filters': {
    'debug_to_warning': {
        '()': '__main__.LevelRangeFilter',
        'low_level': 'DEBUG',
        'high_level': 'WARNING'
    }
}

```

### 12.1.3 Handlers（处理器）

定义日志输出的目的地：

```python
'handlers': {
    # ========== 控制台处理器 ==========
    'console': {
        'class': 'logging.StreamHandler',      # 处理器类
        'level': 'INFO',                        # 处理的最低级别
        'formatter': 'simple',                  # 使用的格式化器
        'filters': [],                          # 使用的过滤器
        'stream': 'ext://sys.stdout',           # 输出流（stdout/stderr）
    },
    
    # ========== 文件处理器（基础） ==========
    'file': {
        'class': 'logging.FileHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'filename': 'logs/app.log',             # 文件路径
        'mode': 'a',                            # 追加模式
        'encoding': 'utf-8',                    # 编码
    },
    
    # ========== 滚动文件处理器（按大小） ==========
    'rotating_file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'filename': 'logs/app.log',
        'maxBytes': 10485760,                   # 10MB
        'backupCount': 5,                       # 保留5个备份
        'encoding': 'utf-8',
    },
    
    # ========== 滚动文件处理器（按时间） ==========
    'timed_file': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'filename': 'logs/app.log',
        'when': 'midnight',                     # 每天午夜轮转
        # 'when': 'H',                          # 每小时
        # 'when': 'M',                          # 每分钟
        # 'when': 'S',                          # 每秒
        # 'when': 'D',                          # 每天
        # 'when': 'W0',                         # 每周一
        'interval': 1,                          # 间隔
        'backupCount': 7,                       # 保留7天
        'encoding': 'utf-8',
    },
    
    # ========== 邮件处理器 ==========
    'email': {
        'class': 'logging.handlers.SMTPHandler',
        'level': 'ERROR',
        'formatter': 'detailed',
        'mailhost': 'smtp.example.com',
        'port': 587,
        'fromaddr': 'noreply@example.com',
        'toaddrs': ['admin@example.com'],
        'subject': 'Application Error',
        'credentials': ('user', 'password'),
        'secure': (),  # 使用TLS
    },
    
    # ========== 网络Socket处理器 ==========
    'socket': {
        'class': 'logging.handlers.SocketHandler',
        'level': 'DEBUG',
        'host': 'localhost',
        'port': 9020,
    },
    
    # ========== HTTP处理器 ==========
    'http': {
        'class': 'logging.handlers.HTTPHandler',
        'level': 'ERROR',
        'host': 'logs.example.com',
        'url': '/api/logs',
        'method': 'POST',
        'secure': True,
    },
    
    # ========== SysLog处理器 ==========
    'syslog': {
        'class': 'logging.handlers.SysLogHandler',
        'level': 'INFO',
        'address': '/dev/log',  # Linux
        # 'address': ('localhost', 514),  # 远程syslog
        'facility': 'user',
    },
    
    # ========== NullHandler（不输出） ==========
    'null': {
        'class': 'logging.NullHandler',
    }
}

```

### 12.1.4 Loggers（日志记录器）

应用程序实际使用的日志接口：

```python
'loggers': {
    # ========== 模块级Logger ==========
    'exercise.api': {
        'level': 'DEBUG',                       # 日志级别
        'propagate': False,                     # 是否传播给父logger
        'filters': [],
        'handlers': ['console', 'rotating_file'],  # 使用的处理器
    },
    
    # ========== 子模块Logger ==========
    'exercise.api.user': {
        'level': 'DEBUG',
        'propagate': False,
        'handlers': ['console'],
    },
    
    # ========== 第三方库Logger ==========
    'urllib3': {
        'level': 'WARNING',                     # 降低第三方库日志级别
        'propagate': False,
        'handlers': [],
    },
    
    'requests': {
        'level': 'WARNING',
        'propagate': False,
    },
}

```

**propagate 属性详解：**

```python
Logger层级结构：
root
 └── exercise
      └── exercise.api
           └── exercise.api.user

如果 propagate=True（默认）：
exercise.api.user 的日志会传播给 exercise.api 和 exercise

如果 propagate=False：
日志只由当前logger的handlers处理，不会传播

```

### 12.1.5 Root Logger（根日志记录器）

```python
'root': {
    'level': 'INFO',
    'handlers': ['console', 'rotating_file']
}
```

根 `logger `是所有 `logger` 的祖先，未配置的 `logger` 会继承 `root` 的配置。

### 12.1.6 完整字典配置示例

```python
import logging.config
import os

def get_logging_config():
    """生成完整的日志配置字典"""
    
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    return {
        'version': 1,
        'disable_existing_loggers': False,
        
        # 格式化器
        'formatters': {
            'console': {
                'format': '%(levelname)s %(name)s:%(lineno)d - %(message)s',
                'datefmt': '%H:%M:%S'
            },
            'file': {
                'format': '[%(asctime)s] %(levelname)s %(name)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        
        # 处理器
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'console',
                'stream': 'ext://sys.stdout'
            },
            'file_all': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'file',
                'filename': f'{log_dir}/all.log',
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf-8'
            },
            'file_error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'file',
                'filename': f'{log_dir}/error.log',
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf-8'
            }
        },
        
        # 日志记录器
        'loggers': {
            'exercise': {
                'level': 'DEBUG',
                'handlers': ['console', 'file_all'],
                'propagate': False
            },
            'exercise.api': {
                'level': 'DEBUG',
                'handlers': ['file_all'],
                'propagate': False
            },
            'exercise.utils': {
                'level': 'DEBUG',
                'handlers': ['file_all'],
                'propagate': False
            }
        },
        
        # 根日志记录器
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file_error']
        }
    }


# 应用配置
logging.config.dictConfig(get_logging_config())

```

## 12.2 配置文件配置

格式选择：

| 格式 | 文件扩展名      | 解析方式                      | 优点                 |
| ---- | --------------- | ----------------------------- | -------------------- |
| INI  | `.ini`, `.conf` | `logging.config.fileConfig()` | 简单、Python内置支持 |
| JSON | `.json`         | 自定义解析 + `dictConfig`     | 结构化、易解析       |
| YAML | `.yaml`, `.yml` | 自定义解析 + `dictConfig`     | 易读、支持注释       |

### 12.2.1 `ini` 格式配置

配置文件示例：

```python
; logging.ini - INI格式日志配置文件

; ==================== 日志格式 ====================
[formatters]
keys=simple,detailed

[formatter_simple]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S

[formatter_detailed]
format=[%(asctime)s] %(levelname)s %(name)s:%(lineno)d - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
class=logging.Formatter

; ==================== 日志处理器 ====================
[handlers]
keys=consoleHandler,fileHandler

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simple
args=(sys.stdout,)

[handler_fileHandler]
class=handlers.RotatingFileHandler
level=DEBUG
formatter=detailed
args=('logs/app.log', 'a', 10485760, 5)
; args格式：


; ==================== 日志记录器 ====================
[loggers]
keys=root,apiLogger,utilsLogger

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_apiLogger]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=exercise.api
propagate=0

[logger_utilsLogger]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=exercise.utils
propagate=0

```

使用方式：

```python
import logging.config

# 方式1：使用fileConfig加载INI文件
logging.config.fileConfig(
    'logging.ini',
    disable_existing_loggers=False  # 不禁用已存在的logger
)

# 使用
logger = logging.getLogger('exercise.api')
logger.info('使用INI配置的日志')

```

### 12.2.2 `json` 格式配置

配置文件示例：

```python
{
    "version": 1,
    "disable_existing_loggers": false,
    
    "formatters": {
        "console": {
            "format": "%(levelname)s %(name)s:%(lineno)d - %(message)s",
            "datefmt": "%H:%M:%S"
        },
        "file": {
            "format": "[%(asctime)s] %(levelname)s %(name)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "console",
            "stream": "ext://sys.stdout"
        },
        "file_all": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": "logs/all.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf-8"
        },
        "file_error": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "file",
            "filename": "logs/error.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf-8"
        },
        "file_json": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": "logs/app.json",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf-8"
        }
    },
    
    "loggers": {
        "exercise": {
            "level": "DEBUG",
            "handlers": ["console", "file_all"],
            "propagate": false
        },
        "exercise.api": {
            "level": "DEBUG",
            "handlers": ["file_all"],
            "propagate": false
        },
        "exercise.utils": {
            "level": "DEBUG",
            "handlers": ["file_all"],
            "propagate": false
        }
    },
    
    "root": {
        "level": "INFO",
        "handlers": ["console", "file_error"]
    }
}

```

使用方式：

```python
import json
import logging.config

def setup_logging_from_json(config_file='logging.json'):
    """从JSON文件加载日志配置"""
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    logging.config.dictConfig(config)
    return logging.getLogger(__name__)


# 使用
logger = setup_logging_from_json()
logger.info('使用JSON配置的日志')

```

### 12.2.3 `yaml` 格式配置

配置文件示例：

```python
# logging.yaml - YAML格式日志配置文件

version: 1
disable_existing_loggers: false

# ==================== 格式化器 ====================
formatters:
  console:
    format: "%(levelname)s %(name)s:%(lineno)d - %(message)s"
    datefmt: "%H:%M:%S"
  
  file:
    format: "[%(asctime)s] %(levelname)s %(name)s:%(lineno)d - %(message)s"
    datefmt: "%Y-%m-%d %H:%M:%S"
  
  detailed:
    format: |
      ============== %(levelname)s ==============
      时间: %(asctime)s
      模块: %(name)s
      文件: %(filename)s:%(lineno)d
      函数: %(funcName)s
      消息: %(message)s
      ===========================================

# ==================== 处理器 ====================
handlers:
  # 控制台输出
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: console
    stream: ext://sys.stdout
  
  # 所有日志文件
  file_all:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: file
    filename: logs/all.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    encoding: utf-8
  
  # 错误日志文件
  file_error:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: detailed
    filename: logs/error.log
    maxBytes: 10485760
    backupCount: 5
    encoding: utf-8
  
  # API模块日志文件
  file_api:
    class: logging.handlers.TimedRotatingFileHandler
    level: DEBUG
    formatter: file
    filename: logs/api.log
    when: midnight
    backupCount: 7
    encoding: utf-8
  
  # Utils模块日志文件
  file_utils:
    class: logging.handlers.TimedRotatingFileHandler
    level: DEBUG
    formatter: file
    filename: logs/utils.log
    when: midnight
    backupCount: 7
    encoding: utf-8

# ==================== 日志记录器 ====================
loggers:
  # API模块
  exercise.api:
    level: DEBUG
    handlers: [file_api, file_all]
    propagate: false
  
  exercise.api.user:
    level: DEBUG
    handlers: [file_api]
    propagate: false
  
  exercise.api.part:
    level: DEBUG
    handlers: [file_api]
    propagate: false
  
  # Utils模块
  exercise.utils:
    level: DEBUG
    handlers: [file_utils, file_all]
    propagate: false
  
  exercise.utils.file_util:
    level: DEBUG
    handlers: [file_utils]
    propagate: false
  
  exercise.utils.op_util:
    level: DEBUG
    handlers: [file_utils]
    propagate: false
  
  # 第三方库日志控制
  urllib3:
    level: WARNING
    propagate: false
  
  requests:
    level: WARNING
    propagate: false

# ==================== 根日志记录器 ====================
root:
  level: INFO
  handlers: [console, file_error]

```

使用方式：

```python
import logging.config
import yaml  # 需要安装: pip install pyyaml

def setup_logging_from_yaml(config_file='logging.yaml'):
    """从YAML文件加载日志配置"""
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    logging.config.dictConfig(config)
    return logging.getLogger(__name__)


# 使用
logger = setup_logging_from_yaml()
logger.info('使用YAML配置的日志')

```

## 12.3 环境感知的动态配置

结合环境变量动态生成配置：

```python
import os
import logging.config
import yaml

def setup_logging(env=None):
    """根据环境动态配置日志"""
    
    # 获取环境
    env = env or os.getenv('APP_ENV', 'development')
    
    # 加载基础配置
    with open('logging.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 根据环境调整配置
    if env == 'production':
        # 生产环境：只输出WARNING及以上级别到控制台
        config['handlers']['console']['level'] = 'WARNING'
        config['root']['level'] = 'WARNING'
        
    elif env == 'development':
        # 开发环境：输出DEBUG级别
        config['handlers']['console']['level'] = 'DEBUG'
        config['root']['level'] = 'DEBUG'
        
    elif env == 'testing':
        # 测试环境：输出INFO级别
        config['handlers']['console']['level'] = 'INFO'
        config['root']['level'] = 'INFO'
    
    # 应用配置
    logging.config.dictConfig(config)
    return logging.getLogger(__name__)


# 使用
# 生产环境: APP_ENV=production python main.py
# 开发环境: APP_ENV=development python main.py
logger = setup_logging()

```

## 12.4 两种配置方式对比

| 对比项       | 字典配置                 | INI配置文件          | JSON配置文件         | YAML配置文件           |
| ------------ | ------------------------ | -------------------- | -------------------- | ---------------------- |
| **易读性**   | 中等                     | 差（格式限制）       | 中等                 | **优**（支持注释）     |
| **灵活性**   | **优**（可编程）         | 差                   | 中等                 | **优**（支持锚点引用） |
| **类型支持** | **优**（完整Python类型） | 差（仅字符串）       | 中等（需类型转换）   | **优**（支持多种类型） |
| **动态配置** | **优**（条件判断）       | 差                   | 中等（需后处理）     | 中等（需后处理）       |
| **部署友好** | 中等（硬编码）           | **优**（外部文件）   | **优**（外部文件）   | **优**（外部文件）     |
| **修改便利** | 差（需改代码）           | **优**（改文件即可） | **优**（改文件即可） | **优**（改文件即可）   |
| **依赖**     | 无                       | 无                   | 无（内置json）       | 需PyYAML               |

## 12.5 推荐方式

**YAML配置文件 + 字典动态调整**

```python
# main.py
import os
import logging.config
import yaml
from pathlib import Path

def setup_logging():
    """推荐的企业级日志配置方案"""
    
    # 1. 加载YAML配置
    config_file = Path(__file__).parent / 'config' / 'logging.yaml'
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 2. 动态调整（环境变量、路径等）
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # 更新所有文件handler的路径
    for handler_name, handler_config in config.get('handlers', {}).items():
        if 'filename' in handler_config:
            handler_config['filename'] = str(log_dir / Path(handler_config['filename']).name)
    
    # 3. 环境感知
    env = os.getenv('APP_ENV', 'development')
    if env == 'production':
        config['handlers']['console']['level'] = 'WARNING'
    
    # 4. 应用配置
    logging.config.dictConfig(config)
    
    return logging.getLogger(__name__)


if __name__ == '__main__':
    logger = setup_logging()
    logger.info("日志系统初始化完成")

```

## 12.6 总结

### 12.6.1 两种配置方式核心对比：

```python
┌─────────────────────────────────────────────────────────────────┐
│                        日志配置架构                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  字典配置                    配置文件配置                          │
│  ┌──────────────────┐                   ┌──────────────────┐    │
│  │  Python字典      │                   │  外部文件          │    │
│  │  logging.config. │                   │  INI/JSON/YAML   │    │
│  │  dictConfig()    │                   │                  │    │
│  └────────┬─────────┘                   └────────┬─────────┘    │
│           │                                      │              │
│           ▼                                      ▼              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              五大核心组件 (共用)                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │   │
│  │  │Formatter │  │ Handler  │  │  Logger  │               │   │
│  │  │(格式化器) │  │(处理器)   │  │(记录器)   │                │   │
│  │  └──────────┘  └──────────┘  └──────────┘               │   │
│  │  ┌──────────┐  ┌──────────┐                              │   │
│  │  │  Filter  │  │   Root   │                              │   │
│  │  │(过滤器)   │  │(根记录器) │                              │   │
│  │  └──────────┘  └──────────┘                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

### 12.6.2 快速选择指南：

```python
场景                          推荐方式
────────────────────────────────────────────────────────────
小型项目、快速原型           → 字典配置
需要部署时修改配置           → YAML配置文件  
企业级项目                    → YAML + 字典动态调整
多环境部署 (dev/test/prod)   → YAML + 环境变量
需要复杂格式、注释            → YAML配置文件
CI/CD 自动化部署             → YAML配置文件

```

### 12.6.3 核心配置要点

组件层级关系：

```python
Logger (日志记录器)
   │
   ├── Handler (处理器) ── 决定日志输出到哪里
   │      ├── StreamHandler (控制台)
   │      ├── FileHandler (文件)
   │      ├── RotatingFileHandler (按大小滚动)
   │      ├── TimedRotatingFileHandler (按时间滚动)
   │      └── SMTPHandler (邮件)
   │
   ├── Formatter (格式化器) ── 决定日志长什么样
   │      └── format字符串
   │
   ├── Filter (过滤器) ── 决定哪些日志被输出
   │
   └── Level (级别) ── 决定日志最低级别
          DEBUG < INFO < WARNING < ERROR < CRITICAL

```

**`propagate` 属性关键理解**

```python
propagate=True (默认):
  子logger日志 → 传播给父logger → 可能重复输出

propagate=False:
  子logger日志 → 不传播 → 只由当前handler处理

建议：明确配置时设为 False，避免重复

```

# 13. **最佳实践**

| 实践           | 说明                                    |
| -------------- | --------------------------------------- |
| **集中配置**   | 在main.py中统一配置，各模块只获取logger |
| **分离日志**   | 不同模块/级别使用不同日志文件           |
| **滚动策略**   | 文件大小10MB或按天滚动，保留5-7份       |
| **格式统一**   | 包含时间、级别、模块、行号、消息        |
| **环境感知**   | 开发DEBUG，生产WARNING/ERROR            |
| **第三方控制** | 降低urllib3、requests等库的日志级别     |

# 14. 字典配置示例

```python
exercise/
├─ main.py                    # 入口文件，集中配置日志
├─ logs/                      # 日志文件目录（自动创建）
│  ├─ main.log               # 主日志文件（所有模块）
│  ├─ api.log                # API模块日志
│  └─ utils.log              # Utils模块日志
└─ src/
   └─ exercise/
       ├─ api/
       │  ├─ __init__.py
       │  ├─ user.py         # 用户API
       │  └─ part.py         # 零件API
       └─ utils/
          ├─ __init__.py
          ├─ file_util.py    # 文件工具
          └─ op_util.py      # 操作工具
```

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py

import logging
import os
from logging import config

from src.exercise.api import user, depart
from src.exercise.utils import file_util, op_util


def setup_logging():
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    config = {
        'version': 1,
        'disable_existing_loggers': False,

        # 格式化器：定义日志输出格式
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            }
        },

        # 处理器: 日志输出目的地
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'detailed',
            },
            'main_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'main.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf-8'
            },
            'api_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'api.log'),
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf-8'
            },
            'utils_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'utils.log'),
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf-8'
            }
        },

        # 日志记录器：应用程序使用的接口
        'loggers': {
            # API模块的logger
            'src.exercise.api': {
                'level': 'DEBUG',
                'handlers': ['console', 'api_file', 'main_file'],
                'propagate': False  # 不向上传播，避免重复打印
            },
            'src.exercise.api.user': {
                'level': 'DEBUG',
                'handlers': ['console', 'api_file'],
                'propagate': False
            },
            'src.exercise.api.part': {
                'level': 'DEBUG',
                'handlers': ['console', 'api_file'],
                'propagate': False
            },

            # Utils模块的logger
            'src.exercise.utils': {
                'level': 'DEBUG',
                'handlers': ['console', 'utils_file', 'main_file'],
                'propagate': False
            },
            'src.exercise.utils.file_util': {
                'level': 'DEBUG',
                'handlers': ['console', 'utils_file'],
                'propagate': False
            },
            'src.exercise.utils.op_util': {
                'level': 'DEBUG',
                'handlers': ['console', 'utils_file'],
                'propagate': False
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'main_file']
        }
    }
    logging.config.dictConfig(config)
    return logging.getLogger(__name__)


def main():
    logger = setup_logging()

    logger.debug('这是 main 的 debug')
    logger.info('这是 main 的 info')
    logger.warning('这是 main 的 warning')
    logger.error('这是 main 的 error')
    logger.critical('这是 main 的 critical')

    user.get_user_info()
    depart.get_depart_info()
    file_util.read_jsonl_file('./data.txt')
    op_util.make()


if __name__ == '__main__':
    main()

```

```python
# user.py

import logging

logger = logging.getLogger(__name__)


def get_user_info():
    logger.debug('这是 user 的 debug')
    logger.info('这是 user 的 info')
    logger.warning('这是 user 的 warning')
    logger.error('这是 user 的 error')
    logger.critical('这是 user 的 critical')
```

其他的主要文件此处不展示了，和 `user.py` 一样的结构，一个函数中只有五个日志记录。

运行 `main.py` 后效果：

```python
2026-08-15 18:48:34 [INFO] __main__:131 - 这是 main 的 info
2026-08-15 18:48:34 [WARNING] __main__:132 - 这是 main 的 warning
2026-08-15 18:48:34 [ERROR] __main__:133 - 这是 main 的 error
2026-08-15 18:48:34 [CRITICAL] __main__:134 - 这是 main 的 critical
2026-08-15 18:48:34 [INFO] src.exercise.api.user:24 - 这是 user 的 info
2026-08-15 18:48:34 [WARNING] src.exercise.api.user:25 - 这是 user 的 warning
2026-08-15 18:48:34 [ERROR] src.exercise.api.user:26 - 这是 user 的 error
2026-08-15 18:48:34 [CRITICAL] src.exercise.api.user:27 - 这是 user 的 critical
2026-08-15 18:48:34 [INFO] src.exercise.api.depart:24 - 这是 depart 的 info
2026-08-15 18:48:34 [WARNING] src.exercise.api.depart:25 - 这是 depart 的 warning
2026-08-15 18:48:34 [ERROR] src.exercise.api.depart:26 - 这是 depart 的 error
2026-08-15 18:48:34 [CRITICAL] src.exercise.api.depart:27 - 这是 depart 的 critical
2026-08-15 18:48:34 [INFO] src.exercise.utils.file_util:27 - 这是 file_util 的 info
2026-08-15 18:48:34 [WARNING] src.exercise.utils.file_util:28 - 这是 file_util 的 warning
2026-08-15 18:48:34 [ERROR] src.exercise.utils.file_util:29 - 这是 file_util 的 error
2026-08-15 18:48:34 [CRITICAL] src.exercise.utils.file_util:30 - 这是 file_util 的 critical
2026-08-15 18:48:34 [INFO] src.exercise.utils.op_util:24 - 这是 op_util 的 info
2026-08-15 18:48:34 [WARNING] src.exercise.utils.op_util:25 - 这是 op_util 的 warning
2026-08-15 18:48:34 [ERROR] src.exercise.utils.op_util:26 - 这是 op_util 的 error
2026-08-15 18:48:34 [CRITICAL] src.exercise.utils.op_util:27 - 这是 op_util 的 critical
```

