# Generated by Django 5.1.3 on 2025-04-13 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_cartitem_payment_choice_order_payment_choice_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='payment_choice',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order_uuid',
        ),
        migrations.AddField(
            model_name='cart',
            name='payment_choice',
            field=models.CharField(choices=[('647f20e3c32dab21a2a5e757', 'CASH'), ('647f20e3c32dab21a2a5e758', 'CARD_ON_TERMINAL'), ('647f20e3c32dab21a2a5e759', 'INVOICE'), ('647f20e3c32dab21a2a5e75a', 'CARD_ONLINE'), ('647f20e3c32dab21a2a5e75b', 'FREE'), ('647f20e3c32dab21a2a5e75c', 'BONUSES'), ('647f20e3c32dab21a2a5e75d', 'PROMO')], default='647f20e3c32dab21a2a5e757', max_length=32),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item_uuid',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID в CRM'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_choice',
            field=models.CharField(choices=[('647f20e3c32dab21a2a5e757', 'CASH'), ('647f20e3c32dab21a2a5e758', 'CARD_ON_TERMINAL'), ('647f20e3c32dab21a2a5e759', 'INVOICE'), ('647f20e3c32dab21a2a5e75a', 'CARD_ONLINE'), ('647f20e3c32dab21a2a5e75b', 'FREE'), ('647f20e3c32dab21a2a5e75c', 'BONUSES'), ('647f20e3c32dab21a2a5e75d', 'PROMO')], default='647f20e3c32dab21a2a5e757', max_length=32),
        ),
    ]
