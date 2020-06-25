from rest_framework import test as rest_test
import requests
import json
import os


class TopicApiTests(rest_test.APITestCase):

    def get_search_results(self, request_data):
        ALGOLIA_INDEX = 'dev_match_city'
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
        return json.loads(content_json)

    def is_disabled(self):
        return os.environ.get('ALGOLIA_SEARCH_API_KEY') is None

    # https://github.com/pg-irc/pathways-frontend/issues/1141 need a test that shows that giving the
    # city as part of the query gives the correct result and that leaving off the city gives the wrong result
    # Test with a query with lat/long in Surrey close to the surrey/new west border, with a search term that
    # includes "Surrey", and confirm that we get results that are all in Surrey. See also #919.

    def test_search_with_city_name_in_query_returns_results_from_city(self):
        if self.is_disabled():
            print('Algolia tests not run, set environment variable ALGOLIA_SEARCH_API_KEY to enable')
            return
        surrey_geocoder = '49.183333,-122.850000'
        query_with_city_name = 'Food Surrey'
        data = {'query': query_with_city_name, 'page': '0', 'hitsPerPage': '20',
                'aroundLatLng': surrey_geocoder, 'aroundPrecision': '5000'}
        results = self.get_search_results(data)
        cities_from_results = [f['address']['city'] for f in results['hits']]
        number_of_results_in_surrey = sum(1 for c in cities_from_results if c == 'Surrey')
        fraction_in_surrey = number_of_results_in_surrey / len(cities_from_results)
        self.assertGreater(fraction_in_surrey, 0.8)

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
