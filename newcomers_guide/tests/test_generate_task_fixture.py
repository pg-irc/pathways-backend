from django.test import TestCase
from newcomers_guide import generate_task_fixture


class GenerateFixtureTest(TestCase):
    def setUp(self):
        self.english_path = 'some/path/chapter/articles/school/en.Elementary_school.txt'
        self.content = 'the content in English'

    def test_include_content_id_from_path(self):
        result = generate_task_fixture.generate_task_fixture([[self.english_path, self.content]])
        expected = (
            'export const buildTasksFixture = (): Store => {\n'
            '    return {\n'
            '        taskMap: '
            '{"school": {'
            '"id": "school", '
            '"title": {"en": "Elementary_school"}, '
            '"description": {"en": "the content in English"}'
            '}}\n'
            '    }\n'
            '}')
        self.assertEqual(result, expected)
