import time
import functools
import logging
from enum import Enum
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
import sys
from typing import Union, Optional


class LogLevel(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


_LEVEL_MAP = {
    LogLevel.DEBUG: logging.DEBUG,
    LogLevel.INFO: logging.INFO,
    LogLevel.WARNING: logging.WARNING,
    LogLevel.ERROR: logging.ERROR,
    LogLevel.CRITICAL: logging.CRITICAL,
}

# 使用集合记录已配置的logger，避免重复配置
_CONFIGURED_LOGGERS = set()


def setup_logger(
        name: str = __name__,
        log_file: str = './logs/app.log',
        log_level: LogLevel = LogLevel.INFO,
        log_format_file: str = '%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s:Line %(lineno)d | %(message)s',
        log_format_console: str = '%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s:Line %(lineno)d | %(message)s',
        log_file_open: bool = True,
        log_console_open: bool = True,
        log_file_level: Union[LogLevel, None] = None,
        log_console_level: Union[LogLevel, None] = None,
        when: str = 'midnight',  # 按天轮转
        backup_count: int = 30,  # 保留30天
) -> logging.Logger:
    """设置日志记录器
    如何使用：

    # ##############################################################
    from log_config import setup_logger, LogLevel
    my_logger = setup_logger(
        log_file='file.log',
        log_console_level=LogLevel.ERROR,
        log_file_level=LogLevel.DEBUG,
    )

    my_logger.info('这是一条 info 日志.')
    my_logger.error('这是一条 error 日志.')
    ...
    # ##############################################################

    Args:
        name ():
        log_file ():
        log_level ():
        log_format_file ():
        log_format_console ():
        log_file_open ():
        log_console_open ():
        log_file_level ():
        log_console_level ():
        when ():
        backup_count ():

    Returns:

    """
    # 创建 Logger
    logger: logging.Logger = logging.getLogger(name)

    # 如果已经配置过，直接返回现有的logger
    if name in _CONFIGURED_LOGGERS:
        return logger

    # 确保日志目录存在
    if log_file_open:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # 设置logger级别为最宽松的，实际级别由handlers控制
    logger.setLevel(logging.DEBUG)

    # 清除现有的handlers（如果有的话）
    logger.handlers.clear()

    # 控制台 handler
    if log_console_open:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(log_format_console))
        console_level = log_console_level if log_console_level is not None else log_level
        console_handler.setLevel(_LEVEL_MAP[console_level])
        logger.addHandler(console_handler)

    # File handler - 使用 TimedRotatingFileHandler 替代 FileHandler
    if log_file_open:
        try:
            # 创建按时间轮转的文件处理器
            file_handler = TimedRotatingFileHandler(
                filename=log_file,
                when=when,
                backupCount=backup_count,
                encoding='utf-8',
                delay=False,  # 立即打开文件
            )
            file_handler.setFormatter(logging.Formatter(log_format_file))
            file_level = log_file_level if log_file_level is not None else log_level
            file_handler.setLevel(_LEVEL_MAP[file_level])
            logger.addHandler(file_handler)
        except Exception as e:
            # 如果文件handler创建失败，只使用控制台handler
            print(f"Failed to create file handler: {e}")
            if not log_console_open:
                # 如果没有控制台handler，添加一个临时的
                fallback_handler = logging.StreamHandler(sys.stdout)
                fallback_handler.setFormatter(logging.Formatter(log_format_console))
                fallback_handler.setLevel(_LEVEL_MAP[log_level])
                logger.addHandler(fallback_handler)

    # 如果没有添加任何handler，添加一个NullHandler避免警告
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    # 设置 propagate 为 False，避免日志重复输出
    logger.propagate = False

    # 记录已配置的logger
    _CONFIGURED_LOGGERS.add(name)

    return logger


# 装饰器版本，用于为函数添加日志记录
def log_function_call(
        logger: Optional[logging.Logger] = None,
        level: LogLevel = LogLevel.DEBUG,
        log_args: bool = True,
        log_result: bool = True
):
    """装饰器，用于记录函数调用
    如何使用：
    # #############################################################
    # Define function ...
    @log_function_call(logger=your_logger)
    def your_func():
        # do something  ...

    # Call function ...
    your_func()
    # #############################################################

    Args:
        logger: 日志记录器，如果为None则使用函数模块的logger
        level: 日志级别，默认为INFO
        log_args: 是否记录函数参数
        log_result: 是否记录函数返回值
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取logger
            _logger = logger or logging.getLogger(func.__module__)

            # 获取日志方法
            log_method = getattr(_logger, level.value)

            # 构建日志消息
            func_name = func.__name__
            args_info = ""

            if log_args:
                args_list = [repr(arg) for arg in args]
                kwargs_list = [f"{k} = {repr(v)}" for k, v in kwargs.items()]
                all_args = ", ".join(args_list + kwargs_list)
                args_info = f" 参数: {all_args}"

            # 记录开始
            log_method(f"开始调用函数: {func_name}, {args_info}")

            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.perf_counter() - start_time

                # 记录成功
                result_info = ""
                if log_result and result is not None:
                    result_str = repr(result)
                    if len(result_str) > 100:
                        result_str = result_str[:100] + "..."
                    result_info = f" 返回: {result_str}"

                log_method(f"函数 {func_name} 执行成功，耗时: {elapsed_time:.6f}秒, {result_info}")
                return result

            except Exception as e:
                elapsed_time = time.perf_counter() - start_time
                _logger.exception(f"函数 {func_name} 执行失败，耗时: {elapsed_time:.6f}秒，错误类型: {type(e).__name__}")
                raise

        return wrapper

    return decorator


if __name__ == '__main__':
    # 创建一个logger，控制台只输出ERROR及以上，文件记录DEBUG及以上
    my_logger = setup_logger(
        name='my_app',
        log_file='file.log',
        log_console_level=LogLevel.ERROR,  # 控制台只输出ERROR及以上
        log_file_level=LogLevel.DEBUG  # 文件记录DEBUG及以上
    )


    @log_function_call(logger=my_logger)
    def main():
        print('This is main function.')
        time.sleep(0.1)  # 添加一点延迟以便看到耗时
        return 42


    @log_function_call(logger=my_logger)
    def add_numbers(a, b=10):
        """测试函数"""
        result = a + b
        print(f"Result: {a} + {b} = {result}")
        return result


    @log_function_call(logger=my_logger)
    def test_error():
        raise RuntimeError()


    print("=== 控制台输出（只显示ERROR及以上）===")
    # 运行装饰器函数 - 这些DEBUG和INFO级别日志不会显示在控制台，但会记录到文件
    main()
    print()
    add_numbers(10, b=20)
    print()
    test_error()

    print("\n=== 直接调用logger方法 ===")
    # 这些日志也不会显示在控制台（因为级别低于ERROR），但会记录到文件
    my_logger.debug('这是一个 debug 信息')
    my_logger.info('这是一个 info 信息')
    my_logger.warning('这是一个 warning 信息')
    my_logger.error('这是一个 error 信息 - 这会显示在控制台')
    my_logger.critical('这是一个 critical 信息 - 这会显示在控制台')

    print("\n=== 检查日志文件 ===")
    print("请查看 file.log 文件，应该包含所有级别的日志（DEBUG及以上）")

# END
