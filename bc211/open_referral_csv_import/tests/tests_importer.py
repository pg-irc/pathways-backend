import unittest
from django.test import TestCase
from ..importer import import_organizations_file


class OpenReferralImporterTests(TestCase):
    def test_missing_organizations_file_throws_exception(self):
        incorrect_file_path = '../foo/organizations.csv'
        with self.assertRaises(FileNotFoundError) as error:
            import_organizations_file(incorrect_file_path)