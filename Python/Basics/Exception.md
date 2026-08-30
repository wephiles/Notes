<h1 align="center">Python Exception</h1>

# 1. `try-except-finally-else` 机制
## 1.1 异常处理机制概述
| 组件         | 作用                    | 执行时机                          |
| ------------ | ----------------------- | --------------------------------- |
| **try**      | 包含可能引发异常的代码  | 总是首先执行                      |
| **except**   | 捕获并处理特定异常      | 仅在 try 中发生匹配的异常时执行   |
| **else**     | 放置依赖 try 成功的代码 | 仅在 try 完全成功（无异常）时执行 |
| **finally**  | 清理资源                | **总是执行**，无论有无异常        |
| 🔑 关键特性： |                         |                                   |
1. 执行顺序：`try -> except(若发生异常)/else(若未发生异常) -> finally`
2. `finally` 总是执行
3. `finally` 中的 `return` 会覆盖 `try/except` 的返回值
4. 异常链：使用 `raise ... from ...` 保留原始异常（见第 2 章）
5. 性能提示：异常处理比条件查询慢，不应用于常规流程控制
⚠️ 常见陷阱：
1. ❌ 裸 `except:` 会捕获 `KeyboardInterrupt` 等系统异常
2. ❌ `finally` 中的 `return` 会覆盖前面的返回值
3. ❌ `finally` 中的异常会覆盖原始异常，导致调用者丢失业务异常的处理机会
4. ❌ 具体异常应放在 `except Exception` 之前
## 1.2 核心语法
```python
try:
    # 可能会引发异常的代码块（受监控的代码）
    ...
except ExceptionType1:
    # 处理 ExceptionType1 及其子类的异常
    ...
except ExceptionType2 as e:
    # 捕获异常并绑定到变量 e
    ...
else:
    # 当 try 块没有抛出任何异常时执行
    ...
finally:
    # 无论是否发生异常，最终都会执行
    ...
```
- **顺序固定**：`try` → 一个或多个 `except` → 可选的 `else` → 可选的 `finally`。
- `else` 必须出现在所有 `except` 之后、`finally` 之前。
- `try...finally` 也是合法的（等价于没有 `except`），用于保证清理。
## 1.3 各子句的职责与执行时机
### 1.3.1 `try` 块
要监控的代码。一旦某条语句抛出异常，该块内后续代码都不会执行，Python 会立即跳转到第一个匹配的 `except` 子句（如果存在）。
### 1.3.2 `except` 块
负责捕获和处理异常。可以指定异常类型，也可以带别名 `as e`。
- 多个 `except` 按顺序匹配，一旦匹配成功，后面的 `except` 不再检查。
- 异常匹配基于继承关系，子类异常会匹配父类的 `except`。
- **裸 `except:`** 会捕获所有异常（包括 `SystemExit`、`KeyboardInterrupt`），通常不推荐，至少应使用 `except Exception:`。
### 1.3.3 `else` 块
- 当且仅当 `try` 块**没有抛出任何异常**时执行。
- 若 try 抛出异常（无论是否被捕获），`else` 都不会执行。
- 好处：将"只在无异常时执行"的代码与 try 代码清晰分开，避免误捕获；且 `else` 中产生的异常不会被前面的 `except` 捕获。
### 1.3.4 `finally` 块
- 无论是否发生异常、异常是否被捕获、是否执行了 `return`/`break`/`continue`，`finally` 都会在离开整个 `try` 语句之前执行。
- 典型用途：释放外部资源（关闭文件、网络连接、释放锁等）。
- 若 `finally` 中包含 `return`/`break`/`continue` 或抛出新异常，会覆盖原有的返回值或控制流。
## 1.4 完整执行流程
1. 执行 `try` 子句。
2. 若没有异常发生：
   - 跳过所有 `except` 子句；
   - 若存在 `else`，执行 `else`；
   - 若存在 `finally`，执行 `finally`（即使 `else` 中发生异常，也会先执行 `finally` 再向外抛）。
