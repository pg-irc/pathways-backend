from django.db import migrations

def forwards_func(apps, schema_editor):
    AddressType = apps.get_model('addresses', 'AddressType')
    db_alias = schema_editor.connection.alias
    AddressType.objects.using(db_alias).bulk_create([
        AddressType(id='physical_address'),
        AddressType(id='postal_address')
    ])

def reverse_func(apps, schema_editor):
    AddressType = apps.get_model('addresses', 'AddressType')
    db_alias = schema_editor.connection.alias
    AddressType.objects.using(db_alias).get(pk='physical_address').delete()
    AddressType.objects.using(db_alias).get(pk='postal_address').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0006_auto_20180129_2332'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
