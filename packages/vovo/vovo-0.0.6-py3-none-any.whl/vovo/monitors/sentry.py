import os

import sentry_sdk


def init_sentry(sentry_uri=None, traces_sample_rate=1.0, profiles_sample_rate=1.0):
    """
    初始化 Sentry 监控配置

    :param sentry_uri: Sentry DSN URI。如果未提供，则从环境变量 'SENTRY_URI' 中获取。
    :param traces_sample_rate: 性能监控的采样率。默认设置为 1.0，表示捕获 100% 的事务。
    :param profiles_sample_rate: 采样事务的性能分析采样率。默认设置为 1.0，表示对采样的 100% 事务进行分析。
    """

    # 如果未传递 sentry_uri 参数，则从环境变量中获取 SENTRY_URI
    if sentry_uri is None:
        sentry_uri = os.getenv('SENTRY_URI')

    # 如果找到 SENTRY_URI，初始化 Sentry 监控
    if sentry_uri:
        sentry_sdk.init(
            dsn=sentry_uri,
            # 设置 traces_sample_rate 为 1.0，以捕获 100% 的事务用于性能监控
            traces_sample_rate=traces_sample_rate,
            # 我们建议在生产环境中调整此值以减少开销
            profiles_sample_rate=profiles_sample_rate,
        )
    else:
        raise ValueError("未找到 SENTRY_URI")