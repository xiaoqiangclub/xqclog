# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 12:00:00 UTC
# 文件描述：企业微信群机器人Webhook告警通知器
# 文件路径：xqclog/alerts/weixin_webhook.py

import requests
from typing import Any

from .base import BaseNotifier, AlertMessage


class WeixinWebhookNotifier(BaseNotifier):
    """企业微信群机器人Webhook通知器"""

    def __init__(self, **config: Any) -> None:
        """
        初始化企业微信Webhook通知器

        :param config: 配置参数
            - webhook: 企业微信机器人Webhook地址（必填）
            - mentioned_list: @的成员ID列表（可选）
            - mentioned_mobile_list: @的手机号列表（可选）
            - enabled: 是否启用（可选，默认True）
            - alert_levels: 触发告警的级别列表（可选）
            - timeout: 请求超时时间（可选，默认5秒）
        """
        super().__init__("weixin_webhook", **config)

        self.webhook = config.get("webhook")
        if not self.webhook:
            raise ValueError("企业微信Webhook通知器需要配置webhook参数")

        self.mentioned_list = config.get("mentioned_list", [])
        self.mentioned_mobile_list = config.get("mentioned_mobile_list", [])
        self.timeout = config.get("timeout", 5)

    def send(self, alert_msg: AlertMessage) -> bool:
        """
        发送企业微信Webhook通知

        :param alert_msg: 告警消息对象
        :return: 是否发送成功
        """
        if not self.should_send(alert_msg.level):
            return False

        try:
            # 根据级别设置emoji
            level_emojis = {
                "DEBUG": "🔍",
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "WARNING": "⚠️",
                "ERROR": "❌",
                "CRITICAL": "🚨",
            }
            emoji = level_emojis.get(alert_msg.level, "📝")

            # 构造Markdown消息
            content = f"## {emoji} <font color=\"warning\">{alert_msg.level}级别日志告警</font>\n"
            content += f">时间: {alert_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f">消息: <font color=\"comment\">{alert_msg.message}</font>\n"

            if alert_msg.module or alert_msg.function or alert_msg.line:
                content += "\n**位置信息**\n"
                if alert_msg.module:
                    content += f">模块: {alert_msg.module}\n"
                if alert_msg.function:
                    content += f">函数: {alert_msg.function}\n"
                if alert_msg.line:
                    content += f">行号: {alert_msg.line}\n"

            if alert_msg.extra:
                content += "\n**额外信息**\n"
                for key, value in alert_msg.extra.items():
                    content += f">{key}: {value}\n"

            # 构造请求数据
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content,
                    "mentioned_list": self.mentioned_list,
                    "mentioned_mobile_list": self.mentioned_mobile_list,
                }
            }

            # 发送请求
            response = requests.post(
                self.webhook,
                json=data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    return True
                else:
                    print(f"企业微信Webhook通知发送失败: {result.get('errmsg')}")
                    return False
            else:
                print(f"企业微信Webhook通知发送失败: HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"企业微信Webhook通知发送异常: {e}")
            return False