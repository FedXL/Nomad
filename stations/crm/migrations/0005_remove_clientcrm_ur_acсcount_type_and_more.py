# Generated by Django 5.1.3 on 2025-03-18 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_remove_clientcrm_ur_account_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientcrm',
            name='ur_acсcount_type',
        ),
        migrations.AddField(
            model_name='clientcrm',
            name='ur_acccount_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
