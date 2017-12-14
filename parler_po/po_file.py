from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
import os
import polib

PARLER_PO_CONTACT = getattr(settings, 'PARLER_PO_CONTACT', None)

def create_pot_file(output_dir, model, po_entries):
    pot_path = _build_pot_path(output_dir, model)
    pot_file = _new_pot_file()
    pot_file.extend(po_entries)
    pot_file.save(pot_path)
    return pot_file

def create_po_file(output_dir, model, po_entries, language_code, pot_file):
    po_path = _build_po_path(output_dir, model, language_code)
    po_file = _new_po_file(pot_file=pot_file, language_code=language_code)
    po_file.extend(po_entries)
    po_file.merge(pot_file)
    po_file.save(po_path)
    return po_file

def _new_pot_file():
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

def _new_po_file(pot_file=None, language_code=None):
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

def _build_pot_path(output_dir, model):
    content_type = ContentType.objects.get_for_model(model)
    domain = _po_domain_for_content_type(content_type)
    pot_name = '{}.pot'.format(domain)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, pot_name)

def _build_po_path(output_dir, model, language_code):
    content_type = ContentType.objects.get_for_model(model)
    domain = _po_domain_for_content_type(content_type)
    po_name = '{}.po'.format(domain)
    language_dir = os.path.join(output_dir, language_code, 'LC_MESSAGES')
    os.makedirs(language_dir, exist_ok=True)
    return os.path.join(language_dir, po_name)

def _po_domain_for_content_type(content_type):
    return '.'.join([content_type.app_label, content_type.model])
