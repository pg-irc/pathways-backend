from django.test import TestCase
import re
from newcomers_guide.split_win_file import is_title, is_tag, get_title, get_tags, parse_string


class TestSplitWinFile(TestCase):

    def test_can_identify_topic_title(self):
        self.assertTrue(is_title('2.28 Topic: Places of Worship'))

    def test_topic_title_may_have_no_leading_number(self):
        self.assertTrue(is_title('Topic: Places of Worship'))

    def test_topic_title_can_be_empty(self):
        self.assertTrue(is_title('2.28 Topic: '))

    def test_topic_cannot_have_leading_arbitrary_text(self):
        self.assertFalse(is_title('Bla Topic: '))

    def test_can_get_title_string(self):
        self.assertEqual(get_title('Topic: Places of Worship'), 'Places of Worship')

    def test_error_on_empty_title(self):
        with self.assertRaises(RuntimeError):
            get_title('Topic:')

    def test_can_identify_topic_tags(self):
        self.assertTrue(is_tag('Tags: healthCare:disability'))

    def test_can_get_zero_tags(self):
        self.assertEqual(get_tags('Tags:'), [])

    def test_can_get_one_tag(self):
        self.assertEqual(get_tags('Tags: healthCare:disability'), ['healthCare:disability'])

    def test_can_get_multiple_tags(self):
        self.assertEqual(get_tags('Tags: healthCare:disability housing:wantToBuy'), ['healthCare:disability',
                                                                                     'housing:wantToBuy'])

    def test_can_get_topic_from_line(self):
        line = '2.20 Topic: Places of Worship\nsome more text goes here'
        writer = parse_string(line)
        self.assertEqual(len(writer.topics), 1)
        self.assertEqual(writer.topics[0].name, 'Places of Worship')

    def test_can_get_tags_from_line(self):
        line = '2.20 Topic: Places of Worship\nTags: first:tag second:tag\nsome more text goes here'
        writer = parse_string(line)
        self.assertEqual(len(writer.topics), 1)
        self.assertEqual(writer.topics[0].tags, ['first:tag', 'second:tag'])

    def test_can_get_text_from_line(self):
        line = '2.20 Topic: Places of Worship\nTags: first:tag second:tag\nsome more text goes here'
        writer = parse_string(line)
        self.assertEqual(len(writer.topics), 1)
        self.assertEqual(writer.topics[0].text, 'some more text goes here')

    def test_can_get_two_topics_from_lines(self):
        line = ('2.10 Topic: Biking\nTags: transport:local\nBiking is fun\n2.11 Topic: Travel by plane\n'
                'Tags: transport:long_distance\nPlanes fly fast\n')
        writer = parse_string(line)
        self.assertEqual(len(writer.topics), 2)
        self.assertEqual(writer.topics[0].name, 'Biking')
        self.assertEqual(writer.topics[1].name, 'Travel by plane')
