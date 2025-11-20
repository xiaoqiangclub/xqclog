# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025/11/20 17:45
# 文件描述：告警功能测试，请使用真实账号测试各种通知渠道
# 文件路径：examples/demo_alert_notifiers.py

"""
告警功能真实测试

本文件包含以下测试场景：
1. 邮件通知测试
2. 钉钉机器人通知测试
3. 企业微信Webhook通知测试
4. 企业微信应用通知测试
5. 多通知器组合测试
6. alert参数控制测试
7. 不同发送策略测试
8. alert_levels=None 测试
"""

# ============================================================================
# 配置区域 - 请将下面的配置参数改为您的真实数据
# ============================================================================

# 邮件配置
EMAIL_CONFIG = {
    "smtp_host": "smtp.example.com",
    "smtp_port": 465,
    "smtp_user": "test@example.com",
    "smtp_password": "your_email_password_here",
    "use_ssl": True,
    "from_name": "XQCLog测试系统",
    "to_addrs": ["receiver@example.com"],
    "timeout": 10,
}

# 钉钉配置
DINGTALK_CONFIG = {
    "webhook": "https://oapi.dingtalk.com/robot/send?access_token=YOUR_DINGTALK_ACCESS_TOKEN",
    "secret": "YOUR_DINGTALK_SECRET",
    "timeout": 5,
}

# 企业微信Webhook配置
WEIXIN_WEBHOOK_CONFIG = {
    "webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WEIXIN_WEBHOOK_KEY",
    "timeout": 5,
}

# 企业微信应用配置
WEIXIN_APP_CONFIG = {
    "corpid": "ww1234567890abcdef",
    "corpsecret": "your_app_secret_here_32_characters_long",
    "agentid": 1000001,
    "touser": "@all",
    "timeout": 10,
}

# ============================================================================
# 测试代码（以下代码无需修改）
# ============================================================================

import time
from xqclog import logger, init_logger, LogConfig


