from django.test import TestCase
from io import StringIO
import re


def is_title(line):
    regex = r'[\d\. ]*Topic:.*'
    if re.fullmatch(regex, line):
        return True
    return False


def get_title(line):
    regex = r'[\d\. ]*Topic:(.*)'
    result = re.match(regex, line)[1].strip()
    if result == '':
        raise RuntimeError(line)
    return result


def is_tag(line):
    regex = r'Tags:.*'
    if re.fullmatch(regex, line):
        return True
    return False


def get_tags(line):
    regex = r'Tags:(.*)'
    result = re.match(regex, line)[1].strip().split()
    return result


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
        self.assertEqual(get_tags('Tags: healthCare:disability housing:wantToBuy'), ['healthCare:disability', 'housing:wantToBuy'])


class Topic:
    def __init__(self, name, tags, text):
        self.name = name
        self.tags = tags
        self.text = text


class TopicWriter:
    def __init__(self):
        self.topics = []
        self.name = ''
        self.tags = []
        self.text = []

    def parse(self, line):
        if is_title(line):
            self.save_current_topic()
            self.name = get_title(line)
            self.tags = []
            self.text = ''
        elif is_tag(line):
            self.tags = get_tags(line)
        else:
            self.text += line

    def save_current_topic(self):
        if self.name:
            self.topics.append(Topic(self.name, self.tags, self.text))

    def done(self):
        self.save_current_topic()
        return self


def parse_string(text):
    writer = TopicWriter()
    for line in text.split('\n'):
        writer.parse(line)
    return writer.done()


class TestBla(TestCase):
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
        line = '2.10 Topic: Biking\nTags: transport:local\nBiking is fun\n2.11 Topic: Travel by plane\nTags: transport:long_distance\nPlanes fly fast\n'
        writer = parse_string(line)
        self.assertEqual(len(writer.topics), 2)
        self.assertEqual(writer.topics[0].name, 'Biking')
        self.assertEqual(writer.topics[1].name, 'Travel by plane')
