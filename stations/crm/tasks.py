import logging
import time
import requests
from celery import shared_task, chain, group
from django.conf import settings
from django.db import transaction
from clients.models import Client
from crm.handlers.address_handler import parse_the_address_string, extract_address_from_string, \
    send_new_address_in_CRM
from crm.models import PhoneCRM, ClientCRM, Address

my_task_logger = logging.getLogger(__name__)
CRM_USER_FIELDS = [field.name for field in ClientCRM._meta.fields if field.name != "id"]
CRM_PHONE_FIELDS = [field.name for field in PhoneCRM._meta.fields if field.name != "id"]
CRM_ADDRESS_FIELDS = [field.name for field in Address._meta.fields if field.name != "id"]

TOKEN = settings.CRM_TOKEN

def clean_phone(phone_number):
    number = phone_number.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('+',"")
    if number.startswith('8'):
        number = '7' + number[1:]
    number = number.strip()
    return number



@shared_task
def update_date_from_CRM():
    my_task_logger.info('start update_database_from_crm')
    url = "https://waterapp.me/cab/api/clients"

    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    params = {
        "page": "9",
        "per_page": "100",
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        users = response.json()
        pages = users.get('pages')
        tasks = [chain(download_file.s(page), parse_file.s()) for page in range(1, pages + 1)]
        group_chain = chain(group(tasks), add_exists_clients.s())
        group_chain.apply_async()
    else:
        my_task_logger.error(f"Ошибка: {response.status_code}, {response.text}")
    return 'all is good'

@shared_task
def download_file(page=None):
    my_task_logger.info('start download_file')
    url = "https://waterapp.me/cab/api/clients"

    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }
    params = {
        "page": page,
        "per_page": "100",
    }

    response = requests.get(url, headers=headers, params=params)
    counter = 0

    while True:
        if counter > 4:
            raise Exception('Too many errors')
        if response.status_code == 200:
            data = response.json()
            my_task_logger.info(f'Data downloaded for page {page}')
            return data
        else:
            my_task_logger.error(f"Ошибка: {response.status_code}, {response.text}")
            time.sleep(4)
            counter += 1


def parse_user(user_data):
    """Parse json for orm model CrmClient"""
    user_data_ = user_data.copy()
    phones = user_data_.get('phones')
    parsed_phones = parse_phones(phones)
    addresses = user_data_.get('addresses')
    addresses = parse_addresses(addresses)
    user_uuid = user_data_['id']
    user_data_['client_uuid'] = user_uuid
    del user_data_['addresses']
    del user_data_['phones']
    del user_data_['id']
    del user_data_['phone']

    my_task_logger.info(f"user_data: {len(user_data_)} phones: {len(parsed_phones)} addresses: {len(addresses)}")
    return user_data_, parsed_phones, addresses

def parse_phones(phones):
    """parce json for orm model Phone"""
    result_phones = []
    for phone in phones:
        phone_data = phone.copy()
        phone_number = phone_data.get('phone')
        phone_number = clean_phone(phone_number)
        del phone_data['phone']
        phone_data['phone'] = phone_number
        result_phones.append(phone_data)
    return result_phones

def parse_addresses(addresses):
    """parce json for orm model Address"""
    """
    
      "id": "64f6cbb2c32dab7f387f5f23",
      "city": "Актау",
      "street": "29",
      "dom": "4",
      "kv": "30",
      "korp": "",
      "floor": "",
      "entrance": "",
      "doorcode": "",
      "comment": "",
      "client_comment": "",
      "district_id": "",
      "delivery_zone_id": "",
      "location": {
        "lat": 43.65880790000001,
        "lng": 51.1974563
      },
      "client_id": "64f6cb99c32dab7f328035f9"
    }
    """
    result_addresses = []
    if addresses:
        for address in addresses:
            data = address.copy()
            data['address_uuid'] = address.get('id')
            location = address.get('location',None)
            if location:
                lat = location.get('lat')
                lng = location.get('lng')
                data['lng'] = lng
                data['lat'] = lat
            else:
                a='zebra'
            del data['location']
            del data['id']

            client_uuid = address.get('client_id')
            if client_uuid:
                data['client_uuid'] = client_uuid
                del data['client_id']
            result_addresses.append(data)
    return result_addresses

