# Generated by Django 3.0.4 on 2020-04-09 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa_tool', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='algorithm',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='relevancyscore',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='searchlocation',
            options={'ordering': ['id']},
        ),
    ]
