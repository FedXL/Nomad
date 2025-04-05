from os import getenv
import requests
from dotenv import load_dotenv
load_dotenv()
Token = getenv('NOMAD_TOKEN')

def check_user_in_crm(phone_number):
    url = 'https://waterapp.me/cab/api/clients'
    headers = { 'Authorization': f'Bearer {Token}', 'Content-Type': 'application/json' }

    params = { 'q': phone_number }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        phone_list = result.get('list')
        if phone_list:
            return result
        else:
            return False
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        return False


def create_user(phone_number, username):
    result = check_user_in_crm(phone_number)
    if result:
        return result
    url = 'https://waterapp.me/cab/api/clients.json'
    headers = { 'Authorization': f'Bearer {Token}', 'Content-Type': 'application/json' }

    client_model = {
        "client": {
            "phones": [
                {
                    "phone": phone_number,
                    "first_name": username,
                    "last_name": "",
                    "comment": "From WatsApp Bot User",
                    "notices": False
                }
            ],
            "comment": "User from WatsApp Bot",
            "drivers_comment": "",
            "client_type": "fiz",
            "email": "",
            "custom_api_fields": {
                "custom_field": ""
            }
        }
    }
    response = requests.post(url, headers=headers, json=client_model)

    if response.status_code in [201, 200]:
        result = response.json()
        my_result = {'list': [result]}
        return result
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        return False
