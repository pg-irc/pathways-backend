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
        if not _instance_is_translatable_model(instance):
            raise TypeError("Instance is not a TranslatableModel")

        if not _instance_has_translatable_field(instance, field_id):
            raise ValueError("Field is not a translated field")

        self.instance = instance
        self.field_id = field_id
        self.msgid = msgid
        self.msgstr = msgstr

    @property
    def _instance_field_id(self):
        return build_instance_field_id(self.instance, self.field_id)

    def __str__(self):
        return self._instance_field_id

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

    @classmethod
    def from_translation(cls, translatable, translation, field_id):
        base_translation = get_base_translation(translatable)

        msgid = getattr(base_translation, field_id, "")
        msgstr = getattr(translation, field_id, "")

        return cls(
            translatable,
            field_id,
            msgid=msgid,
            msgstr=msgstr
        )

    def as_po_entry(self):
        if not self.msgid:
            raise ValueError("Missing base translation")

        return polib.POEntry(
            msgid=self.msgid,
            msgstr=self.msgstr,
            occurrences=[(self._instance_field_id, None)]
        )

    def as_translation(self, language_code):
        base_translation = get_base_translation(self.instance)

        if self.msgid != getattr(base_translation, self.field_id):
            raise ValueError("Invalid msgid")

        if language_code != base_translation.language_code:
            translation, modified = _update_translation(
                self.instance, language_code, self.field_id, self.msgstr
            )
        else:
            translation = None
            modified = False

        return (translation, modified)

def _instance_is_translatable_model(instance):
    return isinstance(instance, TranslatableModel)

def _instance_has_translatable_field(instance, field_id):
    return field_id in instance.translations.model.get_translated_fields()

def _update_translation(translatable, language_code, field_id, msgstr):
    try:
        translation = translatable.get_translation(language_code)
    except translatable.translations.model.DoesNotExist:
        if msgstr:
            translatable.create_translation(language_code)
            translation = translatable.get_translation(language_code)
        else:
            translation = None

    # TODO: If msgstr is blank, should we fall back to the base language? Or
    #       should we expect translators to do that in their PO files?

    if translation:
        setattr(translation, field_id, msgstr)
        modified = translation.is_modified
        translation.save()
    else:
        modified = False

    return (translation, modified)
