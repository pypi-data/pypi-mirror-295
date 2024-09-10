from zuora_sdk import CreateOrderRequest, PreviewOrderRequest, PreviewOrderResponse, PreviewOrderSubscriptionsAsync, \
    PreviewOrderOrderAction, PreviewOrderCreateSubscriptionTerms, PreviewOrderRatePlanOverride, InitialTerm, \
    PreviewOrderCreateSubscription, PreviewOptions, ProcessingOptions, BillingOptions, CreateOrderSubscription, \
    CreateOrderAction, CreateOrderCreateSubscription, OrderActionCreateSubscriptionTerms, CreateOrderRatePlanOverride, \
    CreateOrderResponse, RenewalTerm, ProcessingOptionsWithDelayedCapturePayment

from sample.client import get_client
from zuora_sdk.rest import ApiException
from datetime import date


def preview_order(client=None):
    if not client:
        client = get_client()
    try:
        request = PreviewOrderRequest(**{
            'orderDate': date.today().strftime('%Y-%m-%d'),
            'existingAccountNumber': 'A00000001',
            'subscriptions': [],
            'previewOptions':
                PreviewOptions(preview_thru_type='NumberOfPeriods', preview_number_of_periods=1, preview_types=['BillingDocs'])
        })
        request.subscriptions.append(
            PreviewOrderSubscriptionsAsync(**{
                'orderActions': [PreviewOrderOrderAction(**{
                    'type': 'CreateSubscription',
                    'createSubscription': PreviewOrderCreateSubscription(**{
                        'terms': PreviewOrderCreateSubscriptionTerms(initial_term=InitialTerm(term_type='EVERGREEN')),
                        'subscribeToRatePlans': [
                            # product_rate_plan_id is required for subscriptions???
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
            'existingAccountNumber': 'A00000001',
            'subscriptions': [],
            'processing_options':
                ProcessingOptionsWithDelayedCapturePayment(run_billing=True, billing_options=BillingOptions(target_date=date.today().strftime('%Y-%m-%d')))
        })
        request.subscriptions.append(
            CreateOrderSubscription(**{
                'orderActions': [CreateOrderAction(**{
                    'type': 'CreateSubscription',
                    'createSubscription': CreateOrderCreateSubscription(**{
                        'terms': OrderActionCreateSubscriptionTerms(
                            # renewal_terms is required for OrderActionCreateSubscriptionTerms???
                            initial_term=InitialTerm(term_type='EVERGREEN')),
                        'subscribeToRatePlans': [
                            CreateOrderRatePlanOverride(product_rate_plan_number='PRP-00000151')
                        ]
                    })
                })]
            })
        )
        api_response: CreateOrderResponse = client.orders_api().create_order(request)
        print(api_response)
    except ApiException as e:
        print("Exception when calling OrdersApi->create_order: %s\n" % e)
    return None


if __name__ == '__main__':
    preview_order()
    # have issue with renewal_terms
    create_order()
