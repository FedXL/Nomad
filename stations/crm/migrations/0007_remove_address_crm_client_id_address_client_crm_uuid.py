# Generated by Django 5.1.3 on 2025-03-18 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_alter_clientcrm_birthday_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='crm_client_id',
        ),
        migrations.AddField(
            model_name='address',
            name='client_crm_uuid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
