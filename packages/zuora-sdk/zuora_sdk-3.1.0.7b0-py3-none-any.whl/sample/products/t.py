from zuora_sdk import CreateProductRequest, AccountData, ContactInfo

#
c = CreateProductRequest(
    # name='x',
    description='22',
    effective_start_date='2022-04-01',
    effective_end_date='2032-04-01')
c.item_type__ns = 'x'
#
# c.additional_properties['custom_field'] = 123
print(c.to_json())
_dict = {"Description": 123, "EffectiveStartDate": "2022-04-01", "EffectiveEndDate": "2032-04-01",
         }
c = CreateProductRequest(**_dict)
c.additional_properties['custom_field'] = 123

# print(c.to_json())
a = AccountData(account_number='A00000001', name='x', description=22, effective_start_date='2022-04-01',
                effective_end_date='2032-04-01')
a.name = 'batch1'
a.bill_to_contact = ContactInfo(first_name='x', last_name='x')
a.custom_fields = {'custom_field': 123}
print(a.to_json())
