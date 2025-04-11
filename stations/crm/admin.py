from crm.models import ClientCRM, PhoneCRM, Address
from django.contrib import admin



@admin.register(ClientCRM)
class ClientCRMAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClientCRM._meta.fields]

@admin.register(PhoneCRM)
class PhoneAdmin(admin.ModelAdmin):
    """
    client_watsapp = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='phone_crm', null=True, blank=True)
    client = models.ForeignKey(ClientCRM, related_name='phones', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    comment = models.TextField(blank=True, null=True)
    notices = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    """
    list_display = ('id', 'phone', 'client', 'client_watsapp', 'notices')
    list_display_links = ('id', 'phone')
    search_fields = ('phone', 'client__id')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    clientCrm = models.ForeignKey(ClientCRM, related_name='addresses', on_delete=models.CASCADE)
    crm_client_id = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    dom = models.CharField(max_length=10)
    kv = models.CharField(max_length=10, blank=True, null=True)
    korp = models.CharField(max_length=10, blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)
    entrance = models.CharField(max_length=20, blank=True, null=True)
    doorcode = models.CharField(max_length=20, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    client_comment = models.TextField(blank=True, null=True)
    district_id = models.CharField(max_length=255, blank=True, null=True)
    delivery_zone_id = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    client_uuid = models.CharField(max_length=255, blank=True, null=True)
    """
    list_display = ('id', 'city',
                    'street', 'dom', 'kv', 'korp',
                    'floor', 'entrance', 'doorcode', 'client_uuid')


