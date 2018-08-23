from django.test import TestCase
from newcomers_guide.clean_data import clean_up_links, clean_up_newlines

# Need to replace single newlines with space, except when the line before
# and/or after is a list item or heading. This is because the markdown
# component renders newlines as line breaks, see
# https://github.com/mientjan/react-native-markdown-renderer/issues/74

# For the markdown component, one newline means a line break, two newlines
# or more means a paragraph break. So since we are converting one newline
# into space, we need to convert two newlines into one newline and three or
# more newlines into two newlines. To simplify the implementation, two newlines
# separated by all whitespace is converted into just two newlines as a pre-
# processing step.

# Need to replace multiple spaces with a single space, because the markdown
# component renders larger horizontal spaces for multiple space characters.

# Need to leave all whitespace following one or more newlines unchanged,
# because this whitespace can be meaningful when formatting nested lists.

# One newline is enough before and after headings. Three or more newlines
# in a row is OK, even when they're interspersed with other whitespace


class CleanUpNewlinesTest(TestCase):
    def test_removes_carriage_returns(self):
        text = 'abc\rdef'
        self.assertEqual(clean_up_newlines(text), 'abcdef')

    def test_ignores_whitespace_between_newlines(self):
        text = 'abc\n\t\r \ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\ndef')

    def test_replaces_single_newline_with_space(self):
        text = 'abc\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_replaces_double_newline_with_single_newline(self):
        text = 'abc\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\ndef')

    def test_replaces_tripple_newline_with_double_newline(self):
        text = 'abc\n\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_replaces_four_newlines_with_double_newline(self):
        text = 'abc\n\n\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_leaves_newline_unchanged_before_heading(self):
        text = 'abc\n# def'
        self.assertEqual(clean_up_newlines(text), 'abc\n# def')

    def test_leaves_newline_unchanged_after_heading(self):
        text = 'abc\n# def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n# def\nghi')
        text = '# def\nghi'
        self.assertEqual(clean_up_newlines(text), '# def\nghi')

    def test_leaves_newline_unchanged_before_star_bullet(self):
        text = 'abc\n* def'
        self.assertEqual(clean_up_newlines(text), 'abc\n* def')

    def test_leaves_newline_unchanged_after_star_bullet(self):
        text = 'abc\n* def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n* def\nghi')
        text = '* def\nghi'
        self.assertEqual(clean_up_newlines(text), '* def\nghi')

    def test_leaves_newline_unchanged_before_plus_bullet(self):
        text = 'abc\n+ def'
        self.assertEqual(clean_up_newlines(text), 'abc\n+ def')

    def test_leaves_newline_unchanged_after_plus_bullet(self):
        text = 'abc\n+ def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n+ def\nghi')
        text = '+ def\nghi'
        self.assertEqual(clean_up_newlines(text), '+ def\nghi')

    def test_leaves_newline_unchanged_before_dash_bullet(self):
        text = 'abc\n- def'
        self.assertEqual(clean_up_newlines(text), 'abc\n- def')

    def test_leaves_newline_unchanged_after_dash_bullet(self):
        text = 'abc\n- def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n- def\nghi')
        text = '- def\nghi'
        self.assertEqual(clean_up_newlines(text), '- def\nghi')

    def test_leaves_newline_unchanged_before_indented_line_starting_with_space(self):
        text = 'abc\n def'
        self.assertEqual(clean_up_newlines(text), 'abc\n def')

    def test_leaves_newline_unchanged_after_line_starting_with_space(self):
        text = 'abc\n def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n def\nghi')
        text = ' def\nghi'
        self.assertEqual(clean_up_newlines(text), ' def\nghi')

    def test_leaves_newline_unchanged_before_indented_line_starting_with_tab(self):
        text = 'abc\n\tdef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\tdef')

    def test_leaves_newline_unchanged_after_line_starting_with_tab(self):
        text = 'abc\n\tdef\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n\tdef\nghi')
        text = '\tdef\nghi'
        self.assertEqual(clean_up_newlines(text), '\tdef\nghi')

    def test_leaves_newline_unchanged_before_numbered_list_item_with_period(self):
        text = 'abc\n123. def'
        self.assertEqual(clean_up_newlines(text), 'abc\n123. def')

    def test_leaves_newline_unchanged_after_numbered_list_item_with_period(self):
        text = 'abc\n123. def\nefg'
        self.assertEqual(clean_up_newlines(text), 'abc\n123. def\nefg')
        text = '123. def\nefg'
        self.assertEqual(clean_up_newlines(text), '123. def\nefg')

    def test_leaves_newline_unchanged_before_numbered_list_item_with_bracket(self):
        text = 'abc\n123) def'
        self.assertEqual(clean_up_newlines(text), 'abc\n123) def')

    def test_leaves_newline_unchanged_after_numbered_list_item_with_bracket(self):
        text = 'abc\n123) def\nefg'
        self.assertEqual(clean_up_newlines(text), 'abc\n123) def\nefg')
        text = '123) def\nefg'
        self.assertEqual(clean_up_newlines(text), '123) def\nefg')

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

    def test_handles_newlines_after_punctuation(self):
        text = 'abc,\r\n\r\ndef.\r\n\r\nghi)\r\n\r\njkl'
        self.assertEqual(clean_up_newlines(text), 'abc,\ndef.\nghi)\njkl')

    def test_ignores_spaces_between_newlines(self):
        text = 'abc \n \ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\ndef')

    def test_ignores_carriage_return_between_newlines(self):
        text = 'abc\r\n\r\n\rdef'
        self.assertEqual(clean_up_newlines(text), 'abc\ndef')

    def test_removes_whitespace_before_newline(self):
        text = 'abc\t \r\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_keeps_tripple_newline_with_trailing_white_space(self):
        text = 'abc\n  \n\t\t\n\t def'
        self.assertEqual(clean_up_newlines(text), 'abc\n\n\t def')

    # What to do with bullets, throw an error?
    def ignore_test_replaces_bullet_character_with_star(self):
        text = '• This is a bullet'
        self.assertEqual(clean_up_newlines(text), '* This is a bullet')

    def test_leaves_newline_after_heading_unchanged(self):
        text = 'previous paragraph.\n\n# Heading\nBody text.'
        self.assertEqual(clean_up_newlines(text), 'previous paragraph. \n# Heading\nBody text.')

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
