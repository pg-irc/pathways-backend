from django.test import TestCase
from django.core.exceptions import SuspiciousOperation
from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string
from organizations.tests.helpers import OrganizationBuilder
from services.viewsets import SearchParameters
from services.tests.helpers import ServiceBuilder
from taxonomies.tests.helpers import TaxonomyTermBuilder

class SearchParametersTests(TestCase):
    def test_can_build_with_taxonomy_id(self):
        parameters = SearchParameters({'taxonomy_term' : 'foo:bar'})
        self.assertEqual(parameters.taxonomy_id, 'foo')

    def test_can_build_with_taxonomy_term(self):
        parameters = SearchParameters({'taxonomy_term' : 'foo:bar'})
        self.assertEqual(parameters.taxonomy_term, 'bar')

    def test_throws_on_too_many_field_separators(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : 'foo:bar:baz'})

    def test_throws_on_missing_field_separators(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : 'foobar'})

    def test_throws_on_missing_taxonomy_id(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : ':bar'})

    def test_throws_on_missing_taxonomy_term(self):
        with self.assertRaises(SuspiciousOperation):
            SearchParameters({'taxonomy_term' : 'foo:'})

class ServicesTaxonomicSearchTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()

    def test_taxonomy_search_returns_service(self):
        taxonomy_term = TaxonomyTermBuilder().create()
        service = ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).create()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_term.taxonomy_id,
                                                           taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], service.id)

    def test_taxonomy_search_with_wrong_taxonomy_id_returns_404(self):
        taxonomy_term = TaxonomyTermBuilder().create()
        wrong_taxonomy_term = TaxonomyTermBuilder().create()
        ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).create()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(wrong_taxonomy_term.taxonomy_id,
                                                           taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_taxonomy_search_with_wrong_taxonomy_term_returns_404(self):
        taxonomy_term = TaxonomyTermBuilder().create()
        wrong_taxonomy_term = TaxonomyTermBuilder().create()
        ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).create()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_term.taxonomy_id,
                                                           wrong_taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ServicesFullTextSearchTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()

    def test_full_text_search_returns_service_with_exact_match_on_name(self):
        the_name = a_string()
        service = ServiceBuilder(self.organization).with_name(the_name).create()

        url = '/v1/services/?queries={0}'.format(the_name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], the_name)

    def test_full_text_search_returns_service_with_substring_match_on_name(self):
        part_of_the_name = a_string()
        the_name = part_of_the_name + a_string()
        service = ServiceBuilder(self.organization).with_name(the_name).create()

        url = '/v1/services/?queries={0}'.format(part_of_the_name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], the_name)

    def test_full_text_search_is_case_insensitive(self):
        the_name = 'FooBar'
        the_search_term = 'foobar'
        service = ServiceBuilder(self.organization).with_name(the_name).create()

        url = '/v1/services/?queries={0}'.format(the_search_term)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], the_name)

    def test_full_text_search_returns_service_with_substring_match_to_description(self):
        part_of_the_description = a_string()
        the_description = part_of_the_description + a_string()
        service = ServiceBuilder(self.organization).with_description(the_description).create()

        url = '/v1/services/?queries={0}'.format(part_of_the_description)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['description'], the_description)

    def test_full_text_search_with_multiple_search_terms_returns_service_with_exact_match_on_name(self):
        the_name = a_string()
        service = ServiceBuilder(self.organization).with_name(the_name).create()

        url = '/v1/services/?queries={0}+{1}+{2}'.format(a_string(), the_name, a_string())
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], the_name)

    def test_full_text_search_with_wrong_search_term_returns_404(self):
        service = ServiceBuilder(self.organization).create()

        url = '/v1/services/?queries={0}'.format(a_string())
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
