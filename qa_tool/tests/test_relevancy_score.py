from test_plus.test import TestCase
from qa_tool.tests.helpers import RelevancyScoreBuilder, AlgorithmBuilder, SearchLocationBuilder
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from human_services.services_at_location.tests.helpers import ServiceAtLocationBuilder
from newcomers_guide.tests.helpers import create_topic
from common.testhelpers.random_test_values import an_integer
import datetime


class ReadRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.token = Token.objects.create(user=self.user)
        self.APIClient = APIClient()
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
        response = self.APIClient.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['value'], score_value)

    def test_can_get_when_not_authenticated(self):
        score_value = an_integer()
        score = RelevancyScoreBuilder(self.user).with_value(score_value).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.APIClient.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['value'], score_value)

    def test_can_post(self):
        url = '/qa/v1/relevancyscores/'
        score_value = an_integer()
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data['value'] = score_value
        response = self.APIClient.post(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['value'], score_value)

    def test_response_has_correct_algorithm(self):
        url = '/qa/v1/relevancyscores/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['algorithm'], self.data['algorithm'])

    def test_response_has_correct_search_location(self):
        url = '/qa/v1/relevancyscores/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['search_location'], self.data['search_location'])

    def test_response_has_correct_service_at_location(self):
        url = '/qa/v1/relevancyscores/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['service_at_location'], self.data['service_at_location'])

    def test_response_has_correct_topic(self):
        url = '/qa/v1/relevancyscores/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['topic'], self.data['topic'])

    def test_response_has_correct_user(self):
        url = '/qa/v1/relevancyscores/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['user'], self.user.id)

    def test_response_has_similar_time_stamp(self):
        url = '/qa/v1/relevancyscores/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recreated_time = datetime.datetime.strptime(response.json()['time_stamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertLessEqual(recreated_time, datetime.datetime.now())
        self.assertGreaterEqual(recreated_time + datetime.timedelta(seconds=1), datetime.datetime.now())

    def test_cannot_post_when_not_authenticated(self):
        url = '/qa/v1/relevancyscores/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_post_when_missing_fields(self):
        url = '/qa/v1/relevancyscores/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        bad_data = {
            'value': 2,
            # 'algorithm': missing algorithm
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('fake_test').id,
        }
        response = self.APIClient.post(url, bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_put(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.data['value'] = 3
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_put_when_not_authenticated(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.data['value'] = 3
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_when_not_authenticated(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class WriteRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.token = Token.objects.create(user=self.user)
        self.APIClient = APIClient()
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data = {
            'value': 2,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('test').id,
        }

    def test_can_post_through_url_param(self):
        algorithm = AlgorithmBuilder().create()
        url = '/qa/v1/algorithms/{0}/relevancyscores/'.format(algorithm.pk)
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['algorithm'], algorithm.pk)

    def test_cannot_post_with_improper_url_param(self):
        url = '/qa/v1/algorithms/invalid_algorithm_id/relevancyscores/'
        response = self.APIClient.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
