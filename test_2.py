import requests

# Установите ваш токен авторизации
token = "ваш_токен"

# Установите URL для запроса типов оплаты
url = "https://waterapp.me/cab/api/pay_types.json"

# Установите заголовки для запроса
headers = {
    "Authorization": "Bearer 3292d7e9-813d-472e-957d-36a1b699e81b",
    "Content-Type": "application/json"
}

# Выполните GET запрос
response = requests.get(url, headers=headers)

# Проверьте статус ответа
if response.status_code == 200:
    # Получите список типов оплаты
    pay_types = response.json().get("list", [])
    for pay_type in pay_types:
        print(f"ID: {pay_type['id']}, Title: {pay_type['title']}")
else:
    print(f"Ошибка: {response.status_code}, {response.text}")