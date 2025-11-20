# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 08:00:00 UTC
# 文件描述：xqclog模块的基础使用示例
# 文件路径：examples/basic_usage.py

from xqclog import logger, init_logger, LogConfig


def example_1_quick_start():
    """示例1：快速开始 - 使用默认配置"""
    print("\n========== 示例1：快速开始 ==========")

    # 初始化日志系统（使用默认配置）
    init_logger()

    # 直接使用logger记录日志
    logger.info("这是一条信息日志")
    logger.success("操作成功！")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")


def example_2_custom_config():
    """示例2：自定义配置"""
    print("\n========== 示例2：自定义配置 ==========")

    # 创建自定义配置
    config = LogConfig(
        log_level="DEBUG",
        log_dir="logs/example",
        log_file="my_app.log",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )

    # 使用自定义配置初始化
    init_logger(config)

    logger.debug("这是一条调试日志")
    logger.info("使用自定义配置的日志系统")


def example_3_kwargs_config():
    """示例3：使用关键字参数配置"""
    print("\n========== 示例3：使用关键字参数配置 ==========")

    # 直接传入配置参数
    init_logger(
        log_level="INFO",
        log_dir="logs/example",
        log_file="app.log",
        console_output=True,
        file_output=True,
    )

    logger.info("使用关键字参数配置的日志系统")


def example_4_preset_config():
    """示例4：使用预设配置"""
    print("\n========== 示例4：使用预设配置 ==========")

    # 使用web应用预设
    init_logger(preset="web")

    logger.info("使用Web预设配置（自动分割日志）")
    logger.error("错误日志会写入error.log")


def example_5_exception_logging():
    """示例5：异常日志记录"""
    print("\n========== 示例5：异常日志记录 ==========")

    init_logger(log_level="DEBUG")

    try:
        result = 10 / 0
    except Exception as e:
        logger.exception("捕获到异常")
        # 或者使用error
        logger.error(f"发生错误: {e}")


def example_6_only_console():
    """示例6：仅输出到控制台"""
    print("\n========== 示例6：仅输出到控制台 ==========")

    init_logger(
        log_level="INFO",
        console_output=True,
        file_output=False,
    )

    logger.info("这条日志只会输出到控制台，不会写入文件")


def example_7_only_file():
    """示例7：仅输出到文件"""
    print("\n========== 示例7：仅输出到文件 ==========")

    init_logger(
        log_level="INFO",
        console_output=False,
        file_output=True,
        log_dir="logs/example",
        log_file="file_only.log",
    )

    logger.info("这条日志只会写入文件，不会输出到控制台")
    print("（此日志不会在控制台显示，请查看日志文件）")


def example_8_dynamic_level():
    """示例8：动态修改日志级别"""
    print("\n========== 示例8：动态修改日志级别 ==========")

    init_logger(log_level="INFO")

    logger.debug("这条DEBUG日志不会显示")
    logger.info("当前级别为INFO")

    # 动态修改日志级别
    logger.set_level("DEBUG")

    logger.debug("修改级别后，这条DEBUG日志会显示")


def example_9_auto_split():
    """示例9：自动分割日志文件"""
    print("\n========== 示例9：自动分割日志文件 ==========")

    init_logger(
        log_level="DEBUG",
        log_dir="logs/split_example",
        auto_split=True,  # 启用自动分割
    )

    logger.debug("这条日志会写入 debug.log")
    logger.info("这条日志会写入 info.log")
    logger.warning("这条日志会写入 warning.log")
    logger.error("这条日志会写入 error.log")

    print("查看 logs/split_example 目录，会看到不同级别的日志文件")


def example_10_timer():
    """示例10：使用计时器"""
    print("\n========== 示例10：使用计时器 ==========")

    init_logger()

    # 使用上下文管理器计时
    import time

    with logger.timer("数据处理操作"):
        time.sleep(0.5)
        logger.info("处理中...")

    print("计时器会自动记录操作耗时")


def main():
    """主函数，运行所有示例"""
    print("=" * 60)
    print("XQCLog 基础使用示例")
    print("=" * 60)

    # 运行各个示例
    example_1_quick_start()
    example_2_custom_config()
    example_3_kwargs_config()
    example_4_preset_config()
    example_5_exception_logging()
    example_6_only_console()
    example_7_only_file()
    example_8_dynamic_level()
    example_9_auto_split()
    example_10_timer()

    print("\n" + "=" * 60)
    print("所有基础示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()