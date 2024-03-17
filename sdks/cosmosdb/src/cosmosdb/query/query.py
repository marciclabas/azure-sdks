from typing import Annotated
from pydantic import BaseModel
from azure.cosmos.aio import CosmosClient
import ramda as R
import haskellian.asynch as hka
from .. import KEY, ENDPOINT
from ..util import with_client

@with_client
async def read(
    database: str, container: str,
    id: int | str, partition_key: str | None = None,
    *, client: CosmosClient, url: str = ENDPOINT, key: str = KEY
) -> dict[str]:
    """Point read of an item given its `id` and `partition_key`
    - If `partition_key is None`, it'll be set to `id`
    """
    partition_key = partition_key or id
    cc = client.get_database_client(database).get_container_client(container)
    return await cc.read_item(str(id), partition_key)
    
def name_val(name: str):
    assert name.startswith('@'), "name must start with '@'"
    return name
    
class Param(BaseModel):
    name: Annotated[str, name_val]
    value: str
    
    
@with_client
async def sql(
    database: str, container: str,
    query: str, params: list[Param] = [], partition_key: str | None = None,
    *, client: CosmosClient, url: str = ENDPOINT, key: str = KEY
) -> list[dict[str]]:
    """
    Query via CosmosDB SQL query
    - `query`: e.g "SELECT * FROM x WHERE x.id = @value" (`FROM _` can be anything, e.g. `FROM me`)
    - `params`: e.g. [Param(name="@value", value=user_id)]
    """
    cont = client.get_database_client(database).get_container_client(container)
    return await hka.syncify(cont.query_items(
        query=query, parameters=R.map(Param.model_dump, params),
        partition_key=partition_key
    ))