def test_1_email_only():
    """测试1：仅邮件通知"""
    print("\n" + "=" * 70)
    print("测试1：邮件通知测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,  # 测试时不输出文件
        notifiers=[
            {
                "type": "email",
                **EMAIL_CONFIG,
                "subject_prefix": "[测试告警]",
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    print("\n发送测试日志...")
    logger.info("这是INFO日志，不会发送邮件")
    logger.warning("这是WARNING日志，不会发送邮件")

    print("\n发送ERROR日志（应该收到邮件）...")
    logger.error("【测试】这是ERROR日志，会发送邮件通知")

    print("\n发送CRITICAL日志（应该收到邮件）...")
    logger.critical("【测试】这是CRITICAL日志，会发送邮件通知")

    print(f"\n✅ 测试1完成，请检查邮箱 {EMAIL_CONFIG['to_addrs'][0]}")
    print("预期结果：收到2封邮件（ERROR和CRITICAL各1封）")

    time.sleep(2)  # 等待邮件发送


def test_2_dingtalk_only():
    """测试2：仅钉钉通知"""
    print("\n" + "=" * 70)
    print("测试2：钉钉机器人通知测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        notifiers=[
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    print("\n发送测试日志...")
    logger.info("这是INFO日志，不会发送到钉钉")
    logger.warning("这是WARNING日志，不会发送到钉钉")

    print("\n发送ERROR日志（应该发送到钉钉）...")
    logger.error("【测试】这是ERROR日志，会发送到钉钉")

    print("\n发送CRITICAL日志（应该发送到钉钉）...")
    logger.critical("【测试】这是CRITICAL日志，会发送到钉钉")

    print("\n✅ 测试2完成，请检查钉钉群消息")
    print("预期结果：收到2条钉钉消息（ERROR和CRITICAL各1条）")

    time.sleep(2)


def test_3_weixin_webhook_only():
    """测试3：仅企业微信Webhook通知"""
    print("\n" + "=" * 70)
    print("测试3：企业微信Webhook通知测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        notifiers=[
            {
                "type": "weixin_webhook",
                **WEIXIN_WEBHOOK_CONFIG,
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    print("\n发送测试日志...")
    logger.info("这是INFO日志，不会发送到企业微信")
    logger.warning("这是WARNING日志，不会发送到企业微信")

    print("\n发送ERROR日志（应该发送到企业微信）...")
    logger.error("【测试】这是ERROR日志，会发送到企业微信群")

    print("\n发送CRITICAL日志（应该发送到企业微信）...")
    logger.critical("【测试】这是CRITICAL日志，会发送到企业微信群")

    print("\n✅ 测试3完成，请检查企业微信群消息")
    print("预期结果：收到2条企业微信消息（ERROR和CRITICAL各1条）")

    time.sleep(2)


def test_4_weixin_app_only():
    """测试4：仅企业微信应用通知"""
    print("\n" + "=" * 70)
    print("测试4：企业微信应用通知测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        notifiers=[
            {
                "type": "weixin_app",
                **WEIXIN_APP_CONFIG,
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    print("\n发送测试日志...")
    logger.info("这是INFO日志，不会发送到企业微信应用")
    logger.warning("这是WARNING日志，不会发送到企业微信应用")

    print("\n发送ERROR日志（应该发送到企业微信应用）...")
    logger.error("【测试】这是ERROR日志，会发送到企业微信应用")

    print("\n发送CRITICAL日志（应该发送到企业微信应用）...")
    logger.critical("【测试】这是CRITICAL日志，会发送到企业微信应用")

    print("\n✅ 测试4完成，请检查企业微信应用消息")
    print("预期结果：收到2条企业微信应用消息（ERROR和CRITICAL各1条）")

    time.sleep(2)


def test_5_multi_notifiers_parallel():
    """测试5：多通知器并行发送"""
    print("\n" + "=" * 70)
    print("测试5：多通知器并行发送测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        alert_strategy="parallel",  # 并行发送
        notifiers=[
            # 钉钉
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": ["ERROR"],
            },
            # 企业微信Webhook
            {
                "type": "weixin_webhook",
                **WEIXIN_WEBHOOK_CONFIG,
                "alert_levels": ["ERROR"],
            },
            # 邮件
            {
                "type": "email",
                **EMAIL_CONFIG,
                "subject_prefix": "[并行测试]",
                "alert_levels": ["ERROR"],
            }
        ]
    )

    init_logger(config)

    print("\n发送ERROR日志（应该同时发送到钉钉、企业微信和邮箱）...")
    logger.error("【并行测试】这条ERROR日志会同时发送到3个渠道")

    print("\n✅ 测试5完成")
    print("预期结果：同时收到钉钉消息、企业微信消息和邮件各1条")

    time.sleep(3)  # 等待所有通知发送


def test_6_alert_parameter():
    """测试6：alert参数控制测试"""
    print("\n" + "=" * 70)
    print("测试6：alert参数控制测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        notifiers=[
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": ["ERROR", "CRITICAL"],
            }
        ]
    )

    init_logger(config)

    print("\n场景1：强制发送（INFO + alert=True）")
    logger.info("【alert测试】强制发送的INFO日志", alert=True)
    time.sleep(1)

    print("\n场景2：强制不发送（ERROR + alert=False）")
    logger.error("【alert测试】强制不发送的ERROR日志", alert=False)
    time.sleep(1)

    print("\n场景3：根据配置发送（ERROR，无alert参数）")
    logger.error("【alert测试】根据配置发送的ERROR日志")
    time.sleep(1)

    print("\n✅ 测试6完成")
    print("预期结果：收到2条钉钉消息（场景1的INFO和场景3的ERROR）")

    time.sleep(2)


def test_7_alert_levels_none():
    """测试7：alert_levels=None 测试"""
    print("\n" + "=" * 70)
    print("测试7：alert_levels=None 测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        notifiers=[
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": None,  # 默认不发送
            }
        ]
    )

    init_logger(config)

    print("\n发送普通日志（不应该发送）")
    logger.info("普通INFO日志")
    logger.error("普通ERROR日志")
    logger.critical("普通CRITICAL日志")
    time.sleep(1)

    print("\n发送强制发送的日志（应该发送）")
    logger.critical("【alert_levels=None测试】强制发送的CRITICAL日志", alert=True)
    time.sleep(1)

    print("\n✅ 测试7完成")
    print("预期结果：只收到1条钉钉消息（alert=True的CRITICAL）")

    time.sleep(2)


def test_8_failover_strategy():
    """测试8：故障转移策略测试"""
    print("\n" + "=" * 70)
    print("测试8：故障转移策略测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        alert_strategy="failover",  # 故障转移：轮询直到成功
        alert_retry=2,
        alert_retry_delay=1.0,
        notifiers=[
            # 第一个：钉钉（会成功）
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": ["ERROR"],
            },
            # 第二个：企业微信（如果钉钉成功就不会发送）
            {
                "type": "weixin_webhook",
                **WEIXIN_WEBHOOK_CONFIG,
                "alert_levels": ["ERROR"],
            },
        ]
    )

    init_logger(config)

    print("\n发送ERROR日志（应该只发送到钉钉，企业微信不发送）...")
    logger.error("【故障转移测试】这条ERROR日志使用failover策略")

    print("\n✅ 测试8完成")
    print("预期结果：只收到钉钉消息（第一个成功后停止）")

    time.sleep(2)


def test_9_priority_strategy():
    """测试9：优先级策略测试"""
    print("\n" + "=" * 70)
    print("测试9：优先级策略测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        alert_strategy="priority",  # 优先级策略
        notifiers=[
            # 高优先级：邮件（只发CRITICAL）
            {
                "type": "email",
                **EMAIL_CONFIG,
                "subject_prefix": "[高优先级]",
                "alert_levels": ["CRITICAL"],
                "priority": 100,
            },
            # 中优先级：钉钉（发ERROR和CRITICAL）
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": ["ERROR", "CRITICAL"],
                "priority": 50,
            },
        ]
    )

    init_logger(config)

    print("\n发送ERROR日志（只发送到钉钉）...")
    logger.error("【优先级测试】ERROR日志")
    time.sleep(2)

    print("\n发送CRITICAL日志（发送到邮件和钉钉）...")
    logger.critical("【优先级测试】CRITICAL日志")
    time.sleep(2)

    print("\n✅ 测试9完成")
    print("预期结果：")
    print("  - ERROR：收到1条钉钉消息")
    print("  - CRITICAL：收到1封邮件 + 1条钉钉消息")

    time.sleep(2)


def test_10_structured_logging():
    """测试10：结构化日志 + alert参数"""
    print("\n" + "=" * 70)
    print("测试10：结构化日志 + alert参数测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        notifiers=[
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": ["ERROR"],
            }
        ]
    )

    init_logger(config)

    print("\n测试HTTP请求日志...")
    logger.log_request(
        method="GET",
        url="/api/test",
        status=200,
        duration=0.123,
        alert=False  # 成功请求不告警
    )

    logger.log_request(
        method="POST",
        url="/api/error",
        status=500,
        duration=5.0,
        alert=True  # 错误请求强制告警
    )
    time.sleep(2)

    print("\n测试API调用日志...")
    logger.log_api_call(
        api_name="支付接口测试",
        duration=1.0,
        success=True,
        alert=True,  # 成功也通知
        order_id="TEST001"
    )
    time.sleep(2)

    print("\n测试业务日志...")
    logger.log_business(
        event="测试任务完成",
        level="INFO",
        alert=True,  # 重要业务事件通知
        task_id="TASK001"
    )
    time.sleep(2)

    print("\n✅ 测试10完成")
    print("预期结果：收到3条钉钉消息（500错误、API成功、任务完成）")


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("XQCLog 告警功能真实测试")
    print("=" * 70)
    print("\n说明：")
    print("1. 本测试使用真实账号，会真实发送通知消息")
    print("2. 测试完成后请检查各个通知渠道")
    print("3. 每个测试之间有延迟，避免发送过快")
    print("4. 如需跳过某些测试，可以注释掉对应的函数调用")

    input("\n按回车键开始测试...")

    # 运行所有测试
    test_1_email_only()
    test_2_dingtalk_only()
    test_3_weixin_webhook_only()
    test_4_weixin_app_only()
    test_5_multi_notifiers_parallel()
    test_6_alert_parameter()
    test_7_alert_levels_none()
    test_8_failover_strategy()
    test_9_priority_strategy()
    test_10_structured_logging()

    print("\n" + "=" * 70)
    print("所有测试完成！")
    print("=" * 70)
    print("\n请检查以下通知渠道：")
    print(f"✉️  邮箱：{EMAIL_CONFIG['to_addrs'][0]}")
    print("📱 钉钉群")
    print("💬 企业微信群")
    print("🏢 企业微信应用")
    print("\n测试结果统计：")
    print("  测试1（邮件）：预期2封邮件")
    print("  测试2（钉钉）：预期2条消息")
    print("  测试3（企微Webhook）：预期2条消息")
    print("  测试4（企微应用）：预期2条消息")
    print("  测试5（并行）：预期各1条消息")
    print("  测试6（alert参数）：预期2条钉钉消息")
    print("  测试7（alert_levels=None）：预期1条钉钉消息")
    print("  测试8（故障转移）：预期1条钉钉消息")
    print("  测试9（优先级）：预期1封邮件 + 2条钉钉消息")
    print("  测试10（结构化日志）：预期3条钉钉消息")


