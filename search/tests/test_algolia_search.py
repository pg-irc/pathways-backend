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

    # https://github.com/pg-irc/pathways-frontend/issues/1141 need a test that shows that giving the
    # city as part of the query gives the correct result and that leaving off the city gives the wrong result
    # Test with a query with lat/long in Surrey close to the surrey/new west border, with a search term that
    # includes "Surrey", and confirm that we get results that are all in Surrey. See also #919.

    def test_city_in_query(self):
        if self.is_disabled():
            print('Algolia tests not run, set environment variable ALGOLIA_SEARCH_API_KEY to enable')
            return
        surrey = '49.183333,-122.850000'
        data = {'query': 'Food', 'page': '1', 'hitsPerPage': '20',
                'aroundLatLng': surrey, 'aroundPrecision': ''}
        first_five_results = self.get_search_results(data, 5)
        service_ids = [result['service_id'] for result in first_five_results]
        self.assertIn('47982057', service_ids)

    # https://github.com/pg-irc/pathways-frontend/issues/1127 need a test to show that search with lat/long
    # returns a result and empty string for lat/long also returns a result

    # https://github.com/pg-irc/pathways-frontend/issues/971 need a test with a phrase like "english classes"
    # and compare it to the result with "english for all the classes" or something. Same with "settelment worker",
    # see #919

    # https://github.com/pg-irc/pathways-frontend/issues/919 test with search for "ICBC" should return results
    # with icbc in the service title. Tests covering all the different synonyms should go in here, "english classes"
    # to "language-english" taxonomy term

    # https://github.com/pg-irc/pathways-frontend/issues/916 is just about passing the correct oarameters to
    # Algolia, nothing for us to test.

    # https://github.com/pg-irc/pathways-frontend/issues/908 do a search and assert that the result contains
    # phone numbers

    # https://github.com/pg-irc/pathways-frontend/issues/680 Work in progress

    # https://github.com/pg-irc/pathways-frontend/issues/672 is not relevant, NLP problems

    # https://github.com/pg-irc/pathways-frontend/issues/610 Include test with search term "where to look for a job"
    # ensure that results are relevant

    # https://github.com/pg-irc/pathways-frontend/issues/608 Test for search term "Francophone Settlement Services"
    # ensure that the results are relevant

    # https://github.com/pg-irc/pathways-frontend/issues/591 Test with search for "Public Libraries" from
    # lat/long in surrey, assert that libraries in surrey show up
