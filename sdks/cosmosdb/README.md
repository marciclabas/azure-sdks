# Cosmos DB

Python SDK for Azure Cosmos DB NoSQL

## About Cosmos DB

### Structure (DBs, containers, items)

- A CosmosDB *resource* can have multiple *DBs*
- A *DB* can have multiple *containers*
- A *container* can have multiple *items*

### Identifying

- Every item has a compulsory `id` field
- Every container defines a partition key, compulsory for all of it's items
  - The container's partition key field can be set to any string, including `/id`
- If the container's partition key is, e.g., `username`, a new item would be:
    ```json
    {
        "id": "<uuid>",
        "username": "<username>",
        // other optional fields
    }
    ```

### Querying

- Points reads can be done by giving `db, container, id, partition_key`
- Containers can be queried with SQL
  - Specifying a `partition_key` will limit the query to a partition

## Authorization

Both required fields can be obtained from the Azure Portal, within the Cosmos DB resource, Keys tab:

- `COSMOS_ENDPOINT` (URI in the portal): `https://<resource-name>.documents.azure.com:443/`
- `COSMOS_KEY` (PRIMARY KEY in the portal): `<random base64 string>`

### Environment (.env)

For convenience, you can set `os.environ["COSMOS_ENDPOINT"]` and `os.environ["COSMOS_KEY"]`. If you do, you can skip specifying them on every call.

E.g., create a `.env` file:

```bash
COSMOS_ENDPOINT="<COSMOS_ENDPOINT>"
COSMOS_KEY="<COSMOS_KEY>"
```

Then load it before importing

```python
from dotenv import load_dotenv
load_dotenv()
import cosmosdb as db

db.client() # just works!
```

## API

- Asynchronous (everything is a coroutine)
- Single calls or multiple using a same client:
  ```python
  # single call
  await db.list.dbs(url=COSMOS_ENDPOINT, key=COSMOS_KEY) # these aren't necessary with a .env file

  # multiple calls
  async with db.client(url=COSMOS_ENDPOINT, key=COSMOS_KEY) as client: # idem.
      await db.create.db("<db name>", client=client)
      dbs = await db.list.dbs(client=client)
  ```

### Functions
```python
cosmosdb
  create
    async def db(...)
    async def container(...)
    async def item(...)
  delete
    async def db(...)
    async def container(...)
    async def item(...)
  list
    async def dbs(...)
    async def containers(...)
    async def items(...)
  query
    async def read(...)
    async def sql(...)
```