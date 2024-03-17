from functools import wraps
from azure.cosmos.aio import CosmosClient
import ramda as R
from .. import KEY, ENDPOINT

def with_client(coro):
    """Runs `coro` with client (if provided), otherwise runs within a new client's async context
    - `async def coro(*args, *, client: CosmosClient)`
    """
    @wraps(coro)
    async def f(
        *args, client: CosmosClient | None = None,
        url: str | None = ENDPOINT, key: str | None = KEY, **kwargs
    ):
        kwargs = R.omit(["client", "url", "key"], kwargs)
        if client is None:
            assert url is not None and key is not None, "Provide a key+endpoint or a client"
            async with CosmosClient(url=url, credential=key) as client:
                return await coro(*args, client=client, **kwargs)
        else:
            return await coro(*args, client=client, **kwargs)
    return f

def client(url: str = ENDPOINT, key: str = KEY) -> CosmosClient:
    return CosmosClient(url=url, credential=key)