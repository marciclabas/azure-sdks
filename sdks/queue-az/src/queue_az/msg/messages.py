from typing import Literal, NamedTuple, Callable, Awaitable
from datetime import timedelta
import json
from azure.storage.queue import QueueMessage
from azure.storage.queue.aio import QueueServiceClient
from ..util import with_client, client as make_client
from ..config import CONN_STR
from ..errors import ResourceNotFoundError

@with_client
async def send(
    queue: str, message, timeout: timedelta = timedelta(seconds=0),
    ttl: timedelta | None = None, encoding: Literal['json'] = 'json',
    *, client: QueueServiceClient, conn_str: str = None
) -> ResourceNotFoundError | None:
    """Send `message` to `queue`
    - `timeout`: time before `message` is visible
    - `ttl`: time after which the `message` will be deleted (never if `None`)
    """
    content = json.dumps(message)
    secs_ttl = -1 if ttl is None else ttl.total_seconds()
    qc = client.get_queue_client(queue)
    await qc.send_message(content=content, visibility_timeout=timeout.total_seconds(), time_to_live=secs_ttl)

class PopReturn(NamedTuple):
    message: dict[str] | str
    confirm: Callable[[], Awaitable[None]]

@with_client
async def pop(
    queue: str, encoding: Literal['json', 'raw'] = 'json',
    visibility_timeout: timedelta = timedelta(seconds=30),
    *, client: QueueServiceClient, conn_str: str = None
) -> ResourceNotFoundError | None | PopReturn:
    """Retrieve a message from `queue`. Returns `(message, confirm)`
    - `confirm`: must be called after the message is processed, to confirm its processing.
        - Otherwise, it will reappear in the queue after `visibility_timeout`
    """
    try:
        qc = client.get_queue_client(queue)
        msg = await qc.receive_message(visibility_timeout=visibility_timeout.total_seconds())
        if msg is None:
            return None
        
        async def confirm():
            qc = make_client(conn_str or CONN_STR).get_queue_client(queue)
            await qc.delete_message(msg)
        message = json.loads(msg.content) if encoding == 'json' else msg.content
        return PopReturn(message=message, confirm=confirm)
    except ResourceNotFoundError as e:
        return e


@with_client
async def list(
    queue: str, *, client: QueueServiceClient, conn_str: str = None
) -> ResourceNotFoundError | list[QueueMessage]:
    """List messages without popping"""
    try:
        qc = client.get_queue_client(queue)
        return await qc.peek_messages()
    except ResourceNotFoundError as e:
        return e