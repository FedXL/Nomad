import requests
from django.conf import settings

TOKEN = settings.CRM_TOKEN

def order_example():
    url = "https://waterapp.me/cab/api/orders"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
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

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200 or response.status_code == 201:
        print("Заказ успешно создан!")
        print(response.json())
    else:
        print("Ошибка при создании заказа!")
        print(response.status_code, response.text)


def append_order():

    pass

