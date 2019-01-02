from django.test import TestCase
from search.save_tasks import save_tasks
from search.tests import helpers
from search.models import Task
from common.testhelpers.random_test_values import a_string


class TestSavingTasks(TestCase):
    def setUp(self):
        self.task_id = 'the-task-id'
        self.english_task_name = a_string()
        self.english_task_description = a_string()
        self.one_task = {
            'taskMap': {
                'the-task-id': {
                    'id': 'the-task-id',
                    'title': {
                        'en': self.english_task_name,
                    },
                    'description': {
                        'en': self.english_task_description,
                    },
                    'taxonomyTerms': [
                        {
                            'taxonomyId': 'colour',
                            'taxonomyTermId': 'blue',
                        },
                        {
                            'taxonomyId': 'size',
                            'taxonomyTermId': 'large',
                        }
                    ],
                }
            }
        }

    def test_deletes_existing_records(self):
        two_preexisting_tasks = [a_string(), a_string()]
        helpers.create_tasks(two_preexisting_tasks)

        save_tasks(self.one_task)
        self.assertEqual(Task.objects.count(), 1)

    def test_saves_task_id(self):
        save_tasks(self.one_task)
        records = Task.objects.all()
        self.assertEqual(records[0].id, self.task_id)

    def test_saves_task_title_in_english(self):
        save_tasks(self.one_task)
        records = Task.objects.all()
        self.assertEqual(records[0].name, self.english_task_name)

    def test_saves_task_description_in_english(self):
        save_tasks(self.one_task)
        records = Task.objects.all()
        self.assertEqual(records[0].description, self.english_task_description)

    def test_saves_taxonomy_term_id(self):
        save_tasks(self.one_task)
        record = Task.objects.all()[0]
        self.assertEqual(record.taxonomy_terms.all()[0].taxonomy_id, 'colour')

    def test_saves_taxonomy_term(self):
        save_tasks(self.one_task)
        record = Task.objects.all()[0]
        self.assertEqual(record.taxonomy_terms.all()[0].name, 'blue')

    def test_saves_multiple_taxonomy_terms(self):
        save_tasks(self.one_task)
        record = Task.objects.all()[0]
        self.assertEqual(record.taxonomy_terms.all()[0].taxonomy_id, 'colour')
        self.assertEqual(record.taxonomy_terms.all()[1].taxonomy_id, 'size')
