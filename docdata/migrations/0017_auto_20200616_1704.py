# Generated by Django 2.2.7 on 2020-06-16 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docdata', '0016_auto_20200616_1615'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BillItems',
            new_name='BillItem',
        ),
    ]
