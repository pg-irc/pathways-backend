from django.db import migrations

def forwards_func(apps, schema_editor):
    config = SeedConfiguration(apps, schema_editor)
    for phone_number_type in config.phone_number_types:
        config.model.objects.using(config.db_alias).create(id=phone_number_type)

def reverse_func(apps, schema_editor):
    config = SeedConfiguration(apps, schema_editor)
    for phone_number_type in config.phone_number_types:
        config.model.objects.using(config.db_alias).get(pk=phone_number_type).delete()

class SeedConfiguration:
    def __init__(self, apps, schema_editor):
        self.model = apps.get_model('phone_numbers', 'PhoneNumberType')
        self.db_alias = schema_editor.connection.alias
        self.phone_number_types = [
            'phone1',
            'after_hours',
            'business_line',
            'hot_line',
            'out_of_area',
            'fax',
        ]

class Migration(migrations.Migration):

    dependencies = [
        ('phone_numbers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
