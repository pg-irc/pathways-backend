from django.test import TestCase
from newcomers_guide import parse_file_path


class FilePathParseTests(TestCase):
    def setUp(self):
        self.path = 'some/path/chapter_6_education/articles/Elementary_school/fr.École_primaire.txt'
        self.parsed_path = parse_file_path.parse_file_path(self.path)

    def test_can_extract_chapter(self):
        self.assertEqual(self.parsed_path.chapter, 'chapter_6_education')

    def test_can_extract_content_type(self):
        self.assertEqual(self.parsed_path.type, 'articles')

    def test_can_extract_content_id(self):
        self.assertEqual(self.parsed_path.id, 'Elementary_school')

    def test_can_extract_language(self):
        self.assertEqual(self.parsed_path.locale, 'fr')

    def test_can_extract_localized_content_title(self):
        self.assertEqual(self.parsed_path.title, 'École_primaire')
