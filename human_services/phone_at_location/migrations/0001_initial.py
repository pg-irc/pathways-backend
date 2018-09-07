# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-06 22:39
from __future__ import unicode_literals

import common.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0011_auto_20180227_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneAtLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.TextField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumberType',
            fields=[
                ('id', common.models.RequiredCharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='phoneatlocation',
            name='phone_number_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phone_at_location.PhoneNumberType'),
        ),
    ]
