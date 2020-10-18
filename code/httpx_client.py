import httpx


class HTTPXAsyncClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = httpx.AsyncClient()
        return cls._client


HTTPX_client = HTTPXAsyncClient()
