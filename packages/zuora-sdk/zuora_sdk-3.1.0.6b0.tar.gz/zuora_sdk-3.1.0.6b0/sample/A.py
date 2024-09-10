from pprint import pprint

import zuora_sdk
from zuora_sdk import ProductsApi, CreateProductRequest, GetProductsResponse, Product, CreateContactRequest, ContactResponse
from zuora_sdk.rest import ApiException
from zuora_sdk.zuora_client import ZuoraClient, ZuoraEnvironment


def create_get_product():
    try:

        client = ZuoraClient(client_id='028721ab-81aa-4e5f-9b6a-09e5232a7847',
                             client_secret='JPhD9CQSlzURFm1yCtf8zCZkxvbuF9C4QQ0RFm1dL', env=ZuoraEnvironment.PROD)
        client.set_debug(True)
        client.configuration.verify_ssl = False
        client.add_default_header('X-API-Key', 'a1b2c3d4e5f6g7h8i9j0')
        client.initialize()
        # products: GetProductsResponse = client.products_api().get_products()
        # for p in products.products:
        #     print(client.product_rate_plans_api().get_rate_plans_by_product(p.id))
        #     pass
        # print(client.products_api().get_products())
        # print(client.get_request_timeout())
        # client.set_entity_id('123456789')
        ccr: CreateContactRequest = CreateContactRequest(
            firstName='fff',
            lastName='lll',
            accountNumber='A00009830',
            country="US",
            TextCF__c='this is custom fields'
        )
        # ccr.additional_properties['TextCF__c'] = 'this is custom fields'

        ret: ContactResponse = client.contacts_api().create_contact(ccr)
        print(ret)
        # create_product_request: CreateProductRequest = CreateProductRequest(name='Beverage Delivery Service',
        #                                                                     description='Beverage Delivery Service',
        #                                                                     effective_start_date='2022-04-01',
        #                                                                     effective_end_date='2032-04-01')
        #
        # create_product_request.cc = 'xx'
        #
        # zuora_track_id = '123456789'
        # api_response: zuora_sdk.models.ProxyCreateOrModifyResponse = client.products_api().create_product(create_product_request,
        #                                                                                                   zuora_track_id=zuora_track_id)
        # pprint(api_response)
        # if api_response.success:
        #     product_id: str = api_response.id
        #     api_response: zuora_sdk.models.GetProductResponse = client.products_api().get_product(product_id)
        #     print(api_response)
        # else:
        #     print("fail ot create product")
    except ApiException as e:
        print("Exception when calling ProductsApi->create_product: %s\n" % e)


create_get_product()
