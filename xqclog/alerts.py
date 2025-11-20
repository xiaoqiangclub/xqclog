# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 10:00:00 UTC
# 文件描述：告警通知模块，支持钉钉、企业微信等平台
# 文件路径：xqclog/alerts.py

import requests
from typing import Dict, Any, Optional
import json


def send_alert(
        webhook: str,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]] = None
) -> bool:
    """
    发送告警通知

    :param webhook: Webhook地址
    :param level: 日志级别
    :param message: 消息内容
    :param extra: 额外信息
    :return: 是否发送成功
    """
    try:
        # 判断webhook类型
        if "dingtalk" in webhook or "oapi.dingtalk.com" in webhook:
            return _send_dingtalk(webhook, level, message, extra)
        elif "qyapi.weixin.qq.com" in webhook:
            return _send_weixin(webhook, level, message, extra)
        else:
            # 通用webhook
            return _send_generic(webhook, level, message, extra)
    except Exception as e:
        print(f"发送告警失败: {e}")
        return False


def _send_dingtalk(
        webhook: str,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]]
) -> bool:
    """
    发送钉钉通知

    :param webhook: 钉钉Webhook地址
    :param level: 日志级别
    :param message: 消息内容
    :param extra: 额外信息
    :return: 是否发送成功
    """
    # 根据级别设置颜色
    level_colors = {
        "DEBUG": "🔍",
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🚨",
    }

    emoji = level_colors.get(level, "📝")

    # 构造钉钉消息格式
    content = f"{emoji} **{level}级别日志告警**\n\n"
    content += f"**消息**: {message}\n\n"

    if extra:
        content += "**额外信息**:\n"
        for key, value in extra.items():
            content += f"- {key}: {value}\n"

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"{level}级别日志告警",
            "text": content
        }
    }

    response = requests.post(webhook, json=payload, timeout=5)
    return response.status_code == 200


def _send_weixin(
        webhook: str,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]]
) -> bool:
    """
    发送企业微信通知

    :param webhook: 企业微信Webhook地址
    :param level: 日志级别
    :param message: 消息内容
    :param extra: 额外信息
    :return: 是否发送成功
    """
    # 构造企业微信消息格式
    content = f"{level}级别日志告警\n"
    content += f"消息: {message}\n"

    if extra:
        content += "\n额外信息:\n"
        for key, value in extra.items():
            content += f"{key}: {value}\n"

    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    response = requests.post(webhook, json=payload, timeout=5)
    return response.status_code == 200


def _send_generic(
        webhook: str,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]]
) -> bool:
    """
    发送通用webhook通知

    :param webhook: Webhook地址
    :param level: 日志级别
    :param message: 消息内容
    :param extra: 额外信息
    :return: 是否发送成功
    """
    payload = {
        "level": level,
        "message": message,
        "extra": extra or {}
    }

    response = requests.post(webhook, json=payload, timeout=5)
    return response.status_code == 200