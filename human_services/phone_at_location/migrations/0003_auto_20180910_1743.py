# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-10 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phone_at_location', '0002_auto_20180907_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneatlocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phone_numbers', to='locations.Location'),
        ),
        migrations.AlterField(
            model_name='phoneatlocation',
            name='phone_number_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='phone_at_location.PhoneNumberType'),
        ),
    ]