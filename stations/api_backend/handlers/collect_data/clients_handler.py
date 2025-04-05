import requests


url = "https://waterapp.me"
url += '/cab/api/clients'

request_settings = {
    "url": url,
    "headers": {
        "Authorization": "Bearer 3292d7e9-813d-472e-957d-36a1b699e81b",
        "Content-Type": "application/json"
        },
    "params" : {
        "page": "9",
        "per_page": "100",
    }
}


def collect_data():
    headers = request_settings.get('headers')
    url = request_settings.get('url')
    params = request_settings.get('params')
    response = requests.get(url, headers=headers, params=params)
    pages = response.json().get('pages')

    for page in range(1, pages + 1):
        params_loop = {'page': page, 'per_page': '100'}
        response = requests.get(url, headers=headers, params=params_loop)

        try:
            users = response.json()
            page = users.get('page')
            pages = users.get('pages')
            my_list = users.get('list')

            for num, item in enumerate(my_list):
                phones = item.get('phones')
                phone_string = ""
                for phone in phones:
                    phone_string += phone.get('phone') + ', '
                print(f"{num} {phone_string}")

        except:
            print("Ошибка: Не удалось получить список пользователей")
            print(response.text)
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")


