from django.contrib import admin

from crm.models import ClientCRM
from crm.tasks import update_date_from_CRM, add_exists_clients
from clients.models import Client, ReportEmail

def update_data_test(modeladmin, request, queryset):
    update_date_from_CRM.delay()

def kill_crm_db(modeladmin, request, queryset):
    ClientCRM.objects.all().delete()
    Client.objects.all().delete()


def sync_clients_from_crm_to_bot(modeladmin, request, queryset):
    add_exists_clients.delay()

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'first_visit', 'last_visit')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'phone')
    list_per_page = 100
    actions = [update_data_test,
               kill_crm_db,
               sync_clients_from_crm_to_bot,
               ]

@admin.register(ReportEmail)
class ReportEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_display_links = ('id', 'email')
    search_fields = ('email',)
    list_filter = ('email',)
    list_per_page = 25