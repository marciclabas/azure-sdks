import argparse
import time
import os
from dotenv import load_dotenv
from azure.messaging.webpubsubclient import WebPubSubClient
from azure.messaging.webpubsubclient.models import OnConnectedArgs, \
    OnGroupDataMessageArgs, OnServerDataMessageArgs
from ..util import service
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str)
    parser.add_argument('--user', '-u', type=str, help='User ID')
    parser.add_argument('--hub', type=str)
    parser.add_argument('--roles', '-r', nargs='*', type=str, default=[])
    parser.add_argument('--env', '-e', type=str, help='.env path')
    parser.add_argument('--conn-str', '-c', type=str)
    parser.add_argument('--groups', '-g', nargs='*', type=str, default=[], help='Groups to join')
    args = parser.parse_args()
    
    if args.conn_str is not None:
        conn_str = args.conn_str
    else:
        load_dotenv(args.env)
        conn_str = os.getenv('PUBSUB_CONN_STR')
    
    if args.url is not None:
        url = args.url
    elif args.hub is not None and args.user is not None:
        roles = args.roles + [f'webpubsub.joinLeaveGroup.{g}' for g in args.groups]
        url = service(args.hub, conn_str).get_client_access_token(user_id=args.user, roles=roles)['url']
    else:
        raise ValueError("Provide either --url or (--user and --hub)")
    

    def on_connected(x: OnConnectedArgs):
        print(f'Connected. UserID = {x.user_id}, ConnectionID = {x.connection_id}')

    def on_group(x: OnGroupDataMessageArgs):
        print(f"Group '{x.group}' message from '{x.from_user_id}'. dtype = {x.data_type}, seq_id = {x.sequence_id}:")
        print(x.data)
        
    def on_server(x: OnServerDataMessageArgs):
        print(f"Server message. dtype = {x.data_type}, seq_id = {x.sequence_id}:")
        print(x.data)
    client = WebPubSubClient(url)
    with client:
        for g in args.groups:
            client.join_group(g)
            print(f"Joined group {g}")
        client.subscribe("connected", on_connected)
        client.subscribe("group-message", on_group)
        client.subscribe("server-message", on_server)
        print('Starting client')
        while True:
            time.sleep(1)