@shared_task
def parse_file(data):
    my_task_logger.info('start parse_user')

    """Water Crm -> water bot. Если в боте пользователя нет, то добавляем его"""
    clients_to_bulk_update = []
    clients_to_bulk_create = []

    phones_dict = {}
    phones_to_bulk_update_obj = []
    phones_to_bulk_create_obj = []

    addresses_dict = {}
    addresses_to_bulk_update = []
    addresses_to_bulk_create = []


    users = data.get('list', None)
    assert users, 'No users in file'
    users_crm_vocabulary = {user.get('id'):user for user in users}
    # Это базовые данные для оценки. какой клиент есть а какого создавать
    users_crm_uuids = users_crm_vocabulary.keys()
    clients_objects_to_update = list(ClientCRM.objects.filter(client_uuid__in=users_crm_uuids))
    clients_to_update_uuids = [client.client_uuid for client in clients_objects_to_update]
    clients_to_create = [client_uuid for client_uuid in users_crm_uuids if client_uuid not in clients_to_update_uuids]

    my_task_logger.info(f'users_crm_vocabulary {len(users_crm_vocabulary)}')
    my_task_logger.info(f'clients_objects_to_update {len(clients_objects_to_update)}')
    my_task_logger.info(f'clients_to_create {len(clients_to_create)}')
    my_task_logger.info(f'clients_to_update_uuids {len(clients_to_update_uuids)}')

    for crm_client in clients_objects_to_update:
        data = users_crm_vocabulary.get(crm_client.client_uuid)
        if not data:
            continue
        user_parsed, phones_parsed, addresses_parsed = parse_user(data)

        for field, value in user_parsed.items():
            setattr(crm_client, field, value)

        for phone in phones_parsed:
            phone_number = phone.get('phone')
            phones_dict[phone_number] = {'data':phone,'client': crm_client}

        for address in addresses_parsed:
            addresses_dict[address.get('address_uuid')] = {'data':address,'client': crm_client}
        clients_to_bulk_update.append(crm_client)

    ClientCRM.objects.bulk_update(clients_to_bulk_update, CRM_USER_FIELDS)

    phones_data_keys = phones_dict.keys()
    phones_for_update_obj = list(PhoneCRM.objects.filter(phone__in=phones_data_keys))
    phones_for_update_keys = [phone.phone for phone in phones_for_update_obj]
    my_task_logger.warning(f"phones_data_keys: {len(phones_data_keys)}")
    my_task_logger.warning(f"uniq data keys: {len(set(phones_data_keys))}")
    my_task_logger.warning(f"phones_for_update_keys: {len(phones_for_update_keys)}")
    my_task_logger.warning(f"phones_data_keys: {len(set(phones_data_keys))}")

    phones_for_create_keys = [phone_number for phone_number in phones_data_keys if phone_number not in phones_for_update_keys]
    phones_for_create_data = {phone: phones_dict[phone] for phone in phones_for_create_keys}
    my_task_logger.warning(f"phones_for_create_keys: {len(phones_for_create_keys)}")
    my_task_logger.warning(f"phones_for_update_keys: {len(phones_for_create_data)}")


    for phone_obj in phones_for_update_obj:
        phone_data = phones_dict.get(phone_obj.phone)
        if not phone_data:
            my_task_logger.error('No data in phone_dict')
            continue
        client = phone_data.get('client')
        phone_data = phone_data.get('data')
        for field, value in phone_data.items():
            setattr(phone_obj, field, value)
        setattr(phone_obj,'client',client)
        phones_to_bulk_update_obj.append(phone_obj)
    my_task_logger.info(f"phones to create:")

    for phone_data in phones_for_create_data.values():
        client = phone_data.get('client')
        phone_data = phone_data.get('data')
        phone_obj = PhoneCRM(**phone_data, client=client)
        phones_to_bulk_create_obj.append(phone_obj)

    PhoneCRM.objects.bulk_update(phones_to_bulk_update_obj, CRM_PHONE_FIELDS, batch_size=1000)
    PhoneCRM.objects.bulk_create(phones_to_bulk_create_obj, batch_size=1000,ignore_conflicts=True)

    address_data_keys = addresses_dict.keys()
    addresses_for_update_obj = list(Address.objects.filter(address_uuid__in=address_data_keys))
    addresses_for_update_keys = [address.address_uuid for address in addresses_for_update_obj]
    addresses_for_create_keys = [address_uuid for address_uuid in address_data_keys if address_uuid not in addresses_for_update_keys]
    addresses_for_create_data = {address_uuid: addresses_dict[address_uuid] for address_uuid in addresses_for_create_keys}

    #Обновление адресов
    for address_obj in addresses_for_update_obj:
        address_data = addresses_dict.get(address_obj.address_uuid)
        if not address_data:
            my_task_logger.error('No data in address_dict')
            continue
        client = address_data.get('client')
        address_data = address_data.get('data')
        for field, value in address_data.items():
            setattr(address_obj, field, value)
        setattr(address_obj,'client',client)
        addresses_to_bulk_update.append(address_obj)


    for address_data in addresses_for_create_data.values():
        client = address_data.get('client')
        address_data = address_data.get('data')

        address_obj = Address(**address_data, client=client)
        addresses_to_bulk_create.append(address_obj)

    Address.objects.bulk_update(addresses_to_bulk_update, CRM_ADDRESS_FIELDS, batch_size=1000)
    Address.objects.bulk_create(addresses_to_bulk_create, batch_size=1000)

    addresses_dict = {}
    phones_dict = {}

    for crm_client_uuid in clients_to_create:
        data = users_crm_vocabulary.get(crm_client_uuid, None)
        if not data:
            continue
        my_task_logger.warning(f'Client Data in Create USER: {data}')
        user_parsed, phones_parsed, addresses_parsed = parse_user(data)
        client_crm = ClientCRM(**user_parsed)
        clients_to_bulk_create.append(client_crm)

        for phone in phones_parsed:
            my_task_logger.info(f'phones_parsed {phone}')
            phones_dict[phone.get('phone')] = PhoneCRM(**phone, client=client_crm)
        for address in addresses_parsed:
            addresses_dict[address.get('address_uuid')] = Address(**address, client=client_crm)
    my_task_logger.error(f'phones_dict for create {phones_dict}')
    ClientCRM.objects.bulk_create(clients_to_bulk_create, batch_size=1000)
    PhoneCRM.objects.bulk_create(phones_dict.values(), batch_size=1000, ignore_conflicts=True)
    Address.objects.bulk_create(addresses_dict.values(), batch_size=1000)
    return 'success chain'


