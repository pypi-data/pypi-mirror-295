import six
from zuora_sdk.models import *
from zuora_sdk.rest import ApiException
from zuora_sdk.zuora_client import ZuoraClient, ZuoraEnvironment

def create_order():
    try:

        client = ZuoraClient(client_id='952d3704-c3f0-4b35-b493-52a55d15195e',
                             client_secret='BnaQsgugQRer46MriIncMfY6uN5X5aXs7S7RPvG/Z', env=ZuoraEnvironment.SBX)
        client.set_debug(True)
        client.initialize()
        create_order_request = {"category": "NewSales", "description": "Order create subscription w/ Prepaid Drawdown", "existingAccountNumber": "A00001828", "orderDate": "2021-02-17", "processingOptions": {"billingOptions": {"documentDate": "2023-02-01", "targetDate": "2023-02-01"}, "collectPayment": False, "runBilling": False}, "subscriptions": [{"orderActions": [{"createSubscription": {"subscribeToRatePlans": [{"productRatePlanId": "8ad08ae29111e9fa019120e19580544c"}], "terms": {"initialTerm": {"period": 12, "periodType": "Month", "startDate": "2022-08-17", "termType": "TERMED"}, "renewalSetting": "RENEW_WITH_SPECIFIC_TERM", "renewalTerms": [{"period": 12, "periodType": "Month"}]}}, "triggerDates": [{"name": "ContractEffective", "triggerDate": "2022-08-17"}, {"name": "ServiceActivation", "triggerDate": "2022-08-17"}, {"name": "CustomerAcceptance", "triggerDate": "2022-08-17"}], "type": "CreateSubscription"}]}]}
        request = CreateOrderRequest(**create_order_request)
        ret = client.orders_api().create_order(request)
        print(ret)
    except ApiException as e:
        print("Exception when calling orders_api -> create_order: %s\n" % e)


create_order()
