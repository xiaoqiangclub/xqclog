# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 14:00:00 UTC
# 文件描述：邮件告警通知器
# 文件路径：xqclog/alerts/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Any, List, Union

from .base import BaseNotifier, AlertMessage


class EmailNotifier(BaseNotifier):
    """邮件通知器"""

    def __init__(self, **config: Any) -> None:
        """
        初始化邮件通知器

        :param config: 配置参数
            - smtp_host: SMTP服务器地址（必填）
            - smtp_port: SMTP服务器端口（可选，默认25，SSL默认465）
            - smtp_user: SMTP用户名（必填）
            - smtp_password: SMTP密码（必填）
            - use_ssl: 是否使用SSL（可选，默认False）
            - use_tls: 是否使用TLS（可选，默认False）
            - from_addr: 发件人地址（可选，默认使用smtp_user）
            - from_name: 发件人名称（可选）
            - to_addrs: 收件人地址列表（必填）
            - cc_addrs: 抄送地址列表（可选）
            - subject_prefix: 邮件主题前缀（可选，默认"[日志告警]"）
            - enabled: 是否启用（可选，默认True）
            - alert_levels: 触发告警的级别列表（可选）
            - timeout: 发送超时时间（可选，默认10秒）
        """
        super().__init__("email", **config)

        self.smtp_host = config.get("smtp_host")
        self.smtp_port = config.get("smtp_port", 465 if config.get("use_ssl") else 25)
        self.smtp_user = config.get("smtp_user")
        self.smtp_password = config.get("smtp_password")

        if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
            raise ValueError("邮件通知器需要配置smtp_host、smtp_user和smtp_password参数")

        self.use_ssl = config.get("use_ssl", False)
        self.use_tls = config.get("use_tls", False)
        self.from_addr = config.get("from_addr", self.smtp_user)
        self.from_name = config.get("from_name", "XQCLog")

        self.to_addrs = config.get("to_addrs", [])
        if isinstance(self.to_addrs, str):
            self.to_addrs = [self.to_addrs]
        if not self.to_addrs:
            raise ValueError("邮件通知器需要配置to_addrs参数（收件人列表）")

        self.cc_addrs = config.get("cc_addrs", [])
        if isinstance(self.cc_addrs, str):
            self.cc_addrs = [self.cc_addrs]

        self.subject_prefix = config.get("subject_prefix", "[日志告警]")
        self.timeout = config.get("timeout", 10)

    def _create_message(self, alert_msg: AlertMessage) -> MIMEMultipart:
        """
        创建邮件消息

        :param alert_msg: 告警消息对象
        :return: 邮件消息对象
        """
        # 创建邮件对象
        message = MIMEMultipart('alternative')

        # 设置主题
        subject = f"{self.subject_prefix} {alert_msg.level}级别告警"
        message['Subject'] = Header(subject, 'utf-8')

        # 设置发件人
        if self.from_name:
            message['From'] = Header(f"{self.from_name} <{self.from_addr}>", 'utf-8')
        else:
            message['From'] = self.from_addr

        # 设置收件人
        message['To'] = ", ".join(self.to_addrs)

        # 设置抄送
        if self.cc_addrs:
            message['Cc'] = ", ".join(self.cc_addrs)

        # 构造纯文本内容
        text_content = self._format_text_content(alert_msg)
        text_part = MIMEText(text_content, 'plain', 'utf-8')

        # 构造HTML内容
        html_content = self._format_html_content(alert_msg)
        html_part = MIMEText(html_content, 'html', 'utf-8')

        # 添加内容（先添加纯文本，再添加HTML）
        message.attach(text_part)
        message.attach(html_part)

        return message

    def _format_text_content(self, alert_msg: AlertMessage) -> str:
        """
        格式化纯文本邮件内容

        :param alert_msg: 告警消息对象
        :return: 纯文本内容
        """
        lines = [
            f"【{alert_msg.level}级别日志告警】",
            "",
            f"时间: {alert_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"级别: {alert_msg.level}",
            f"消息: {alert_msg.message}",
            "",
        ]

        if alert_msg.module or alert_msg.function or alert_msg.line:
            lines.append("位置信息:")
            if alert_msg.module:
                lines.append(f"  模块: {alert_msg.module}")
            if alert_msg.function:
                lines.append(f"  函数: {alert_msg.function}")
            if alert_msg.line:
                lines.append(f"  行号: {alert_msg.line}")
            lines.append("")

        if alert_msg.extra:
            lines.append("额外信息:")
            for key, value in alert_msg.extra.items():
                lines.append(f"  {key}: {value}")
            lines.append("")

        lines.append("---")
        lines.append("此邮件由 XQCLog 日志系统自动发送")

        return "\n".join(lines)

    def _format_html_content(self, alert_msg: AlertMessage) -> str:
        """
        格式化HTML邮件内容

        :param alert_msg: 告警消息对象
        :return: HTML内容
        """
        # 根据级别设置颜色
        level_colors = {
            "DEBUG": "#6c757d",
            "INFO": "#0dcaf0",
            "SUCCESS": "#198754",
            "WARNING": "#ffc107",
            "ERROR": "#dc3545",
            "CRITICAL": "#8b0000",
        }
        color = level_colors.get(alert_msg.level, "#6c757d")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Microsoft YaHei', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: {color};
                    color: white;
                    padding: 20px;
                    border-radius: 5px 5px 0 0;
                    text-align: center;
                }}
                .content {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border: 1px solid #dee2e6;
                    border-top: none;
                }}
                .info-item {{
                    margin-bottom: 10px;
                    padding: 8px;
                    background-color: white;
                    border-left: 3px solid {color};
                }}
                .label {{
                    font-weight: bold;
                    color: {color};
                }}
                .section {{
                    margin-top: 15px;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 10px;
                    border-top: 1px solid #dee2e6;
                    text-align: center;
                    color: #6c757d;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🚨 {alert_msg.level}级别日志告警</h2>
            </div>
            <div class="content">
                <div class="info-item">
                    <span class="label">时间:</span> {alert_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
                </div>
                <div class="info-item">
                    <span class="label">级别:</span> {alert_msg.level}
                </div>
                <div class="info-item">
                    <span class="label">消息:</span> {alert_msg.message}
                </div>
        """

        # 位置信息
        if alert_msg.module or alert_msg.function or alert_msg.line:
            html += '<div class="section"><strong>位置信息:</strong><br>'
            if alert_msg.module:
                html += f'<div class="info-item">模块: {alert_msg.module}</div>'
            if alert_msg.function:
                html += f'<div class="info-item">函数: {alert_msg.function}</div>'
            if alert_msg.line:
                html += f'<div class="info-item">行号: {alert_msg.line}</div>'
            html += '</div>'

        # 额外信息
        if alert_msg.extra:
            html += '<div class="section"><strong>额外信息:</strong><br>'
            for key, value in alert_msg.extra.items():
                html += f'<div class="info-item">{key}: {value}</div>'
            html += '</div>'

        html += """
            </div>
            <div class="footer">
                此邮件由 XQCLog 日志系统自动发送，请勿回复
            </div>
        </body>
        </html>
        """

        return html

    def send(self, alert_msg: AlertMessage) -> bool:
        """
        发送邮件告警

        :param alert_msg: 告警消息对象
        :return: 是否发送成功
        """
        if not self.should_send(alert_msg.level):
            return False

        try:
            # 创建邮件消息
            message = self._create_message(alert_msg)

            # 所有收件人（包括抄送）
            all_recipients = self.to_addrs + self.cc_addrs

            # 连接SMTP服务器并发送
            if self.use_ssl:
                with smtplib.SMTP_SSL(
                        self.smtp_host,
                        self.smtp_port,
                        timeout=self.timeout
                ) as smtp:
                    smtp.login(self.smtp_user, self.smtp_password)
                    smtp.send_message(message, self.from_addr, all_recipients)
            else:
                with smtplib.SMTP(
                        self.smtp_host,
                        self.smtp_port,
                        timeout=self.timeout
                ) as smtp:
                    if self.use_tls:
                        smtp.starttls()
                    smtp.login(self.smtp_user, self.smtp_password)
                    smtp.send_message(message, self.from_addr, all_recipients)

            return True

        except Exception as e:
            print(f"邮件告警发送失败: {e}")
            return False