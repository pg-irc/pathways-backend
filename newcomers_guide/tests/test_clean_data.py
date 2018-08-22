from django.test import TestCase
from newcomers_guide.clean_data import clean_up_links, clean_up_newlines

# Need to replace single newlines with space, except when the next line
# is a list item or heading. This is because the markdown component renders
# newlines as line breaks,
# see https://github.com/mientjan/react-native-markdown-renderer/issues/74

# Need to replace multiple spaces with a single space, because the markdown
# component renders larger horizontal spaces for multiple space characters.

# Need to leave all whitespace following one or more newlines unchanged,
# because this whitespace can be meaningful when formatting nested lists.

# One newline is enough before and after headings. Three or more newlines
# in a row is OK, even when they're interspersed with other whitespace

# Algorithm:
# All carriage returns are removed
# All whitespace before a newline is removed
# All spaces and tabs after a newline are left untouched
# All newline characters with no trailing white space are replaced with space


class CleanUpNewlinesTest(TestCase):
    def test_removes_carriage_returns(self):
        text = 'abc\rdef'
        self.assertEqual(clean_up_newlines(text), 'abcdef')

    def test_replaces_single_newline_with_space(self):
        text = 'abc\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_leaves_newline_unchanged_before_heading(self):
        text = 'abc\n# def'
        self.assertEqual(clean_up_newlines(text), 'abc\n# def')

    def test_leaves_newline_unchanged_before_star_bullet(self):
        text = 'abc\n* def'
        self.assertEqual(clean_up_newlines(text), 'abc\n* def')

    def test_leaves_newline_unchanged_before_plus_bullet(self):
        text = 'abc\n+ def'
        self.assertEqual(clean_up_newlines(text), 'abc\n+ def')

    def test_leaves_newline_unchanged_before_dash_bullet(self):
        text = 'abc\n- def'
        self.assertEqual(clean_up_newlines(text), 'abc\n- def')

    def test_leaves_newline_unchanged_before_whitespace(self):
        text = 'abc\n def'
        self.assertEqual(clean_up_newlines(text), 'abc\n def')

    def test_leaves_newline_unchanged_before_tab(self):
        text = 'abc\n\tdef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\tdef')

    def test_replaces_single_newline_in_two_places_with_spaces(self):
        text = 'abc\ndef\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc def ghi')

    def test_replaces_single_newlines_with_space_also_after_punctuation(self):
        text = 'abc,\r\ndef.\r\nghi)\r\njkl'
        self.assertEqual(clean_up_newlines(text), 'abc, def. ghi) jkl')

    def test_leaves_double_newlines_unchanged_also_after_punctuation(self):
        text = 'abc,\r\n\r\ndef.\r\n\r\nghi)\r\n\r\njkl'
        self.assertEqual(clean_up_newlines(text), 'abc,\n\ndef.\n\nghi)\n\njkl')

    def test_leaves_double_newlines_unchanged_when_separated_by_space(self):
        text = 'abc \n \n def'
        self.assertEqual(clean_up_newlines(text), 'abc\n\n def')

    def test_leaves_double_newlines_unchanged_when_separated_by_carriage_return(self):
        text = 'abc\r\n\r\n\rdef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_leaves_double_newlines_unchanged_when_separated_by_tabs(self):
        text = 'abc\t\n\t\n\tdef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\n\tdef')

    def test_removes_whitespace_before_newline(self):
        text = 'abc\t \r\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_keeps_tripple_newline_with_trailing_white_space(self):
        text = 'abc\n  \n\t\t\n\t def'
        self.assertEqual(clean_up_newlines(text), 'abc\n\n\n\t def')

    def test_removes_carriage_return_within_newlines(self):
        text = 'abc\n\r\n\rdef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    # What to do with bullets, throw an error?
    def ignore_test_replaces_bullet_character_with_star(self):
        text = '• This is a bullet'
        self.assertEqual(clean_up_newlines(text), '* This is a bullet')

    def test_leaves_newline_after_heading_unchanged(self):
        text = 'previous paragraph.\n\n# Heading\nBody text.'
        self.assertEqual(clean_up_newlines(text), 'previous paragraph.\n\n# Heading\nBody text.')

    def test_leaves_newline_after_heading_at_the_start_of_string_unchanged(self):
        text = '# Heading\nBody text.'
        self.assertEqual(clean_up_newlines(text), '# Heading\nBody text.')


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
