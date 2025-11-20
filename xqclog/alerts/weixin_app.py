# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 12:00:00 UTC
# 文件描述：企业微信应用消息告警通知器
# 文件路径：xqclog/alerts/weixin_app.py

import requests
import time
from typing import Any, Optional

from .base import BaseNotifier, AlertMessage


class WeixinAppNotifier(BaseNotifier):
    """企业微信应用消息通知器"""

    def __init__(self, **config: Any) -> None:
        """
        初始化企业微信应用通知器

        :param config: 配置参数
            - corpid: 企业ID（必填）
            - corpsecret: 应用的Secret（必填）
            - agentid: 应用的AgentId（必填）
            - touser: 接收消息的用户ID列表，用|分隔（可选，默认@all）
            - toparty: 接收消息的部门ID列表，用|分隔（可选）
            - totag: 接收消息的标签ID列表，用|分隔（可选）
            - enabled: 是否启用（可选，默认True）
            - alert_levels: 触发告警的级别列表（可选）
            - timeout: 请求超时时间（可选，默认5秒）
        """
        super().__init__("weixin_app", **config)

        self.corpid = config.get("corpid")
        self.corpsecret = config.get("corpsecret")
        self.agentid = config.get("agentid")

        if not all([self.corpid, self.corpsecret, self.agentid]):
            raise ValueError("企业微信应用通知器需要配置corpid、corpsecret和agentid参数")

        self.touser = config.get("touser", "@all")
        self.toparty = config.get("toparty", "")
        self.totag = config.get("totag", "")
        self.timeout = config.get("timeout", 5)

        # access_token缓存
        self._access_token: Optional[str] = None
        self._token_expire_time: float = 0

    def _get_access_token(self) -> Optional[str]:
        """
        获取access_token（带缓存）

        :return: access_token或None
        """
        # 检查缓存
        if self._access_token and time.time() < self._token_expire_time:
            return self._access_token

        try:
            # 获取新的access_token
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            params = {
                "corpid": self.corpid,
                "corpsecret": self.corpsecret,
            }

            response = requests.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    self._access_token = result.get("access_token")
                    # 提前5分钟过期
                    expires_in = result.get("expires_in", 7200)
                    self._token_expire_time = time.time() + expires_in - 300
                    print(f"✅ 获取企业微信access_token成功")
                    return self._access_token
                else:
                    print(f"❌ 获取企业微信access_token失败: {result.get('errmsg')}")
                    return None
            else:
                print(f"❌ 获取企业微信access_token失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ 获取企业微信access_token异常: {e}")
            import traceback
            traceback.print_exc()
            return None

    def send(self, alert_msg: AlertMessage) -> bool:
        """
        发送企业微信应用消息

        :param alert_msg: 告警消息对象
        :return: 是否发送成功
        """
        try:
            # 获取access_token
            access_token = self._get_access_token()
            if not access_token:
                return False

            # 构造markdown消息内容
            content = f"## {alert_msg.level}级别日志告警\n\n"
            content += f"**时间**: {alert_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"**消息**: {alert_msg.message}\n"

            if alert_msg.module or alert_msg.function or alert_msg.line:
                content += "\n### 位置信息\n"
                if alert_msg.module:
                    content += f"- 模块: `{alert_msg.module}`\n"
                if alert_msg.function:
                    content += f"- 函数: `{alert_msg.function}`\n"
                if alert_msg.line:
                    content += f"- 行号: `{alert_msg.line}`\n"

            if alert_msg.extra:
                content += "\n### 额外信息\n"
                for key, value in alert_msg.extra.items():
                    if key.startswith('_'):
                        continue
                    content += f"- {key}: {value}\n"

            # 构造请求数据（使用markdown消息）
            data = {
                "touser": self.touser,
                "toparty": self.toparty,
                "totag": self.totag,
                "msgtype": "markdown",
                "agentid": self.agentid,
                "markdown": {
                    "content": content
                }
            }

            # 发送请求
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            response = requests.post(url, json=data, timeout=self.timeout)

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    print(f"✅ 企业微信应用消息发送成功: {alert_msg.level} - {alert_msg.message[:50]}")
                    return True
                else:
                    print(f"❌ 企业微信应用消息发送失败: {result.get('errmsg')}")
                    return False
            else:
                print(f"❌ 企业微信应用消息发送失败: HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ 企业微信应用消息发送异常: {e}")
            import traceback
            traceback.print_exc()
            return False