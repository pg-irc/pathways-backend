from django.test import TestCase
from newcomers_guide.clean_data import clean_up_links, clean_up_newlines


class CleanUpNewlinesTest(TestCase):
    def test_replaces_single_newline_with_space(self):
        text = 'abc\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_replaces_single_newline_in_two_places_with_spaces(self):
        text = 'abc\ndef\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc def ghi')

    def test_replaces_single_newlines_with_space_also_after_punctiation(self):
        text = 'abc,\r\ndef.\r\nghi)\r\njkl'
        self.assertEqual(clean_up_newlines(text), 'abc, def. ghi) jkl')

    def test_replaces_double_newlines_with_paragraph_break_also_after_punctiation(self):
        text = 'abc,\r\n\r\ndef.\r\n\r\nghi)\r\n\r\njkl'
        self.assertEqual(clean_up_newlines(text), 'abc,\n\ndef.\n\nghi)\n\njkl')

    def test_replaces_one_newline_surrounded_by_whitspace(self):
        text = 'abc\t \n\r\t def'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_replaces_double_newline_with_paragraph_break(self):
        text = 'abc\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_replaces_tripple_newline_with_paragraph_break(self):
        text = 'abc\n\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_replaces_double_newline_carriage_return_with_paragraph_break(self):
        text = 'abc\n\r\n\rdef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_inserts_newline_after_heading(self):
        text = 'previous paragraph.\n\n# Heading\nBody text.'
        self.assertEqual(clean_up_newlines(text), 'previous paragraph.\n\n# Heading\n\nBody text.')

    def test_inserts_newline_after_heading_at_the_start_of_string(self):
        text = '# Heading\nBody text.'
        self.assertEqual(clean_up_newlines(text), '# Heading\n\nBody text.')

    def test_does_not_insert_newline_after_pound_character_in_text(self):
        text = 'some text with #2 in it.\nSome more text'
        self.assertEqual(clean_up_newlines(text), 'some text with #2 in it. Some more text')


class CleanUpLinksTest(TestCase):
    def test_replaces_http_link_with_markdown(self):
        text = 'abc http://example.com def'
        self.assertEqual(clean_up_links(text), 'abc [example.com](http://example.com) def')

    def test_replaces_two_links_with_markdown(self):
        text = 'abc http://example.com def http://example.org ghi'
        expected = 'abc [example.com](http://example.com) def [example.org](http://example.org) ghi'
        self.assertEqual(clean_up_links(text), expected)

    def test_includes_just_host_in_link_name(self):
        text = 'abc http://example.com/foo/bar def'
        self.assertEqual(clean_up_links(text), 'abc [example.com](http://example.com/foo/bar) def')

    def test_replaces_https_link_with_markdown(self):
        text = 'https://example.com'
        self.assertEqual(clean_up_links(text), '[example.com](https://example.com)')
