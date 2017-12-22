from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from unittest.mock import MagicMock

class TestNotTranslatable(models.Model):
    class Meta:
        app_label = 'parlerpo'
        managed = False
