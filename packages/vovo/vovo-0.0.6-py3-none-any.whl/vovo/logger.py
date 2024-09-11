import logging
import structlog
import sys
from colorama import init

# 初始化 colorama 以支持 Windows 系统上的颜色显示
init(autoreset=True)

Logger = structlog.get_logger()


def configure_logging(log_format="key_value", log_level=logging.INFO, use_colors=True):
    """
    配置 structlog 日志记录器。

    :param use_colors: 是否启用颜色输出（默认启用）
    :param log_format: 日志输出格式 ('key_value' 或 'json')
    :param log_level: 日志级别，默认是 logging.INFO
    """

    # 配置 Python 原生 logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # 选择输出格式（KeyValueRenderer 或 JSONRenderer）
    if log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=use_colors)

    # 配置 structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,  # 根据日志级别过滤
            structlog.stdlib.add_logger_name,  # 添加 logger 名称
            structlog.stdlib.add_log_level,  # 添加日志级别
            structlog.processors.StackInfoRenderer(),  # 如果有异常，添加栈信息
            structlog.processors.format_exc_info,  # 格式化异常信息
            structlog.processors.TimeStamper(fmt="iso"),  # 添加时间戳
            renderer,  # 使用选择的渲染器（支持颜色和多种格式）
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
