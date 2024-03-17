# Azure Web PubSub

> Python SDK for Azure Web PubSub

## Disclaimer

Unless you need something decently simple (e.g. server-to-client one-way communication), I think Socket.IO may be a better option. Azure Web PubSub has a managed service for Socket.IO (read more [here](https://learn.microsoft.com/en-us/azure/azure-web-pubsub/socketio-overview)), or you can host your own server with [`python-socketio`](https://python-socketio.readthedocs.io/en/stable/)

## Installation

```bash
pip install pubsub-az
```

## Authorization

- `PUBSUB_CONN_STR` (Connection string in the portal)

### Environment (.env)

For convenience, you can set `os.environ["PUBSUB_CONN_STR"]` and can skip specifying it on every call.

E.g., create a `.env` file:

```bash
PUBSUB_CONN_STR="<PUBSUB_CONN_STR>"
```

Then load it before importing

```python
from dotenv import load_dotenv
load_dotenv()
import pubsub_az as pz

pz.service(hub='<hub>') # just works!
```

## CLI

Basic listener priting messages received. To install, run:

```bash
pip install pubsub-az[client]
```

Then, to execute from the terminal:

```bash
pubsub-client --user "<user-id>" --hub "<hub>" --groups "<g1>" "<g2>" # ...
```