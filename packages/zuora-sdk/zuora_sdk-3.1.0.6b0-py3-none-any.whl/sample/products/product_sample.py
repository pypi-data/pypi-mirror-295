from sample.client import get_client
from zuora_sdk import CreateProductRequest
from zuora_sdk.rest import ApiException


def create_and_get_product(client=None):
    if client is None:
        client = get_client()
    try:
        api_response = client.products_api().create_product(
            CreateProductRequest(**{
                'Name': 'Beverage Delivery Service',
                'Description': 'Beverage Delivery Service',
                'EffectiveStartDate': '2022-04-01',
                'EffectiveEndDate': '2032-04-01'}))
        if api_response.success:
            product_id = api_response.id
            api_response = get_product_by_id(product_id)
            print(api_response)
        else:
            print("fail to create product")
    except ApiException as e:
        print("Exception when calling ProductsApi->create_product: %s\n" % e)


def get_product_by_id(product_id: str, client=None):
    if client is None:
        client = get_client()
    try:
        api_response = client.products_api().get_product(product_id)
    except ApiException as e:
        print("Exception when calling ProductsApi->get_product: %s\n" % e)
    else:
        return api_response


def delete_product(product_id: str, client=None):
    if client is None:
        client = get_client()
    try:
        api_response = client.products_api().delete_product(product_id)
    except ApiException as e:
        print("Exception when calling ProductsApi->delete_product: %s\n" % e)
    else:
        return api_response


def query_products(client=None):
    if client is None:
        client = get_client()
    try:
        api_response = client.object_queries_api().query_products()
        if api_response.data:
            prod = api_response.data[0]
            print('Product Number: %s, Name: %s'% (prod.product_number, prod.name))
            return api_response
        else:
            print('No products found')
    except ApiException as e:
        print("Exception when calling ObjectQueriesApi->query_products: status: %s, reason: %s"
              % (e.status, e.reason))


def query_rate_plan_by_id(product_id:str=None, client=None):
    if client is None:
        client = get_client()
    try:
        api_response = client.object_queries_api().query_product_rate_plans(
            filter=['productId.EQ:%s' % product_id],
            expand=['productrateplancharges', 'productrateplancharges.productrateplanchargetiers'])
        if api_response['data']:
            rate_plan = api_response['data'][0]
            print('Rate Plan Number: %s, Name: %s' % (rate_plan['productRatePlanNumber'], rate_plan['name']))
            if rate_plan['productRatePlanCharges'][0]:
                rate_plan_charge = rate_plan['productRatePlanCharges'][0]
                print('Charge Name: %s, Billing Period: %s' %
                      (rate_plan_charge['productRatePlanChargeNumber'], rate_plan_charge['billingPeriod']))
                rate_plan_charge_tier = rate_plan_charge['productRatePlanChargeTiers'][0]
                print('Tier Active: %s, Currency: %s, Price: %s' %
                      (rate_plan_charge_tier['active'], rate_plan_charge_tier['currency'], rate_plan_charge_tier['price']))
            else:
                print('No rate plan charges found for rate plan %s' % rate_plan['name'])
        else:
            print('No rate plans found for product %s' % product_id)
        return api_response
    except ApiException as e:
        print("Exception when calling ObjectQueriesApi->query_product_rate_plans: status: %s, reason: %s" %
              (e.status, e.reason))


if __name__ == '__main__':
    create_and_get_product()
    query_products()
    query_rate_plan_by_id('8ad097b4917efc7701917f0d297d01b7')