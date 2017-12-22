from organizations.models import Organization

BASE_LANGUAGE = 'en'

def add_base_translation(instance, **fields):
    return add_translation(instance, BASE_LANGUAGE, **fields)

def add_translation(instance, language_code, **fields):
    instance.save()

    if not instance.has_translation(language_code):
        instance.create_translation(language_code)

    translation = instance.get_translation(language_code)

    for field_name, value in fields.items():
        setattr(translation, field_name, value)

    translation.save()

    return translation
