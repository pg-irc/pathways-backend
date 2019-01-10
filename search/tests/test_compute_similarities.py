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

    def test_import_removes_doubly_escaped_bold_markup_from_service_descriptioin(self):
        name = 'Langley Child Development Centre'
        description_with_markup = ('The &amp;lt;b&amp;gt;Aboriginal Infant and Supported Child '
                                   'Development Program&amp;lt;/b&amp;gt; utilizes cultural '
                                   'teachings to engage children of Aboriginal heritage who have '
                                   'or are at risk for delays.')
        expected_without_markup = ('Langley Child Development Centre '
                                   'The Aboriginal Infant and Supported Child '
                                   'Development Program utilizes cultural '
                                   'teachings to engage children of Aboriginal heritage who have '
                                   'or are at risk for delays.')
        ServiceBuilder(self.organization).with_name(name).with_description(description_with_markup).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertEqual(descriptions[0], expected_without_markup)

    def test_import_removes_doubly_escaped_strong_markup_from_service_descriptioin(self):
        name = 'Last Post Fund'
        description_with_markup = ('Delivers the &amp;lt;strong&amp;gt;Veterans Affairs Canada '
                                   'Funeral and Burial Program&amp;lt;/strong&amp;gt; for veterans '
                                   'across Canada.')
        expected_without_markup = ('Last Post Fund '
                                   'Delivers the Veterans Affairs Canada '
                                   'Funeral and Burial Program for veterans '
                                   'across Canada.')
        ServiceBuilder(self.organization).with_name(name).with_description(description_with_markup).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertEqual(descriptions[0], expected_without_markup)

    def test_import_unescapes_html_entity_reference(self):
        name = 'Representation Services'
        description_with_markup = ('in situations such as getting an immediate court order to '
                                   'ensure client&#39;s or their children&#39;s safety and security')
        expected_without_markup = ('Representation Services '
                                   'in situations such as getting an immediate court order to '
                                   'ensure client\'s or their children\'s safety and security')
        ServiceBuilder(self.organization).with_name(name).with_description(description_with_markup).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertEqual(descriptions[0], expected_without_markup)

    def test_computing_similarity_matrix(self):
        similarity_matrix = compute_similarities(['this is a bit of text',
                                                  'this is a similar bit of text',
                                                  'now for something different'])
        self.assertGreater(similarity_matrix[0, 0], 0.99)
        self.assertGreater(similarity_matrix[0, 1], 0.85)
        self.assertLess(similarity_matrix[0, 2], 0.10)
