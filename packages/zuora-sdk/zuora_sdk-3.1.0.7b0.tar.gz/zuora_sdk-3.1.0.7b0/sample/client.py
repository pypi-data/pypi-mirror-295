import os
from dotenv import load_dotenv
from zuora_sdk.rest import ApiException
from zuora_sdk.zuora_client import ZuoraClient, ZuoraEnvironment

load_dotenv()


def get_client():
    try:
        client = ZuoraClient(client_id=os.environ.get('ZUORA_CLIENT_ID'),
                             client_secret=os.environ.get('ZUORA_CLIENT_SECRET'),
                             env=ZuoraEnvironment.SBX)
        client.initialize()
        client.set_debug(True)
    except ApiException as ex:
        print("Error create api client", ex)
    else:
        return client
