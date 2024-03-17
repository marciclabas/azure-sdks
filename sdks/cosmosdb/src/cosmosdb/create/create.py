from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey
from .. import KEY, ENDPOINT
from ..util import with_client

@with_client
async def db(
    database: str, *, client: CosmosClient | None = None,
    url: str = ENDPOINT, key: str = KEY, **kwargs
):
    """Creates a new DB"""
    await client.create_database(database, **kwargs)

@with_client
async def container(
    database: str, container: str, partition_key: str = "/id", *,
    client: CosmosClient | None = None, url: str | None = ENDPOINT, key: str | None = KEY,
    **kwargs
):
    """Creates container within DB (also creates database if needed)"""
    db = await client.create_database_if_not_exists(database)
    key_path = PartitionKey(path=partition_key)
    await db.create_container(id=container, partition_key=key_path, **kwargs)
    
@with_client
async def item(
    database: str, container: str, body: dict[str], replace: bool = True,
    *, client: CosmosClient | None = None, url: str | None = ENDPOINT, key: str | None = KEY,
) -> dict[str]:
    db = client.get_database_client(database)
    cc = db.get_container_client(container)
    if replace:
        return await cc.upsert_item(body)
    else:
        return await cc.create_item(body)
