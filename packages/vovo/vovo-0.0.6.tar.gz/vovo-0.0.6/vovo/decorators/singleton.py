import threading


def singleton(cls):
    """
    单例装饰器
    """
    instances = {}
    lock = threading.Lock()  # 锁对象，确保线程安全

    def get_instance(*args, **kwargs):
        if cls not in instances:  # 第一次检查（无锁）
            with lock:
                if cls not in instances:  # 第二次检查（有锁）
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
