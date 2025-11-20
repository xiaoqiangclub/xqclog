# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 12:00:00 UTC
# 文件描述：告警通知的抽象基类，定义通知器接口
# 文件路径：xqclog/alerts/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class AlertMessage:
    """告警消息数据类"""

    def __init__(
            self,
            level: str,
            message: str,
            timestamp: Optional[datetime] = None,
            extra: Optional[Dict[str, Any]] = None,
            module: Optional[str] = None,
            function: Optional[str] = None,
            line: Optional[int] = None,
            force_send: Optional[bool] = None,  # 新增：强制发送标志
    ) -> None:
        """
        初始化告警消息

        :param level: 日志级别
        :param message: 消息内容
        :param timestamp: 时间戳
        :param extra: 额外信息
        :param module: 模块名
        :param function: 函数名
        :param line: 行号
        :param force_send: 强制发送标志（True=强制发送, False=强制不发送, None=根据级别判断）
        """
        self.level = level
        self.message = message
        self.timestamp = timestamp or datetime.now()
        self.extra = extra or {}
        self.module = module
        self.function = function
        self.line = line
        self.force_send = force_send  # 新增

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        :return: 字典表示
        """
        return {
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "extra": self.extra,
            "module": self.module,
            "function": self.function,
            "line": self.line,
            "force_send": self.force_send,  # 新增
        }


class BaseNotifier(ABC):
    """告警通知器抽象基类"""

    def __init__(self, name: str, **config: Any) -> None:
        """
        初始化通知器

        :param name: 通知器名称
        :param config: 配置参数
        """
        self.name = name
        self.config = config
        self.enabled = config.get("enabled", True)

    @abstractmethod
    def send(self, alert_msg: AlertMessage) -> bool:
        """
        发送告警通知

        :param alert_msg: 告警消息对象
        :return: 是否发送成功
        """
        pass

    def should_send(self, alert_msg: AlertMessage) -> bool:
        """
        判断是否应该发送此告警

        :param alert_msg: 告警消息对象
        :return: 是否应该发送
        """
        # 1. 检查通知器是否启用
        if not self.enabled:
            return False

        # 2. 最高优先级：检查强制发送标志
        if alert_msg.force_send is not None:
            return alert_msg.force_send

        # 3. 检查级别过滤
        alert_levels = self.config.get("alert_levels")

        # 如果 alert_levels 为 None，表示默认不发送（除非强制发送）
        if alert_levels is None:
            return False

        # 如果 alert_levels 是空列表，也表示不发送
        if not alert_levels:
            return False

        # 检查当前日志级别是否在配置的告警级别中
        if alert_msg.level not in alert_levels:
            return False

        return True

    def format_message(self, alert_msg: AlertMessage) -> str:
        """
        格式化消息（可被子类覆盖）

        :param alert_msg: 告警消息对象
        :return: 格式化后的消息
        """
        parts = [
            f"级别: {alert_msg.level}",
            f"时间: {alert_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"消息: {alert_msg.message}",
        ]

        if alert_msg.module:
            parts.append(f"模块: {alert_msg.module}")
        if alert_msg.function:
            parts.append(f"函数: {alert_msg.function}")
        if alert_msg.line:
            parts.append(f"行号: {alert_msg.line}")

        if alert_msg.extra:
            parts.append("\n额外信息:")
            for key, value in alert_msg.extra.items():
                parts.append(f"  {key}: {value}")

        return "\n".join(parts)