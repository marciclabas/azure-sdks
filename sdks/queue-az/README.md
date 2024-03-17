# Azure Queue Storage

## Installation

```bash
pip install queue-az
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
import queue_az as qz

qz.client() # just works!
```

## API

- Asynchronous (everything is a coroutine)
- Single calls or multiple using a same client:
  ```python
  # single call
  await qz.list.containers(conn_str=CONN_STR) # ain't necessary with a .env file

  # multiple calls
  async with qz.client() as client:
    queues = await qz.list(client=client)
    for q in queues:
      print(await qz.msg.list(q, client=client))
  ```

### Functions

```python
queue_az
  def client(...) -> QueueServiceClient
  async def create(...)
  async def delete(...)
  async def list(...)
  msg
    async def send(...)
    async def pop(...)
    async def list(...)
```