3. 若有异常发生：
   - 寻找匹配的 `except`。找到则执行该块，然后执行 `finally`；
   - 没找到则异常被暂存，执行 `finally` 后重新向外层抛出。
4. 若在 `try`/`except`/`else` 中执行了 `return`/`break`/`continue`：
   - `finally` 依然会在真正跳出之前执行；
   - 若 `finally` 内也有 `return`/`break`，它会取代原本的返回值或跳转。
## 1.5 关键细节与陷阱
### 1.5.1 `finally` 中 `return` 的覆盖问题
```python
def demo():
    try:
        return 1
    finally:
        return 2
print(demo())  # 输出 2
```
`try` 中的 `return 1` 在即将返回时进入 `finally`，`finally` 中的 `return 2` 直接导致函数返回 `2`，原先的 `1` 被丢弃。**避免在 `finally` 中使用 `return` 或 `break`**。
### 1.5.2 `finally` 中的异常屏蔽
```python
def func():
    try:
        raise ValueError("原始异常")
    finally:
        raise TypeError("新异常")
```
若 `finally` 中抛出新异常，它会取代原本活跃的异常。上面代码最终抛出 `TypeError`，`ValueError` 丢失（可通过 `__context__` 隐式追溯，但不会自动再次抛出）。
实际案例——`finally` 中的异常导致调用者无法捕获业务异常：
```python
def func_test_except_1(a, b):
    try:
        a / b
    except ZeroDivisionError:
        raise ZeroDivisionError
    else:
        print("没有错误")
    finally:
        with open('not_exists_file.txt', 'r') as fp:
            pass
try:
    func_test_except_1(4, 0)
except ZeroDivisionError:
    print('调用者捕获了除0异常')
except FileNotFoundError:
    print('调用者捕获了文件不存在异常')
# 运行结果: 调用者捕获了文件不存在异常
# 调用者只能捕获 FileNotFoundError，未能捕获 ZeroDivisionError —— except 块中的异常被覆盖了
```
💡 防止方法：**避免在 `finally` 中抛出异常**。
### 1.5.3 `break` 与 `continue` 同理
在循环中，`finally` 的 `break`/`continue` 会覆盖 `try` 或 `except` 中的跳转。
### 1.5.4 `else` 存在的重要意义
没有 `else` 时，"只在成功时执行"的代码通常有两种写法，各有问题：
- 放在 `try` 内：可能抛出被误捕获的异常类型；
- 放在 `try...except` 之后：没有语法保证它们只在成功时运行，阅读时需要额外推理。
`else` 明确表达"这段代码只在 try 无异常时运行"，且其产生的异常不会被前面的 `except` 捕获。
### 1.5.5 异常匹配顺序
```python
try:
    ...
except LookupError:   # 处理 IndexError 和 KeyError
    ...
except IndexError:    # 永远不会执行，因为 IndexError 是 LookupError 的子类
    ...
```
应将**更具体的异常放在前面，更宽泛的放在后面**。
## 1.6 常见组合模式
- **`try...except...finally`**：捕获异常并保证清理。
- **`try...except...else`**：区分异常处理和成功时继续的逻辑。
- **`try...finally`**：不处理异常，只保证资源释放（异常继续向外传播）。
- **`try...except...else...finally`**：完整形态，清晰严谨。
## 1.7 最佳实践与实际示例
```python
# 推荐模式
try:
    # 可能失败的代码
    ...
except SpecificError as e:   # 捕获具体异常（放在宽泛异常之前）
    handle_error(e)
else:
    process_success()        # 无异常时执行
finally:
    cleanup()                # 清理资源
```
实际示例：
```python
def read_config(path):
    file = None
    try:
        file = open(path, 'r')
        data = file.read()
    except FileNotFoundError:
        print(f"配置文件不存在: {path}")
        return {}
    except PermissionError:
        print(f"没有权限读取: {path}")
        return {}
    else:
        # 仅在读取成功时解析
        return parse_config(data)
    finally:
        if file:
            file.close()
```
基础行为演示：
```python
try:
    1 / 0
except ZeroDivisionError:
    print('❌ 出现除零异常')
else:
    print('没有抛出任何异常或错误')
finally:
    print('最终执行的代码块')
# 执行结果：
# ❌ 出现除零异常
# 最终执行的代码块
```
无异常时：
```python
try:
    3 / 1
except ZeroDivisionError:
    print('❌ 出现除零异常')
else:
    print('没有抛出任何异常或错误')
finally:
    print('最终执行的代码块')
# 执行结果：
# 没有抛出任何异常或错误
# 最终执行的代码块
```
# 2. `raise ... from ...` 异常链
`raise ... from ...` 是 Python 3 引入的**异常链**语法，用于在捕获一个异常后抛出另一个异常时，保留原始异常的上下文信息。
## 2.1 基本语法
```python
try:
    # 可能出错的代码
    ...
except SomeException as e:
    # 抛出新异常，并链接原始异常
    raise NewException("新异常信息") from e
```
## 2.2 不使用 `from` 导致原始异常丢失
```python
def load_config():
    try:
        with open("config.json") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise ValueError("配置文件加载失败")   # 原始异常丢失！
load_config()
# 只能看到 ValueError，看不到原始的 FileNotFoundError
```
## 2.3 使用 `raise ... from ...` 保留异常链
```python
def load_config():
    try:
        with open("config.json") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise ValueError("配置文件加载失败") from e   # 保留原始异常
load_config()
```
输出：
```plaintext
ValueError: 配置文件加载失败
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "example.py", line 7, in load_config
    with open("config.json") as f:
FileNotFoundError: [Errno 2] No such file or directory: 'config.json'
```
## 2.4 三种抛出方式对比
### 2.4.1 普通 `raise`（隐式链）
```python
def func_test_except_1(a, b):
    try:
        a / b
    except ZeroDivisionError:
        raise ValueError('除数不能为0')
func_test_except_1(4, 0)
```
回溯信息：
```plaintext
Traceback (most recent call last):
  File "demo2.py", line 20, in func_test_except_1
    a / b
ZeroDivisionError: division by zero
During handling of the above exception, another exception occurred:
  👈 隐式异常链（During handling...）
Traceback (most recent call last):
  File "demo2.py", line 22, in func_test_except_1
    raise ValueError('除数不能为0')
ValueError: 除数不能为0
```
### 2.4.2 `raise ... from ...`（显式链）
```python
def func_test_except_1(a, b):
    try:
        a / b
    except ZeroDivisionError as e:
        raise ValueError('除数不能为0') from e
func_test_except_1(4, 0)
```
回溯信息：
```plaintext
Traceback (most recent call last):
  File "demo2.py", line 20, in func_test_except_1
    a / b
ZeroDivisionError: division by zero
The above exception was the direct cause of the following exception:
  👈 显式声明因果关系（The above exception was the direct cause...）
Traceback (most recent call last):
  File "demo2.py", line 22, in func_test_except_1
    raise ValueError('除数不能为0') from e
ValueError: 除数不能为0
```
### 2.4.3 `raise ... from None`（隐藏原始异常）
```python
def func_test_except_1(a, b):
    try:
        a / b
    except ZeroDivisionError:
        raise ValueError('除数不能为0') from None   # 隐藏原始异常
func_test_except_1(4, 0)
```
回溯信息（看不到原始异常）：
```plaintext
Traceback (most recent call last):
  File "demo2.py", line 22, in func_test_except_1
    raise ValueError('除数不能为0') from None
ValueError: 除数不能为0
```
适用场景：完全隐藏内部实现细节，对外只暴露高层异常：
```python
def authenticate(username, password):
    try:
        # 内部验证逻辑
        if not check_internal_db(username):
            raise InternalDBError("数据库连接失败")
    except InternalDBError:
        # 对外只暴露认证失败，隐藏内部实现细节
        raise AuthenticationError("用户名或密码错误") from None
```
# 3. 自定义异常
## 3.1 基础自定义异常
### 3.1.1 最简单的自定义异常
```python
class MyException(Exception):
    pass
def get_age(age: int) -> int:
    if age < 0:
        raise MyException('年龄是负数')
    return age
def main():
    print(get_age(18))
    print(get_age(-12))
if __name__ == '__main__':
    main()
```
控制台输出：
```python
18
Traceback (most recent call last):
  File "main.py", line 21, in <module>
    main()
  File "main.py", line 16, in main
    print(get_age(-12))
  File "main.py", line 10, in get_age
    raise MyException('年龄是负数')
MyException: 年龄是负数
```
### 3.1.2 带自定义属性的异常
```python
class MyException(Exception):
    def __init__(self, message: str, field_name, invalid_value):
        super().__init__(message)
        self.field_name = field_name
        self.invalid_value = invalid_value
        self.message = message
    def __str__(self):
        return f'字段 {self.field_name} 的值 {self.invalid_value} 无效: {self.message}'
def invalid_email(email, phone):
    if '@' not in email:
        raise MyException(
            '邮箱格式错误',
            field_name='email',
            invalid_value=email
        )
    if not phone.startswith('+86'):
        raise MyException(
            '手机号不是以"+86"开头',
            field_name='phone',
            invalid_value=phone
        )
    return email, phone
def main():
    invalid_email('error@email', '11123456789')
if __name__ == '__main__':
    main()
```
控制台输出：
```python
Traceback (most recent call last):
  File "main.py", line 38, in <module>
    main()
  File "main.py", line 33, in main
    invalid_email('error@email', '11123456789')
  File "main.py", line 24, in invalid_email
    raise MyException(
MyException: 字段 phone 的值 11123456789 无效: 手机号不是以"+86"开头
```
## 3.2 完整自定义异常类实现（带错误码和时间戳）
```python
import time
from dataclasses import dataclass
@dataclass
class ErrorDetail:
    code: int
    message: int
    timestamp: float = None
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
class BusinessException(Exception):
    def __init__(self, message, error_code: int = 500,
                 details: dict | None = None,
                 cause: Exception | None = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
        self.message = message
        self.timestamp = time.time()
        self.error_detail = ErrorDetail(
            code=error_code,
            message=message,
            timestamp=self.timestamp,
        )
    def __str__(self):
        base = f'[{self.error_code}] {self.message}'
        if self.details:
            details_str = ', '.join(f'{key}={value}' for key, value in self.details.items())
            base += f' ({details_str})'
        return base
    def to_dict(self):
        return {
            'error_code': self.error_code,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp,
            'exception_type': self.__class__.__name__,
        }
    def add_detail(self, key, value):
        self.details[key] = value
        return self
# 业务子类
class UserNotFoundError(BusinessException):
    def __init__(self, user_id, **kwargs):
        super().__init__(
            message=f"用户 {user_id} 不存在！",
            error_code=404,
            details={'user_id': user_id},
            **kwargs
        )
class InsufficientBalanceFundsError(BusinessException):
    def __init__(self, current_balance, require_amount, **kwargs):
        super().__init__(
            message="余额不足",
            error_code=400,
            details={
                'current_balance': current_balance,
                'require_amount': require_amount,
            },
            **kwargs
        )
def main():
    try:
        user_id = 123465
        raise UserNotFoundError(user_id)
    except UserNotFoundError as e:
        print(e)
        print(e.to_dict())
    try:
        require_amount = 100
        raise InsufficientBalanceFundsError(20, 100)
    except InsufficientBalanceFundsError as e:
        print(e)
        print(e.to_dict())
if __name__ == '__main__':
    main()
```
控制台输出：
```python
[404] 用户 123465 不存在！ (user_id=123465)
{'error_code': 404, 'message': '用户 123465 不存在！', 'details': {'user_id': 123465}, 'timestamp': 1766728307.336313, 'exception_type': 'UserNotFoundError'}
[400] 余额不足 (current_balance=20, require_amount=100)
{'error_code': 400, 'message': '余额不足', 'details': {'current_balance': 20, 'require_amount': 100}, 'timestamp': 1766728307.3363638, 'exception_type': 'InsufficientBalanceFundsError'}
```
## 3.3 异常继承的层级结构
创建有层次的异常体系，便于按类别捕获：
```python
class APIException(Exception):
    """API异常基类"""
    status_code = 500
    default_message = "服务器内部错误"
    def __init__(self, message=None, details=None):
        self.message = message or self.default_message
        self.details = details or {}
        super().__init__(self.message)
# 客户端错误 (4xx)
class ClientError(APIException):
    """客户端错误基类"""
    status_code = 400
    default_message = "客户端请求错误"
class ValidationError(ClientError):
    status_code = 422
    default_message = "数据验证失败"
class AuthenticationError(ClientError):
    status_code = 401
    default_message = "认证失败"
class AuthorizationError(ClientError):
    status_code = 403
    default_message = "权限不足"
# 服务器错误 (5xx)
class ServerError(APIException):
    status_code = 500
    default_message = "服务器内部错误"
class DatabaseError(ServerError):
    status_code = 503
    default_message = "数据库操作失败"
class ExternalServiceError(ServerError):
    status_code = 502
    default_message = "外部服务不可用"
# 使用示例
def validate_user_data(data):
    if "username" not in data:
        raise ValidationError(
            "缺少必要字段",
            details={"missing_field": "username"}
        )
    if len(data.get("username", "")) < 3:
        raise ValidationError(
            "用户名太短",
            details={
                "field": "username",
                "value": data.get("username"),
                "min_length": 3
            }
        )
```
## 3.4 高级功能实现
### 3.4.1 支持异常链和上下文
```python
class ContextualException(Exception):
    """支持上下文的异常"""
    def __init__(self, message, context=None, cause=None):
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.cause = cause
        self.stack = []
    def add_context(self, key, value):
        """添加上下文信息"""
        self.context[key] = value
        return self
    def wrap(self, func):
        """包装函数，自动捕获并添加上下文"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, ContextualException):
                    # 如果不是我们的异常，包装它
                    e = ContextualException(str(e), cause=e)
                # 添加上下文
                e.add_context("function", func.__name__)
                e.add_context("args", args)
                e.add_context("kwargs", kwargs)
                raise e
        return wrapper
# 使用
@ContextualException("数据处理").wrap
def process_data(data):
    # 业务逻辑
    if data["value"] > 100:
        raise ContextualException("值过大", context={"max_value": 100})
    return data["value"] * 2
try:
    result = process_data({"value": 150})
except ContextualException as e:
    print(f"错误: {e.message}")
    print(f"上下文: {e.context}")
    # 上下文: {'max_value': 100, 'function': 'process_data',
    #          'args': ({'value': 150},), 'kwargs': {}}
```
### 3.4.2 可序列化的异常
```python
import json
from datetime import datetime
class SerializableException(Exception):
    """可序列化为JSON的异常"""
    def __init__(self, message, code=None, metadata=None):
        super().__init__(message)
        self.message = message
        self.code = code or "UNKNOWN_ERROR"
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()
        self.type = self.__class__.__name__
    def to_json(self, indent=2):
        """转换为JSON字符串"""
        data = {
            "type": self.type,
            "code": self.code,
            "message": self.message,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
        return json.dumps(data, indent=indent, ensure_ascii=False)
    def to_dict(self):
        """转换为字典"""
        return {
            "type": self.type,
            "code": self.code,
            "message": self.message,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
    @classmethod
    def from_dict(cls, data):
        """从字典创建异常"""
        instance = cls(
            message=data["message"],
            code=data.get("code"),
            metadata=data.get("metadata", {})
        )
        instance.timestamp = data.get("timestamp")
        return instance
# 使用
try:
    raise SerializableException(
        "文件处理失败",
        code="FILE_PROCESS_ERROR",
        metadata={
            "filename": "data.txt",
            "size": 1024,
            "attempts": 3
        }
    )
except SerializableException as e:
    print(e.to_json())
    # {
    #   "type": "SerializableException",
    #   "code": "FILE_PROCESS_ERROR",
    #   "message": "文件处理失败",
    #   "timestamp": "2023-10-01T12:00:00",
    #   "metadata": {
    #     "filename": "data.txt",
    #     "size": 1024,
    #     "attempts": 3
    #   }
    # }
    # 也可以存储到文件或发送到日志系统
    with open("error_log.json", "w") as f:
        f.write(e.to_json())
```
### 3.4.3 支持多语言错误消息
```python
class InternationalizedException(Exception):
    """支持国际化的异常"""
    # 错误消息模板（可以在运行时加载）
    MESSAGES = {
        "en": {
            "USER_NOT_FOUND": "User {user_id} not found",
            "INVALID_EMAIL": "Invalid email address: {email}",
            "PERMISSION_DENIED": "Permission denied for {action}"
        },
        "zh": {
            "USER_NOT_FOUND": "用户 {user_id} 不存在",
            "INVALID_EMAIL": "无效的邮箱地址: {email}",
            "PERMISSION_DENIED": "没有执行 {action} 的权限"
        }
    }
    def __init__(self, error_key, locale="en", **kwargs):
        self.error_key = error_key
        self.locale = locale
        self.params = kwargs
        # 获取本地化消息
        message_template = self._get_message_template(error_key, locale)
        message = message_template.format(**kwargs)
        super().__init__(message)
    def _get_message_template(self, error_key, locale):
        """获取本地化消息模板"""
        if locale in self.MESSAGES and error_key in self.MESSAGES[locale]:
            return self.MESSAGES[locale][error_key]
        # 回退到英文
        return self.MESSAGES["en"].get(error_key, f"Unknown error: {error_key}")
    def with_locale(self, locale):
        """切换到指定语言"""
        return InternationalizedException(
            self.error_key, locale=locale, **self.params
        )
# 使用
try:
    raise InternationalizedException(
        "USER_NOT_FOUND", user_id=123, locale="zh"
    )
except InternationalizedException as e:
    print(e)                      # 用户 123 不存在
    print(e.with_locale("en"))    # User 123 not found
```
## 3.5 实际应用场景
### 3.5.1 Web API 错误处理
```python
from fastapi import HTTPException
from typing import Optional
class APIError(HTTPException):
    """API错误异常"""
    def __init__(self, status_code: int, code: str, message: str,
                 details: Optional[dict] = None):
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message,
                "details": details or {}
            }
        )
        self.code = code
        self.message = message
        self.details = details
class NotFoundError(APIError):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            status_code=404,
            code="NOT_FOUND",
            message=f"{resource} not found",
            details={"resource": resource, "id": resource_id}
        )
class BadRequestError(APIError):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            status_code=400,
            code="BAD_REQUEST",
            message=message,
            details=details
        )
```
### 3.5.2 数据库操作异常
```python
class DatabaseException(Exception):
    """数据库异常基类"""
    def __init__(self, message, query=None, params=None):
        super().__init__(message)
        self.query = query
        self.params = params
        self.message = message
    def __str__(self):
        base = super().__str__()
        if self.query:
            base += f"\nQuery: {self.query}"
        if self.params:
            base += f"\nParams: {self.params}"
        return base
class DuplicateEntryError(DatabaseException):
    """唯一约束冲突"""
    pass
class ForeignKeyViolationError(DatabaseException):
    """外键约束冲突"""
    pass
class DeadlockError(DatabaseException):
    """死锁错误"""
    pass
```