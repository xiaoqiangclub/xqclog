# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 14:00:00 UTC
# 文件描述：生产环境完整配置示例
# 文件路径：examples/production_example.py

from xqclog import logger, init_logger, LogConfig


def setup_production_logging():
    """配置生产环境日志系统"""

    config = LogConfig(
        # 基础配置
        log_level="INFO",
        log_dir="/var/log/myapp",
        log_file="app.log",

        # 日志轮转
        rotation="500 MB",
        retention="90 days",
        compression="gz",

        # 输出控制
        console_output=False,  # 生产环境不输出到控制台
        file_output=True,
        auto_split=True,  # 按级别分割

        # 性能优化
        enqueue=True,
        diagnose=False,  # 生产环境关闭诊断

        # 告警配置
        alert_strategy="priority",  # 使用优先级策略
        alert_retry=3,
        alert_retry_delay=2.0,

        notifiers=[
            # 第1级：邮件 - 只在手动触发时发送给高管
            {
                "type": "email",
                "smtp_host": "smtp.company.com",
                "smtp_port": 465,
                "smtp_user": "alert@company.com",
                "smtp_password": "password",
                "use_ssl": True,
                "to_addrs": ["ceo@company.com", "cto@company.com"],
                "subject_prefix": "[🚨紧急生产告警]",
                "alert_levels": None,  # 👈 默认不发送，避免打扰高管
                "priority": 100,
            },

            # 第2级：企业微信应用 - ERROR和CRITICAL
            {
                "type": "weixin_app",
                "corpid": "wwxxx",
                "corpsecret": "secret",
                "agentid": 1000002,
                "touser": "DevTeam|OpsTeam",
                "alert_levels": ["ERROR", "CRITICAL"],
                "priority": 90,
            },

            # 第3级：钉钉 - ERROR和CRITICAL
            {
                "type": "dingtalk",
                "webhook": "https://oapi.dingtalk.com/robot/send?access_token=TOKEN",
                "secret": "SECRET",
                "at_mobiles": ["13800138000", "13800138001"],
                "alert_levels": ["ERROR", "CRITICAL"],
                "priority": 80,
            },
        ]
    )

    init_logger(config)
    logger.info("生产环境日志系统初始化完成")


def simulate_production_scenarios():
    """模拟生产环境的各种场景"""

    print("\n========== 模拟生产环境场景 ==========\n")

    # 场景1：应用启动
    print("场景1：应用启动")
    logger.info("应用启动", version="1.0.0", environment="production")
    print("  → 记录INFO日志，不发送告警\n")

    # 场景2：业务操作成功
    print("场景2：订单处理成功")
    logger.log_business(
        event="订单创建",
        order_id="ORD20240120001",
        amount=999.99,
        user_id=12345
    )
    print("  → 记录业务日志，不发送告警\n")

    # 场景3：用户操作错误（不需要告警）
    print("场景3：用户操作错误")
    logger.error(
        "用户输入验证失败",
        alert=False,  # 👈 预期的错误，不需要告警
        user_id=12345,
        reason="手机号格式错误"
    )
    print("  → 记录ERROR日志，alert=False不发送告警\n")

    # 场景4：第三方服务异常（需要告警）
    print("场景4：第三方支付服务异常")
    logger.error(
        "支付服务调用失败",
        order_id="ORD20240120002",
        error_code="TIMEOUT",
        retry_count=3
    )
    print("  → 记录ERROR日志，发送到企业微信和钉钉\n")

    # 场景5：数据库连接异常（需要告警）
    print("场景5：数据库连接异常")
    logger.critical(
        "数据库连接池耗尽",
        pool_size=100,
        active_connections=100,
        waiting_requests=50
    )
    print("  → 记录CRITICAL日志，发送到企业微信和钉钉\n")

    # 场景6：核心业务故障（需要通知高管）
    print("场景6：核心业务完全瘫痪")
    logger.critical(
        "订单系统完全宕机，影响所有用户",
        alert=True,  # 👈 强制发送到所有渠道，包括邮件
        affected_users=10000,
        downtime_minutes=5
    )
    print("  → 记录CRITICAL日志，alert=True发送到所有渠道（包括CEO邮件）\n")

    # 场景7：系统恢复通知（通知高管）
    print("场景7：系统恢复")
    logger.info(
        "订单系统已恢复正常",
        alert=True,  # 👈 重要通知，发送给所有人
        recovery_time="2025-11-18 10:15:00",
        total_downtime_minutes=10
    )
    print("  → 记录INFO日志，alert=True发送恢复通知给所有渠道\n")

    # 场景8：性能监控
    print("场景8：API性能监控")
    logger.log_performance(
        metric_name="订单API响应时间",
        value=1234.5,
        unit="ms",
        alert=True if 1234.5 > 1000 else False  # 👈 超过阈值才告警
    )
    print("  → 响应时间超过阈值，发送性能告警\n")

    # 场景9：定时任务完成
    print("场景9：每日报表生成完成")
    logger.info(
        "每日销售报表生成完成",
        alert=True,  # 👈 重要任务完成，通知相关人员
        total_orders=5000,
        total_amount=999999.99,
        report_path="/reports/daily_20240120.pdf"
    )
    print("  → 记录INFO日志，alert=True发送完成通知\n")


def main():
    """主函数"""
    print("=" * 70)
    print("生产环境日志配置示例")
    print("=" * 70)

    # 配置日志系统
    setup_production_logging()

    # 模拟各种场景
    simulate_production_scenarios()

    print("=" * 70)
    print("生产环境示例运行完成")
    print("=" * 70)

    print("\n💡 生产环境配置要点：")
    print("1. 邮件设置 alert_levels=None，避免频繁打扰高管")
    print("2. 只在关键问题时使用 alert=True 发送邮件")
    print("3. 使用 alert=False 过滤预期的错误")
    print("4. 企业微信和钉钉处理常规错误告警")
    print("5. 使用优先级策略确保重要通知优先发送")


if __name__ == "__main__":
    main()