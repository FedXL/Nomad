# Generated by Django 5.1.3 on 2025-04-13 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_client_last_address_uuid'),
        ('crm', '0018_alter_phonecrm_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonecrm',
            name='client_watsapp',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phone_crm_w', to='clients.client'),
        ),
    ]
