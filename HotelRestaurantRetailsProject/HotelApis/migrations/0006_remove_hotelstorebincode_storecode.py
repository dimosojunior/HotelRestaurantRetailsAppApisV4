# Generated by Django 4.1.3 on 2023-09-21 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HotelApis', '0005_hotelprocessconfig_alter_hotelbusinessunit_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelstorebincode',
            name='StoreCode',
        ),
    ]
