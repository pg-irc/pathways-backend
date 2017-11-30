from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
import os
import polib

PARLER_PO_BASE_LANGUAGE = getattr(settings, 'PARLER_PO_BASE_LANGUAGE', 'en')
PARLER_PO_CONTACT = getattr(settings, 'PARLER_PO_CONTACT', None)

class TranslationEntry(object):
    def __init__(self, instance, field_id, msgid, msgstr):
        self.instance = instance
        self.field_id = field_id
        self.msgid = msgid
        self.msgstr = msgstr

    @classmethod
    def from_po_entry(cls, po_entry):
        for (instance_field_id, _lineno) in po_entry.occurrences:
            yield cls._from_instance_field_id(
                instance_field_id,
                msgid=po_entry.msgid,
                msgstr=po_entry.msgstr
            )

    @classmethod
    def _from_instance_field_id(cls, instance_field_id, *args, **kwargs):
        parts = instance_field_id.split('@', 3)
        if len(parts) == 3:
            (content_type_id, field_id, instance_pk) = parts
            content_type = parse_content_type_id(content_type_id)
            instance = content_type.get_object_for_this_type(pk=instance_pk)
            return cls(instance, field_id, *args, **kwargs)
        else:
            msg = _("Invalid instance field id: {}").format(instance_field_id)
            raise ValueError(msg)

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.instance)

    @property
    def content_type_id(self):
        return content_type_id(self.content_type)

    @property
    def instance_field_id(self):
        return "{model}@{field}@{instance}".format(
            model=self.content_type_id,
            field=self.field_id,
            instance=self.instance.pk
        )

    @property
    def model(self):
        return self.instance.translations.model

    def as_po_entry(self):
        return polib.POEntry(
            msgid=self.msgid,
            msgstr=self.msgstr,
            occurrences=[(self.instance_field_id, None)]
        )

    def get_translation(self, language_code):
        base_translation = get_base_translation(self.instance)

        try:
            translation = self.instance.get_translation(language_code)
        except self.model.DoesNotExist:
            self.instance.create_translation(language_code)
            translation = self.instance.get_translation(language_code)

        base_msgid = getattr(base_translation, self.field_id)

        if base_msgid != self.msgid:
            msg = _("Incorrect msgid")
            raise ValueError(msg)
        else:
            return translation

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

def get_pot_path(output_dir, model):
    content_type = ContentType.objects.get_for_model(model)
    domain = content_type_id(content_type)
    pot_name = '{}.pot'.format(domain)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, pot_name)

def get_po_path(output_dir, model, language_code):
    content_type = ContentType.objects.get_for_model(model)
    domain = content_type_id(content_type)
    po_name = '{}.po'.format(domain)
    language_dir = os.path.join(output_dir, language_code, 'LC_MESSAGES')
    os.makedirs(language_dir, exist_ok=True)
    return os.path.join(language_dir, po_name)

def content_type_id(content_type):
    return '.'.join([content_type.app_label, content_type.model])

def parse_content_type_id(content_type_id):
    parts = content_type_id.split('.')
    if len(parts) == 2:
        (app_label, model) = parts
        return ContentType.objects.get(app_label=app_label, model=model)
    else:
        msg = _("Invalid content type id: {}").format(content_type_id)
        raise ValueError(msg)
