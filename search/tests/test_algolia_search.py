from rest_framework import test as rest_test
import requests
import json
import os


class TopicApiTests(rest_test.APITestCase):

    def get_search_results(self, request_data, element_count):
        ALGOLIA_INDEX = 'dev_phones'
        ALGOLIA_SEARCH_API_KEY = os.environ.get('ALGOLIA_SEARCH_API_KEY')
        ALGOLIA_APPLICATION_ID = 'MMYH1Z0D3O'

        url = 'https://MMYH1Z0D3O-dsn.algolia.net/1/indexes/' + ALGOLIA_INDEX + '/query'
        headers = {
            'X-Algolia-API-Key': ALGOLIA_SEARCH_API_KEY,
            'Content-Type': 'application/json',
            'X-Algolia-Application-Id': ALGOLIA_APPLICATION_ID,
        }
        request_json = json.dumps(request_data)
        response = requests.post(url, headers=headers, data=request_json)
        content_json = response.content.decode('utf-8')
        content = json.loads(content_json)
        first_n_hits = content['hits'][0:element_count]
        return first_n_hits

    def is_disabled(self):
        return os.environ.get('ALGOLIA_SEARCH_API_KEY') is None

    def test_foo(self):
        if self.is_disabled():
            print('Algolia tests not run, set environment variable ALGOLIA_SEARCH_API_KEY to enable')
            return

        data = {'query': 'Food', 'page': '1', 'hitsPerPage': '20',
                'aroundLatLng': '', 'aroundPrecision': ''}
        first_five_results = self.get_search_results(data, 5)
        service_ids = [result['service_id'] for result in first_five_results]
        self.assertIn('47982057', service_ids)
