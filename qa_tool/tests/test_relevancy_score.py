from test_plus.test import TestCase
from qa_tool.tests.helpers import RelevancyScoreBuilder, AlgorithmBuilder, SearchLocationBuilder
from rest_framework import status
from django.utils import timezone
from human_services.services_at_location.tests.helpers import ServiceAtLocationBuilder
from newcomers_guide.tests.helpers import create_topic


class ReadRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.client.force_login(user=self.user)
        self.data = {
            'id': 1,
            'value': 2,
            'time_stamp': timezone.now(),
            'algorithm': AlgorithmBuilder().create().id,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('test').id,
            'user': self.user.id
        }

    def test_can_get_entities(self):
        RelevancyScoreBuilder(self.user).with_value(1).create()
        RelevancyScoreBuilder(self.user).with_value(3).create()
        url = '/v1/relevancyscores/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_entity(self):
        score = RelevancyScoreBuilder(self.user).with_value(3).build()
        score.save()
        url = '/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['value'], 3)

    def test_can_post(self):
        url = '/v1/relevancyscores/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_put(self):
        score = RelevancyScoreBuilder(self.user).build()
        score.save()
        url = '/v1/relevancyscores/{0}/'.format(score.pk)
        self.data['value'] = 3
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_can_delete(self):
        score = RelevancyScoreBuilder(self.user).build()
        score.save()
        url = '/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_delete_just_by_pk(self):
        score = RelevancyScoreBuilder(self.user).build()
        score.save()
        RelevancyScoreBuilder(self.user).create()
        url = '/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WriteRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.client.force_login(user=self.user)
        self.data = {
            'id': 1,
            'value': 2,
            'time_stamp': timezone.now(),
            'algorithm': AlgorithmBuilder().create().id,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('test').id,
            'user': self.user.id
        }

    def test_can_post(self):
        algorithm = AlgorithmBuilder().create()
        url = '/v1/algorithms/{0}/relevancyscores/'.format(algorithm.pk)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
