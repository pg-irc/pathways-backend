# Generated by Django 3.0.4 on 2020-04-09 17:40

import common.models
import django.core.validators
from django.db import migrations
import django.db.models.deletion
import parler.fields
import re


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20190725_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=common.models.RequiredCharField(max_length=200, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='organizationtranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='organizations.Organization'),
        ),
    ]