def run_quick_test():
    """快速测试（只测试基本功能）"""
    print("=" * 70)
    print("XQCLog 快速测试")
    print("=" * 70)

    config = LogConfig(
        log_level="INFO",
        console_output=True,
        file_output=False,
        notifiers=[
            {
                "type": "dingtalk",
                **DINGTALK_CONFIG,
                "alert_levels": ["ERROR"],
            }
        ]
    )

    init_logger(config)

    print("\n发送测试日志...")
    logger.info("INFO日志，不会发送")
    logger.error("【快速测试】ERROR日志，会发送到钉钉")

    print("\n✅ 快速测试完成，请检查钉钉群消息")


if __name__ == "__main__":
    print("\n请选择测试模式：")
    print("1. 完整测试（测试所有功能，约需5-10分钟）")
    print("2. 快速测试（只测试钉钉通知，约需10秒）")
    print("3. 单项测试（选择特定测试项）")

    choice = input("\n请输入选项（1/2/3）：").strip()

    if choice == "1":
        run_all_tests()
    elif choice == "2":
        run_quick_test()
    elif choice == "3":
        print("\n可用的测试项：")
        print("1 - 邮件通知")
        print("2 - 钉钉通知")
        print("3 - 企业微信Webhook")
        print("4 - 企业微信应用")
        print("5 - 多通知器并行")
        print("6 - alert参数控制")
        print("7 - alert_levels=None")
        print("8 - 故障转移策略")
        print("9 - 优先级策略")
        print("10 - 结构化日志")

        test_choice = input("\n请输入测试项编号（1-10）：").strip()

        test_map = {
            "1": test_1_email_only,
            "2": test_2_dingtalk_only,
            "3": test_3_weixin_webhook_only,
            "4": test_4_weixin_app_only,
            "5": test_5_multi_notifiers_parallel,
            "6": test_6_alert_parameter,
            "7": test_7_alert_levels_none,
            "8": test_8_failover_strategy,
            "9": test_9_priority_strategy,
            "10": test_10_structured_logging,
        }

        if test_choice in test_map:
            test_map[test_choice]()
        else:
            print("❌ 无效的选项")
    else:
        print("❌ 无效的选项")