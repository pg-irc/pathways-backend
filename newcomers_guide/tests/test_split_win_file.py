from django.test import TestCase
import re
from newcomers_guide.split_win_file import is_chapter, is_title, is_tag, get_chapter, get_title, get_tags, parse_string


class TestSplitWinFile(TestCase):

    def test_can_identify_chapter_title(self):
        self.assertTrue(is_chapter('8 CHAPTER 8 - Driving'))

    def test_can_get_chapter_title(self):
        self.assertEqual(get_chapter('8 CHAPTER 8 - Driving'), 'CHAPTER 8 - Driving')

    def test_error_on_empty_chapter_title(self):
        with self.assertRaises(RuntimeError):
            get_chapter('8 CHAPTER 8')

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
        self.assertEqual(writer.topics[0].text, 'some more text goes here\n')

    def test_can_get_multiple_lines_of_text(self):
        line = '2.20 Topic: Places of Worship\nTags: first:tag second:tag\nsome more text goes here\nand here\nand then some more'
        writer = parse_string(line)
        self.assertEqual(len(writer.topics), 1)
        self.assertEqual(writer.topics[0].text, 'some more text goes here\nand here\nand then some more\n')

    def test_can_get_two_topics_from_lines(self):
        line = ('2.10 Topic: Biking\nTags: transport:local\nBiking is fun\n2.11 Topic: Travel by plane\n'
                'Tags: transport:long_distance\nPlanes fly fast\n')
        writer = parse_string(line)
        self.assertEqual(len(writer.topics), 2)
        self.assertEqual(writer.topics[0].name, 'Biking')
        self.assertEqual(writer.topics[1].name, 'Travel by plane')

    def test_can_get_chapter_name(self):
        line = '8 CHAPTER 8 - Driving\nTopic: Places of worship'
        writer = parse_string(line)
        self.assertEqual(writer.topics[0].chapter, 'CHAPTER 8 - Driving')

    def test_chapter_name_applies_to_several_topics(self):
        line = ('8 CHAPTER 8 - Driving\n'
                '1.23 Topic: First topic\n'
                'Some text\n'
                '1.24 Topic: Second topic\n'
                'Some more text')
        writer = parse_string(line)
        self.assertEqual(writer.topics[0].chapter, 'CHAPTER 8 - Driving')
        self.assertEqual(writer.topics[1].chapter, 'CHAPTER 8 - Driving')

    def test_compute_file_path(self):
        line = ('8 CHAPTER 8 - Driving\n1.23 Topic: Buying a new or used vehicle (car or truck)\nTags: explore:driving driving:cost\nThis is about driving\n')
        writer = parse_string(line)
        self.assertEqual(writer.topics[0].file_path(), 'win/CHAPTER 8 - Driving/topics/Buying a new or used vehicle (car or truck)/')

    def test_compute_file_name(self):
        line = ('8 CHAPTER 8 - Driving\n1.23 Topic: Buying a new or used vehicle (car or truck)\nTags: explore:driving driving:cost\nThis is about driving\n')
        writer = parse_string(line)
        self.assertEqual(writer.topics[0].file_name(), 'win/CHAPTER 8 - Driving/topics/Buying a new or used vehicle (car or truck)/en.Buying a new or used vehicle (car or truck).md')
