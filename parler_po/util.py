from datetime import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
import argparse
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

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.instance)

    @property
    def content_type_id(self):
        return content_type_id(self.content_type)

    @property
    def translatable_id(self):
        return "{model}:{instance}".format(
            model=self.content_type_id,
            instance=self.instance.pk
        )

    def as_po_entry(self):
        return polib.POEntry(
            msgid=self.msgid,
            msgstr=self.msgstr,
            occurrences=[(self.translatable_id, self.field_id)]
        )

def argparse_dir_type(dir_name):
    dir_path = os.path.abspath(dir_name)

    if os.path.exists(dir_path):
        if not os.path.isdir(dir_path):
            msg = _("The path {} must be a directory").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        elif not os.access(dir_path, os.W_OK):
            msg = _("The directory {} must be writable").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return dir_path
    else:
        try:
            os.makedirs(dir_path)
        except OSError as e:
            msg = _("The directory {} does not exist").format(dir_path)
            raise argparse.ArgumentTypeError(msg)
        else:
            return dir_path

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

def new_po_file(pot_file=None):
    now_str = datetime.utcnow().isoformat()

    po_file = polib.POFile()
    po_file.metadata = dict()

    if pot_file:
        po_file.metadata.update(pot_file.metadata)

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
