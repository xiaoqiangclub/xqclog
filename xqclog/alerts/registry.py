# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 12:00:00 UTC
# 文件描述：通知器注册表，管理内置和自定义通知器
# 文件路径：xqclog/alerts/registry.py

from typing import Dict, Type, Optional

from .base import BaseNotifier


class NotifierRegistry:
    """通知器注册表"""

    def __init__(self) -> None:
        """初始化注册表"""
        self._registry: Dict[str, Type[BaseNotifier]] = {}
        self._register_builtin()

    def _register_builtin(self) -> None:
        """注册内置通知器"""
        from .dingtalk import DingTalkNotifier
        from .weixin_webhook import WeixinWebhookNotifier
        from .weixin_app import WeixinAppNotifier
        from .email import EmailNotifier  # 新增

        self._registry["dingtalk"] = DingTalkNotifier
        self._registry["weixin_webhook"] = WeixinWebhookNotifier
        self._registry["weixin_app"] = WeixinAppNotifier
        self._registry["email"] = EmailNotifier  # 新增

    def register(
            self,
            name: str,
            notifier_class: Type[BaseNotifier]
    ) -> None:
        """
        注册通知器

        :param name: 通知器名称
        :param notifier_class: 通知器类
        """
        if not issubclass(notifier_class, BaseNotifier):
            raise TypeError(f"{notifier_class} 必须继承自 BaseNotifier")

        self._registry[name] = notifier_class

    def get(self, name: str) -> Optional[Type[BaseNotifier]]:
        """
        获取通知器类

        :param name: 通知器名称
        :return: 通知器类或None
        """
        return self._registry.get(name)

    def list_all(self) -> list:
        """
        列出所有已注册的通知器名称

        :return: 通知器名称列表
        """
        return list(self._registry.keys())