@shared_task
def hello_task():
    print('hello')
    return 'hello'

@shared_task
def add_exist_client(*args,**kwargs):
    phone_number = kwargs.get('phone')
    phone_number = clean_phone(phone_number)
    my_task_logger.info(f'so phone number is {phone_number}')
    time.sleep(1)
    phone_obj = PhoneCRM.objects.filter(phone=phone_number).first()
    if not phone_obj:
        my_task_logger.error(f'No phone with {phone_number}')
        raise ValueError(f'No phone_CRM with {phone_number}')
    client_watsapp = Client.objects.filter(phone=phone_number).first()
    if client_watsapp:
        phone_obj.client_watsapp = client_watsapp
        phone_obj.save()
    else:
        my_task_logger.error(f'No client with phone {phone_number}')
    return 'completed'


@shared_task
def add_exists_clients(*args, **kwargs):
    my_task_logger.info('CLIENTS ADD !')
    phones_obj = PhoneCRM.objects.all()
    phones_bot_dict = {phone.phone:phone for phone in Client.objects.all()}
    phones_bot = phones_bot_dict.keys()
    phones_to_update = []
    new_clients=[]
    update_clients=[]
    for phone_obj in phones_obj:
        if phone_obj.phone not in phones_bot:
            new_clients.append(Client(phone=phone_obj.phone,
                                         username='from crm',
                                         first_name=phone_obj.first_name,
                                         last_name=phone_obj.last_name))
        elif phone_obj.phone in phones_bot:
            client = phones_bot_dict[phone_obj.phone]
            client.first_name = phone_obj.first_name
            client.last_name = phone_obj.last_name
            update_clients.append(client)
    my_task_logger.info(f'new cliens to create {len(new_clients)}')
    if new_clients:
        with transaction.atomic():
            Client.objects.bulk_create(new_clients, batch_size=1000, ignore_conflicts=True)
    if update_clients:
        with transaction.atomic():
            Client.objects.bulk_update(update_clients, ['first_name','last_name'], batch_size=1000)

    clients_bot = {client.phone:client for client in Client.objects.all()}

    for phone_obj in phones_obj:
        if phone_obj.phone:
            client = clients_bot.get(phone_obj.phone)
            if phone_obj.client_watsapp != client:
                phone_obj.client_watsapp = client
                phones_to_update.append(phone_obj)
    if phones_to_update:
        with transaction.atomic():
            PhoneCRM.objects.bulk_update(phones_to_update, ['client_watsapp'], batch_size=1000)
    my_task_logger.info(f'Добавлено клиентов: {len(new_clients)}')
    return f'Добавлено {len(new_clients)} клиентов и обновлено {len(update_clients)}'


def add_new_address(phone,address_string):
    """return (True/False, comment)"""
    phone = clean_phone(phone)
    phone_obj = PhoneCRM.objects.filter(phone=phone).first()
    client_crm_obj = phone_obj.client
    watsapp_client = phone_obj.client_watsapp
    if not client_crm_obj:
        my_task_logger.error(f'No client with phone {phone}')
        return False,'no client'
    uuid_client = client_crm_obj.client_uuid
    address_dict = extract_address_from_string(address_string)
    address_dict['client_id'] = uuid_client
    my_task_logger.warning('address_dict: {} '.format(address_dict))
    if not address_dict.get('street') or not address_dict.get('dom'):
        return False,'Не распознан дом или улица (ошибка в джанге)'
    response = send_new_address_in_CRM(address_dict)
    if response.status_code == 200:
        try:
            address_data = response.json()
            address_data = address_data.get('address')
        except:
            my_task_logger.error('Error in json')
            return False, response.text
        my_task_logger.info(f"address before save to bot {address_data}")
        parsed_address = parse_addresses([address_data])
        parsed_address = parsed_address[0]
        model_fields = {field.name for field in Address._meta.get_fields()}
        filtered_data = {key: value for key, value in parsed_address.items() if key in model_fields}
        address_obj = Address.objects.create(**filtered_data, client=client_crm_obj)
        my_task_logger.info(f'Address created: {address_obj}')
        watsapp_client.last_address_uuid = address_obj.address_uuid
        watsapp_client.save()
        return True, address_obj.id
    else:
        return False, response.text



@shared_task
def add_new_address_task(phone, address_string):
    """Дабаляет новый адрес в CRM"""
    result = add_new_address(phone, address_string)
    return result




