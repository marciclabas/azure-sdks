# Azure Blob

## Installation

```bash
pip install blob-az
```

## Authorization

The required connection string can be obtained from the Azure Portal, within the Storage account, "Access keys" tab

### Environment (.env)

For convenience, you can set `os.environ["BLOB_CONN_STR"]`. If you do, you can skip specifying it on every call.

E.g., create a `.env` file:

```bash
BLOB_CONN_STR="<BLOB_CONN_STR>"
```

Then load it before importing

```python
from dotenv import load_dotenv
load_dotenv()
import blob_az as bz

bz.client() # just works!
```

## API

- Asynchronous (everything is a coroutine)
- Single calls or multiple using a same client:
  ```python
  # single call
  await bz.list.containers(conn_str=CONN_STR) # ain't necessary with a .env file

  # multiple calls
  async with bz.client() as client: # idem.
      await bz.container.create("<container-name>", client=client)
      cs = await bz.list.containers(client=client)
  ```

### Functions

```python
az_blob
    def client(...) -> BlobServiceClient
    list
        async def containers(...) -> list[dict]
        async def blobs(...) -> list[dict]
    container
        async def create(...)
        async def delete(...)
    blob
        async def upload(...)
        async def download(...) -> bytes
        def url(...) -> str # generate SAS url for blob
```