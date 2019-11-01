from test_plus.test import TestCase
from qa_tool.tests.helpers import RelevancyScoreBuilder, AlgorithmBuilder, SearchLocationBuilder
from rest_framework import status
from human_services.services_at_location.tests.helpers import ServiceAtLocationBuilder
from newcomers_guide.tests.helpers import create_topic
from common.testhelpers.random_test_values import an_integer


class ReadRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.data = {
            'value': 2,
            'algorithm': AlgorithmBuilder().create().id,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('test').id,
        }

    def test_can_get_one_entity(self):
        score_value = an_integer()
        score = RelevancyScoreBuilder(self.user).with_value(score_value).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.client.force_login(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['value'], score_value)

    def test_can_get_when_not_authenticated(self):
        score_value = an_integer()
        score = RelevancyScoreBuilder(self.user).with_value(score_value).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['value'], score_value)

    def test_can_post(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['algorithm'], self.data['algorithm'])
        self.assertEqual(response.json()['search_location'], self.data['search_location'])
        self.assertEqual(response.json()['service_at_location'], self.data['service_at_location'])
        self.assertEqual(response.json()['topic'], self.data['topic'])

    def test_cannot_post_when_not_authenticated(self):
        url = '/qa/v1/relevancyscores/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_put(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.data['value'] = 3
        self.client.force_login(user=self.user)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_cannot_put_when_not_authenticated(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.data['value'] = 3
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_when_not_authenticated(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_just_by_pk(self):
        score = RelevancyScoreBuilder(self.user).create()
        RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WriteRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.client.force_login(user=self.user)
        self.data = {
            'value': 2,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('test').id,
        }

    def test_can_post(self):
        algorithm = AlgorithmBuilder().create()
        url = '/qa/v1/algorithms/{0}/relevancyscores/'.format(algorithm.pk)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
