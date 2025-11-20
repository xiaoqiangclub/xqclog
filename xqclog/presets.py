# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2025-11-18 10:00:00 UTC
# 文件描述：预设配置，为不同应用场景提供开箱即用的日志配置
# 文件路径：xqclog/presets.py

from typing import Dict, Any
import os


class Presets:
    """预设配置集合"""

    @staticmethod
    def get_environment() -> str:
        """
        自动检测运行环境

        :return: 环境名称（development/testing/production）
        """
        env = os.getenv("ENV", os.getenv("ENVIRONMENT", "development")).lower()
        if env in ["prod", "production"]:
            return "production"
        elif env in ["test", "testing"]:
            return "testing"
        else:
            return "development"

    @staticmethod
    def development() -> Dict[str, Any]:
        """
        开发环境配置

        :return: 配置字典
        """
        return {
            "log_level": "DEBUG",
            "console_output": True,
            "file_output": True,
            "colorize": True,
            "diagnose": True,
            "log_dir": "logs/dev",
            "rotation": "50 MB",
            "retention": "7 days",
        }

    @staticmethod
    def testing() -> Dict[str, Any]:
        """
        测试环境配置

        :return: 配置字典
        """
        return {
            "log_level": "INFO",
            "console_output": True,
            "file_output": True,
            "colorize": True,
            "diagnose": False,
            "log_dir": "logs/test",
            "rotation": "100 MB",
            "retention": "14 days",
        }

    @staticmethod
    def production() -> Dict[str, Any]:
        """
        生产环境配置

        :return: 配置字典
        """
        return {
            "log_level": "WARNING",
            "console_output": False,
            "file_output": True,
            "colorize": False,
            "diagnose": False,
            "log_dir": "logs/prod",
            "rotation": "500 MB",
            "retention": "90 days",
            "compression": "gz",
        }

    @staticmethod
    def web() -> Dict[str, Any]:
        """
        Web应用配置

        :return: 配置字典
        """
        return {
            "log_level": "INFO",
            "console_output": True,
            "file_output": True,
            "log_dir": "logs/web",
            "rotation": "200 MB",
            "retention": "30 days",
            "auto_split": True,
        }

    @staticmethod
    def crawler() -> Dict[str, Any]:
        """
        爬虫应用配置

        :return: 配置字典
        """
        return {
            "log_level": "INFO",
            "console_output": True,
            "file_output": True,
            "log_dir": "logs/crawler",
            "rotation": "100 MB",
            "retention": "14 days",
            "enqueue": True,
        }

    @staticmethod
    def data_pipeline() -> Dict[str, Any]:
        """
        数据处理配置

        :return: 配置字典
        """
        return {
            "log_level": "INFO",
            "console_output": True,
            "file_output": True,
            "log_dir": "logs/data",
            "rotation": "1 GB",
            "retention": "60 days",
            "compression": "gz",
        }

    @staticmethod
    def get(preset_name: str) -> Dict[str, Any]:
        """
        获取指定的预设配置

        :param preset_name: 预设名称
        :return: 配置字典
        """
        presets_map = {
            "development": Presets.development,
            "testing": Presets.testing,
            "production": Presets.production,
            "web": Presets.web,
            "crawler": Presets.crawler,
            "data": Presets.data_pipeline,
            "auto": lambda: getattr(Presets, Presets.get_environment())(),
        }

        if preset_name not in presets_map:
            raise ValueError(f"未知的预设配置: {preset_name}")

        return presets_map[preset_name]()