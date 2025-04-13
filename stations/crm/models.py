from django.db import models
from clients.models import Client

class ClientCRM(models.Model):
    client_uuid = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    birthday = models.CharField(blank=True, null=True)
    fio = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    drivers_comment = models.CharField(max_length=255, blank=True, null=True)

    bonuses = models.IntegerField(default=0)
    orders_count = models.IntegerField(default=0)
    has_rek = models.BooleanField(default=False)
    code = models.CharField(max_length=255, blank=True, null=True)
    custom_api_fields = models.JSONField(blank=True, null=True)
    integration_guid = models.CharField(max_length=255, blank=True, null=True)
    contract_1c_id = models.CharField(max_length=255, blank=True, null=True)
    contract_1c_title = models.CharField(max_length=255, blank=True, null=True)
    contract_1c_start_date = models.CharField(max_length=255,blank=True, null=True)

    client_type = models.CharField(max_length=10, choices=[('fiz', 'Физическое лицо'), ('ur', 'Юридическое лицо')],blank=True, null=True)
    ur_type = models.CharField(max_length=10,blank=True, null=True)
    ur_title = models.CharField(max_length=255, blank=True, null=True)
    ur_dir = models.CharField(max_length=255, blank=True, null=True)
    ur_dir_rod = models.CharField(max_length=255, blank=True, null=True)
    ur_dir_sokr = models.CharField(max_length=255, blank=True, null=True)
    ur_address = models.TextField(blank=True, null=True)
    ur_address_index = models.CharField(max_length=20, blank=True, null=True)
    ur_address_region_code = models.CharField(max_length=20, blank=True, null=True)
    ur_address_region = models.CharField(max_length=255, blank=True, null=True)
    ur_address_district = models.CharField(max_length=255, blank=True, null=True)
    ur_address_city = models.CharField(max_length=255, blank=True, null=True)
    ur_address_settlement = models.CharField(max_length=255, blank=True, null=True)
    ur_address_street = models.CharField(max_length=255, blank=True, null=True)
    ur_address_house = models.CharField(max_length=50, blank=True, null=True)
    ur_address_korp = models.CharField(max_length=50, blank=True, null=True)
    ur_address_kv = models.CharField(max_length=50, blank=True, null=True)
    ur_address_other = models.CharField(blank=True, null=True)
    ur_off_address=models.CharField(max_length=255, blank=True, null=True)
    ur_off_address_index=models.CharField(max_length=20, blank=True, null=True)
    ur_off_address_region_code = models.CharField(max_length=20, blank=True, null=True)
    ur_off_address_region = models.CharField(max_length=255, blank=True, null=True)
    ur_off_address_district = models.CharField(max_length=255, blank=True, null=True)
    ur_off_address_city = models.CharField(max_length=255, blank=True, null=True)
    ur_off_address_settlement = models.CharField(max_length=255, blank=True, null=True)
    ur_off_address_street = models.CharField(max_length=255, blank=True, null=True)
    ur_off_address_house = models.CharField(max_length=50, blank=True, null=True)
    ur_off_address_korp = models.CharField(max_length=50, blank=True, null=True)
    ur_off_address_kv = models.CharField(max_length=50, blank=True, null=True)
    ur_off_address_other = models.CharField(blank=True, null=True)
    ur_inn = models.CharField(max_length=20, blank=True, null=True)
    ur_kpp = models.CharField(max_length=20, blank=True, null=True)
    ur_ogrn_ip = models.CharField(max_length=20, blank=True, null=True)
    ur_okpo = models.CharField(max_length=20, blank=True, null=True)
    ur_accounter_fio = models.CharField(max_length=255, blank=True, null=True)
    ur_accounter_fio_sokr = models.CharField(max_length=255, blank=True, null=True)
    ur_bank_title = models.CharField(max_length=255, blank=True, null=True)
    ur_bank_bik = models.CharField(max_length=20, blank=True, null=True)
    ur_account_number = models.CharField(max_length=50, blank=True, null=True)
    ur_kor_account = models.CharField(max_length=50, blank=True, null=True)
    ur_phone = models.CharField(max_length=20, blank=True, null=True)
    ur_email = models.EmailField(blank=True, null=True)
    ur_invoice_fio = models.CharField(max_length=255, blank=True, null=True)
    ur_invoice_position = models.CharField(max_length=255, blank=True, null=True)
    ur_store_position=models.CharField(max_length=255, blank=True, null=True)
    ur_store_sign = models.CharField(max_length=255, blank=True, null=True)
    ur_acccount_type = models.CharField(max_length=255, blank=True, null=True)
    ur_vat = models.CharField(max_length=10, blank=True, null=True)

