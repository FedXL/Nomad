# Generated by Django 5.1.3 on 2025-03-17 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_phone_client_watsapp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phone',
            name='client',
        ),
        migrations.RemoveField(
            model_name='phone',
            name='client_watsapp',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='ClientCRM',
        ),
        migrations.DeleteModel(
            name='Phone',
        ),
    ]
