import requests
from django.conf import settings
from shop.models import Order
TOKEN = settings.CRM_TOKEN



"""
payload = {
        "order": {
            "client_id": "6507dd0ac32dab0b63f9a2be",
            "address_id": "6507dd2ac32dab0b85f7efaf",
            "pay_type_id": "647f20e3c32dab21a2a5e757",
            "items": [
                {
                    "item_id": "65081414c32dab0b5efe7007",
                    "art": "",
                    "title": "Вода Nomad 18.9л",
                    "price": 95000,
                    "quantity": 1
                }
            ],
            "delivery_type": "delivery",
            "status_symbol": "waiting_approve",
            "order_source": "crm",
            "date": "11.04.2025",
            "time_from": "06:00",
            "time_to": "07:00",
            "comment": "Комментарий",
            "phone": "+7 (778) 580-3010",
            "custom_api_fields": {
                "custom_field": "Любые поля! которые могут вам понадобиться"
            }
        }
    }
"""


def send_order(payload):
    url = "https://waterapp.me/cab/api/orders"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200 or response.status_code == 201:
        return True, response.json()
    else:
        return False, response.text

def create_order_model(order_id):
    order = Order.objects.get(id=order_id)
    items = order.order_items.all()
    items_list = [item.to_crm_dict() for item in order.order_items.all() if item.item_uuid]
    client = order.client
    address_uuid = client.last_address_uuid
    phone_crm = client.phone_crm_w
    crm_client = phone_crm.client
    crm_uuid = crm_client.client_uuid
    if items_list:
        payload = {
        "order": {
            "client_id": crm_uuid,
            "address_id": address_uuid,
            "pay_type_id": order.payment_choice,
            "items": items_list,
            "delivery_type": "delivery",
            "status_symbol": "waiting_approve",
            "order_source": "webhook",
            "date": order.delivery_date.strftime("%d.%m.%Y"),
            "time_from": order.time_start,
            "time_to": order.time_end,
            "comment": "211",
            "phone": phone_crm.phone,
            "custom_api_fields": {"from_WhatsApp": "yes"}
        }
    }
        return payload
    else:
        return False

