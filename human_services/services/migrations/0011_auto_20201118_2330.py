# Generated by Django 3.1.2 on 2020-11-18 23:30

import common.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_auto_20201027_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='website',
            field=common.models.OptionalCharField(max_length=255, validators=[django.core.validators.URLValidator()]),
        ),
    ]
