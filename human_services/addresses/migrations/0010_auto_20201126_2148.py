# Generated by Django 3.1.2 on 2020-11-26 21:48

import common.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0009_auto_20201124_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=common.models.OptionalCharField(max_length=200),
        ),
    ]
