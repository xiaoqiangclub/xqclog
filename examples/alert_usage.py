# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 14:00:00 UTC
# 文件描述：xqclog模块的告警功能使用示例，展示alert参数和alert_levels的用法
# 文件路径：examples/alert_usage.py

from xqclog import logger, init_logger, LogConfig


def example_1_basic_alert():
    """示例1：基础告警配置"""
    print("\n========== 示例1：基础告警配置 ==========")
    print("说明：只有ERROR和CRITICAL级别会触发告警")

    config = LogConfig(
        log_level="INFO",
        notifiers=[
            {
                "type": "dingtalk",
                "webhook": "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
                "alert_levels": ["ERROR", "CRITICAL"],  # 只有这两个级别会发送
            }
        ]
    )

    init_logger(config)

    logger.info("普通信息")  # ✅ 记录  ❌ 不发送通知
    logger.warning("警告信息")  # ✅ 记录  ❌ 不发送通知
    logger.error("错误信息")  # ✅ 记录  ✅ 发送通知
    logger.critical("严重错误")  # ✅ 记录  ✅ 发送通知

    print("\n✅ INFO和WARNING不会发送通知")
    print("✅ ERROR和CRITICAL会发送到钉钉")


def example_2_alert_parameter():
    """示例2：使用alert参数强制控制"""
    print("\n========== 示例2：使用alert参数强制控制 ==========")
    print("说明：alert参数优先级最高，可以覆盖alert_levels配置")

    config = LogConfig(
        log_level="INFO",
        notifiers=[
            {
                "type": "dingtalk",
                "webhook": "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    # 场景1：强制发送（即使INFO不在alert_levels中）
    logger.info("重要通知：系统升级完成", alert=True)
    print("✅ INFO级别 + alert=True → 强制发送通知")

    # 场景2：强制不发送（即使ERROR在alert_levels中）
    logger.error("已知错误，已处理", alert=False)
    print("✅ ERROR级别 + alert=False → 强制不发送")

    # 场景3：使用默认逻辑
    logger.error("未处理的错误")
    print("✅ ERROR级别 + 无alert参数 → 根据alert_levels发送")


def example_3_alert_levels_none():
    """示例3：alert_levels=None 的用法"""
    print("\n========== 示例3：alert_levels=None 的用法 ==========")
    print("说明：设置为None表示默认不发送，只在手动指定alert=True时发送")

    config = LogConfig(
        log_level="INFO",
        notifiers=[
            {
                "type": "email",
                "smtp_host": "smtp.qq.com",
                "smtp_port": 465,
                "smtp_user": "your@qq.com",
                "smtp_password": "password",
                "use_ssl": True,
                "to_addrs": ["admin@example.com"],
                "alert_levels": None,  # 👈 默认不发送
            }
        ]
    )

    init_logger(config)

    logger.info("普通信息")  # ❌ 不发送
    logger.error("普通错误")  # ❌ 不发送（alert_levels=None）
    logger.critical("严重错误")  # ❌ 不发送（alert_levels=None）
    logger.critical("需要CEO知晓", alert=True)  # ✅ 发送（alert=True强制发送）

    print("\n✅ 所有日志默认都不发送邮件")
    print("✅ 只有手动指定alert=True才发送")


def example_4_multi_notifiers():
    """示例4：多通知器组合使用"""
    print("\n========== 示例4：多通知器组合使用 ==========")
    print("说明：不同通知器可以配置不同的alert_levels")

    config = LogConfig(
        log_level="INFO",
        alert_strategy="parallel",  # 并行发送
        notifiers=[
            # 钉钉 - 常规错误通知
            {
                "type": "dingtalk",
                "webhook": "https://oapi.dingtalk.com/robot/send?access_token=TOKEN1",
                "alert_levels": ["ERROR", "CRITICAL"],
            },
            # 企业微信 - 只通知严重错误
            {
                "type": "weixin_app",
                "corpid": "wwxxx",
                "corpsecret": "secret",
                "agentid": 1000002,
                "touser": "DevLead",
                "alert_levels": ["CRITICAL"],
            },
            # 邮件 - 只在手动触发时发送
            {
                "type": "email",
                "smtp_host": "smtp.qq.com",
                "smtp_port": 465,
                "smtp_user": "alert@qq.com",
                "smtp_password": "password",
                "use_ssl": True,
                "to_addrs": ["ceo@company.com"],
                "alert_levels": None,  # 默认不发送
            }
        ]
    )

    init_logger(config)

    print("\n场景1：普通错误")
    logger.error("数据处理失败")
    print("  → 钉钉：✅ 发送")
    print("  → 企业微信：❌ 不发送（不在alert_levels中）")
    print("  → 邮件：❌ 不发送（alert_levels=None）")

    print("\n场景2：严重错误")
    logger.critical("数据库宕机")
    print("  → 钉钉：✅ 发送")
    print("  → 企业微信：✅ 发送")
    print("  → 邮件：❌ 不发送（alert_levels=None）")

    print("\n场景3：需要CEO知晓的问题")
    logger.critical("核心业务完全瘫痪", alert=True)
    print("  → 钉钉：✅ 发送")
    print("  → 企业微信：✅ 发送")
    print("  → 邮件：✅ 发送（alert=True强制发送）")


def example_5_business_scenarios():
    """示例5：实际业务场景"""
    print("\n========== 示例5：实际业务场景 ==========")

    config = LogConfig(
        log_level="INFO",
        notifiers=[
            {
                "type": "dingtalk",
                "webhook": "https://oapi.dingtalk.com/robot/send?access_token=TOKEN",
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    print("\n场景1：支付业务")

    def process_payment(order_id: str, success: bool, reason: str = ""):
        """模拟支付处理"""
        if success:
            logger.info(f"支付成功: {order_id}")
        else:
            # 支付失败可能是正常情况（如余额不足），不需要告警
            logger.error(
                f"支付失败: {order_id}, 原因: {reason}",
                alert=False  # 👈 不发送告警
            )

    process_payment("ORD001", True)
    print("  → 支付成功：记录日志，不发送告警")

    process_payment("ORD002", False, "余额不足")
    print("  → 支付失败（余额不足）：记录ERROR日志，但不发送告警")

    print("\n场景2：系统监控")

    # 网络异常需要人工介入
    logger.error("支付网络异常", alert=True)
    print("  → 网络异常：强制发送告警")

    print("\n场景3：定时任务完成通知")

    # 即使是INFO级别，也需要通知
    logger.info("每日报表生成完成", alert=True)
    print("  → 任务完成：INFO级别但发送通知")


def example_6_structured_log_with_alert():
    """示例6：结构化日志中使用alert参数"""
    print("\n========== 示例6：结构化日志中使用alert参数 ==========")
    print("说明：所有结构化日志方法都支持alert参数")

    config = LogConfig(
        log_level="INFO",
        notifiers=[
            {
                "type": "dingtalk",
                "webhook": "https://oapi.dingtalk.com/robot/send?access_token=TOKEN",
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    # HTTP请求日志
    logger.log_request(
        method="GET",
        url="/api/users",
        status=200,
        duration=0.1,
        alert=False  # 成功请求不需要告警
    )
    print("✅ 成功的HTTP请求：alert=False，不发送告警")

    logger.log_request(
        method="POST",
        url="/api/pay",
        status=500,
        duration=5.0,
        alert=True  # 支付接口错误需要告警
    )
    print("✅ 支付接口错误：alert=True，强制发送告警")

    # API调用日志
    logger.log_api_call(
        api_name="第三方支付",
        duration=2.0,
        success=True,
        alert=True,  # 支付成功也通知
        amount=1000.0
    )
    print("✅ 支付成功：alert=True，发送通知")

    # 业务日志
    logger.log_business(
        event="用户注册",
        level="INFO",
        alert=True,  # 重要业务事件需要通知
        user_id=12345
    )
    print("✅ 用户注册：alert=True，发送通知")


def example_7_priority_control():
    """示例7：优先级控制示例"""
    print("\n========== 示例7：优先级控制示例 ==========")
    print("说明：展示告警控制的三层优先级")

    config = LogConfig(
        log_level="INFO",
        notifiers=[
            {
                "type": "dingtalk",
                "webhook": "https://oapi.dingtalk.com/robot/send?access_token=TOKEN",
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    print("\n优先级1：alert=True（最高）")
    logger.info("重要通知", alert=True)
    print("  → INFO + alert=True = 发送通知 ✅")

    print("\n优先级2：alert=False（最高）")
    logger.error("已知错误", alert=False)
    print("  → ERROR + alert=False = 不发送 ❌")

    print("\n优先级3：根据alert_levels判断")
    logger.error("未知错误")
    print("  → ERROR + alert未设置 + ERROR在alert_levels中 = 发送通知 ✅")

    logger.warning("警告信息")
    print("  → WARNING + alert未设置 + WARNING不在alert_levels中 = 不发送 ❌")


def main():
    """主函数"""
    print("=" * 70)
    print("XQCLog 告警功能使用示例")
    print("=" * 70)
    print("\n注意：以下示例使用的是示例webhook，不会真正发送通知")
    print("实际使用时请替换为真实的webhook地址\n")

    example_1_basic_alert()
    example_2_alert_parameter()
    example_3_alert_levels_none()
    example_4_multi_notifiers()
    example_5_business_scenarios()
    example_6_structured_log_with_alert()
    example_7_priority_control()

    print("\n" + "=" * 70)
    print("所有告警示例运行完成！")
    print("=" * 70)

    print("\n💡 关键要点总结：")
    print("1. alert_levels 配置决定哪些级别触发告警")
    print("2. alert=True 强制发送（最高优先级）")
    print("3. alert=False 强制不发送（最高优先级）")
    print("4. alert_levels=None 默认不发送，只在alert=True时发送")
    print("5. 所有日志方法和结构化日志方法都支持alert参数")


if __name__ == "__main__":
    main()