# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 12:00:00 UTC
# 文件描述：钉钉机器人告警通知器
# 文件路径：xqclog/alerts/dingtalk.py

import requests
import hmac
import hashlib
import base64
import time
from typing import Any
from urllib.parse import quote_plus

from .base import BaseNotifier, AlertMessage


class DingTalkNotifier(BaseNotifier):
    """钉钉机器人通知器"""

    def __init__(self, **config: Any) -> None:
        """
        初始化钉钉通知器

        :param config: 配置参数
            - webhook: 钉钉机器人Webhook地址（必填）
            - secret: 钉钉机器人密钥（可选，用于签名）
            - at_mobiles: @的手机号列表（可选）
            - at_all: 是否@所有人（可选，默认False）
            - enabled: 是否启用（可选，默认True）
            - alert_levels: 触发告警的级别列表（可选）
            - timeout: 请求超时时间（可选，默认5秒）
        """
        super().__init__("dingtalk", **config)

        self.webhook = config.get("webhook")
        if not self.webhook:
            raise ValueError("钉钉通知器需要配置webhook参数")

        self.secret = config.get("secret")
        self.at_mobiles = config.get("at_mobiles", [])
        self.at_all = config.get("at_all", False)
        self.timeout = config.get("timeout", 5)

    def _generate_sign(self) -> tuple:
        """
        生成签名

        :return: (timestamp, sign)
        """
        if not self.secret:
            return None, None

        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256
        ).digest()
        sign = quote_plus(base64.b64encode(hmac_code))

        return timestamp, sign

    def send(self, alert_msg: AlertMessage) -> bool:
        """
        发送钉钉通知

        :param alert_msg: 告警消息对象
        :return: 是否发送成功
        """
        # ✅ 删除这里的 should_send 检查，因为在 manager 中已经统一检查了

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
            content = f"## {emoji} {alert_msg.level}级别日志告警\n\n"
            content += f"**时间**: {alert_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            content += f"**消息**: {alert_msg.message}\n\n"

            if alert_msg.module or alert_msg.function or alert_msg.line:
                content += "**位置信息**:\n"
                if alert_msg.module:
                    content += f"- 模块: {alert_msg.module}\n"
                if alert_msg.function:
                    content += f"- 函数: {alert_msg.function}\n"
                if alert_msg.line:
                    content += f"- 行号: {alert_msg.line}\n"
                content += "\n"

            if alert_msg.extra:
                content += "**额外信息**:\n"
                for key, value in alert_msg.extra.items():
                    # 跳过内部使用的 _alert 字段
                    if key.startswith('_'):
                        continue
                    content += f"- {key}: {value}\n"

            # 构造请求数据
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"{alert_msg.level}级别告警",
                    "text": content
                },
                "at": {
                    "atMobiles": self.at_mobiles,
                    "isAtAll": self.at_all
                }
            }

            # 添加签名
            url = self.webhook
            if self.secret:
                timestamp, sign = self._generate_sign()
                url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"

            # 发送请求
            response = requests.post(
                url,
                json=data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    print(f"✅ 钉钉通知发送成功: {alert_msg.level} - {alert_msg.message[:50]}")
                    return True
                else:
                    print(f"❌ 钉钉通知发送失败: {result.get('errmsg')}")
                    return False
            else:
                print(f"❌ 钉钉通知发送失败: HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ 钉钉通知发送异常: {e}")
            import traceback
            traceback.print_exc()
            return False