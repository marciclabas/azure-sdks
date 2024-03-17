from typing import Literal, Annotated, Any
from pydantic import BaseModel, StringConstraints, model_serializer
from azure.cosmos.aio import CosmosClient
import ramda as R
from .. import KEY, ENDPOINT
from ..util import with_client

Path = Annotated[str, StringConstraints(pattern='/.*')]

class ValueOp(BaseModel):
    op: Literal['add', 'replace', 'set', 'incr', 'remove']
    value: Any
    path: Path

class MoveOp(BaseModel):
    op: Literal['move'] = 'move'
    from_: Path
    to: Path
    
    @model_serializer
    def dump(self) -> dict[str, Any]:
        return {
            'op': self.op,
            'from': self.from_,
            'path': self.to
        }

Op = ValueOp | MoveOp

@with_client
async def item(
    database: str, container: str, id: str, ops: list[Op], partition_key: str | None = None,
    *, client: CosmosClient | None = None, url: str | None = ENDPOINT, key: str | None = KEY,
) -> dict[str]:
    """Partial update (PATCH) a given item. See [Azure's docs](https://learn.microsoft.com/en-us/azure/cosmos-db/partial-document-update) and [python SDK docs](https://learn.microsoft.com/en-us/azure/cosmos-db/partial-document-update-getting-started?tabs=python) for details
    - Returns the patched object"""
    cc = client.get_database_client(database).get_container_client(container)
    dict_ops = [op.model_dump(mode='json') for op in ops]
    return await cc.patch_item(item=id, partition_key=partition_key or id, patch_operations=dict_ops)
