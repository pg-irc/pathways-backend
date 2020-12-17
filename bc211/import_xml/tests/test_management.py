from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from six import StringIO

ONE_AGENCY_FIXTURE = 'bc211/import_xml/tests/data/BC211_data_one_agency.xml'
MULTI_AGENCY_FIXTURE = 'bc211/import_xml/tests/data/BC211_data_excerpt.xml'

class TestImportBc211Data(TestCase):
    def test_import_one_record(self):
        out = StringIO()
        call_command('import_bc211_data', ONE_AGENCY_FIXTURE, stdout=out)
        expected = ('1 organizations created. 1 locations created. 1 services created.')
        self.assertIn(expected, out.getvalue())

    def test_import_many_records(self):
        out = StringIO()
        call_command('import_bc211_data', MULTI_AGENCY_FIXTURE, stdout=out)
        expected = ('15 organizations created. 39 locations created. 39 services created.')
        self.assertIn(expected, out.getvalue())

    def test_import_invalid_file(self):
        out = StringIO()
        with self.assertRaises(CommandError):
            call_command('import_bc211_data', 'NonExistentFile', stdout=out)
