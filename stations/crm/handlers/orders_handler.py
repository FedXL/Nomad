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


def order_example(payload):
    url = "https://waterapp.me/cab/api/orders"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print("Заказ успешно создан!")
        print(response.json())
    else:
        print("Ошибка при создании заказа!")
        print(response.status_code, response.text)

def create_order_model(order_id):
    order = Order.objects.get(id=order_id)
    items = order.order_items.all()
    items_list = [item.to_dict() for item in order.order_items.all() if item.item_uuid]
    client = order.client
    phone_crm = client.phone_crm_w
    crm_client = phone_crm.client
    crm_uuid = crm_client.uuid
    if items_list:
        payload = {
        "order": {
            "client_id": crm_uuid,
            "address_id": order.address_id,
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