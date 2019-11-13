import datetime
from test_plus.test import TestCase
from qa_tool.tests.helpers import RelevancyScoreBuilder, AlgorithmBuilder, SearchLocationBuilder
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from human_services.services_at_location.tests.helpers import ServiceAtLocationBuilder
from newcomers_guide.tests.helpers import create_topic
from common.testhelpers.random_test_values import an_integer, a_string


class GETRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.token = Token.objects.create(user=self.user)
        self.APIClient = APIClient()
        self.data = {
            'value': an_integer(),
            'algorithm': AlgorithmBuilder().create().id,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic(a_string()).id,
        }

    def test_can_get_one_entity_unauthenticated(self):
        score_value = an_integer()
        score = RelevancyScoreBuilder(self.user).with_value(score_value).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.APIClient.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['value'], score_value)

    def test_can_get_entities_unauthenticated(self):
        RelevancyScoreBuilder(self.user).create()
        RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_cannot_get_non_existent_entity_unauthenticated(self):
        url = '/qa/v1/relevancyscores/0/'
        response = self.APIClient.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DELETERelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.token = Token.objects.create(user=self.user)
        self.APIClient = APIClient()
        self.data = {
            'value': an_integer(),
            'algorithm': AlgorithmBuilder().create().id,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic(a_string()).id,
        }

    def test_can_delete(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.APIClient.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_unauthenticated(self):
        score = RelevancyScoreBuilder(self.user).create()
        url = '/qa/v1/relevancyscores/{0}/'.format(score.pk)
        response = self.APIClient.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_delete_non_existent_entity(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/0/'
        response = self.APIClient.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PUTRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.new_user = self.make_user(username='testuser2')
        self.token = Token.objects.create(user=self.user)
        self.APIClient = APIClient()
        self.sample_score = RelevancyScoreBuilder(self.user).create()
        self.data = {
            'value': an_integer(),
            'algorithm': AlgorithmBuilder().create().id,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic(a_string()).id,
        }

    def test_can_put_value(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_value = an_integer()
        self.data['value'] = new_value
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['value'], new_value)

    def test_can_put_algorithm(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_algorithm = AlgorithmBuilder().create()
        self.data['algorithm'] = new_algorithm.id
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['algorithm'], new_algorithm.id)

    def test_can_put_search_location(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_search_location = SearchLocationBuilder().create()
        self.data['search_location'] = new_search_location.id
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['search_location'], new_search_location.id)

    def test_can_put_service_at_location(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_service_at_location = ServiceAtLocationBuilder().create()
        self.data['service_at_location'] = new_service_at_location.id
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['service_at_location'], new_service_at_location.id)

    def test_can_put_topic(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_topic = create_topic(a_string())
        self.data['topic'] = new_topic.id
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['topic'], new_topic.id)

    def test_put_response_has_new_time_stamp(self):
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recreated_time = datetime.datetime.strptime(response.json()['time_stamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertLessEqual(recreated_time, datetime.datetime.now())
        self.assertGreaterEqual(recreated_time + datetime.timedelta(seconds=1), datetime.datetime.now())

    def test_can_put_with_different_credential(self):
        new_token = Token.objects.create(user=self.new_user)
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        new_value = an_integer()
        self.data['value'] = new_value
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['user'], self.new_user.id)
        self.assertEqual(response.json()['value'], new_value)

    def test_cannot_put_id(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        new_id = an_integer()
        self.data['id'] = new_id
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), 'id of relevancyscore is immutable')

    def test_cannot_put_user(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.data['user'] = self.new_user.id
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), 'user_id of relevancyscore is immutable')

    def test_cannot_put_unauthenticated(self):
        url = '/qa/v1/relevancyscores/{0}/'.format(self.sample_score.pk)
        self.data['value'] = an_integer()
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_put_non_existent_entity(self):
        url = '/qa/v1/relevancyscores/0/'
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.APIClient.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class POSTRelevancyScoreTests(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.token = Token.objects.create(user=self.user)
        self.APIClient = APIClient()
        self.score_value = an_integer()
        self.data_without_algorithm_in_body = {
            'value': self.score_value,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic('test').id,
        }
        self.data_with_algorithm_in_body = {
            'value': self.score_value,
            'algorithm': AlgorithmBuilder().create().id,
            'search_location': SearchLocationBuilder().create().id,
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic(a_string()).id,
        }

    def test_can_post_with_algorithm_in_body_not_in_url_short_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, data=self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['value'], self.score_value)

    def test_can_post_with_algorithm_in_url_not_in_body_long_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        algorithm = AlgorithmBuilder().create()
        url = '/qa/v1/algorithms/{0}/relevancyscores/'.format(algorithm.pk)
        response = self.APIClient.post(url, data=self.data_without_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['value'], self.score_value)

    def test_post_response_has_correct_algorithm(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['algorithm'], self.data_with_algorithm_in_body['algorithm'])

    def test_post_response_has_correct_search_location(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['search_location'], self.data_with_algorithm_in_body['search_location'])

    def test_post_response_has_correct_service_at_location(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['service_at_location'],
                         self.data_with_algorithm_in_body['service_at_location'])

    def test_post_response_has_correct_topic(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['topic'], self.data_with_algorithm_in_body['topic'])

    def test_post_response_has_correct_user(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['user'], self.user.id)

    def test_post_response_has_accurate_time_stamp(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recreated_time = datetime.datetime.strptime(response.json()['time_stamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertLessEqual(recreated_time, datetime.datetime.now())
        self.assertGreaterEqual(recreated_time + datetime.timedelta(seconds=1), datetime.datetime.now())

    def test_cannot_post_unauthenticated(self):
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, data=self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_post_with_invalid_algorithm_in_url_valid_algorithm_in_body_long_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/algorithms/0/relevancyscores/'
        response = self.APIClient.post(url, data=self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_post_without_algorithm_in_body_or_url_short_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, data=self.data_without_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_post_with_invalid_algorithm_in_url_missing_algorithm_in_body_long_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/qa/v1/algorithms/0/relevancyscores/'
        response = self.APIClient.post(url, data=self.data_without_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_post_with_algorithm_in_body_and_url_short_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        algorithm_id = self.data_with_algorithm_in_body['algorithm']
        url = '/qa/v1/relevancyscores/{0}/'.format(algorithm_id)
        response = self.APIClient.post(url, data=self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_post_with_algorithm_in_body_and_url_long_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        algorithm_id = self.data_with_algorithm_in_body['algorithm']
        url = '/qa/v1/algorithms/{0}/relevancyscores/'.format(algorithm_id)
        response = self.APIClient.post(url, data=self.data_with_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_post_with_algorithm_in_url_not_in_body_short_url(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        algorithm_id = AlgorithmBuilder().create().id
        url = '/qa/v1/relevancyscores/{0}/'.format(algorithm_id)
        response = self.APIClient.post(url, data=self.data_without_algorithm_in_body)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_post_when_missing_fields(self):
        self.APIClient.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        bad_data = {
            'value': an_integer(),
            'algorithm': AlgorithmBuilder().create().id,
            # 'search_location': missing search_location
            'service_at_location': ServiceAtLocationBuilder().create().id,
            'topic': create_topic(a_string()).id,
        }
        url = '/qa/v1/relevancyscores/'
        response = self.APIClient.post(url, bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
