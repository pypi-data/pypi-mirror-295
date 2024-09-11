import os

from zuora_sdk import CreateAccountRequest, CreateAccountContact

from sample.client import get_client

from zuora_sdk.zuora_client import ZuoraClient, ZuoraEnvironment
from zuora_sdk.rest import ApiException


def query_accounts(client=None, **kwargs):
    if client is None:
        client = get_client()
    try:
        client.object_queries_api()
        api_response = client.object_queries_api().query_accounts(**kwargs)
        return api_response
    except ApiException as e:
        print("Exception when calling ObjectQueriesApi->query_account: %s %s\n" % (e.status, e.reason))


def create_account(client=None):
    if client is None:
        client = get_client()
    try:
        account = client.accounts_api().create_account(
            CreateAccountRequest(**{
                'name': 'Amy Lawrence\'s account',
                'billToContact': CreateAccountContact(**{
                    'firstName': 'Amy',
                    'lastName': 'Lawrence',
                    'state': 'California',
                    'country': 'USA'
                }),
                'autoPay': False,
                'currency': 'USD',
                'billCycleDay': 1
            }))
        print('Account is created, Number: %s' % account.account_number)
        return account
    except ApiException as e:
        print("Exception when calling AccountsApi->create_account: status: %s, reason: %s"
              % (e.status, e.reason))


def query_account_by_key(account_key, client=None):
    if not client:
        client = get_client()
    try:

        api_response = client.object_queries_api().query_account_by_key(
            account_key,
            expand=['billTo'])
        print(api_response)
        return api_response
    except ApiException as e:
        if e.status == 404:
            print("Account %s not found" % account_key)
        else:
            print("Exception when calling ObjectQueriesApi->query_account_by_key: status: %s, reason: %s, body: %s"
                  % (e.status, e.reason, e.body))


if __name__ == '__main__':
    # pass
    ret = create_account()
    print(query_accounts(filter=['accountnumber.EQ:%s' % ret.account_number]))
    result = query_account_by_key('A00000001')
