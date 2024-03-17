"""
### Cosmos DB
> Python SDK for Azure Cosmos DB NoSQL

- `.env`: by default, `COSMOS_ENDPOINT` and `COSMOS_KEY` are retrieved from environment vars. If unset, you'll have to provide or set them manually
"""
from .env import ENDPOINT, KEY
from .util import client, CosmosClient
from . import util, list, create, delete, query, patch