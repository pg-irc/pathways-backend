from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
import os
import polib

PARLER_PO_BASE_LANGUAGE = getattr(settings, 'PARLER_PO_BASE_LANGUAGE', 'en')
PARLER_PO_CONTACT = getattr(settings, 'PARLER_PO_CONTACT', None)

def get_base_translation(translatable):
    if translatable.has_translation(PARLER_PO_BASE_LANGUAGE):
        return translatable.get_translation(PARLER_PO_BASE_LANGUAGE)
    else:
        return None

def new_pot_file():
    now_str = datetime.utcnow().isoformat()

    pot_file = polib.POFile()
    pot_file.metadata = dict()

    pot_file.metadata['Project-Id-Version'] = '1.0'
    pot_file.metadata['Report-Msgid-Bugs-To'] = PARLER_PO_CONTACT
    pot_file.metadata['POT-Creation-Date'] = now_str
    pot_file.metadata['MIME-Version'] = '1.0'
    pot_file.metadata['Content-Type'] = 'text/plain; charset=utf-8'
    pot_file.metadata['Content-Transfer-Encoding'] = '8bit'

    return pot_file

def new_po_file(pot_file=None, language_code=None):
    now_str = datetime.utcnow().isoformat()

    po_file = polib.POFile()
    po_file.metadata = dict()

    if pot_file:
        po_file.metadata.update(pot_file.metadata)

    po_file.metadata['Language'] = language_code
    po_file.metadata['PO-Revision-Date'] = now_str
    po_file.metadata['MIME-Version'] = '1.0'
    po_file.metadata['Content-Type'] = 'text/plain; charset=utf-8'
    po_file.metadata['Content-Transfer-Encoding'] = '8bit'

    return po_file

def build_pot_path(output_dir, model):
    content_type = ContentType.objects.get_for_model(model)
    domain = build_content_type_id(content_type)
    pot_name = '{}.pot'.format(domain)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, pot_name)

def build_po_path(output_dir, model, language_code):
    content_type = ContentType.objects.get_for_model(model)
    domain = build_content_type_id(content_type)
    po_name = '{}.po'.format(domain)
    language_dir = os.path.join(output_dir, language_code, 'LC_MESSAGES')
    os.makedirs(language_dir, exist_ok=True)
    return os.path.join(language_dir, po_name)

def build_content_type_id(content_type):
    return '.'.join([content_type.app_label, content_type.model])

def parse_content_type_id(content_type_id):
    parts = content_type_id.split('.')
    if len(parts) == 2:
        (app_label, model) = parts
        return ContentType.objects.get(app_label=app_label, model=model)
    else:
        msg = _("Invalid content type id: {}").format(content_type_id)
        raise ValueError(msg)

def build_instance_field_id(instance, field_id):
    content_type = ContentType.objects.get_for_model(instance)
    content_type_id = build_content_type_id(content_type)
    return "{model}@{field}@{instance}".format(
        model=content_type_id,
        field=field_id,
        instance=instance.pk
    )

def parse_instance_field_id(instance_field_id):
    parts = instance_field_id.split('@', 3)
    if len(parts) == 3:
        (content_type_id, field_id, instance_pk) = parts
        content_type = parse_content_type_id(content_type_id)
        instance = content_type.get_object_for_this_type(pk=instance_pk)
        return (instance, field_id)
    else:
        msg = _("Invalid instance field id: {}").format(instance_field_id)
        raise ValueError(msg)
