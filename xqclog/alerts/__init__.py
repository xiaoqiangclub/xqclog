# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 12:00:00 UTC
# 文件描述：告警模块的入口文件
# 文件路径：xqclog/alerts/__init__.py

from .base import BaseNotifier, AlertMessage
from .dingtalk import DingTalkNotifier
from .weixin_webhook import WeixinWebhookNotifier
from .weixin_app import WeixinAppNotifier
from .email import EmailNotifier
from .manager import AlertManager, get_alert_manager
from .registry import NotifierRegistry

__all__ = [
    "BaseNotifier",
    "AlertMessage",
    "DingTalkNotifier",
    "WeixinWebhookNotifier",
    "WeixinAppNotifier",
    "EmailNotifier",  # 新增
    "AlertManager",
    "get_alert_manager",
    "NotifierRegistry",
]