import asyncio
from datetime import datetime, timedelta
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContainerSasPermissions, generate_container_sas
from .. import CONN_STR, KEY
from ..util import with_client
from .. import list, blob

@with_client
async def create(
    container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR
):
    await client.create_container(container)

@with_client
async def delete(container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR):
    await client.delete_container(container)

@with_client
async def clear(container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR):
    blobs = await list.blobs(container, client=client)
    return await asyncio.gather(*[
        blob.delete(container, b, client=client)
        for b in blobs
    ])
    
def sas(
    container: str, *, account_key: str = KEY, conn_str: str | None = CONN_STR,
    client: BlobServiceClient | None = None,
    expiry: datetime = datetime.now() + timedelta(days=1),
    permission = ContainerSasPermissions(read=True)
) -> str:
    """Token for access to the whole container. Usage: `authed_url = {blob_url}?{sas(container)}`"""
    assert conn_str is not None or client is not None, "Provide a connection string or a client"
    client = client or BlobServiceClient.from_connection_string(conn_str)
    token = generate_container_sas(
      account_name=client.account_name, container_name=container,
      account_key=account_key, expiry=expiry, permission=permission
    )
    return token

def url(
    container: str, conn_str: str | None = CONN_STR,
    client: BlobServiceClient | None = None
) -> str:
    """Unauthenticated URL. Use together with `bz.container.sas` to access"""
    client = client or BlobServiceClient.from_connection_string(conn_str)
    return client.get_container_client(container).url
