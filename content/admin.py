from django.contrib import admin
from parler.admin import TranslatableAdmin
from content.models import Alert

class AlertAdmin(TranslatableAdmin):
    pass

admin.site.register(Alert, AlertAdmin)
