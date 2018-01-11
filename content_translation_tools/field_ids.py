from django.contrib.contenttypes.models import ContentType

from content_translation_tools.exceptions import (
    ContentTypeDoesNotExistError,
    InvalidContentTypeIDError,
    InvalidInstanceFieldIDError,
    ModelInstanceDoesNotExistError
)

def build_instance_field_id(instance, field_id):
    content_type = ContentType.objects.get_for_model(instance)
    content_type_id = _build_content_type_id(content_type)
    return "{model}@{field}@{instance}".format(
        model=content_type_id,
        field=field_id,
        instance=instance.pk
    )

def parse_instance_field_id(instance_field_id):
    parts = instance_field_id.split('@', 3)

    if len(parts) != 3 or all(parts) is False:
        raise InvalidInstanceFieldIDError()

    (content_type_id, field_id, instance_pk) = parts

    content_type = _parse_content_type_id(content_type_id)
    model = content_type.model_class()

    if model is None:
        raise ModelInstanceDoesNotExistError()

    try:
        instance = model.objects.get(pk=instance_pk)
    except model.DoesNotExist:
        raise ModelInstanceDoesNotExistError()
    else:
        return (instance, field_id)

def build_model_id(model):
    content_type = ContentType.objects.get_for_model(model)
    return _build_content_type_id(content_type)

def parse_model_id(model_id):
    content_type = _parse_content_type_id(model_id)
    return content_type.model_class()

def _build_content_type_id(content_type):
    return '.'.join([content_type.app_label, content_type.model])

def _parse_content_type_id(content_type_id):
    parts = content_type_id.split('.')

    if len(parts) != 2 or all(parts) is False:
        raise InvalidContentTypeIDError()

    (app_label, model) = parts

    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model)
    except ContentType.DoesNotExist:
        raise ContentTypeDoesNotExistError()
    else:
        return content_type
