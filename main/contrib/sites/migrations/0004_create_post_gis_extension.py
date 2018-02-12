from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0003_set_site_domain_and_name'),
    ]

    operations = [
        CreateExtension('postgis')
    ]
