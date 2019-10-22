from rest_framework import test as rest_test
from rest_framework import status
from qa_tool.tests.helpers import SearchLocationBuilder


class SearchLocationsTests(rest_test.APITestCase):
    def setUp(self):
        self.data = {
            'id': 'The id',
            'name': 'The name',
            'point': '1 ,2 '
        }

    def test_can_get_entities(self):
        SearchLocationBuilder().with_name("wonderland").create()
        SearchLocationBuilder().with_name("playland").create()
        url = '/v1/searchlocations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_entity(self):
        searchlocation = SearchLocationBuilder().with_name('HiVE').build()
        searchlocation.save()
        url = '/v1/searchlocations/{0}/'.format(searchlocation.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'HiVE')

    def test_cannot_post(self):
        url = '/v1/searchlocations/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put(self):
        searchlocation = SearchLocationBuilder().build()
        searchlocation.save()
        url = '/v1/searchlocations/{0}/'.format(searchlocation.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete(self):
        searchlocation = SearchLocationBuilder().build()
        searchlocation.save()
        url = '/v1/searchlocations/{0}/'.format(searchlocation.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