"""
{'order': {'id': '67fbf8aaa4fcf623e5ad1613',
'city_branch_id': '647f20e0c32dab21a2a5e749',
'client_id': '67e85fe2fc13b0002f157a40',
'client': {'id': '67e85fe2fc13b0002f157a40',
'phone': None, 'phones': [{'phone': '79989999999', 'comment': 'From WatsApp Bot User', 'notices': False, 'first_name': 'Tester!', 'last_name': ''}],
'email': '', 'birthday': '', 'fio': None,
'created_at': '2025-03-30T02:02:26.589+05:00',
'updated_at': '2025-03-30T03:25:52.367+05:00',
'comment': 'User from WatsApp Bot',
'drivers_comment': '', 'bonuses': 0, 'orders_count': 0, 'has_rek': False, 'code': None,
'custom_api_fields': {'custom_field': ''}, 'integration_guid': '', 'addresses': [],
'contract_1c_id': None, 'contract_1c_title': None, 'contract_1c_start_date': None,
'client_type': 'fiz', 'ur_type': 'ooo', 'ur_title': '', 'ur_dir': '',
'ur_dir_rod': '', 'ur_dir_sokr': '', 'ur_address': '', 'ur_address_index': '',
'ur_address_region_code': '', 'ur_address_region': '', 'ur_address_district': '',
'ur_address_city': '', 'ur_address_settlement': '', 'ur_address_street': '',
'ur_address_house': '', 'ur_address_korp': '', 'ur_address_kv': '',
'ur_address_other': '', 'ur_off_address': '', 'ur_off_address_index': '',
'ur_off_address_region_code': '', 'ur_off_address_region': '',
'ur_off_address_district': '', 'ur_off_address_city': '',
'ur_off_address_settlement': '', 'ur_off_address_street': '',
'ur_off_address_house': '', 'ur_off_address_korp': '',
'ur_off_address_kv': '', 'ur_off_address_other': '', 'ur_inn': '', 'ur_kpp': '',
'ur_ogrn_ip': '', 'ur_okpo': '', 'ur_accounter_fio': '', 'ur_accounter_fio_sokr': '',
'ur_bank_title': '', 'ur_bank_bik': '', 'ur_account_number': '', 'ur_kor_account': '',
'ur_phone': '', 'ur_email': '', 'ur_invoice_fio': '', 'ur_invoice_position': '',
'ur_store_position': '', 'ur_store_sign': '',
'ur_acccount_type': 'simple', 'ur_vat': '0'},
'phone': '79989999999', 'fio': '', 'address_id': '67e87e9f3c42a40015404bd7',
'address_model': {'id': '67e87e9f3c42a40015404bd7', 'city': 'Алматы',
'street': 'Розыбакиева (Достык) улица', 'dom': '52',
'kv': None, 'korp': '',
'floor': None, 'entrance': None, 'doorcode': '',
'comment': 'Розыбакиева 52', 'client_comment': '',
'map_addr': 'Алматы,  Розыбакиева (Достык) улица д 52',
'full_addr': 'Розыбакиева (Достык) улица д 52 Розыбакиева 52',
'full_addr_with_city': 'Алматы,  Розыбакиева (Достык) улица д 52 Розыбакиева 52',
'details': 'Розыбакиева 52', 'curier': {'map_addr': 'Алматы,  Розыбакиева (Достык) улица д 52',
'map_addr_full': 'Алматы, Розыбакиева (Достык) улица, д 52',
'details': 'Розыбакиева 52'}, 'district_id': '',
'district': None, 'delivery_zone_id': '', 'item_stocks_report': [],
'persisted': True, 'location': {'lat': None, 'lng': None},
'is_dirty': False, 'can_user_edit': False},
'district_id': '', 'delivery_zone_id': '',
'items': [{'item_id': '65081414c32dab0b5efe7007',
'title': 'water_19L', 'choosen_toppings': None,
'topping_ids': None, 'art': '', 'descr': None, 'quantity': 3,
'price_conditions': None, 'icon_url': None, 'price': 95000, 'actual_price': None}],
'status_symbol': 'waiting_approve', 'status_reason': '',
'status_changed_time': None, 'date': '15.04.2025',
'time_from': '9:00', 'time_to': '15:00', 'sum': 285000,
'pay_sum': 285000, 'pay_type_id': '647f20e3c32dab21a2a5e757',
'pay_type': {'id': '647f20e3c32dab21a2a5e757', 'title': 'Нал',
'system_name': 'cash', 'cashbox': {'id': '647f20e9c32dab21a2a5e790', 'title': 'Нал'},
'is_just_send': True, 'is_cash': False, 'driver_can_collect_money': True,
'need_mark_scan': False, 'receipt_creation': 'none', 'receipt_creation_type': 'cash_buy',
'title_1c': None}, 'delivery_type': 'delivery', 'store_id': '647f20e9c32dab21a2a5e792',
'order_group_id': None, 'order_group': None, 'integration_guid': '',
'custom_api_fields': {'from_WhatsApp': 'yes'}, 'for_1c': False, 'docs_created_1c': False,
'docs_order_created_1c': False, 'docs_bill_created_1c': False, 'docs_invoice_created_1c': False,
'docs_realization_created_1c': False, 'docs_waybill_created_1c': False, 'docs_cash_receipt_created_1c': False,
'docs_return_created_1c': False, 'order_source': 'webhook',
'items_with_marking': [{'item_id': '65081414c32dab0b5efe7007', 'title': 'water_19L', 'art': '',
 'price': 95000, 'quantity': 3,
'marking': [], 'kizes': []}], 'marking': []}}
"""