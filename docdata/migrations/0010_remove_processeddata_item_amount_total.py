# Generated by Django 2.2.7 on 2020-06-07 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docdata', '0009_auto_20200607_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processeddata',
            name='item_amount_total',
        ),
    ]
