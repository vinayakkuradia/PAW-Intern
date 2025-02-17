# Generated by Django 2.2.7 on 2020-05-24 12:29

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_file', models.CharField(max_length=50)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('json_data', jsonfield.fields.JSONField()),
            ],
        ),
    ]
