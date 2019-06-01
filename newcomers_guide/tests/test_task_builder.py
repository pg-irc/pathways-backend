from django.test import TestCase
from newcomers_guide.parse_data import TaskBuilder


class TaskBuilderTest(TestCase):
    def setUp(self):
        self.topic = TaskBuilder()

    def test_can_set_id(self):
        self.topic.set_id('xyz')
        self.assertJSONEqual(self.topic.to_json(),
                             '{"completed": false, "relatedTopics": [], "id": "xyz"}')

    def test_can_set_title_in_a_locale(self):
        self.topic.set_title_in_locale('en', 'xyz')
        self.assertJSONEqual(self.topic.to_json(),
                             '{"completed": false, "relatedTopics": [], "title": {"en": "xyz"}}')

    def test_can_set_title_in_multile_locales(self):
        self.topic.set_title_in_locale('en', 'xyz')
        self.topic.set_title_in_locale('fr', 'abc')
        self.assertJSONEqual(self.topic.to_json(),
                             '{"completed": false, "relatedTopics": [], "title": {"en": "xyz", "fr": "abc"}}')

    def test_can_set_description_in_a_locale(self):
        self.topic.set_description_in_locale('en', 'xyz')
        self.assertJSONEqual(self.topic.to_json(),
                             '{"completed": false, "relatedTopics": [], "description": {"en": "xyz"}}')

    def test_can_create_complete_task(self):
        self.topic.set_id('the topic id').\
            set_title_in_locale('en', 'the title in English').\
            set_title_in_locale('fr', 'the title in French').\
            set_description_in_locale('en', 'the description in English').\
            set_description_in_locale('fr', 'the description in French')

        expected = ('{'
                    '"completed": false, '
                    '"id": "the topic id", '
                    '"title": {"en": "the title in English", "fr": "the title in French"}, '
                    '"description": {"en": "the description in English", "fr": "the description in French"}, '
                    '"relatedTopics": []'
                    '}')
        self.assertJSONEqual(self.topic.to_json(), expected)
