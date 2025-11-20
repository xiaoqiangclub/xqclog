# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 08:00:00 UTC
# 文件描述：日志配置类，用于管理日志系统的各项配置参数
# 文件路径：xqclog/config.py

from typing import Optional, Dict, Any, Union, List
from pathlib import Path
import yaml
import json


class LogConfig:
    """日志配置类"""

    def __init__(
            self,
            log_level: str = "INFO",
            log_dir: str = "logs",
            log_file: str = "app.log",
            rotation: str = "100 MB",
            retention: str = "30 days",
            compression: str = "zip",
            encoding: str = "utf-8",
            enqueue: bool = True,
            backtrace: bool = True,
            diagnose: bool = True,
            colorize: bool = True,
            format_string: Optional[str] = None,
            console_output: bool = True,
            file_output: bool = True,
            auto_split: bool = False,
            # 告警配置（新版）
            notifiers: Optional[List[Dict[str, Any]]] = None,
            alert_strategy: str = "parallel",  # 新增：发送策略
            alert_retry: int = 3,  # 新增：重试次数
            alert_retry_delay: float = 1.0,  # 新增：重试延迟（秒）
            alert_timeout: float = 5.0,  # 新增：发送超时（秒）
            # 向后兼容（旧版配置）
            alert_webhook: Optional[str] = None,
            alert_levels: Optional[List[str]] = None,
    ) -> None:
        """
        初始化日志配置

        :param log_level: 日志级别，可选值：TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
        :param log_dir: 日志文件存储目录
        :param log_file: 日志文件名称
        :param rotation: 日志文件轮转大小或时间，如 "100 MB", "1 week", "00:00"
        :param retention: 日志文件保留时间，如 "30 days", "1 week"
        :param compression: 日志文件压缩格式，可选值：zip, gz, bz2, xz
        :param encoding: 日志文件编码格式
        :param enqueue: 是否启用异步写入，提高性能
        :param backtrace: 是否显示详细的异常堆栈信息
        :param diagnose: 是否显示变量值诊断信息
        :param colorize: 控制台输出是否启用彩色
        :param format_string: 自定义日志格式字符串
        :param console_output: 是否输出到控制台
        :param file_output: 是否输出到文件
        :param auto_split: 是否按日志级别自动分割文件
        :param notifiers: 通知器配置列表
        :param alert_strategy: 告警发送策略（parallel-并行发送全部, sequential-顺序发送全部,
                               failover-轮询发送直到成功, priority-按优先级发送）
        :param alert_retry: 单个通知器发送失败时的重试次数
        :param alert_retry_delay: 重试延迟时间（秒）
        :param alert_timeout: 单个通知器发送超时时间（秒）
        :param alert_webhook: 旧版告警webhook地址（向后兼容）
        :param alert_levels: 旧版触发告警的日志级别列表（向后兼容）
        """
        self.log_level = log_level.upper()
        self.log_dir = log_dir
        self.log_file = log_file
        self.rotation = rotation
        self.retention = retention
        self.compression = compression
        self.encoding = encoding
        self.enqueue = enqueue
        self.backtrace = backtrace
        self.diagnose = diagnose
        self.colorize = colorize
        self.console_output = console_output
        self.file_output = file_output
        self.auto_split = auto_split

        # 告警配置
        self.alert_strategy = alert_strategy
        self.alert_retry = alert_retry
        self.alert_retry_delay = alert_retry_delay
        self.alert_timeout = alert_timeout

        # 通知器配置
        self.notifiers = notifiers or []

        # 向后兼容：如果使用旧版配置，自动转换
        if alert_webhook and not notifiers:
            # 根据webhook URL判断类型
            if "dingtalk" in alert_webhook or "oapi.dingtalk.com" in alert_webhook:
                notifier_type = "dingtalk"
            elif "qyapi.weixin.qq.com" in alert_webhook:
                notifier_type = "weixin_webhook"
            else:
                notifier_type = "webhook"

            self.notifiers = [{
                "type": notifier_type,
                "webhook": alert_webhook,
                "alert_levels": alert_levels or ["ERROR", "CRITICAL"],
                "enabled": True,
            }]

        # 默认日志格式
        if format_string is None:
            self.format_string = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )
        else:
            self.format_string = format_string

    @property
    def log_path(self) -> Path:
        """
        获取完整的日志文件路径

        :return: 日志文件路径对象
        """
        return Path(self.log_dir) / self.log_file

    def add_notifier(
            self,
            notifier_type: str,
            **config: Any
    ) -> 'LogConfig':
        """
        添加通知器配置

        :param notifier_type: 通知器类型
        :param config: 通知器配置参数
        :return: 返回self以支持链式调用
        """
        notifier_config = {
            "type": notifier_type,
            **config
        }
        self.notifiers.append(notifier_config)
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转换为字典

        :return: 配置字典
        """
        return {
            "log_level": self.log_level,
            "log_dir": self.log_dir,
            "log_file": self.log_file,
            "rotation": self.rotation,
            "retention": self.retention,
            "compression": self.compression,
            "encoding": self.encoding,
            "enqueue": self.enqueue,
            "backtrace": self.backtrace,
            "diagnose": self.diagnose,
            "colorize": self.colorize,
            "format_string": self.format_string,
            "console_output": self.console_output,
            "file_output": self.file_output,
            "auto_split": self.auto_split,
            "notifiers": self.notifiers,
            "alert_strategy": self.alert_strategy,
            "alert_retry": self.alert_retry,
            "alert_retry_delay": self.alert_retry_delay,
            "alert_timeout": self.alert_timeout,
        }

    @classmethod
    def from_file(cls, config_file: Union[str, Path]) -> 'LogConfig':
        """
        从配置文件加载配置

        :param config_file: 配置文件路径（支持 .yaml, .yml, .json）
        :return: LogConfig实例
        """
        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        # 读取文件内容
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.suffix in ['.yaml', '.yml']:
                config_data = yaml.safe_load(f)
            elif config_path.suffix == '.json':
                config_data = json.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")

        # 提取logging相关配置
        if 'logging' in config_data:
            config_data = config_data['logging']

        return cls(**config_data)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'LogConfig':
        """
        从字典创建配置

        :param config_dict: 配置字典
        :return: LogConfig实例
        """
        return cls(**config_dict)