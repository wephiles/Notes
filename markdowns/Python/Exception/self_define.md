<h1 style="text-align: center;">自定义异常</h1>

# 一、基础自定义异常

## 1.1 最简单的自定义异常

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
    pass


if __name__ == '__main__':
    main()
```

控制台输出情况：
```
18
Traceback (most recent call last):
  File "D:\project\WorkJinYu\AdTimeV10\main.py", line 21, in <module>
    main()
    ~~~~^^
  File "D:\project\WorkJinYu\AdTimeV10\main.py", line 16, in main
    print(get_age(-12))
          ~~~~~~~^^^^^
  File "D:\project\WorkJinYu\AdTimeV10\main.py", line 10, in get_age
    raise MyException('年龄是负数')
MyException: 年龄是负数
```

## 1.2 带自定义属性的异常

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
    pass


if __name__ == '__main__':
    main()
```

运行上述脚本，控制台输出：

```python
Traceback (most recent call last):
  File "D:\project\WorkJinYu\AdTimeV10\main.py", line 38, in <module>
    main()
    ~~~~^^
  File "D:\project\WorkJinYu\AdTimeV10\main.py", line 33, in main
    invalid_email('error@email', '11123456789')
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\project\WorkJinYu\AdTimeV10\main.py", line 24, in invalid_email
    raise MyException(
    ...<3 lines>...
    )
MyException: 字段 phone 的值 11123456789 无效: 手机号不是以"+86"开头
```

# 二、完整自定义异常类实现

## 2.1 带错误码和时间戳的异常

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

    def __init__(self,
                 message,
                 error_code: int = 500,
                 details: dict | None = None,
                 cause: Exception | None = None
                 ):
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


# 使用示例
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

# 三、异常继承的层级结构

## 3.1 创建有层次的异常体系

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
    """数据验证错误"""
    status_code = 422
    default_message = "数据验证失败"

class AuthenticationError(ClientError):
    """认证错误"""
    status_code = 401
    default_message = "认证失败"

class AuthorizationError(ClientError):
    """授权错误"""
    status_code = 403
    default_message = "权限不足"

# 服务器错误 (5xx)
class ServerError(APIException):
    """服务器错误基类"""
    status_code = 500
    default_message = "服务器内部错误"

class DatabaseError(ServerError):
    """数据库错误"""
    status_code = 503
    default_message = "数据库操作失败"

class ExternalServiceError(ServerError):
    """外部服务错误"""
    status_code = 502
    default_message = "外部服务不可用"

# 使用
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

# 四、高级功能实现

## 4.1 支持异常链和上下文

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

## 4.2 可序列化的异常

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

## 4.3 支持多语言错误消息

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
            self.error_key,
            locale=locale,
            **self.params
        )

# 使用
try:
    raise InternationalizedException(
        "USER_NOT_FOUND",
        user_id=123,
        locale="zh"
    )
except InternationalizedException as e:
    print(e)  # 用户 123 不存在
    
    # 切换到英文
    print(e.with_locale("en"))  # User 123 not found
```

# 五、实际应用场景

## 5.1 Web API 错误处理

```python
from fastapi import HTTPException
from typing import Optional

class APIError(HTTPException):
    """API错误异常"""
    
    def __init__(self, 
                 status_code: int,
                 code: str,
                 message: str,
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

## 5.2 数据库操作异常

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













































































































































































