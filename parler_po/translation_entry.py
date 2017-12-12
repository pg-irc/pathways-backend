from django.core.exceptions import ObjectDoesNotExist
from parler.models import TranslatableModel
import logging
import polib

from parler_po.exceptions import (
    FieldNotTranslatableError,
    InvalidMsgidError,
    MasterInstanceLookupError,
    MissingMsgidError,
    ModelNotTranslatableError,
    ProtectedTranslationError
)
from parler_po.util import (
    get_base_translation,
    build_instance_field_id,
    parse_instance_field_id
)

class TranslationEntry(object):
    def __init__(self, instance, field_id, msgid, msgstr):
        if not _instance_is_translatable_model(instance):
            raise ModelNotTranslatableError(instance.__class__)

        if not _instance_has_translatable_field(instance, field_id):
            raise FieldNotTranslatableError(field_id)

        base_translation = get_base_translation(instance)

        if not msgid:
            raise MissingMsgidError()

        if msgid != getattr(base_translation, field_id):
            raise InvalidMsgidError()

        self._instance = instance
        self._field_id = field_id
        self._msgid = msgid
        self._msgstr = msgstr
        self._base_translation = base_translation

    @property
    def model(self):
        return self._instance.__class__

    @property
    def _instance_field_id(self):
        return build_instance_field_id(self._instance, self._field_id)

    def __str__(self):
        return self._instance_field_id

    @classmethod
    def from_po_entry(cls, po_entry, occurrence):
        (instance_field_id, _lineno) = occurrence

        try:
            instance, field_id = parse_instance_field_id(instance_field_id)
        except (ObjectDoesNotExist, ValueError) as error:
            raise MasterInstanceLookupError(error)

        return cls(
            instance,
            field_id,
            msgid=po_entry.msgid,
            msgstr=po_entry.msgstr
        )

    @classmethod
    def from_translation(cls, translation, field_id):
        base_translation = get_base_translation(translation.master)

        if base_translation:
            msgid = getattr(base_translation, field_id, '')
        else:
            msgid = ''

        msgstr = getattr(translation, field_id, '')

        return cls(
            translation.master,
            field_id,
            msgid=msgid,
            msgstr=msgstr
        )

    def as_po_entry(self):
        return polib.POEntry(
            msgid=self._msgid,
            msgstr=self._msgstr,
            occurrences=[(self._instance_field_id, None)]
        )

    def save_translation(self, language_code):
        if language_code == self._base_translation.language_code:
            raise ProtectedTranslationError()

        return _update_translation(
            self._instance, language_code, self._field_id, self._msgstr
        )

def _instance_is_translatable_model(instance):
    return isinstance(instance, TranslatableModel)

def _instance_has_translatable_field(instance, field_id):
    return field_id in instance.translations.model.get_translated_fields()

def _update_translation(translatable, language_code, field_id, msgstr):
    try:
        translation = translatable.get_translation(language_code)
    except translatable.translations.model.DoesNotExist as error:
        if msgstr:
            translatable.create_translation(language_code)
            translation = translatable.get_translation(language_code)
        else:
            translation = None

    # TODO: If msgstr is blank, should we fall back to the base language? Or
    #       should we expect translators to do that in their PO files?

    if translation:
        setattr(translation, field_id, msgstr)
        is_modified = translation.is_modified
        translation.save()
    else:
        is_modified = False

    return is_modified
