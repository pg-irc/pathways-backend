from rest_framework import test as rest_test
import requests
import json
import os


class TopicApiTests(rest_test.APITestCase):

    def get_search_results(self, data, element_count):
        ALGOLIA_INDEX = 'dev_phones'
        ALGOLIA_SEARCH_API_KEY = os.environ.get('ALGOLIA_SEARCH_API_KEY')
        ALGOLIA_APPLICATION_ID = 'MMYH1Z0D3O'
        url = 'https://MMYH1Z0D3O-dsn.algolia.net/1/indexes/' + ALGOLIA_INDEX + '/query'
        headers = {
            'X-Algolia-API-Key': ALGOLIA_SEARCH_API_KEY,
            'Content-Type': 'application/json',
            'X-Algolia-Application-Id': ALGOLIA_APPLICATION_ID,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        content_json = response.content.decode('utf-8')
        content = json.loads(content_json)
        elements = content['hits'][0:element_count]
        return elements

    def test_foo(self):
        data = {'query': 'Food', 'page': '1', 'hitsPerPage': '20',
                'aroundLatLng': '', 'aroundPrecision': ''}
        five_first_results = self.get_search_results(data, 5)
        elements = [element['service_id'] for element in five_first_results]
        self.assertIn('47982057', elements)
