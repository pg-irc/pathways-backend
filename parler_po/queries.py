from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from parler.models import TranslatableModel

PARLER_PO_BASE_LANGUAGE = getattr(settings, 'PARLER_PO_BASE_LANGUAGE', 'en')

def get_base_translation(instance):
    try:
        return instance.get_translation(PARLER_PO_BASE_LANGUAGE)
    except instance.translations.model.DoesNotExist:
        return None

def all_translatable_models():
    for content_type in ContentType.objects.all():
        model_class = content_type.model_class()
        if model_class and is_translatable_model(model_class):
            yield model_class

def is_translatable_model(model):
    return issubclass(model, TranslatableModel)
