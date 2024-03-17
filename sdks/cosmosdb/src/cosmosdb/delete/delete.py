from azure.cosmos.aio import CosmosClient
from .. import KEY, ENDPOINT
from ..util import with_client

@with_client
async def db(
    database: str, *, client: CosmosClient, url: str = ENDPOINT, key: str = KEY
):
    await client.delete_database(database)

@with_client     
async def container(
    database: str, container: str, *, client: CosmosClient, url: str = ENDPOINT, key: str = KEY
):
    db = client.get_database_client(database)
    await db.delete_container(container)

@with_client
async def item(
    database: str, container: str, id: str, partition_key: str | None = None,
    *, client: CosmosClient, url: str | None = ENDPOINT, key: str | None = KEY
):
    """Delete an item given its `id` and `partition_key`
    - If `partition_key is None`, it'll be set to `id`
    """
    partition_key = partition_key or id
    db = client.get_database_client(database)
    cc = db.get_container_client(container)
    await cc.delete_item(id, partition_key)
