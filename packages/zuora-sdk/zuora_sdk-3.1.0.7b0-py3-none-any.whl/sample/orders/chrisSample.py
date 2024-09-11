from zuora_sdk import CreateOrderRequest, PreviewOrderRequest, PreviewOrderResponse, PreviewOrderSubscriptionsAsync, \
    PreviewOrderOrderAction, PreviewOrderCreateSubscriptionTerms, PreviewOrderRatePlanOverride, InitialTerm, \
    PreviewOrderCreateSubscription, PreviewOptions, ProcessingOptions, BillingOptions, CreateOrderSubscription, \
    CreateOrderAction, CreateOrderCreateSubscription, OrderActionCreateSubscriptionTerms, CreateOrderRatePlanOverride, \
    CreateOrderResponse, RenewalTerm, GetSubscriptionResponse

from sample.client import get_client
from zuora_sdk.rest import ApiException
from datetime import date


def get_subscription(client=None, subscription_number=None):
    if not client:
        client = get_client()
    r: GetSubscriptionResponse = client.subscriptions_api().get_subscription_by_key(subscription_number)
    print(r)
    print(r.rate_plans[0].rate_plan_charges[0].mrr)
    pass


def preview_order(client=None):
    if not client:
        client = get_client()
    try:
        request = PreviewOrderRequest(**{
            'order_date': date.today().strftime('%Y-%m-%d'),
            'existing_account_number': 'A00000001',
            'subscriptions': [],
            'preview_options':
                PreviewOptions(preview_thru_type='NumberOfPeriods', preview_number_of_periods=1, preview_types=['BillingDocs'])
        })
        request.subscriptions.append(
            PreviewOrderSubscriptionsAsync(**{
                'order_actions': [PreviewOrderOrderAction(**{
                    'type': 'CreateSubscription',
                    'create_subscription': PreviewOrderCreateSubscription(**{
                        'terms': PreviewOrderCreateSubscriptionTerms(initial_term=InitialTerm(term_type='EVERGREEN')),
                        'subscribe_to_rate_plans': [
                            PreviewOrderRatePlanOverride(product_rate_plan_number='PRP-00000151')
                        ]
                    })
                })]
            })
        )
        api_response: PreviewOrderResponse = client.orders_api().preview_order(request)
        print(api_response)
    except ApiException as e:
        print("Exception when calling OrdersApi->preview_order: %s\n" % e)
    return None


def create_order(client=None):
    if not client:
        client = get_client()
    try:
        request = CreateOrderRequest(**{
            'order_date': date.today().strftime('%Y-%m-%d'),
            'existing_account_number': 'A00000001',
            'subscriptions': [],
            'processing_options':
                ProcessingOptions(run_billing=True, billing_options=BillingOptions(target_date=date.today().strftime('%Y-%m-%d')))
        })
        request.subscriptions.append(
            CreateOrderSubscription(**{
                'order_actions': [CreateOrderAction(**{
                    'type': 'CreateSubscription',
                    'create_subscription': CreateOrderCreateSubscription(**{
                        'terms': OrderActionCreateSubscriptionTerms(
                            initial_term=InitialTerm(term_type='EVERGREEN')),
                        'subscribe_to_rate_plans': [
                            CreateOrderRatePlanOverride(product_rate_plan_number='PRP-00000151')
                        ]
                    })
                })]
            })
        )
        api_response: CreateOrderResponse = client.orders_api().create_order(request)

        print(api_response)
        return api_response.subscriptions[0].subscription_number
    except ApiException as e:
        print("Exception when calling OrdersApi->create_order: %s\n" % e)
    return None


if __name__ == '__main__':
    client = get_client()
    number = create_order(client)
    get_subscription(client, subscription_number=number)
