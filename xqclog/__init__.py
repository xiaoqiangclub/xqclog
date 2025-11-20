# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 08:00:00 UTC
# 文件描述：xqclog模块的入口文件，提供便捷的导入接口
# 文件路径：xqclog/__init__.py

from .logger import XQCLogger, get_logger, init_logger
from .config import LogConfig
from .presets import Presets
from . import decorators

__version__ = "0.0.1"
__author__ = "Xiaoqiang"
__description__ = "基于Loguru的简易日志模块 - XiaoqiangClub"

__all__ = [
    "XQCLogger",
    "get_logger",
    "init_logger",
    "LogConfig",
    "Presets",
    "decorators",
    "logger",
]

# 提供默认的logger实例，可以直接使用
logger = get_logger()