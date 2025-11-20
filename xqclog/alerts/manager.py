# 作者：Xiaoqiang
# 微信公众号：XiaoqiangClub
# 创建时间：2024-01-20 12:00:00 UTC
# 文件描述：告警通知管理器，管理多个通知渠道
# 文件路径：xqclog/alerts/manager.py

from typing import List, Dict, Any, Type, Optional
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base import BaseNotifier, AlertMessage
from .registry import NotifierRegistry


class AlertManager:
    """告警通知管理器（单例模式）"""

    _instance: Optional['AlertManager'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'AlertManager':
        """
        实现线程安全的单例模式

        :return: AlertManager实例
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """初始化告警管理器"""
        if not hasattr(self, '_initialized'):
            self.notifiers: List[BaseNotifier] = []
            self.registry = NotifierRegistry()
            self.strategy = "parallel"  # 发送策略
            self.retry_count = 3  # 重试次数
            self.retry_delay = 1.0  # 重试延迟
            self.timeout = 5.0  # 发送超时
            self._executor = ThreadPoolExecutor(max_workers=10)
            self._initialized = True

    def configure(
            self,
            strategy: str = "parallel",
            retry_count: int = 3,
            retry_delay: float = 1.0,
            timeout: float = 5.0,
    ) -> None:
        """
        配置告警管理器

        :param strategy: 发送策略（parallel/sequential/failover/priority）
        :param retry_count: 重试次数
        :param retry_delay: 重试延迟（秒）
        :param timeout: 发送超时（秒）
        """
        self.strategy = strategy
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout

    def add_notifier(
            self,
            notifier_type: str,
            priority: int = 0,
            **config: Any
    ) -> None:
        """
        添加通知器

        :param notifier_type: 通知器类型（dingtalk/weixin_webhook/weixin_app/email/custom）
        :param priority: 优先级（用于priority策略）
        :param config: 通知器配置
        """
        notifier_class = self.registry.get(notifier_type)
        if notifier_class is None:
            raise ValueError(f"未知的通知器类型: {notifier_type}")

        # 将优先级添加到配置中
        config['_priority'] = priority

        notifier = notifier_class(**config)
        # 将优先级作为属性添加到通知器
        notifier._priority = priority
        self.notifiers.append(notifier)

        # 按优先级排序（从高到低）
        self.notifiers.sort(key=lambda n: getattr(n, '_priority', 0), reverse=True)

    def register_custom_notifier(
            self,
            name: str,
            notifier_class: Type[BaseNotifier]
    ) -> None:
        """
        注册自定义通知器

        :param name: 通知器名称
        :param notifier_class: 通知器类
        """
        self.registry.register(name, notifier_class)

    def _send_with_retry(
            self,
            notifier: BaseNotifier,
            alert_msg: AlertMessage
    ) -> Dict[str, Any]:
        """
        带重试的发送

        :param notifier: 通知器实例
        :param alert_msg: 告警消息
        :return: 发送结果
        """
        result = {
            "notifier": notifier.name,
            "success": False,
            "attempts": 0,
            "error": None,
            "skipped": False,  # 新增：是否跳过发送
        }

        # 检查是否应该发送（移到这里，统一处理）
        if not notifier.should_send(alert_msg):
            result["skipped"] = True
            result["success"] = True  # 跳过也算"成功"（没有错误）
            return result

        for attempt in range(1, self.retry_count + 1):
            result["attempts"] = attempt
            try:
                success = notifier.send(alert_msg)
                if success:
                    result["success"] = True
                    return result
                else:
                    result["error"] = "发送失败"
            except Exception as e:
                result["error"] = str(e)

            # 如果不是最后一次尝试，等待后重试
            if attempt < self.retry_count:
                time.sleep(self.retry_delay)

        return result

    def _send_parallel(self, alert_msg: AlertMessage) -> Dict[str, Any]:
        """
        并行发送策略：同时发送到所有通知器

        :param alert_msg: 告警消息
        :return: 发送结果
        """
        results = {
            "strategy": "parallel",
            "total": len(self.notifiers),
            "success": 0,
            "failed": 0,
            "skipped": 0,  # 新增：跳过的数量
            "details": []
        }

        # 使用线程池并行发送
        futures = {
            self._executor.submit(self._send_with_retry, notifier, alert_msg): notifier
            for notifier in self.notifiers
        }

        for future in as_completed(futures, timeout=self.timeout * 2):
            try:
                result = future.result()
                results["details"].append(result)
                if result.get("skipped"):
                    results["skipped"] += 1
                elif result["success"]:
                    results["success"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                notifier = futures[future]
                results["details"].append({
                    "notifier": notifier.name,
                    "success": False,
                    "error": str(e)
                })
                results["failed"] += 1

        return results

    def _send_sequential(self, alert_msg: AlertMessage) -> Dict[str, Any]:
        """
        顺序发送策略：按顺序发送到所有通知器

        :param alert_msg: 告警消息
        :return: 发送结果
        """
        results = {
            "strategy": "sequential",
            "total": len(self.notifiers),
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }

        for notifier in self.notifiers:
            result = self._send_with_retry(notifier, alert_msg)
            results["details"].append(result)
            if result.get("skipped"):
                results["skipped"] += 1
            elif result["success"]:
                results["success"] += 1
            else:
                results["failed"] += 1

        return results

    def _send_failover(self, alert_msg: AlertMessage) -> Dict[str, Any]:
        """
        故障转移策略：轮询发送直到成功

        :param alert_msg: 告警消息
        :return: 发送结果
        """
        results = {
            "strategy": "failover",
            "total": len(self.notifiers),
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }

        for notifier in self.notifiers:
            result = self._send_with_retry(notifier, alert_msg)
            results["details"].append(result)

            if result.get("skipped"):
                results["skipped"] += 1
                continue  # 跳过的不算成功，继续尝试下一个
            elif result["success"]:
                results["success"] = 1
                # 成功后立即返回，不再尝试其他通知器
                return results
            else:
                results["failed"] += 1

        return results

    def _send_priority(self, alert_msg: AlertMessage) -> Dict[str, Any]:
        """
        优先级策略：按优先级发送，高优先级成功后继续发送同优先级

        :param alert_msg: 告警消息
        :return: 发送结果
        """
        results = {
            "strategy": "priority",
            "total": len(self.notifiers),
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }

        # 按优先级分组（已经排序过）
        current_priority = None
        continue_sending = True

        for notifier in self.notifiers:
            if not continue_sending:
                break

            priority = getattr(notifier, '_priority', 0)

            # 如果优先级降低且已有成功发送，停止发送
            if current_priority is not None and priority < current_priority and results["success"] > 0:
                break

            current_priority = priority

            result = self._send_with_retry(notifier, alert_msg)
            results["details"].append(result)

            if result.get("skipped"):
                results["skipped"] += 1
            elif result["success"]:
                results["success"] += 1
            else:
                results["failed"] += 1

        return results

    def send_alert(
            self,
            level: str,
            message: str,
            force_send: Optional[bool] = None,  # 新增参数
            **extra: Any
    ) -> Dict[str, Any]:
        """
        发送告警到配置的通知渠道

        :param level: 日志级别
        :param message: 消息内容
        :param force_send: 强制发送标志（True=强制发送, False=强制不发送, None=根据配置判断）
        :param extra: 额外信息
        :return: 发送结果
        """
        if not self.notifiers:
            return {
                "strategy": self.strategy,
                "total": 0,
                "success": 0,
                "failed": 0,
                "skipped": 0,
                "details": [],
                "message": "没有配置通知器"
            }

        alert_msg = AlertMessage(
            level=level,
            message=message,
            extra=extra.get("extra", {}),
            module=extra.get("module"),
            function=extra.get("function"),
            line=extra.get("line"),
            force_send=force_send,  # 传递强制发送标志
        )

        # 根据策略选择发送方式
        if self.strategy == "parallel":
            return self._send_parallel(alert_msg)
        elif self.strategy == "sequential":
            return self._send_sequential(alert_msg)
        elif self.strategy == "failover":
            return self._send_failover(alert_msg)
        elif self.strategy == "priority":
            return self._send_priority(alert_msg)
        else:
            raise ValueError(f"未知的发送策略: {self.strategy}")

    def clear_notifiers(self) -> None:
        """清空所有通知器"""
        self.notifiers.clear()

    def get_notifiers_count(self) -> int:
        """
        获取通知器数量

        :return: 通知器数量
        """
        return len(self.notifiers)

    def shutdown(self) -> None:
        """关闭管理器，清理资源"""
        self._executor.shutdown(wait=True)


# 全局实例
_alert_manager = AlertManager()


def get_alert_manager() -> AlertManager:
    """
    获取全局告警管理器实例

    :return: AlertManager实例
    """
    return _alert_manager