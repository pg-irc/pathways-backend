from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel
import logging
import polib

from parler_po.util import (
    get_base_translation,
    content_type_id,
    parse_content_type_id
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
        return cls._from_instance_field_id(
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
    def _content_type(self):
        return ContentType.objects.get_for_model(self.instance)

    @property
    def content_type_id(self):
        return content_type_id(self._content_type)

    @property
    def _translation_model(self):
        return self.instance.translations.model

    @property
    def instance_field_id(self):
        return "{model}@{field}@{instance}".format(
            model=self.content_type_id,
            field=self.field_id,
            instance=self.instance.pk
        )

    def as_po_entry(self):
        return polib.POEntry(
            msgid=self.msgid,
            msgstr=self.msgstr,
            occurrences=[(self.instance_field_id, None)]
        )

    def get_base_translation(self):
        return get_base_translation(self.instance)

    def get_translation(self, language_code):
        base_translation = self.get_base_translation()

        if not self.field_id in base_translation.get_translated_fields():
            raise ValueError("Field is not a translatable field")
        elif self.msgid != getattr(base_translation, self.field_id):
            msg = _("Incorrect msgid")
            raise ValueError(msg)
        else:
            try:
                translation = self.instance.get_translation(language_code)
            except self._translation_model.DoesNotExist:
                self.instance.create_translation(language_code)
                translation = self.instance.get_translation(language_code)
                import ipdb; ipdb.set_trace()
            return translation
