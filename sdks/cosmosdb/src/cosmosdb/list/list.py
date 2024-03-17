from azure.cosmos.aio import CosmosClient
import haskellian.asynch as hka
from .. import KEY, ENDPOINT
from ..util import with_client

@with_client
async def dbs(
    *, client: CosmosClient | None, url: str | None = ENDPOINT, key: str | None = KEY
) -> list[dict[str]]:
    """List all databases of the Cosmos DB resource"""
    return await hka.syncify(client.list_databases())
    
@with_client
async def containers(
    database: str, *, client: CosmosClient | None, url: str = ENDPOINT, key: str = KEY
) -> list[dict[str]]:
    """List all containers of a given database"""
    db = client.get_database_client(database)
    return await hka.syncify(db.list_containers())

@with_client
async def items(
    database: str, container: str, *,
    client: CosmosClient | None, url: str = ENDPOINT, key: str = KEY
) -> list[dict[str]]:
    """List all items of a given container (within a database)"""
    db = client.get_database_client(database)
    cc = db.get_container_client(container)
    return await hka.syncify(cc.read_all_items())
