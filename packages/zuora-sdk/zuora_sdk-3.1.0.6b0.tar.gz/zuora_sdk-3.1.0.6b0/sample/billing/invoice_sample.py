from sample.client import get_client
from zuora_sdk.rest import ApiException
from datetime import date


def query_invoice_by_number(invoice_number, client=None):
    if not client:
        client = get_client()
    try:
        api_response = client.object_queries_api().query_invoice_by_key(
            invoice_number,
            expand=['invoiceItems'])
        print(api_response)
    except ApiException as e:
        if e.status == 404:
            print("Invoice %s not found" % invoice_number)
        else:
            print("Exception when calling ObjectQueriesApi->query_invoice_by_key: status: %s, reason: %s"
                  % (e.status, e.reason))


def query_invoices_by_account(account_key, client=None):
    if not client:
        client = get_client()
    try:
        api_response = client.object_queries_api().query_invoices(
            filter=['accountId.EQ:%s' % account_key])
        print(api_response)
    except ApiException as e:
        print("Exception when calling ObjectQueriesApi->query_invoices_by_account: %s" % e)


if __name__ == '__main__':
    # pass
    query_invoice_by_number('INV00000315')
    query_invoices_by_account('2c92c0f96db4d8cc016db9400a4e4c16')