from django.contrib import admin

from crm.tasks import order_send_to_crm_task
from shop.models import Order, Cart, CartItem, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


def send_order_to_crm_test(modeladmin, request, queryset):
    """
    Test function to send order to CRM
    """
    for order in queryset:
        print(f"Sending order {order.id} to CRM")
        order_send_to_crm_task.delay(order.id)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [OrderItemInline]
    actions = [send_order_to_crm_test]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields]
    inlines = [CartItemInline]