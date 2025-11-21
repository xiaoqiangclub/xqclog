# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 08:00:00 UTC
# 文件描述：xqclog模块的入口文件，提供便捷的导入接口
# 文件路径：xqclog/__init__.py

from .logger import XQCLogger, get_logger, init_logger
from .config import LogConfig
from .presets import Presets
from . import decorators

from .alerts.email import EmailNotifier
from .alerts.dingtalk import DingTalkNotifier
from .alerts.weixin_app import WeixinAppNotifier
from .alerts.weixin_webhook import WeixinWebhookNotifier

__version__ = "0.0.3"
__author__ = "Xiaoqiang"
__description__ = "⚡ 基于 Loguru 的自用 Python 日志模块 - 开箱即用"

__all__ = [
    "XQCLogger",
    "get_logger",
    "init_logger",
    "LogConfig",
    "Presets",
    "decorators",
    "logger",

    # 告警通知类
    "EmailNotifier",
    "DingTalkNotifier",
    "WeixinAppNotifier",
    "WeixinWebhookNotifier",
]

# 静默初始化 - 开箱即用（使用 LogConfig 的默认配置）
# 配置说明：
# - 只输出到控制台（不创建目录和文件）
# - DEBUG 级别（显示所有日志）
# - 启用彩色输出
# - 不输出初始化提示信息（静默初始化）
logger = init_logger(silent=True)
