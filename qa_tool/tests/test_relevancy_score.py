from test_plus.test import TestCase
from qa_tool.tests.helpers import RelevancyScoreBuilder, AlgorithmBuilder, SearchLocationBuilder
from rest_framework import status
from human_services.services_at_location.tests.helpers import ServiceAtLocationBuilder
from newcomers_guide.tests.helpers import create_topic
from common.testhelpers.random_test_values import an_integer
from datetime import datetime


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
        score_value = an_integer()
        self.client.force_login(user=self.user)
        self.data['value'] = score_value
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['value'], score_value)

    def test_response_has_correct_algorithm(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['algorithm'], self.data['algorithm'])

    def test_response_has_correct_search_location(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['search_location'], self.data['search_location'])

    def test_response_has_correct_service_at_location(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['service_at_location'], self.data['service_at_location'])

    def test_response_has_correct_topic(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['topic'], self.data['topic'])

    def test_response_has_correct_user(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['user'], self.user.id)

    def test_response_has_similar_time_stamp(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recreated_date = datetime.strptime(response.json()['time_stamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertLessEqual(recreated_date, datetime.now())

    def test_cannot_post_when_not_authenticated(self):
        url = '/qa/v1/relevancyscores/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_post_when_missing_fields(self):
        url = '/qa/v1/relevancyscores/'
        self.client.force_login(user=self.user)
        bad_data = {
            'value': 2,
            # 'algorithm': missing algorithm
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('fake_test').id,
        }
        response = self.client.post(url, bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_can_post_through_url_param(self):
        algorithm = AlgorithmBuilder().create()
        url = '/qa/v1/algorithms/{0}/relevancyscores/'.format(algorithm.pk)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['algorithm'], algorithm.pk)

    def test_cannot_post_with_improper_url_param(self):
        url = '/qa/v1/algorithms/invalid_algorithm_id/relevancyscores/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
