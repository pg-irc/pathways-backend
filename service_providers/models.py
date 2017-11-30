from django.db import models
from parler.models import TranslatableModel, TranslatedFields

class ServiceProvider(TranslatableModel):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    translations = TranslatedFields(
        description=models.TextField(blank=True)
    )

    def __str__(self):
        return self.name
