from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from parler.models import TranslatableModel
import polib

from translation.exceptions import (
    FieldNotTranslatableError,
    InvalidMsgidError,
    MasterInstanceLookupError,
    MissingMsgidError,
    ModelNotTranslatableError,
    ContentTranslationToolsError,
    ProtectedTranslationError
)
from translation.field_ids import build_instance_field_id, parse_instance_field_id
from translation.queries import get_base_translation, is_translatable_model

class TranslatableString(object):
    def __init__(self, instance, field_id, source_str, translated_str):
        if not is_translatable_model(instance.__class__):
            raise ModelNotTranslatableError(instance.__class__)

        base_translation = get_base_translation(instance)

        if not _instance_has_translatable_field(instance, field_id):
            raise FieldNotTranslatableError(field_id)

        if not source_str:
            raise MissingMsgidError()

        if source_str != getattr(base_translation, field_id):
            raise InvalidMsgidError()

        self._instance = instance
        self._field_id = field_id
        self._source_str = source_str
        self._translated_str = translated_str
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
        except ContentTranslationToolsError as error:
            raise MasterInstanceLookupError(error)

        return cls(
            instance,
            field_id,
            source_str=po_entry.msgid,
            translated_str=po_entry.msgstr
        )

    @classmethod
    def all_from_po_entry(cls, po_entry, errors_out=[]):
        for occurrence in po_entry.occurrences:
            try:
                translatable_string = cls.from_po_entry(po_entry, occurrence)
            except ContentTranslationToolsError as error:
                errors_out.append(
                    _("Skipping \"{occurrence}\": {error}").format(
                        occurrence=":".join(n for n in occurrence if n),
                        error=error
                    )
                )
            else:
                yield translatable_string

    @classmethod
    def from_translation(cls, translation, field_id):
        base_translation = get_base_translation(translation.master)

        if base_translation:
            source_str = getattr(base_translation, field_id, '')
        else:
            source_str = ''

        translated_str = getattr(translation, field_id, '')

        return cls(
            translation.master,
            field_id,
            source_str=source_str,
            translated_str=translated_str
        )

    @classmethod
    def all_from_translation(cls, translation, errors_out=[]):
        for field_id in translation.get_translated_fields():
            try:
                translatable_string = cls.from_translation(translation, field_id)
            except MissingMsgidError as error:
                if getattr(translation, field_id, None):
                    errors_out.append(
                        _("Skipping \"{translation} - {field_id}\": {error}").format(
                            translation=translation.master,
                            field_id=field_id,
                            error=error
                        )
                    )
                else:
                    pass
            else:
                yield translatable_string

    def as_po_entry(self, strip_msgstr=False):
        return polib.POEntry(
            msgid=self._source_str,
            msgstr=self._translated_str if not strip_msgstr else '',
            occurrences=[(self._instance_field_id, None)]
        )

    def save_translation(self, language_code):
        if language_code == self._base_translation.language_code:
            raise ProtectedTranslationError()

        return _update_translation_for_translatable_instance(
            self._instance, language_code, self._field_id, self._translated_str
        )

def all_model_base_strings(model, **kwargs):
    for instance in model.objects.all():
        base_translation = get_base_translation(instance)
        yield from TranslatableString.all_from_translation(base_translation, **kwargs)

def all_model_translated_strings(model, language, **kwargs):
    for instance in model.objects.all():
        try:
            translation = instance.get_translation(language)
        except instance.translations.model.DoesNotExist:
            pass
        else:
            yield from TranslatableString.all_from_translation(translation, **kwargs)

def _instance_has_translatable_field(instance, field_id):
    return field_id in instance.translations.model.get_translated_fields()

def _update_translation_for_translatable_instance(instance, language_code, field_id, translated_str):
    try:
        translation = instance.get_translation(language_code)
    except instance.translations.model.DoesNotExist as error:
        if translated_str:
            instance.create_translation(language_code)
            translation = instance.get_translation(language_code)
        else:
            translation = None

    # TODO: If translated_str is blank, should we fall back to the base language? Or
    #       should we expect translators to do that in their PO files?

    if translation and getattr(translation, field_id, None) != translated_str:
        setattr(translation, field_id, translated_str)
        translation.save()
        is_modified = True
    else:
        is_modified = False

    return is_modified
