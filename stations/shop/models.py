from django.db import models
from django.utils import timezone
from clients.models import Client
from shop.utils import cart_buttons_generator

class PaymentMethod(models.TextChoices):
    CASH = '647f20e3c32dab21a2a5e757', 'CASH'
    CARD_ON_TERMINAL = '647f20e3c32dab21a2a5e758', 'CARD_ON_TERMINAL'
    INVOICE = '647f20e3c32dab21a2a5e759', 'INVOICE'
    CARD_ONLINE = '647f20e3c32dab21a2a5e75a', 'CARD_ONLINE'
    FREE = '647f20e3c32dab21a2a5e75b', 'FREE'
    BONUSES = '647f20e3c32dab21a2a5e75c', 'BONUSES'
    PROMO = '647f20e3c32dab21a2a5e75d', 'PROMO'


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE,
                                  related_name="cart_related",
                                  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    spot = models.CharField(max_length=255, null=True, blank=True)
    payment_choice = models.CharField(
        max_length=32,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )

    def __str__(self):
        return f"Cart {self.id} - {self.client}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart_items.all())

    def shopping_cart_buttons(self, language):
        items = self.cart_items.prefetch_related('product').all()
        summary_price = self.total_price
        buttons = cart_buttons_generator(items,summary_price, language)
        return buttons

    def extract_time_spot(self) -> tuple:
        """return day, start_time, end_time"""
        if not self.spot:
            return None
        day = self.spot
        data = day.rsplit('_', 2)
        assert len(data) == 3, "Invalid time spot format"
        day, start_time, end_time = data

        start_time = f"{start_time}:00"
        end_time = f"{end_time}:00"

        if day == "today":
            date = timezone.now().date()
        elif day == "tomorrow":
            date = timezone.now().date() + timezone.timedelta(days=1)
        elif day == "after_tomorrow":
            date = timezone.now().date() + timezone.timedelta(days=2)
        else:
            raise ValueError("Invalid day value in time spot")
        return date, start_time, end_time



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey('api_backend.ProductBlock', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

    def to_dict(self):
        uuid = self.product.uuid if hasattr(self.product, 'uuid') else None

        return {
            "product": self.product.product_name,
            "product_header_kaz": self.product.header_kaz,
            "product_header_rus": self.product.header_rus,
            "quantity": self.quantity,
            "price": self.product.price,
            "total_price": self.total_price,
            "crm_id": uuid,
        }

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[("pending", "pending"),
                                                      ("completed", "completed"),
                                                      ("canceled", "canceled")],
                              default="pending")

    delivery_date = models.DateField(default=None, null=True, blank=True)
    time_start = models.CharField(max_length=5, null=True, blank=True)
    time_end = models.CharField(max_length=5, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    payment_choice = models.CharField(
        max_length=32,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart.cart_items.all())

    def __str__(self):
        return f"Order {self.id} - {self.client.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey('api_backend.ProductBlock', on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=255,verbose_name='Название продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость в тенге')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    item_uuid = models.CharField(max_length=255, verbose_name='ID в CRM', null=True, blank=True)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    def save(self, *args, **kwargs):
        product_uuid = getattr(self.product, 'uuid', None)
        if not product_uuid:
            print('no')
        else:
            self.item_uuid = product_uuid
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "product": self.product_name,
            "quantity": self.quantity,
            "price": self.price * 100,
            "total_price": self.total_price,
            "crm_id": self.item_uuid,
        }

    def to_crm_dict(self):
        if self.item_uuid:
            return {
                "item_id": self.item_uuid,
                "art": "",
                "title": self.product_name,
                "price": self.price * 100,
                "quantity": self.quantity
            }
        else:
            return None