# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 10:00:00 UTC
# 文件描述：xqclog模块的高级使用示例
# 文件路径：examples/advanced_usage.py

import time
from xqclog import logger, init_logger, LogConfig
from xqclog.decorators import log_execution, catch_errors, timer


def example_1_preset_auto():
    """示例1：自动环境识别"""
    print("\n========== 示例1：自动环境识别 ==========")

    # 自动根据ENV环境变量识别环境
    # 设置环境变量: export ENV=production
    init_logger(preset="auto")

    logger.info("根据环境变量自动配置")


def example_2_config_file():
    """示例2：从配置文件加载"""
    print("\n========== 示例2：从配置文件加载 ==========")

    # 先创建一个示例配置文件
    import yaml
    config_content = {
        "logging": {
            "log_level": "DEBUG",
            "log_dir": "logs/from_config",
            "log_file": "app.log",
            "rotation": "50 MB",
            "retention": "7 days",
        }
    }

    with open("logging_example.yaml", "w") as f:
        yaml.dump(config_content, f)

    # 从配置文件加载
    init_logger(config_file="logging_example.yaml")

    logger.info("从配置文件加载的日志系统")

    # 清理示例文件
    import os
    os.remove("logging_example.yaml")


def example_3_decorators():
    """示例3：使用装饰器"""
    print("\n========== 示例3：使用装饰器 ==========")

    init_logger(log_level="INFO")

    @log_execution(log_args=True, log_time=True)
    def calculate(a: int, b: int) -> int:
        """计算函数"""
        time.sleep(0.1)
        return a + b

    @catch_errors(reraise=False, default_return=0)
    def risky_function(x: int) -> int:
        """可能出错的函数"""
        if x < 0:
            raise ValueError("x不能为负数")
        return x * 2

    @timer(name="数据处理")
    def process_data():
        """处理数据"""
        time.sleep(0.2)
        return "完成"

    # 调用函数
    result1 = calculate(10, 20)
    print(f"计算结果: {result1}")

    result2 = risky_function(-1)  # 会捕获异常，返回默认值0
    print(f"风险函数结果: {result2}")

    result3 = process_data()
    print(f"处理结果: {result3}")


def example_4_structured_logging():
    """示例4：结构化日志"""
    print("\n========== 示例4：结构化日志 ==========")

    init_logger(log_level="INFO")

    # HTTP请求日志
    logger.log_request(
        method="GET",
        url="/api/users",
        status=200,
        duration=0.123,
        user_id=12345,
    )

    logger.log_request(
        method="POST",
        url="/api/login",
        status=401,
        duration=0.056,
        reason="密码错误",
    )

    # 数据库查询日志
    logger.log_db_query(
        query="SELECT * FROM users WHERE id = 1",
        duration=0.015,
        rows=1,
    )

    # API调用日志
    logger.log_api_call(
        api_name="支付宝支付",
        duration=1.234,
        success=True,
        order_id="ORD123456",
    )

    # 性能指标日志
    logger.log_performance(
        metric_name="API响应时间",
        value=123.45,
        unit="ms",
    )

    # 业务日志
    logger.log_business(
        event="用户注册",
        user_id=12345,
        username="张三",
    )


def example_5_context_binding():
    """示例5：上下文绑定"""
    print("\n========== 示例5：上下文绑定 ==========")

    init_logger()

    # 绑定上下文信息
    user_logger = logger.bind(user_id=12345, username="张三")
    user_logger.info("用户登录")
    user_logger.info("用户查看订单")

    # 使用上下文管理器
    with logger.contextualize(request_id="REQ-12345", ip="192.168.1.1"):
        logger.info("处理请求")
        logger.info("返回响应")


def main():
    """主函数"""
    print("=" * 60)
    print("XQCLog 高级用法示例")
    print("=" * 60)

    example_1_preset_auto()
    example_2_config_file()
    example_3_decorators()
    example_4_structured_logging()
    example_5_context_binding()

    print("\n" + "=" * 60)
    print("所有高级示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()