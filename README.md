<div align="center">

![XQCLog](https://s2.loli.net/2025/11/20/4WYkx7HXB5JO6Mv.jpg)

[![PyPI Version](https://img.shields.io/badge/PyPI-0.0.2-blue)](https://pypi.org/project/xqclog/) 
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/) 
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/xiaoqiangclub/xqclog/blob/main/LICENSE) 
[![Loguru](https://img.shields.io/badge/Based%20on-Loguru-orange)](https://github.com/Delgan/loguru)

**⚡ 基于 Loguru 的自用 Python 日志模块 - 开箱即用**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [详细文档](#-详细文档) • [完整示例](#-完整示例) • [API 参考](#-api-参考)

</div>

---

## 📚 目录

- [简介](#-简介)
- [功能特性](#-功能特性)
- [安装](#-安装)
- [快速开始](#-快速开始)
- [详细文档](#-详细文档)
  - [基础配置](#基础配置)
  - [预设配置](#预设配置)
  - [配置文件](#配置文件)
  - [日志级别](#日志级别)
  - [日志分割](#日志分割)
  - [告警通知](#告警通知)
  - [装饰器](#装饰器)
  - [结构化日志](#结构化日志)
  - [上下文管理](#上下文管理)
- [完整示例](#-完整示例)
- [API 参考](#-api-参考)
- [最佳实践](#-最佳实践)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)
- [打赏支持](#-打赏支持)

---

## 🎯 简介

**XQCLog** 是一个基于 [Loguru](https://github.com/Delgan/loguru) 开发的自用 Python 日志模块，专注于提供开箱即用、功能强大的日志解决方案。

### 为什么选择 XQCLog？

相比直接使用 Loguru，XQCLog 提供了以下增强功能：

| 特性 | Loguru 原生 | XQCLog |
|------|------------|--------|
| 基础日志功能 | ✅ | ✅ |
| 环境自适应配置 | ❌ 需手动配置 | ✅ `preset="auto"` 一键适配 |
| 配置文件支持 | ❌ 需自己实现 | ✅ 原生支持 YAML/JSON |
| 场景预设 | ❌ | ✅ Web/爬虫/数据处理等预设 |
| 多渠道告警 | ❌ 需自己集成 | ✅ 钉钉/企业微信/邮件开箱即用 |
| 灵活告警控制 | ❌ | ✅ `alert` 参数精确控制 |
| 告警策略 | ❌ | ✅ 并行/顺序/故障转移/优先级 |
| 装饰器支持 | ❌ 需自己实现 | ✅ `@log_execution` `@timer` 等 |
| 结构化日志 | ❌ | ✅ HTTP/数据库/API 等专用方法 |

---

## ✨ 功能特性

### 🎯 核心功能

- **📊 多级别日志** - TRACE、DEBUG、INFO、SUCCESS、WARNING、ERROR、CRITICAL
- **🎨 彩色输出** - 控制台日志彩色显示，提升可读性
- **🗂️ 智能分割** - 按级别、大小、时间自动分割日志文件
- **🔄 自动轮转** - 支持按大小或时间轮转，自动压缩旧日志
- **⚡ 异步写入** - 不影响应用性能的异步日志写入
- **🔍 异常追踪** - 详细的异常堆栈和变量诊断信息

### 🔔 智能告警

**支持的通知方式：**

| 通知方式 | 特性 |
|---------|------|
| **钉钉机器人** | ✅ Webhook ✅ 签名认证 ✅ @指定人 |
| **企业微信群机器人** | ✅ Webhook ✅ Markdown 格式 ✅ @指定人 |
| **企业微信应用** | ✅ 企业应用消息 ✅ Token 缓存 |
| **邮件通知** | ✅ SMTP ✅ SSL/TLS ✅ HTML 格式 ✅ 抄送 |
| **自定义通知器** | ✅ 可扩展任何第三方平台 |

**告警控制机制：**

```python
# 三层控制优先级（从高到低）
1. alert 参数         # 最高优先级，强制控制
   ├─ alert=True     → 强制发送（无论配置）
   ├─ alert=False    → 强制不发送（无论配置）
   └─ alert=None     → 使用配置判断

2. alert_levels 配置  # 根据日志级别判断
   ├─ ["ERROR", "CRITICAL"]  → 只有这些级别发送
   ├─ None                   → 默认不发送
   └─ []                     → 不发送

3. 默认行为           # 不发送
```

**发送策略：**

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| **parallel** | 同时发送到所有通知器 | 多渠道同时通知 |
| **sequential** | 按顺序发送到所有通知器 | 需要保证顺序 |
| **failover** | 轮询发送直到成功 | 高可靠性需求 |
| **priority** | 按优先级发送 | 分级通知 |

### 🎭 场景预设

| 预设 | 适用场景 | 日志级别 | 特点 |
|------|---------|---------|------|
| **auto** | 自动识别 | 根据 ENV 环境变量 | 自动适配开发/测试/生产 |
| **development** | 开发环境 | DEBUG | 详细诊断信息 |
| **testing** | 测试环境 | INFO | 适度日志 |
| **production** | 生产环境 | WARNING | 仅警告和错误 |
| **web** | Web 应用 | INFO | 自动分割日志 |
| **crawler** | 爬虫应用 | INFO | 异步写入优化 |
| **data** | 数据处理 | INFO | 大容量日志支持 |

---

## 📦 安装

### 使用 pip

```bash
pip install xqclog
```

### 使用 Poetry（推荐）

```bash
poetry add xqclog
```

### 从源码安装

```bash
git clone https://github.com/xiaoqiangclub/xqclog.git
cd xqclog
poetry install
```

---

## 🚀 快速开始

### 1️⃣ 最简单的使用（10 秒上手）

```python
from xqclog import logger, init_logger

# 默认 DEBUG 级别，彩色输出
logger.info("Hello, XQCLog!")
logger.success("操作成功 ✅")
logger.warning("这是一个警告 ⚠️")
logger.error("发生错误 ❌")
```

### 2️⃣ 使用预设配置

```python
from xqclog import logger, init_logger

# 自动根据环境变量配置（推荐）
# export ENV=production
init_logger(preset="auto")

# 或使用特定预设
init_logger(preset="web")        # Web 应用
init_logger(preset="crawler")    # 爬虫应用
init_logger(preset="production") # 生产环境

logger.info("使用预设配置")
```

### 3️⃣ 添加告警通知

```python
from xqclog import init_logger, logger, LogConfig

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

logger.info("普通日志，不会发送通知")
logger.error("错误日志，会发送到钉钉")  # ✅ 发送通知
```

### 4️⃣ 灵活控制告警

```python
from xqclog import init_logger, logger

init_logger(
    notifiers=[
        {
            "type": "dingtalk",
            "webhook": "https://...",
            "alert_levels": ["ERROR", "CRITICAL"],
        }
    ]
)

# 场景1：强制发送（即使 INFO 不在 alert_levels 中）
logger.info("重要通知：系统升级完成", alert=True)  # ✅ 强制发送

# 场景2：强制不发送（即使 ERROR 在 alert_levels 中）
logger.error("已知错误，已处理", alert=False)  # ❌ 强制不发送

# 场景3：使用默认逻辑（根据 alert_levels 判断）
logger.error("未处理的错误")  # ✅ 根据配置发送
```

### 5️⃣ 使用配置文件

```bash
# 复制配置模板
cp logging.yaml.example logging.yaml

# 编辑配置文件，替换为真实的参数
vim logging.yaml
```

```python
from xqclog import init_logger, logger

# 从配置文件加载
init_logger(config_file="logging.yaml")

logger.info("从配置文件加载的日志系统")
```

---

## 📖 详细文档

### 基础配置

#### LogConfig 完整参数

```python
from xqclog import LogConfig

config = LogConfig(
    # ========== 基础配置 ==========
    log_level="INFO",              # 日志级别：TRACE/DEBUG/INFO/SUCCESS/WARNING/ERROR/CRITICAL
    log_dir="logs",                # 日志目录
    log_file="app.log",            # 日志文件名
    
    # ========== 日志轮转 ==========
    rotation="100 MB",             # 轮转条件：
                                   #   - 按大小："100 MB", "1 GB"
                                   #   - 按时间："1 week", "1 day"
                                   #   - 按时刻："00:00"（每天零点）
    
    retention="30 days",           # 保留时间："30 days", "1 week", "2 months"
    compression="zip",             # 压缩格式：zip/gz/bz2/xz
    
    # ========== 输出控制 ==========
    console_output=True,           # 是否输出到控制台
    file_output=True,              # 是否输出到文件
    auto_split=False,              # 是否按级别自动分割文件
    
    # ========== 格式化 ==========
    encoding="utf-8",              # 文件编码
    colorize=True,                 # 控制台彩色输出
    format_string=None,            # 自定义日志格式
    
    # ========== 性能优化 ==========
    enqueue=True,                  # 异步写入（推荐开启）
    
    # ========== 调试信息 ==========
    backtrace=True,                # 显示详细堆栈
    diagnose=True,                 # 显示变量诊断（生产环境建议关闭）
    
    # ========== 告警配置 ==========
    alert_strategy="parallel",     # 发送策略：parallel/sequential/failover/priority
    alert_retry=3,                 # 失败重试次数
    alert_retry_delay=1.0,         # 重试延迟（秒）
    alert_timeout=5.0,             # 发送超时（秒）
    notifiers=[],                  # 通知器配置列表
)
```

#### 三种初始化方式

```python
from xqclog import init_logger, LogConfig

# 方式1：使用配置对象
config = LogConfig(log_level="INFO", log_dir="logs/myapp")
init_logger(config)

# 方式2：使用关键字参数
init_logger(log_level="DEBUG", log_dir="logs", auto_split=True)

# 方式3：使用配置文件
init_logger(config_file="logging.yaml")
```

---

### 预设配置

#### 自动环境识别

```python
from xqclog import init_logger, logger

# 自动根据 ENV 或 ENVIRONMENT 环境变量识别
# export ENV=production
init_logger(preset="auto")

logger.info("自动适配环境配置")
```

**环境识别规则：**

| 环境变量值 | 使用的预设 |
|-----------|-----------|
| `prod`, `production` | production |
| `test`, `testing` | testing |
| 其他 | development |

#### 各预设详情

| 预设 | log_level | log_dir | rotation | retention | 特殊配置 |
|------|-----------|---------|----------|-----------|---------|
| **development** | DEBUG | logs/dev | 50 MB | 7 days | diagnose=True |
| **testing** | INFO | logs/test | 100 MB | 14 days | - |
| **production** | WARNING | logs/prod | 500 MB | 90 days | console_output=False, compression=gz |
| **web** | INFO | logs/web | 200 MB | 30 days | auto_split=True |
| **crawler** | INFO | logs/crawler | 100 MB | 14 days | enqueue=True |
| **data** | INFO | logs/data | 1 GB | 60 days | compression=gz |

#### 使用示例

```python
from xqclog import init_logger

# 开发环境
init_logger(preset="development")

# 生产环境
init_logger(preset="production")

# Web 应用
init_logger(preset="web")
```

---

### 配置文件

#### 配置文件模板

查看 `logging.yaml.example` 获取完整配置模板。

**基础配置示例：**

```yaml
# logging.yaml
logging:
  # 基础配置
  log_level: INFO
  log_dir: logs
  log_file: app.log
  rotation: 100 MB
  retention: 30 days
  
  # 告警配置
  notifiers:
    - type: dingtalk
      webhook: "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
      alert_levels:
        - ERROR
        - CRITICAL
```

#### 从配置文件加载

```python
from xqclog import init_logger, logger

# 加载 YAML 配置
init_logger(config_file="logging.yaml")

# 或加载 JSON 配置
init_logger(config_file="logging.json")

logger.info("配置文件加载成功")
```

#### 保存配置到文件

```python
from xqclog import logger, init_logger

# 初始化
init_logger(log_level="INFO", auto_split=True)

# 保存当前配置
logger.save_config("my_config.yaml")
```

---

### 日志级别

#### 可用级别

```python
from xqclog import logger, init_logger

init_logger(log_level="DEBUG")

logger.trace("追踪信息")      # TRACE - 最详细的调试信息
logger.debug("调试信息")      # DEBUG - 调试信息
logger.info("普通信息")       # INFO - 一般信息
logger.success("成功信息")    # SUCCESS - 操作成功
logger.warning("警告信息")    # WARNING - 警告
logger.error("错误信息")      # ERROR - 错误
logger.critical("严重错误")   # CRITICAL - 严重错误
```

#### 日志级别说明

| 级别 | 用途 | 是否应该配置告警 |
|------|------|----------------|
| TRACE | 非常详细的调试 | ❌ 否 |
| DEBUG | 调试信息 | ❌ 否 |
| INFO | 一般信息 | ❌ 否（特殊情况用 `alert=True`） |
| SUCCESS | 成功操作 | ❌ 否 |
| WARNING | 警告信息 | ⚠️ 谨慎（容易产生告警疲劳） |
| ERROR | 错误信息 | ✅ **推荐** |
| CRITICAL | 严重错误 | ✅ **强烈推荐** |

#### 动态修改级别

```python
from xqclog import logger, init_logger

init_logger(log_level="INFO")

logger.debug("不会显示")
logger.info("会显示")

# 动态修改
logger.set_level("DEBUG")

logger.debug("现在会显示了")
```

---

### 日志分割

#### 按级别自动分割

```python
from xqclog import init_logger, logger

init_logger(
    log_level="DEBUG",
    log_dir="logs",
    auto_split=True  # 👈 启用自动分割
)

logger.debug("写入 debug.log")
logger.info("写入 info.log")
logger.warning("写入 warning.log")
logger.error("写入 error.log")
logger.critical("写入 critical.log")
```

**生成的文件结构：**

```
logs/
├── debug.log
├── info.log
├── success.log
├── warning.log
├── error.log
└── critical.log
```

#### 按大小轮转

```python
init_logger(rotation="100 MB")  # 达到 100MB 时轮转
```

#### 按时间轮转

```python
# 每天轮转
init_logger(rotation="1 day")

# 每周轮转
init_logger(rotation="1 week")

# 每天零点轮转
init_logger(rotation="00:00")

# 每天中午轮转
init_logger(rotation="12:00")
```

#### 日志压缩和保留

```python
init_logger(
    rotation="100 MB",
    retention="30 days",   # 只保留 30 天
    compression="zip"      # 压缩为 zip 格式
)
```

---

### 告警通知

#### 告警触发机制

XQCLog 提供三层告警控制机制：

**控制优先级（从高到低）：**

```
1. alert 参数（最高优先级）
   ├─ alert=True   → 强制发送通知
   ├─ alert=False  → 强制不发送
   └─ alert=None   → 使用下一级判断

2. alert_levels 配置
   ├─ alert_levels=None           → 默认不发送
   ├─ alert_levels=[]             → 不发送
   └─ level in alert_levels       → 发送

3. 默认行为
   └─ 不发送
```

**工作流程：**

```
记录日志
    ↓
是否设置 alert 参数？
    ├─ 是 → alert=True  → ✅ 发送
    │       alert=False → ❌ 不发送
    └─ 否 → 检查 alert_levels
            ├─ None → ❌ 不发送
            ├─ 级别在列表中 → ✅ 发送
            └─ 级别不在列表中 → ❌ 不发送
```

#### 通知器配置

##### 1. 钉钉机器人

```python
from xqclog import init_logger, LogConfig

config = LogConfig(
    log_level="INFO",
    notifiers=[
        {
            "type": "dingtalk",
            "webhook": "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
            "secret": "YOUR_SECRET",           # 可选：签名密钥
            "at_mobiles": ["13800138000"],     # 可选：@的手机号
            "at_all": False,                   # 可选：是否@所有人
            "alert_levels": ["ERROR", "CRITICAL"],
            "timeout": 5,                      # 可选：超时时间
            "enabled": True,                   # 可选：是否启用
            "priority": 100,                   # 可选：优先级
        }
    ]
)

init_logger(config)
```

##### 2. 企业微信群机器人

```python
config = LogConfig(
    notifiers=[
        {
            "type": "weixin_webhook",
            "webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY",
            "mentioned_list": ["user1", "user2"],          # 可选：@的成员ID
            "mentioned_mobile_list": ["13800138000"],      # 可选：@的手机号
            "alert_levels": ["ERROR", "CRITICAL"],
            "priority": 90,
        }
    ]
)
```

##### 3. 企业微信应用

```python
config = LogConfig(
    notifiers=[
        {
            "type": "weixin_app",
            "corpid": "ww1234567890abcdef",      # 必填：企业ID
            "corpsecret": "YOUR_SECRET",         # 必填：应用Secret
            "agentid": 1000002,                  # 必填：应用AgentId
            "touser": "@all",                    # 可选：接收用户
            "toparty": "",                       # 可选：接收部门
            "totag": "",                         # 可选：接收标签
            "alert_levels": ["ERROR", "CRITICAL"],
            "priority": 80,
        }
    ]
)
```

##### 4. 邮件通知

```python
config = LogConfig(
    notifiers=[
        {
            "type": "email",
            "smtp_host": "smtp.qq.com",          # 必填：SMTP服务器
            "smtp_port": 465,                    # 可选：端口
            "smtp_user": "your@qq.com",          # 必填：SMTP用户名
            "smtp_password": "your_password",    # 必填：SMTP密码/授权码
            "use_ssl": True,                     # 可选：使用SSL
            "use_tls": False,                    # 可选：使用TLS
            "from_addr": "your@qq.com",          # 可选：发件人
            "from_name": "XQCLog告警",           # 可选：发件人名称
            "to_addrs": ["admin@example.com"],   # 必填：收件人列表
            "cc_addrs": ["manager@example.com"], # 可选：抄送列表
            "subject_prefix": "[生产告警]",      # 可选：主题前缀
            "alert_levels": ["ERROR", "CRITICAL"],
            "priority": 70,
        }
    ]
)
```

**常用邮箱 SMTP 配置：**

| 邮箱 | SMTP 服务器 | SSL 端口 | TLS 端口 | 说明 |
|------|------------|---------|---------|------|
| QQ 邮箱 | smtp.qq.com | 465 | 587 | 需要使用授权码 |
| 163 邮箱 | smtp.163.com | 465 | 994 | 需开启SMTP服务 |
| Gmail | smtp.gmail.com | 465 | 587 | 需应用专用密码 |
| Outlook | smtp.office365.com | 587 | 587 | - |

#### 发送策略

##### parallel（并行发送）- 默认

同时发送到所有通知器：

```python
config = LogConfig(
    alert_strategy="parallel",  # 默认策略
    notifiers=[...]
)
```

**适用场景：** 多渠道同时通知

##### sequential（顺序发送）

按顺序发送到所有通知器：

```python
config = LogConfig(
    alert_strategy="sequential",
    notifiers=[...]
)
```

**适用场景：** 需要保证顺序

##### failover（故障转移）

轮询发送直到成功：

```python
config = LogConfig(
    alert_strategy="failover",
    alert_retry=3,
    alert_retry_delay=2.0,
    notifiers=[
        {"type": "dingtalk", ...},      # 优先尝试
        {"type": "weixin_app", ...},    # 失败则尝试
        {"type": "email", ...},         # 最后尝试
    ]
)
```

**适用场景：** 高可靠性需求

##### priority（优先级发送）

按优先级发送：

```python
config = LogConfig(
    alert_strategy="priority",
    notifiers=[
        {
            "type": "weixin_app",
            "priority": 100,  # 最高优先级
            "alert_levels": ["CRITICAL"],
        },
        {
            "type": "dingtalk",
            "priority": 50,
            "alert_levels": ["ERROR", "CRITICAL"],
        },
    ]
)
```

**适用场景：** 分级通知

#### alert 参数详解

##### 基本用法

```python
from xqclog import init_logger, logger

init_logger(
    notifiers=[
        {
            "type": "dingtalk",
            "webhook": "https://...",
            "alert_levels": ["ERROR", "CRITICAL"],
        }
    ]
)

# 场景1：强制发送（无论配置）
logger.info("重要通知", alert=True)  # ✅ 发送

# 场景2：强制不发送（无论配置）
logger.error("已知错误", alert=False)  # ❌ 不发送

# 场景3：根据配置（默认行为）
logger.error("未知错误")  # ✅ 发送（ERROR在alert_levels中）
logger.warning("警告")    # ❌ 不发送（WARNING不在alert_levels中）
```

##### alert_levels=None 的用法

设置为 `None` 表示默认不发送，只在手动指定时发送：

```python
config = LogConfig(
    notifiers=[
        {
            "type": "email",
            "smtp_host": "smtp.qq.com",
            "smtp_port": 465,
            "smtp_user": "alert@qq.com",
            "smtp_password": "password",
            "use_ssl": True,
            "to_addrs": ["ceo@company.com"],
            "alert_levels": None,  # 👈 默认不发送
        }
    ]
)

init_logger(config)

# 所有日志默认都不发送邮件
logger.error("普通错误")          # ❌ 不发送
logger.critical("严重错误")       # ❌ 不发送

# 只有手动指定才发送
logger.critical("系统崩溃", alert=True)  # ✅ 发送邮件
```

**适用场景：** 重要通知渠道（如邮件），避免频繁打扰，只在关键时刻手动触发

##### 结构化日志中使用 alert

所有结构化日志方法都支持 `alert` 参数：

```python
# HTTP 请求日志
logger.log_request(
    method="POST",
    url="/api/pay",
    status=500,
    duration=5.0,
    alert=True  # 支付接口错误需要告警
)

# 数据库查询日志
logger.log_db_query(
    query="UPDATE orders SET status=?",
    duration=10.5,
    rows=1000,
    alert=True  # 慢查询告警
)

# API 调用日志
logger.log_api_call(
    api_name="支付宝支付",
    duration=2.0,
    success=True,
    alert=True,  # 支付成功也通知
    amount=1000.0
)

# 业务日志
logger.log_business(
    event="用户注册",
    level="INFO",
    alert=True,  # 重要业务事件
    user_id=12345
)
```

#### 实际应用示例

##### 示例1：支付业务

```python
def process_payment(order_id: str, amount: float):
    try:
        result = payment_api.pay(order_id, amount)
        
        if result.success:
            logger.info(f"支付成功: {order_id}")
            return True
        else:
            # 支付失败可能是正常情况（余额不足等）
            logger.error(
                f"支付失败: {order_id}, 原因: {result.reason}",
                alert=False  # 👈 不发送告警
            )
            return False
            
    except NetworkError:
        # 网络错误需要人工介入
        logger.error(
            f"支付网络异常: {order_id}",
            alert=True  # 👈 强制发送告警
        )
        return False
```

##### 示例2：多通知器分级

```python
config = LogConfig(
    alert_strategy="parallel",
    notifiers=[
        # 钉钉 - 常规错误
        {
            "type": "dingtalk",
            "webhook": "https://...",
            "alert_levels": ["ERROR", "CRITICAL"],
        },
        # 企业微信 - 只通知严重错误
        {
            "type": "weixin_app",
            "corpid": "...",
            "corpsecret": "...",
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

# 普通错误
logger.error("数据处理失败")
# → 钉钉：✅ 发送
# → 企业微信：❌ 不发送
# → 邮件：❌ 不发送

# 严重错误
logger.critical("数据库宕机")
# → 钉钉：✅ 发送
# → 企业微信：✅ 发送
# → 邮件：❌ 不发送

# 核心业务故障（需CEO知晓）
logger.critical("订单系统瘫痪", alert=True)
# → 钉钉：✅ 发送
# → 企业微信：✅ 发送
# → 邮件：✅ 发送（alert=True强制发送）
```

---

### 装饰器

#### @log_execution - 记录函数执行

```python
from xqclog import logger, init_logger
from xqclog.decorators import log_execution

init_logger()

@log_execution(
    level="INFO",         # 日志级别
    log_args=True,        # 是否记录参数
    log_result=True,      # 是否记录返回值
    log_time=True         # 是否记录执行时间
)
def calculate(a: int, b: int) -> int:
    return a + b

result = calculate(10, 20)

# 输出：
# 执行函数: __main__.calculate | 参数: args=(10, 20), kwargs={}
# 函数执行成功: __main__.calculate | 耗时: 0.0001秒 | 返回值: 30
```

#### @catch_errors - 捕获异常

```python
from xqclog.decorators import catch_errors

@catch_errors(
    level="ERROR",           # 日志级别
    reraise=False,          # 是否重新抛出异常
    default_return=None     # 异常时的默认返回值
)
def risky_function(x: int) -> int:
    if x < 0:
        raise ValueError("x 不能为负数")
    return x * 2

result = risky_function(-1)  # 返回 None，不抛出异常
```

#### @timer - 计时器

```python
from xqclog.decorators import timer

@timer(name="数据处理", level="INFO")
def process_data():
    import time
    time.sleep(1)
    return "完成"

result = process_data()

# 输出：
# ⏱️  开始计时: 数据处理
# ⏱️  数据处理 执行完成，耗时: 1.0001秒
```

---

### 结构化日志

#### HTTP 请求日志

```python
from xqclog import logger, init_logger

init_logger()

logger.log_request(
    method="GET",
    url="/api/users",
    status=200,
    duration=0.123,
    # 可选参数
    user_id=12345,
    ip="192.168.1.1",
    alert=False  # 成功请求不需要告警
)

# 输出：🌐 GET /api/users - 200 - 0.123s
```

#### 数据库查询日志

```python
logger.log_db_query(
    query="SELECT * FROM users WHERE id = ?",
    duration=0.015,
    rows=100,
    db_name="main",
    table="users"
)

# 输出：💾 数据库查询 - 0.015s - 100 rows
#      SELECT * FROM users WHERE id = ?
```

#### API 调用日志

```python
logger.log_api_call(
    api_name="支付宝支付",
    duration=1.234,
    success=True,
    order_id="ORD123456",
    amount=99.9
)

# 输出：📡 API调用: 支付宝支付 - ✅ 成功 - 1.234s
```

#### 性能指标日志

```python
logger.log_performance(
    metric_name="API响应时间",
    value=123.45,
    unit="ms",
    endpoint="/api/users"
)

# 输出：📊 性能指标: API响应时间 = 123.45ms
```

#### 业务日志

```python
logger.log_business(
    event="用户注册",
    level="INFO",
    user_id=12345,
    username="张三",
    email="zhangsan@example.com"
)

# 输出：💼 业务事件: 用户注册
```

---

### 上下文管理

#### 计时器上下文

```python
from xqclog import logger, init_logger

init_logger()

with logger.timer("数据处理", level="INFO"):
    import time
    time.sleep(1)

# 输出：
# ⏱️  开始: 数据处理
# ⏱️  完成: 数据处理，耗时: 1.0001秒
```

#### 绑定上下文信息

```python
# 方式1：bind 方法
user_logger = logger.bind(user_id=12345, username="张三")
user_logger.info("用户登录")
user_logger.info("查看订单")

# 方式2：contextualize 上下文管理器
with logger.contextualize(request_id="REQ-12345", ip="192.168.1.1"):
    logger.info("处理请求")
    logger.info("返回响应")
```

---

## 💼 完整示例

### 示例1：生产环境配置

```python
from xqclog import init_logger, logger, LogConfig

# 生产环境完整配置
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
    console_output=False,  # 生产环境不输出控制台
    file_output=True,
    auto_split=True,       # 按级别分割
    
    # 性能优化
    enqueue=True,
    diagnose=False,        # 生产环境关闭诊断
    
    # 告警配置
    alert_strategy="priority",
    alert_retry=3,
    alert_retry_delay=2.0,
    
    notifiers=[
        # 邮件 - 只在手动触发时发送
        {
            "type": "email",
            "smtp_host": "smtp.company.com",
            "smtp_port": 465,
            "smtp_user": "alert@company.com",
            "smtp_password": "password",
            "use_ssl": True,
            "to_addrs": ["ceo@company.com"],
            "alert_levels": None,  # 默认不发送
            "priority": 100,
        },
        # 企业微信 - ERROR和CRITICAL
        {
            "type": "weixin_app",
            "corpid": "wwxxx",
            "corpsecret": "secret",
            "agentid": 1000002,
            "touser": "DevTeam",
            "alert_levels": ["ERROR", "CRITICAL"],
            "priority": 90,
        },
        # 钉钉 - ERROR和CRITICAL
        {
            "type": "dingtalk",
            "webhook": "https://...",
            "alert_levels": ["ERROR", "CRITICAL"],
            "priority": 80,
        },
    ]
)

init_logger(config)

# 应用启动
logger.info("应用启动", version="1.0.0")

# 业务处理
logger.error("一般错误")  # 发送到企业微信和钉钉
logger.critical("系统崩溃", alert=True)  # 发送到所有渠道包括邮件
```

### 示例2：Flask Web 应用

```python
from flask import Flask, request
from xqclog import logger, init_logger

# 使用 Web 预设
init_logger(preset="web")

app = Flask(__name__)

@app.before_request
def log_request_info():
    logger.bind(
        request_id=request.headers.get('X-Request-ID', 'N/A'),
        ip=request.remote_addr
    ).info(f"收到请求: {request.method} {request.path}")

@app.after_request
def log_response_info(response):
    logger.log_request(
        method=request.method,
        url=request.path,
        status=response.status_code,
        duration=0.1,
        ip=request.remote_addr
    )
    return response

@app.route('/api/users')
def get_users():
    with logger.timer("查询用户"):
        users = [{"id": 1, "name": "张三"}]
        logger.log_db_query(
            query="SELECT * FROM users",
            duration=0.015,
            rows=len(users)
        )
    return {"users": users}

if __name__ == '__main__':
    app.run()
```

### 示例3：数据处理任务

```python
import pandas as pd
from xqclog import logger, init_logger
from xqclog.decorators import log_execution, timer

# 使用数据处理预设
init_logger(preset="data", log_level="INFO", auto_split=True)

@log_execution(log_args=True, log_time=True)
def load_data(file_path: str) -> pd.DataFrame:
    """加载数据"""
    with logger.timer("加载数据"):
        df = pd.read_csv(file_path)
        logger.info(f"加载 {len(df)} 行数据")
        return df

@timer(name="数据处理")
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """处理数据"""
    logger.info("开始数据清洗")
    df_clean = df.dropna()
    
    logger.log_performance(
        metric_name="数据清洗完成率",
        value=len(df_clean) / len(df) * 100,
        unit="%"
    )
    
    return df_clean

def main():
    logger.log_business("开始数据处理任务")
    
    df = load_data("input.csv")
    df_processed = process_data(df)
    df_processed.to_csv("output.csv", index=False)
    
    logger.log_business("数据处理完成", alert=True)  # 完成后通知

if __name__ == '__main__':
    main()
```

---

## 📚 API 参考

### LogConfig 类

**主要参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| log_level | str | "INFO" | 日志级别 |
| log_dir | str | "logs" | 日志目录 |
| log_file | str | "app.log" | 日志文件名 |
| rotation | str | "100 MB" | 轮转条件 |
| retention | str | "30 days" | 保留时间 |
| auto_split | bool | False | 自动分割 |
| alert_strategy | str | "parallel" | 告警策略 |
| alert_retry | int | 3 | 重试次数 |
| notifiers | list | [] | 通知器列表 |

**方法：**

```python
# 从文件加载
config = LogConfig.from_file("logging.yaml")

# 从字典创建
config = LogConfig.from_dict({"log_level": "INFO"})

# 转换为字典
config_dict = config.to_dict()
```

### XQCLogger 类

**日志记录方法（均支持 alert 参数）：**

```python
logger.trace(message, *args, alert=None, **kwargs)
logger.debug(message, *args, alert=None, **kwargs)
logger.info(message, *args, alert=None, **kwargs)
logger.success(message, *args, alert=None, **kwargs)
logger.warning(message, *args, alert=None, **kwargs)
logger.error(message, *args, alert=None, **kwargs)
logger.critical(message, *args, alert=None, **kwargs)
logger.exception(message, *args, alert=None, **kwargs)
```

**结构化日志方法：**

```python
logger.log_request(method, url, status, duration, alert=None, **extra)
logger.log_db_query(query, duration, rows=None, alert=None, **extra)
logger.log_api_call(api_name, duration, success=True, alert=None, **extra)
logger.log_performance(metric_name, value, unit="ms", alert=None, **extra)
logger.log_business(event, level="INFO", alert=None, **extra)
```

**上下文管理：**

```python
logger.timer(name, level="INFO")
logger.bind(**kwargs)
logger.contextualize(**kwargs)
```

**配置管理：**

```python
logger.set_level(level)
logger.get_config()
logger.save_config(config_file)
```

---

## 💡 最佳实践

### 1. 环境配置

使用预设配置适配不同环境：

```python
import os
from xqclog import init_logger

# 推荐：使用 auto 预设
init_logger(preset="auto")

# 或手动判断
env = os.getenv("ENV", "development")
if env == "production":
    init_logger(preset="production")
else:
    init_logger(preset="development")
```

### 2. 告警配置建议

```python
# ✅ 推荐：只告警需要人工介入的问题
alert_levels = ["ERROR", "CRITICAL"]

# ⚠️ 谨慎：可能产生告警疲劳
alert_levels = ["WARNING", "ERROR", "CRITICAL"]

# ✅ 推荐：重要通知用 alert_levels=None
{
    "type": "email",
    "to_addrs": ["ceo@company.com"],
    "alert_levels": None  # 默认不发送，手动触发
}
```

### 3. 避免告警疲劳

```python
# ❌ 不推荐：所有错误都告警
logger.error("用户输入错误")

# ✅ 推荐：区分需要人工介入的错误
logger.error("用户输入错误", alert=False)  # 不告警
logger.error("数据库连接失败", alert=True)  # 需要告警
```

### 4. 结构化日志

```python
# ✅ 推荐：使用结构化方法
logger.log_request(method="GET", url="/api/users", status=200, duration=0.1)

# ❌ 不推荐：使用普通字符串
logger.info("GET /api/users 200 0.1s")
```

### 5. 异常处理

```python
try:
    risky_operation()
except Exception as e:
    # ✅ 推荐：使用 exception（自动记录堆栈）
    logger.exception("操作失败")
    
    # ❌ 不推荐：使用 error（丢失堆栈）
    logger.error(f"操作失败: {e}")
```

### 6. 性能优化

```python
# 生产环境推荐配置
init_logger(
    enqueue=True,        # 异步写入
    diagnose=False,      # 关闭诊断
    backtrace=True,      # 保留异常追踪
)
```

---

## ❓ 常见问题

### Q1: 如何控制哪些日志发送通知？

**A:** 有三种方式（优先级从高到低）：

1. **使用 alert 参数（最高优先级）**
```python
logger.error("错误", alert=False)  # 强制不发送
logger.info("重要", alert=True)    # 强制发送
```

2. **配置 alert_levels**
```python
notifiers=[{
    "type": "dingtalk",
    "alert_levels": ["ERROR", "CRITICAL"]  # 只有这两个级别发送
}]
```

3. **设置 alert_levels=None**
```python
notifiers=[{
    "type": "email",
    "alert_levels": None  # 默认不发送，只在 alert=True 时发送
}]
```

### Q2: alert 参数在哪些方法中可用？

**A:** 所有日志方法都支持：

```python
# 基础方法
logger.info("...", alert=True)
logger.error("...", alert=True)

# 结构化日志
logger.log_request(..., alert=True)
logger.log_db_query(..., alert=True)
logger.log_api_call(..., alert=True)
logger.log_business(..., alert=True)
```

### Q3: 如何在多个模块中使用？

**A:** XQCLog 使用单例模式，直接导入即可：

```python
# module_a.py
from xqclog import logger
logger.info("模块 A")

# module_b.py
from xqclog import logger
logger.info("模块 B")

# main.py
from xqclog import init_logger
import module_a, module_b

init_logger()  # 只需初始化一次
```

### Q4: 如何测试告警是否正常？

**A:**
```python
from xqclog import logger, init_logger

init_logger(
    notifiers=[{
        "type": "dingtalk",
        "webhook": "https://...",
        "alert_levels": ["ERROR"]
    }]
)

# 手动触发测试
logger.error("【测试】告警系统测试，请忽略")
```

### Q5: QQ 邮箱发送失败？

**A:** QQ 邮箱需要使用授权码：

1. 登录 QQ 邮箱
2. 设置 -> 账户 -> 开启 SMTP 服务
3. 获取授权码
4. 使用授权码作为 `smtp_password`（不是 QQ 密码）

### Q6: 日志文件太大怎么办？

**A:** 使用日志轮转和压缩：

```python
init_logger(
    rotation="100 MB",      # 超过100MB轮转
    retention="30 days",    # 只保留30天
    compression="gz"        # 压缩旧日志
)
```

### Q7: 企业微信通知收不到？

**A:** 检查以下几点：

1. 确认 `corpid`、`corpsecret`、`agentid` 正确
2. 确认应用有发送消息权限
3. 确认接收人在通讯录中
4. 查看日志中的错误信息

---

## 📝 更新日志

## 🆕 最新更新 v0.0.3

**✨ 开箱即用**
- 🚀 现在无需手动初始化，直接导入即可使用！
```python
from xqclog import logger

logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
# 就这么简单！无需配置，默认 DEBUG 级别，彩色输出
```


---

### v0.0.2 (2025-11-21)

**🐛 Bug 修复**
- **修复日志调用者名称显示问题**
  - 所有日志方法添加 `opt(depth=1)` 参数，确保正确识别真实的调用者
  - 修复前：所有日志显示为 `xqclog.logger`
  - 修复后：正确显示调用者的模块名、函数名和行号

**✨ 新功能**
- **支持标准库 logging 格式**
  - 新增 `logging_format` 参数，兼容标准库 `logging` 的格式字符串
  - 自动将 logging 格式转换为 loguru 格式
  - 便于从标准库 logging 迁移

```python
# 使用 logging 格式初始化
from xqclog import init_logger

logger = init_logger(
    logging_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

### v0.0.1 (2025-11-18)

🎉 **首次发布**

**核心功能：**
- ✨ 基于 [Loguru](https://github.com/Delgan/loguru) 增强封装
- ✨ 7种预设配置（auto/development/testing/production/web/crawler/data）
- ✨ 配置文件支持（YAML/JSON）
- ✨ 日志自动分割、轮转、压缩
- ✨ 彩色控制台输出
- ✨ 异步日志写入

**告警通知：**
- ✨ 钉钉机器人通知（支持签名、@人）
- ✨ 企业微信 Webhook 通知
- ✨ 企业微信应用通知（支持 Token 缓存）
- ✨ 邮件通知（支持 SSL/TLS、HTML 格式、抄送）
- ✨ 自定义通知器支持

**灵活告警控制：**
- ✨ `alert` 参数精确控制发送
- ✨ `alert_levels` 支持 `None`（默认不发送）
- ✨ 三层优先级控制机制

**发送策略：**
- ✨ parallel（并行发送）
- ✨ sequential（顺序发送）
- ✨ failover（故障转移）
- ✨ priority（优先级发送）
- ✨ 自动重试机制

**增强功能：**
- ✨ 装饰器支持（@log_execution、@catch_errors、@timer）
- ✨ 结构化日志（HTTP、数据库、API、性能、业务）
- ✨ 上下文管理（timer、bind、contextualize）
- ✨ 完整的类型注解
- ✨ 中文友好的文档

---


<div align="center">

### ⭐ 如果这个项目对您有帮助，请给一个 Star ⭐

### 💖 打赏支持

如果您觉得这个项目对您有帮助，欢迎打赏支持！

![打赏支持](https://s2.loli.net/2025/11/10/lQRcAvN3Lgxukqb.png)

---

**Made with ❤️ by [XiaoqiangClub](https://xiaoqiangclub.github.io/)**

</div>