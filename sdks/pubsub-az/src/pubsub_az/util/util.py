from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient as AsyncService
from azure.messaging.webpubsubservice import WebPubSubServiceClient
from .. import CONN_STR

def service(hub: str, conn_str: str = CONN_STR) -> WebPubSubServiceClient:
    s: WebPubSubServiceClient = WebPubSubServiceClient.from_connection_string(
        connection_string=conn_str, hub=hub
    )
    return s

def async_service(hub: str, conn_str: str = CONN_STR) -> AsyncService:
    s: AsyncService = AsyncService.from_connection_string(
        connection_string=conn_str, hub=hub
    )
    return s