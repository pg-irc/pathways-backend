# Generated by Django 2.1.2 on 2018-11-09 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20180910_1743'),
        ('search', '0004_auto_20181109_1737'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskServiceSimilarityScores',
            new_name='TaskServiceSimilarityScore',
        ),
    ]
