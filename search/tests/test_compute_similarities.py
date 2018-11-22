from django.test import TestCase
from search.compute_similarities import (to_task_ids_and_descriptions,
                                         to_service_ids_and_descriptions,
                                         compute_similarities)
from human_services.services.models import Service
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import a_string


class TestTaskSimilarityScore(TestCase):
    def setUp(self):
        self.task_id = a_string()
        self.english_task_title = a_string()
        self.english_task_description = a_string()
        self.data = {
            'taskMap': {
                self.task_id: {
                    'completed': False,
                    'id': self.task_id,
                    'title': {
                        'en': self.english_task_title,
                    },
                    'description': {
                        'en': self.english_task_description
                    }
                }
            }
        }
        self.organization = OrganizationBuilder().create()

    def test_getting_ids_for_task_returns_task_id(self):
        ids, _ = to_task_ids_and_descriptions(self.data)
        self.assertEqual(ids[0], self.task_id)

    def test_converts_task_id_to_slug(self):
        self.data['taskMap'][self.task_id]['id'] = 'This is the id'
        ids, _ = to_task_ids_and_descriptions(self.data)
        self.assertEqual(ids[0], 'this-is-the-id')

    def test_getting_description_for_task_returns_task_title_and_description(self):
        _, descriptions = to_task_ids_and_descriptions(self.data)
        self.assertEqual(descriptions[0],
                         self.english_task_title + ' ' + self.english_task_description)

    def test_getting_id_for_service_returns_id(self):
        service = ServiceBuilder(self.organization).create()
        ids, _ = to_service_ids_and_descriptions(Service.objects.all())
        self.assertEqual(ids[0], service.id)

    def test_getting_description_for_service_returns_name_and_description(self):
        name = a_string()
        description = a_string()
        ServiceBuilder(self.organization).with_name(name).with_description(description).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertEqual(descriptions[0], name + ' ' + description)

    def test_computing_similarity_matrix(self):
        similarity_matrix = compute_similarities(['this is a bit of text',
                                                  'this is a similar bit of text',
                                                  'now for something different'])
        self.assertGreater(similarity_matrix[0, 0], 0.99)
        self.assertGreater(similarity_matrix[0, 1], 0.85)
        self.assertLess(similarity_matrix[0, 2], 0.10)
