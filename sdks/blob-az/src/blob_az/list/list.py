from azure.storage.blob.aio import BlobServiceClient
import haskellian.asynch as hka
from ..util import with_client

@with_client
async def containers(
    *, client: BlobServiceClient, conn_str: str = None
) -> list[dict[str]]:
    return await hka.syncify(client.list_containers())

@with_client
async def blobs(
    container: str, *, client: BlobServiceClient, conn_str: str = None
) -> list[str]:
    cc = client.get_container_client(container)
    return await hka.syncify(cc.list_blob_names())