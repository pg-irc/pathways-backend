# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 23:11
from __future__ import unicode_literals

import common.models
from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20171214_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=(common.models.ValidateOnSaveMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ServiceLocationTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('description', models.TextField(blank=True, null=True)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='locations.ServiceLocation')),
            ],
            options={
                'verbose_name': 'service location Translation',
                'db_table': 'locations_servicelocation_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
    ]
