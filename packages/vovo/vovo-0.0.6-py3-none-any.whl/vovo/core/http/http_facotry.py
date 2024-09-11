import httpx

DEFAULT_CONNECTION_TIMEOUT: int = 30
DEFAULT_REQUEST_TIMEOUT: int = 100


class VovoClientFactory:
    """Http client factory"""

    @staticmethod
    def get_client(base_url: str = '', headers: dict = None) -> httpx.AsyncClient:
        """Returns a native HTTP AsyncClient(httpx.AsyncClient) instance

          Args:
            base_url (str): The base URL for the client.
            headers (dict, optional): Custom headers to include in the requests. Defaults to None.

        Returns:
            httpx.AsyncClient
        """
        timeout = httpx.Timeout(DEFAULT_REQUEST_TIMEOUT, connect=DEFAULT_CONNECTION_TIMEOUT)
        return httpx.AsyncClient(timeout=timeout, http2=True, base_url=base_url, headers=headers)
