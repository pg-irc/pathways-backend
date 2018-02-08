from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
import os
import polib

from translation.translatable_string import all_model_base_strings, all_model_translated_strings

def create_pot_file_for_model(model, **kwargs):
    pot_file = _new_pot_file()

    translatable_strings = all_model_base_strings(model, **kwargs)
    for translatable_string in translatable_strings:
        po_entry = translatable_string.as_po_entry(strip_msgstr=True)
        pot_file.append(po_entry)

    return pot_file

def create_po_file_for_model(model, language, **kwargs):
    po_file = _new_po_file(language)

    translatable_strings = all_model_translated_strings(model, language, **kwargs)
    for translatable_string in translatable_strings:
        po_entry = translatable_string.as_po_entry(strip_msgstr=False)
        po_file.append(po_entry)

    return po_file

def _new_pot_file():
    now_str = datetime.utcnow().isoformat()

    pot_file = polib.POFile()
    pot_file.metadata = dict()

    pot_file.metadata['Project-Id-Version'] = '1.0'
    pot_file.metadata['Report-Msgid-Bugs-To'] = _get_default_po_contact()
    pot_file.metadata['POT-Creation-Date'] = now_str
    pot_file.metadata['MIME-Version'] = '1.0'
    pot_file.metadata['Content-Type'] = 'text/plain; charset=utf-8'
    pot_file.metadata['Content-Transfer-Encoding'] = '8bit'

    return pot_file

def _new_po_file(language=None):
    now_str = datetime.utcnow().isoformat()

    po_file = polib.POFile()
    po_file.metadata = dict()

    po_file.metadata['Language'] = language
    po_file.metadata['PO-Revision-Date'] = now_str
    po_file.metadata['MIME-Version'] = '1.0'
    po_file.metadata['Content-Type'] = 'text/plain; charset=utf-8'
    po_file.metadata['Content-Transfer-Encoding'] = '8bit'

    return po_file

def _get_default_po_contact():
    return getattr(settings, 'PARLER_PO_CONTACT', None)
