# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 08:00:00 UTC
# 文件描述：日志核心类，基于loguru实现的日志管理器
# 文件路径：xqclog/logger.py

import sys
import time
from pathlib import Path
from typing import Optional, Union, Any, Dict
from contextlib import contextmanager
from loguru import logger as loguru_logger

from .config import LogConfig
from .presets import Presets


class XQCLogger:
    """XQC日志管理器，基于loguru的单例日志类"""

    _instance: Optional['XQCLogger'] = None
    _initialized: bool = False

    def __new__(cls) -> 'XQCLogger':
        """
        实现单例模式

        :return: XQCLogger实例
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """初始化日志管理器"""
        if not self._initialized:
            self.logger = loguru_logger
            self.config: Optional[LogConfig] = None
            self._alert_manager = None
            # 移除默认的handler
            self.logger.remove()
            XQCLogger._initialized = True

    def init(
            self,
            config: Optional[LogConfig] = None,
            preset: Optional[str] = None,
            config_file: Optional[Union[str, Path]] = None,
            **kwargs: Any
    ) -> 'XQCLogger':
        """
        初始化日志系统

        :param config: 日志配置对象，如果为None则使用默认配置
        :param preset: 预设配置名称（auto/development/testing/production/web/crawler/data）
        :param config_file: 配置文件路径（支持 .yaml, .yml, .json）
        :param kwargs: 直接传入的配置参数，会覆盖config中的对应参数
        :return: 返回self以支持链式调用
        """
        # 优先级：kwargs > config > config_file > preset > 默认配置

        # 1. 从preset加载
        if preset:
            preset_config = Presets.get(preset)
            config = LogConfig(**preset_config)

        # 2. 从配置文件加载
        elif config_file:
            config = LogConfig.from_file(config_file)

        # 3. 使用提供的config或默认config
        elif config is None:
            config = LogConfig()

        # 4. kwargs参数覆盖config
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)

        self.config = config

        # 移除所有已存在的handler
        self.logger.remove()

        # 添加控制台输出
        if config.console_output:
            self.logger.add(
                sys.stdout,
                format=config.format_string,
                level=config.log_level,
                colorize=config.colorize,
                backtrace=config.backtrace,
                diagnose=config.diagnose,
                enqueue=config.enqueue,
            )

        # 添加文件输出
        if config.file_output:
            # 确保日志目录存在
            log_dir = Path(config.log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)

            if config.auto_split:
                # 自动分割：不同级别的日志写入不同文件
                self._add_split_handlers(config)
            else:
                # 统一日志文件
                self.logger.add(
                    config.log_path,
                    format=config.format_string,
                    level=config.log_level,
                    rotation=config.rotation,
                    retention=config.retention,
                    compression=config.compression,
                    encoding=config.encoding,
                    backtrace=config.backtrace,
                    diagnose=config.diagnose,
                    enqueue=config.enqueue,
                )

        # 配置告警管理器
        if config.notifiers:
            self._setup_alert_manager(config)

        self.logger.info(f"日志系统初始化成功，日志级别: {config.log_level}")
        if config.file_output:
            if config.auto_split:
                self.logger.info(f"日志目录: {config.log_dir}（已启用自动分割）")
            else:
                self.logger.info(f"日志文件路径: {config.log_path.absolute()}")

        if config.notifiers:
            self.logger.info(f"已配置 {len(config.notifiers)} 个告警通知器，策略: {config.alert_strategy}")

        return self

    def _add_split_handlers(self, config: LogConfig) -> None:
        """
        添加分割的日志处理器（不同级别写入不同文件）

        :param config: 日志配置对象
        """
        log_dir = Path(config.log_dir)

        # 定义日志级别和对应的文件
        levels = {
            "DEBUG": "debug.log",
            "INFO": "info.log",
            "SUCCESS": "success.log",
            "WARNING": "warning.log",
            "ERROR": "error.log",
            "CRITICAL": "critical.log",
        }

        for level, filename in levels.items():
            self.logger.add(
                log_dir / filename,
                format=config.format_string,
                level=level,
                filter=lambda record, lvl=level: record["level"].name == lvl,
                rotation=config.rotation,
                retention=config.retention,
                compression=config.compression,
                encoding=config.encoding,
                backtrace=config.backtrace,
                diagnose=config.diagnose,
                enqueue=config.enqueue,
            )

    def _setup_alert_manager(self, config: LogConfig) -> None:
        """
        配置告警管理器

        :param config: 日志配置对象
        """
        from .alerts import get_alert_manager

        self._alert_manager = get_alert_manager()
        self._alert_manager.clear_notifiers()  # 清空之前的配置

        # 配置发送策略
        self._alert_manager.configure(
            strategy=config.alert_strategy,
            retry_count=config.alert_retry,
            retry_delay=config.alert_retry_delay,
            timeout=config.alert_timeout,
        )

        # 添加通知器
        notifiers_added = 0
        for notifier_config in config.notifiers:
            # 复制配置，避免修改原配置
            notifier_cfg = notifier_config.copy()

            notifier_type = notifier_cfg.pop("type", None)
            if not notifier_type:
                self.logger.warning("通知器配置缺少type字段，跳过")
                continue

            priority = notifier_cfg.pop("priority", 0)

            try:
                self._alert_manager.add_notifier(
                    notifier_type,
                    priority=priority,
                    **notifier_cfg
                )
                notifiers_added += 1
                self.logger.debug(f"已添加通知器: {notifier_type} (优先级: {priority})")
            except Exception as e:
                self.logger.error(f"添加通知器失败 ({notifier_type}): {e}")

        # 添加告警sink
        if notifiers_added > 0:
            self._add_alert_handler()

    def _add_alert_handler(self) -> None:
        """添加告警处理器"""
        if self._alert_manager is None:
            return

        def alert_sink(message):
            """告警sink函数"""
            record = message.record

            # 从extra中获取alert参数
            force_send = record.get("extra", {}).get("_alert")

            # 异步发送告警，避免阻塞日志系统
            try:
                self._alert_manager.send_alert(
                    level=record["level"].name,
                    message=record["message"],
                    force_send=force_send,  # 传递强制发送标志
                    module=record.get("name"),
                    function=record.get("function"),
                    line=record.get("line"),
                    extra=record.get("extra", {})
                )
            except Exception as e:
                # 发送告警失败不应该影响日志记录
                print(f"发送告警失败: {e}")

        self.logger.add(
            alert_sink,
            level="DEBUG",  # 在通知器中会再次过滤级别
            format="{message}",
        )

    def trace(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录TRACE级别日志

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.trace(message, *args, **kwargs)

    def debug(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录DEBUG级别日志

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录INFO级别日志

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.info(message, *args, **kwargs)

    def success(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录SUCCESS级别日志

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.success(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录WARNING级别日志

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录ERROR级别日志

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录CRITICAL级别日志

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录异常信息

        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.exception(message, *args, **kwargs)

    def log(self, level: str, message: str, *args: Any, alert: Optional[bool] = None, **kwargs: Any) -> None:
        """
        记录指定级别的日志

        :param level: 日志级别
        :param message: 日志消息
        :param alert: 是否发送告警（True=强制发送, False=强制不发送, None=根据配置判断）
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        if alert is not None:
            kwargs['_alert'] = alert
        self.logger.log(level, message, *args, **kwargs)

    def set_level(self, level: str) -> None:
        """
        动态设置日志级别

        :param level: 日志级别
        """
        if self.config:
            old_level = self.config.log_level
            self.config.log_level = level.upper()
            # 重新初始化以应用新的级别
            self.init(self.config)
            self.logger.info(f"日志级别已从 {old_level} 更改为 {level.upper()}")
        else:
            self.logger.warning("未初始化配置，无法设置日志级别")

    @contextmanager
    def timer(self, name: str = "操作", level: str = "INFO"):
        """
        计时器上下文管理器

        :param name: 计时器名称
        :param level: 日志级别
        """
        start_time = time.time()
        self.log(level, f"⏱️  开始: {name}")

        try:
            yield
        finally:
            elapsed = time.time() - start_time
            self.log(level, f"⏱️  完成: {name}，耗时: {elapsed:.4f}秒")

    def log_request(
            self,
            method: str,
            url: str,
            status: int,
            duration: float,
            alert: Optional[bool] = None,
            **extra: Any
    ) -> None:
        """
        记录HTTP请求日志

        :param method: 请求方法
        :param url: 请求URL
        :param status: 响应状态码
        :param duration: 请求耗时（秒）
        :param alert: 是否发送告警
        :param extra: 额外信息
        """
        # 根据状态码确定日志级别
        if 200 <= status < 300:
            level = "INFO"
        elif 300 <= status < 400:
            level = "INFO"
        elif 400 <= status < 500:
            level = "WARNING"
        else:
            level = "ERROR"

        # 格式化消息
        message = f"🌐 {method} {url} - {status} - {duration:.3f}s"

        # 添加alert参数到extra
        if alert is not None:
            extra['_alert'] = alert

        # 添加额外信息到日志上下文
        if extra:
            self.logger.bind(**extra).log(level, message)
        else:
            self.log(level, message)

    def log_db_query(
            self,
            query: str,
            duration: float,
            rows: Optional[int] = None,
            alert: Optional[bool] = None,
            **extra: Any
    ) -> None:
        """
        记录数据库查询日志

        :param query: SQL查询语句
        :param duration: 查询耗时（秒）
        :param rows: 影响行数
        :param alert: 是否发送告警
        :param extra: 额外信息
        """
        rows_info = f"- {rows} rows" if rows is not None else ""

        # 根据耗时确定日志级别
        if duration > 5.0:
            level = "WARNING"
        elif duration > 10.0:
            level = "ERROR"
        else:
            level = "DEBUG"

        message = f"💾 数据库查询 - {duration:.3f}s {rows_info}\n{query}"

        # 添加alert参数到extra
        if alert is not None:
            extra['_alert'] = alert

        if extra:
            self.logger.bind(**extra).log(level, message)
        else:
            self.log(level, message)

    def log_api_call(
            self,
            api_name: str,
            duration: float,
            success: bool = True,
            alert: Optional[bool] = None,
            **extra: Any
    ) -> None:
        """
        记录API调用日志

        :param api_name: API名称
        :param duration: 调用耗时（秒）
        :param success: 是否成功
        :param alert: 是否发送告警
        :param extra: 额外信息
        """
        status = "✅ 成功" if success else "❌ 失败"
        level = "INFO" if success else "ERROR"

        message = f"📡 API调用: {api_name} - {status} - {duration:.3f}s"

        # 添加alert参数到extra
        if alert is not None:
            extra['_alert'] = alert

        if extra:
            self.logger.bind(**extra).log(level, message)
        else:
            self.log(level, message)

    def log_performance(
            self,
            metric_name: str,
            value: float,
            unit: str = "ms",
            alert: Optional[bool] = None,
            **extra: Any
    ) -> None:
        """
        记录性能指标日志

        :param metric_name: 指标名称
        :param value: 指标值
        :param unit: 单位
        :param alert: 是否发送告警
        :param extra: 额外信息
        """
        message = f"📊 性能指标: {metric_name} = {value:.2f}{unit}"

        # 添加alert参数到extra
        if alert is not None:
            extra['_alert'] = alert

        if extra:
            self.logger.bind(**extra).info(message)
        else:
            self.info(message)

    def log_business(
            self,
            event: str,
            level: str = "INFO",
            alert: Optional[bool] = None,
            **extra: Any
    ) -> None:
        """
        记录业务日志

        :param event: 业务事件
        :param level: 日志级别
        :param alert: 是否发送告警
        :param extra: 额外信息
        """
        message = f"💼 业务事件: {event}"

        # 添加alert参数到extra
        if alert is not None:
            extra['_alert'] = alert

        if extra:
            self.logger.bind(**extra).log(level, message)
        else:
            self.log(level, message)

    def add_handler(
            self,
            sink: Union[str, Path, Any],
            **kwargs: Any
    ) -> int:
        """
        添加自定义的日志处理器

        :param sink: 日志输出目标（文件路径、流对象等）
        :param kwargs: loguru的add方法支持的其他参数
        :return: 处理器ID
        """
        handler_id = self.logger.add(sink, **kwargs)
        self.logger.info(f"已添加新的日志处理器: {sink}")
        return handler_id

    def remove_handler(self, handler_id: int) -> None:
        """
        移除指定的日志处理器

        :param handler_id: 处理器ID
        """
        self.logger.remove(handler_id)
        self.logger.info(f"已移除日志处理器: {handler_id}")

    def bind(self, **kwargs: Any):
        """
        绑定上下文信息到日志

        :param kwargs: 要绑定的键值对
        :return: 绑定了上下文的logger
        """
        return self.logger.bind(**kwargs)

    def contextualize(self, **kwargs: Any):
        """
        上下文管理器，在代码块内绑定上下文信息

        :param kwargs: 要绑定的键值对
        :return: 上下文管理器
        """
        return self.logger.contextualize(**kwargs)

    def patch(self, patcher):
        """
        给日志记录添加补丁函数

        :param patcher: 补丁函数
        :return: 上下文管理器
        """
        return self.logger.patch(patcher)

    def opt(self, **kwargs: Any):
        """
        配置日志选项

        :param kwargs: 选项参数
        :return: 配置了选项的logger
        """
        return self.logger.opt(**kwargs)

    def get_logger(self):
        """
        获取原始的loguru logger对象，用于高级用法

        :return: loguru的logger对象
        """
        return self.logger

    def get_alert_manager(self):
        """
        获取告警管理器

        :return: AlertManager实例或None
        """
        return self._alert_manager

    def add_notifier(
            self,
            notifier_type: str,
            priority: int = 0,
            **config: Any
    ) -> None:
        """
        动态添加通知器

        :param notifier_type: 通知器类型
        :param priority: 优先级
        :param config: 通知器配置
        """
        if self._alert_manager is None:
            from .alerts import get_alert_manager
            self._alert_manager = get_alert_manager()

        try:
            self._alert_manager.add_notifier(
                notifier_type,
                priority=priority,
                **config
            )
            self.logger.info(f"已动态添加通知器: {notifier_type} (优先级: {priority})")

            # 如果是第一个通知器，需要添加alert handler
            if self._alert_manager.get_notifiers_count() == 1:
                self._add_alert_handler()
        except Exception as e:
            self.logger.error(f"添加通知器失败 ({notifier_type}): {e}")

    def register_custom_notifier(
            self,
            name: str,
            notifier_class: type
    ) -> None:
        """
        注册自定义通知器

        :param name: 通知器名称
        :param notifier_class: 通知器类
        """
        if self._alert_manager is None:
            from .alerts import get_alert_manager
            self._alert_manager = get_alert_manager()

        self._alert_manager.register_custom_notifier(name, notifier_class)
        self.logger.info(f"已注册自定义通知器: {name}")

    def get_config(self) -> Optional[LogConfig]:
        """
        获取当前配置

        :return: LogConfig实例或None
        """
        return self.config

    def save_config(self, config_file: Union[str, Path]) -> None:
        """
        保存当前配置到文件

        :param config_file: 配置文件路径（支持 .yaml, .json）
        """
        if self.config is None:
            self.logger.warning("没有可保存的配置")
            return

        import yaml
        import json

        config_path = Path(config_file)
        config_dict = {"logging": self.config.to_dict()}

        with open(config_path, 'w', encoding='utf-8') as f:
            if config_path.suffix in ['.yaml', '.yml']:
                yaml.dump(config_dict, f, allow_unicode=True, default_flow_style=False)
            elif config_path.suffix == '.json':
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")

        self.logger.info(f"配置已保存到: {config_path.absolute()}")


# 创建全局日志实例
_global_logger = XQCLogger()


def get_logger() -> XQCLogger:
    """
    获取全局日志实例

    :return: XQCLogger实例
    """
    return _global_logger


def init_logger(
        config: Optional[LogConfig] = None,
        preset: Optional[str] = None,
        config_file: Optional[Union[str, Path]] = None,
        **kwargs: Any
) -> XQCLogger:
    """
    初始化全局日志系统（便捷函数）

    :param config: 日志配置对象
    :param preset: 预设配置名称
    :param config_file: 配置文件路径
    :param kwargs: 配置参数
    :return: XQCLogger实例
    """
    return _global_logger.init(config=config, preset=preset, config_file=config_file, **kwargs)