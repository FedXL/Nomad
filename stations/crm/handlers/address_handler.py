import logging
import requests
from django.conf import settings
from deep_translator import GoogleTranslator
from langdetect import detect

address_logger = logging.getLogger('address_logger')
address_logger.setLevel(logging.INFO)
address_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(address_formatter)
address_logger.addHandler(console_handler)

API_KEY = settings.API_KEY_GOOGLE
translator = GoogleTranslator(source="kk", target="ru")

def parse_address_openstreetmap(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {
        "User-Agent": "water-bot-template/1.0 (fedorkuruts@email.com)"  # Без этого могут блокировать
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if not data:
        return None

    address_data = data[0].get("address", {})
    latitude = data[0].get("lat")
    longitude = data[0].get("lon")
    address_data['location'] = {
        'lng': str(longitude),
        'lat': str(latitude)
    }
    """
         "location": {
        "lat": 43.65880790000001,
        "lng": 51.1974563
      },
    """
    """
    {'road': 'Розыбакиева (Достык) улица',
     'suburb': 'Достық',
      'city_district': 'Ауэзовский район',
       'city': 'Алматы',
        'ISO3166-2-lvl4': 'KZ-75',
         'postcode': '040212',
          'country': 'Қазақстан',
           'country_code': 'kz'}
    """
    return address_data

def smart_translate(text):
    try:
        lang = detect(text)
        if lang == "ru":
            return text  # Если текст уже на русском, не переводим
        return GoogleTranslator(source="auto", target="ru").translate(text)
    except Exception:
        return text


def parse_the_address_string(address_str):
    """
        {
      "house_number": "Номер дома",
      "road": "Улица, проспект, переулок",
      "city": "Город",
      "state": "Область, регион",
      "postcode": "Почтовый индекс",
      "country": "Страна",
      "unit": "Квартира, офис",
      "level": "Этаж",
      "entrance": "Подъезд",
      "staircase": "Лестничный пролёт",
      "po_box": "Почтовый ящик",
      "house": "Корпус, строение"
        }
    """
    address_logger.info(f"address_str: {address_str}")



    address_ru = smart_translate(address_str)
    address_logger.info(f"address_ru: {address_ru}")
    parsed = parse_address_openstreetmap(address_ru)
    address_logger.info(f"parsed: {parsed}")
    if not parsed:
        address_logger.error(f"Не удалось распарсить адрес: {address_ru}")
        raise ValueError('Не удалось распарсить адрес')
    parsed['base_string'] = address_str
    return parsed

def convert_to_crm_model(address_dict) -> dict:
    """
{
  "client_id": "64f85542c32dab3fcb956932",
  "title": "Новый адрес",
  "city": "Актау",
  "street": "Ленина",
  "dom": "29",
  "kv": "1",
  "korp": "",
  "floor": "4",
  "entrance": "2",
  "doorcode": "243",
  "comment": "Комментарий для водителя",
  "client_comment": "Комментарий клиента",
  "location_detect": false,
  "auto_detect_zones": true,
  "custom_api_fields": {
  "custom_field": "Любые поля! которые могут вам понадобиться"
}
{
      "house_number": "Номер дома",
      "road": "Улица, проспект, переулок",
      "city": "Город",
      "state": "Область, регион",
      "postcode": "Почтовый индекс",
      "country": "Страна",
      "unit": "Квартира, офис",
      "level": "Этаж",
      "entrance": "Подъезд",
      "staircase": "Лестничный пролёт",
      "po_box": "Почтовый ящик",
      "house": "Корпус, строение"
}


    {'road': 'Розыбакиева (Достык) улица',
     'suburb': 'Достық',
      'city_district': 'Ауэзовский район',
       'city': 'Алматы',
        'ISO3166-2-lvl4': 'KZ-75',
         'postcode': '040212',
          'country': 'Қазақстан',
           'country_code': 'kz'}


    """

    result_dict = {
        "client_id": None,
        "title": "Новый адрес из вотсап бота",
        "city": address_dict.get('city',None),
        "street": address_dict.get('road',None),
        "dom": address_dict.get('house_number',None),
        "kv": address_dict.get('unit',None),
        "korp": "",
        "floor": address_dict.get('level',None),
        "entrance": address_dict.get('entrance',None),
        "doorcode": "",
        "comment": address_dict.get('base_string',None),
        "client_comment": "",
        "location_detect": True,
        "location": {"lng": address_dict['location']['lng'],
                     "lat": address_dict['location']['lat']},
        "auto_detect_zones": True,
        "custom_api_fields": {}
    }
    return result_dict


def extract_address_from_string(address_str):
    """
    Takes a string address and returns a dictionary with the parsed address.
    """
    parsed_address = parse_the_address_string(address_str)
    crm_model = convert_to_crm_model(parsed_address)
    return crm_model


def send_new_address_in_CRM(model_data:dict):
    url = "https://waterapp.me/cab/api/addresses.json"
    headers = {
        "Authorization": settings.CRM_TOKEN,
        "Content-Type": "application/json"
    }
    data = {**model_data}
    response = requests.post(url, json=data, headers=headers)

    return response



def parse_address_google(address_string):

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address_string}&key={API_KEY}"

    response = requests.get(url)
    if response.status_code==200:
        print("Успех")
    else:
        print("Ошибка:", response.status_code)
        print(response.text)
        return False, response.text
    data = response.json()
    if data["status"] == "OK":
        components = data["results"][0]["address_components"]
        parsed_address = {comp["types"][0]: comp["long_name"] for comp in components}
        print(parsed_address)
    else:
        print("Ошибка:", data["status"])

