def to_dict(self):
    phones = self.phones.all()
    if phones:
        phones_numbers = [phone.phone for phone in phones]
    else:
        phones_numbers = []
    addresses = self.addresses.all()
    if addresses:
        addresses = [address.to_dict() for address in addresses]
    else:
        addresses = []

    result = {
        "phone": self.phone,
        "phones": phones_numbers,
        "email": self.email,
        "birthday": self.birthday,
        "fio": self.fio,
        "created_at": self.created_at,
        "updated_at": self.updated_at,
        "comment": self.comment,
        "drivers_comment": self.drivers_comment,
        "bonuses": self.bonuses,
        "orders_count": self.orders_count,
        "has_rek": self.has_rek,
        "code": self.code,
        "custom_api_fields": self.custom_api_fields,
        "integration_guid": self.integration_guid,
        "addresses": addresses,
        "contract_1c_id": self.contract_1c_id,
        "contract_1c_title": self.contract_1c_title,
        "contract_1c_start_date": self.contract_1c_start_date,
        "client_type": self.client_type,
        "ur_type":  self.ur_type,
        "ur_title": self.ur_title,
        "ur_dir": self.ur_dir,
        "ur_dir_rod": self.ur_dir_rod,
        "ur_dir_sokr": self.ur_dir_sokr,
        "ur_address": self.ur_address,
        "ur_address_index": self.ur_address_index,
        "ur_address_region_code": self.ur_address_region_code,
        "ur_address_region": self.ur_address_region,
        "ur_address_district": self.ur_address_district,
        "ur_address_city": self.ur_address_city,
        "ur_address_settlement": self.ur_address_settlement,
        "ur_address_street": self.ur_address_street,
        "ur_address_house": self.ur_address_house,
        "ur_address_korp": self.ur_address_korp,
        "ur_address_kv": self.ur_address_kv,
        "ur_address_other": self.ur_address_other,
        "ur_off_address": self.ur_off_address,
        "ur_off_address_index": self.ur_off_address_index,
        "ur_off_address_region_code": self.ur_off_address_region_code,
        "ur_off_address_region": self.ur_off_address_region,
        "ur_off_address_district": self.ur_off_address_district,
        "ur_off_address_city": self.ur_off_address_city,
        "ur_off_address_settlement": self.ur_off_address_settlement,
        "ur_off_address_street": self.ur_off_address_street,
        "ur_off_address_house": self.ur_off_address_house,
        "ur_off_address_korp": self.ur_off_address_korp,
        "ur_off_address_kv": self.ur_off_address_kv,
        "ur_off_address_other": self.ur_off_address_other,
        "ur_inn": self.ur_inn,
        "ur_kpp": self.ur_kpp,
        "ur_ogrn_ip": self.ur_ogrn_ip,
        "ur_okpo": self.ur_okpo,
        "ur_accounter_fio": self.ur_accounter_fio,
        "ur_accounter_fio_sokr": self.ur_accounter_fio_sokr,
        "ur_bank_title": self.ur_bank_title,
        "ur_bank_bik": self.ur_bank_bik,
        "ur_account_number": self.ur_account_number,
        "ur_kor_account": self.ur_kor_account,
        "ur_phone": self.ur_phone,
        "ur_email": self.ur_email,
        "ur_invoice_fio": self.ur_invoice_fio,
        "ur_invoice_position": self.ur_invoice_position,
        "ur_store_position": self.ur_store_position,
        "ur_store_sign": self.ur_store_sign,
        "ur_accсount_type": self.ur_acccount_type,
        "ur_vat": self.ur_vat
    }
    return result


class PhoneCRM(models.Model):
    """
    {
    "phone": "+7 (777) 703-8108",
    "comment": "",
    "notices": true,
    "first_name": "Нура",
    "last_name": ""
  }
    """
    client_watsapp = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='phone_crm_w', null=True, blank=True)
    client = models.ForeignKey(ClientCRM, related_name='phones_crm', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=30,unique=True)
    comment = models.TextField(blank=True, null=True)
    notices = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    client_uuid = models.CharField(max_length=255, blank=True, null=True)

    def to_dict(self):
        return {
            "phone": self.phone,
            "comment": self.comment,
            "notices": self.notices,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Address(models.Model):
    """
    {
    "id": "64f6cbb2c32dab7f387f5f23",
    "city+": "Актау",
    "street+": "29",
    "dom+": "4",
    "kv+": "30",
    "korp+": "",
    "floor+": "",
    "entrance+": "",
    "doorcode+": "",
    "comment+": "",
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

    client = models.ForeignKey(ClientCRM, related_name='addresses',
                               on_delete=models.CASCADE, null=True, blank=True)
    address_uuid = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    dom = models.CharField(max_length=255)
    kv = models.CharField(max_length=255, blank=True, null=True)
    korp = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=255, blank=True, null=True)
    entrance = models.CharField(max_length=255, blank=True, null=True)
    doorcode = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    client_comment = models.TextField(blank=True, null=True)
    district_id = models.CharField(max_length=255, blank=True, null=True)
    delivery_zone_id = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True,null=True)
    client_uuid = models.CharField(max_length=255, blank=True, null=True)


    def to_dict(self):
        return {
            "id": self.crm_client_id,
            "city": self.city,
            "street": self.street,
            "dom": self.dom,
            "kv": self.kv,
            "korp": self.korp,
            "floor": self.floor,
            "entrance": self.entrance,
            "doorcode": self.doorcode,
            "comment": self.comment,
            "client_comment": self.client_comment,
            "district_id": self.district_id,
            "delivery_zone_id": self.delivery_zone_id,
            "location": {
                "lat": self.lat,
                "lng": self.lng
            },
            "client_id": self.client_uuid
        }




