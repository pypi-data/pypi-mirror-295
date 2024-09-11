from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractHttpClient(ABC):
    """
    HTTP 客户端的抽象基类，异步请求的方法。
    """

    @abstractmethod
    async def request_async(self, method: str, url: str, params: Dict[str, Any] = None,
                            data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Any:
        """
        异步 HTTP 请求

        :param method: HTTP 方法（GET, POST, PUT, DELETE 等）
        :param url: 请求的相对或完整 URL
        :param params: URL 查询参数，可选
        :param data: 请求体数据，可选
        :param headers: 自定义请求头，可选
        :return: 返回响应的数据
        """
        pass

