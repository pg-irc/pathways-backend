from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel
import logging
import polib

from parler_po.util import (
    get_base_translation,
    build_instance_field_id,
    parse_instance_field_id
)

class TranslationEntry(object):
    def __init__(self, instance, field_id, msgid, msgstr):
        if not isinstance(instance, TranslatableModel):
            raise TypeError("instance must be a TranslatableModel")
        else:
            self.instance = instance
            self.field_id = field_id
            self.msgid = msgid
            self.msgstr = msgstr

    @classmethod
    def from_po_entry(cls, po_entry, occurrence):
        (instance_field_id, _lineno) = occurrence
        instance, field_id = parse_instance_field_id(instance_field_id)
        return cls(
            instance,
            field_id,
            msgid=po_entry.msgid,
            msgstr=po_entry.msgstr
        )

    @property
    def base_translation(self):
        return get_base_translation(self.instance)

    @property
    def _translation_model(self):
        return self.instance.translations.model

    @property
    def _instance_field_id(self):
        return build_instance_field_id(self.instance, self.field_id)

    def __str__(self):
        return self._instance_field_id

    def as_po_entry(self):
        return polib.POEntry(
            msgid=self.msgid,
            msgstr=self.msgstr,
            occurrences=[(self._instance_field_id, None)]
        )

    def get_translation(self, language_code):
        base_translation = self.base_translation

        if not self.field_id in base_translation.get_translated_fields():
            raise ValueError("Field is not a translatable field")
        elif self.msgid != getattr(base_translation, self.field_id):
            msg = _("Incorrect msgid")
            raise ValueError(msg)
        else:
            try:
                translation = self.instance.get_translation(language_code)
            except self.translation_model.DoesNotExist:
                self.instance.create_translation(language_code)
                translation = self.instance.get_translation(language_code)
            return translation
