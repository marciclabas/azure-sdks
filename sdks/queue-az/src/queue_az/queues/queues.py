from azure.storage.queue.aio import QueueServiceClient
from ..util import with_client
from ..errors import ResourceExistsError
from .. import CONN_STR

@with_client
async def list(
    *, client: QueueServiceClient, conn_str: str = CONN_STR
):
    return [q async for q in client.list_queues()]

@with_client
async def create(
    name: str, metadata: dict[str, str] | None = None,
    *, client: QueueServiceClient, conn_str: str = CONN_STR
) -> ResourceExistsError | None:
    try:
        await client.create_queue(name, metadata=metadata)
    except ResourceExistsError as e:
        return e

@with_client
async def delete(
    name: str, *, client: QueueServiceClient, conn_str: str = CONN_STR
):
    await client.delete_queue(queue=name)