# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 10:00:00 UTC
# 文件描述：日志装饰器，提供便捷的函数日志记录功能
# 文件路径：xqclog/decorators.py

import time
import functools
from typing import Callable, Any, Optional


def log_execution(
        level: str = "INFO",
        log_args: bool = True,
        log_result: bool = False,
        log_time: bool = True
) -> Callable:
    """
    记录函数执行的装饰器

    :param level: 日志级别
    :param log_args: 是否记录函数参数
    :param log_result: 是否记录函数返回值
    :param log_time: 是否记录执行时间
    :return: 装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from .logger import get_logger
            logger = get_logger()
            func_name = f"{func.__module__}.{func.__name__}"

            # 记录开始
            msg_parts = [f"执行函数: {func_name}"]
            if log_args and (args or kwargs):
                msg_parts.append(f"参数: args={args}, kwargs={kwargs}")

            logger.log(level, " | ".join(msg_parts))

            # 执行函数
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                # 记录成功
                success_parts = [f"函数执行成功: {func_name}"]
                if log_time:
                    success_parts.append(f"耗时: {elapsed:.4f}秒")
                if log_result:
                    success_parts.append(f"返回值: {result}")

                logger.log(level, " | ".join(success_parts))
                return result

            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"函数执行失败: {func_name} | "
                    f"耗时: {elapsed:.4f}秒 | "
                    f"错误: {str(e)}"
                )
                raise

        return wrapper

    return decorator


def catch_errors(
        level: str = "ERROR",
        reraise: bool = True,
        default_return: Any = None
) -> Callable:
    """
    捕获并记录异常的装饰器

    :param level: 日志级别
    :param reraise: 是否重新抛出异常
    :param default_return: 发生异常时的默认返回值
    :return: 装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from .logger import get_logger
            logger = get_logger()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                func_name = f"{func.__module__}.{func.__name__}"
                logger.log(
                    level,
                    f"函数 {func_name} 发生异常: {str(e)}"
                )
                logger.exception(f"异常详情:")

                if reraise:
                    raise
                return default_return

        return wrapper

    return decorator


def timer(name: Optional[str] = None, level: str = "INFO") -> Callable:
    """
    计时装饰器

    :param name: 计时器名称
    :param level: 日志级别
    :return: 装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            from .logger import get_logger
            logger = get_logger()
            timer_name = name or f"{func.__module__}.{func.__name__}"

            start_time = time.time()
            logger.log(level, f"⏱️  开始计时: {timer_name}")

            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.log(level, f"⏱️  {timer_name} 执行完成，耗时: {elapsed:.4f}秒")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"⏱️  {timer_name} 执行失败，耗时: {elapsed:.4f}秒")
                raise

        return wrapper

    return decorator