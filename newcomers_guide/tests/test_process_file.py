from django.test import TestCase
from newcomers_guide import process_file
from common.testhelpers.random_test_values import a_string


class ProcessMultipleFileTest(TestCase):
    def setUp(self):
        self.english_path = 'some/path/chapter/articles/school/en.Elementary_school.txt'

        self.content = a_string()
        self.result = process_file.process_all_files([[self.english_path, self.content]])

    def test_include_content_id_from_path(self):
        self.assertEqual(self.result['school']['id'], 'school')

    def test_include_localzed_title_from_path(self):
        self.assertEqual(self.result['school']['title']['en'], 'Elementary_school')

    def test_include_localzed_content(self):
        self.assertEqual(self.result['school']['description']['en'], self.content)

    def test_clean_up_content_linebreaks(self):
        result = process_file.process_all_files([[self.english_path, 'abc \n def']])
        description = result['school']['description']['en']
        self.assertEqual(description, 'abc def')

    def test_clean_up_content_links(self):
        result = process_file.process_all_files([[self.english_path, 'abc http://example.com def']])
        description = result['school']['description']['en']
        self.assertEqual(description, 'abc [example.com](http://example.com) def')

    def test_handle_localized_titles_when_processing_the_same_content_in_different_locales(self):
        french_path = 'some/path/chapter/articles/school/fr.École_primaire.txt'
        result = process_file.process_all_files([[self.english_path, a_string()],
                                                 [french_path, a_string()]])
        self.assertEqual(result['school']['title']['en'], 'Elementary_school')
        self.assertEqual(result['school']['title']['fr'], 'École_primaire')

    def test_handle_localized_description_when_processing_the_same_content_in_different_locales(self):
        french_path = 'some/path/chapter/articles/school/fr.École_primaire.txt'
        english_description = a_string()
        french_description = a_string()
        result = process_file.process_all_files([[self.english_path, english_description],
                                                 [french_path, french_description]])
        self.assertEqual(result['school']['description']['en'], english_description)
        self.assertEqual(result['school']['description']['fr'], french_description)

    def test_combine_files_for_different_content(self):
        secondary_path = 'some/path/chapter/articles/2school/en.Secondary_school.txt'
        result = process_file.process_all_files([[self.english_path, a_string()],
                                                 [secondary_path, a_string()]])
        self.assertEqual(result['school']['title']['en'], 'Elementary_school')
        self.assertEqual(result['2school']['title']['en'], 'Secondary_school')
