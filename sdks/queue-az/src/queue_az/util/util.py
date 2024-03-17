from functools import wraps
import ramda as R
from azure.storage.queue.aio import QueueServiceClient
from .. import CONN_STR


def with_client(coro):
    """Runs `coro` with client (if provided), otherwise runs within a new client's async context
    - `async def coro(*args, *, client: CosmosClient)`
    """
    @wraps(coro)
    async def f(
        *args, client: QueueServiceClient | None = None,
        conn_str: str | None = CONN_STR, **kwargs
    ):
        kwargs = R.omit(["client", "url", "key"], kwargs)
        if client is None:
            assert conn_str is not None, "Provide a connection string or a client"
            async with QueueServiceClient.from_connection_string(conn_str) as client:
                return await coro(*args, client=client, **kwargs)
        else:
            return await coro(*args, client=client, **kwargs)
    return f

def client(conn_str: str = CONN_STR) -> QueueServiceClient:
    return QueueServiceClient.from_connection_string(conn_str)