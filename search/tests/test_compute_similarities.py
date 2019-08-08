from django.test import TestCase
from search.compute_similarities import (to_topic_ids_and_descriptions,
                                         to_service_ids_and_descriptions,
                                         compute_similarities_by_tf_idf)
from human_services.services.models import Service
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import a_string


class TestTopicSimilarityScore(TestCase):
    def setUp(self):
        self.topic_id = a_string()
        self.english_topic_title = a_string()
        self.english_topic_description = a_string()
        self.data = {
            'taskMap': {
                self.topic_id: {
                    'completed': False,
                    'id': self.topic_id,
                    'title': {
                        'en': self.english_topic_title,
                    },
                    'description': {
                        'en': self.english_topic_description
                    }
                }
            }
        }
        self.organization = OrganizationBuilder().create()

    def test_getting_ids_for_topic_returns_topic_id(self):
        ids, _ = to_topic_ids_and_descriptions(self.data)
        self.assertEqual(ids[0], self.topic_id)

    def test_converts_topic_id_to_slug(self):
        self.data['taskMap'][self.topic_id]['id'] = 'This is the id'
        ids, _ = to_topic_ids_and_descriptions(self.data)
        self.assertEqual(ids[0], 'this-is-the-id')

    def test_getting_description_for_topic_returns_topic_title_and_description(self):
        _, descriptions = to_topic_ids_and_descriptions(self.data)
        self.assertEqual(descriptions[0],
                         self.english_topic_title + ' ' + self.english_topic_description)

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
        topic_ids = [a_string()]
        service_ids = [a_string(), a_string()]
        similarity_matrix = compute_similarities_by_tf_idf(['this is a bit of text',
                                                            'this is a similar bit of text',
                                                            'now for something different'],
                                                           topic_ids, service_ids)
        self.assertGreater(similarity_matrix[0, 0], 0.99)
        self.assertGreater(similarity_matrix[0, 1], 0.70)
        self.assertLess(similarity_matrix[0, 2], 0.10)

    def test_ignores_stop_words_when_computing_similarity(self):
        topic_ids = [a_string()]
        service_ids = [a_string(), a_string()]
        stop_words_from_spacy = 'already also although always among amongst amount an and another'
        similarity_matrix = compute_similarities_by_tf_idf(['this is a bit of text',
                                                            'this is a similar bit of text ' + stop_words_from_spacy,
                                                            'now for something different ' + stop_words_from_spacy],
                                                           topic_ids, service_ids)
        self.assertGreater(similarity_matrix[0, 0], 0.99)
        self.assertGreater(similarity_matrix[0, 1], 0.70)
        self.assertLess(similarity_matrix[0, 2], 0.10)

    def test_removes_local_phone_numbers_from_description(self):
        description_with_phone_numbers = 'Call 778-123-4567 or 604-123-4567 for more information.'
        description_without_phone_numbers = ('Call  or  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_removes_international_phone_numbers_from_description(self):
        description_with_phone_numbers = 'Call 1-800-123-4567 for more information.'
        description_without_phone_numbers = ('Call  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_removes_phone_numbers_in_brackets_from_description(self):
        description_with_phone_numbers = 'Call 1-(800)-123-4567 or (604)-123-4567 for more information.'
        description_without_phone_numbers = ('Call  or  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_removes_phone_numbers_beginning_with_plus_sign_from_description(self):
        description_with_phone_numbers = 'Call +1-800-123-4567 or +604-123-4567 for more information.'
        description_without_phone_numbers = ('Call  or  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_removes_phone_numbers_beginning_with_plus_sign_and_two_numbers_from_description(self):
        description_with_phone_numbers = 'Call +49-800-123-4567 for more information.'
        description_without_phone_numbers = ('Call  for more information.')
        ServiceBuilder(self.organization).with_description(description_with_phone_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(description_without_phone_numbers, descriptions[0])

    def test_does_not_remove_numbers_that_are_not_phone_numbers(self):
        description_with_numbers = 'In 2017 the Canadian population was approximately 36,710,0000.'
        expected_description = ('In 2017 the Canadian population was approximately 36,710,0000.')
        ServiceBuilder(self.organization).with_description(description_with_numbers).create()
        _, descriptions = to_service_ids_and_descriptions(Service.objects.all())
        self.assertIn(expected_description, descriptions[0])
