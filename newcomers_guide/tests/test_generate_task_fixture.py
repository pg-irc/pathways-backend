from django.test import TestCase
from newcomers_guide import generate_task_fixture


class GenerateFixtureTest(TestCase):
    def setUp(self):
        self.english_path = 'some/path/chapter/tasks/To_learn_english/en.Learn_english.txt'
        self.content = 'the content in English'

    def test_include_content_id_from_path(self):
        result = generate_task_fixture.generate_task_fixture([[self.english_path, self.content]])
        expected = (
            'export const buildTasksFixture = (): Store => {\n'
            '    return {\n'
            '        taskMap: '
            '{"To_learn_english": {'
            '"id": "To_learn_english", '
            '"title": {"en": "Learn_english"}, '
            '"description": {"en": "the content in English"}'
            '}}\n'
            '    }\n'
            '}')
        self.assertEqual(result, expected)
