from django.core import exceptions
from django.test import TestCase
import re


def is_title(line):
    if re.fullmatch(r'.*Topic: *\S.*', line):
        return True
    return False

def get_title(line):
    return ''


class TestSplitWinFile(TestCase):

    def test_can_identify_topic_title(self):
        self.assertTrue(is_title('2.28 Topic: Places of Worship'))

    def x_test_topic_title_may_have_no_leading_number(self):
        self.assertTrue(is_title('Topic: Places of Worship'))

    def test_topic_title_cannot_be_empty(self):
        self.assertFalse(is_title('Topic: '))

    def x_test_can_get_title_string(self):
        self.assertEqual(get_title('Topic: Places of Worship'), 'Places of Worship')
