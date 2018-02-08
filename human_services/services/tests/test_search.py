from django.test import TestCase
from django.core.exceptions import SuspiciousOperation
from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.viewsets import SearchParameters
from human_services.services.tests.helpers import ServiceBuilder
from human_services.taxonomies.tests.helpers import TaxonomyTermBuilder

class SearchParametersTests(TestCase):
    def test_can_build_with_taxonomy_id(self):
        parameters = SearchParameters({'taxonomy_term' : 'foo:bar'})
        self.assertEqual(parameters.taxonomy_id, 'foo')

    def test_can_build_with_taxonomy_term(self):
        parameters = SearchParameters({'taxonomy_term' : 'foo:bar'})
        self.assertEqual(parameters.taxonomy_term, 'bar')

    def test_taxonomy_parameter_is_optional(self):
        parameters = SearchParameters({})
        self.assertIsNone(parameters.taxonomy_id)
        self.assertIsNone(parameters.taxonomy_term)

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

    def test_can_build_full_text_search_term(self):
        parameters = SearchParameters({'search' : 'foo'})
        self.assertCountEqual(parameters.full_text_search_terms, ['foo'])

    def test_full_text_search_term_is_optional(self):
        parameters = SearchParameters({})
        self.assertIsNone(parameters.full_text_search_terms)

    # Django replaces + characters with space in URL parameter argument
    def test_full_text_search_terms_are_split_on_space(self):
        parameters = SearchParameters({'search' : 'foo bar'})
        self.assertCountEqual(parameters.full_text_search_terms, ['foo', 'bar'])

    def test_full_text_search_terms_are_stripped_of_white_space(self):
        parameters = SearchParameters({'search' : '  foo   bar  '})
        self.assertCountEqual(parameters.full_text_search_terms, ['foo', 'bar'])

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

    def test_taxonomy_search_with_wrong_taxonomy_id_returns_empty_array(self):
        taxonomy_term = TaxonomyTermBuilder().create()
        wrong_taxonomy_term = TaxonomyTermBuilder().create()
        ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).create()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(wrong_taxonomy_term.taxonomy_id,
                                                           taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_taxonomy_search_with_wrong_taxonomy_term_returns_empty_array(self):
        taxonomy_term = TaxonomyTermBuilder().create()
        wrong_taxonomy_term = TaxonomyTermBuilder().create()
        ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).create()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_term.taxonomy_id,
                                                           wrong_taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

class ServicesFullTextSearchTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()

    def test_full_text_search_returns_service_with_exact_match_on_name(self):
        the_name = a_string()
        service = ServiceBuilder(self.organization).with_name(the_name).create()

        url = '/v1/services/?search={0}'.format(the_name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], the_name)

    def test_full_text_search_returns_service_with_substring_match_on_name(self):
        part_of_the_name = a_string()
        the_name = part_of_the_name + a_string()
        service = ServiceBuilder(self.organization).with_name(the_name).create()

        url = '/v1/services/?search={0}'.format(part_of_the_name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], the_name)

    def test_full_text_search_is_case_insensitive(self):
        the_name = 'FooBar'
        the_search_term = 'foobar'
        service = ServiceBuilder(self.organization).with_name(the_name).create()

        url = '/v1/services/?search={0}'.format(the_search_term)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], the_name)

    def test_full_text_search_returns_service_with_substring_match_to_description(self):
        part_of_the_description = a_string()
        the_description = part_of_the_description + a_string()
        service = ServiceBuilder(self.organization).with_description(the_description).create()

        url = '/v1/services/?search={0}'.format(part_of_the_description)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['description'], the_description)

    def test_full_text_search_with_two_search_terms_implies_logical_and(self):
        first_name = a_string()
        second_name = a_string()
        combined_name = first_name + second_name
        ServiceBuilder(self.organization).with_name(first_name).create()
        ServiceBuilder(self.organization).with_name(second_name).create()
        ServiceBuilder(self.organization).with_name(combined_name).create()

        url = '/v1/services/?search={0}+{1}'.format(first_name, second_name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], combined_name)

    def test_full_text_search_with_no_match_returns_empty_array(self):
        service = ServiceBuilder(self.organization).create()

        url = '/v1/services/?search={0}'.format(a_string())
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_full_text_search_ignores_empty_search_term(self):
        ServiceBuilder(self.organization).create()

        url = '/v1/services/?search={0}+{1}+{2}'.format('', a_string(), a_string())
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_can_combine_taxonomic_search_and_full_text_search(self):
        the_search_term = a_string()
        the_taxonomy_term = TaxonomyTermBuilder().create()

        a_service = (ServiceBuilder(self.organization).
                                                with_name(the_search_term + a_string()).
                                                with_taxonomy_terms([the_taxonomy_term]).
                                                create())
        ServiceBuilder(self.organization).with_taxonomy_terms([the_taxonomy_term]).create()
        ServiceBuilder(self.organization).with_name(the_search_term + a_string()).create()

        url = '/v1/services/?search={0}&taxonomy_term={1}:{2}'.format(the_search_term,
                                                                       the_taxonomy_term.taxonomy_id,
                                                                       the_taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], a_service.name)

class ServicesSearchSorting(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()

    def create_many_services(self, count):
        for i in range(0, count):
            one_based_id = i + 1
            id_as_string = str(one_based_id)
            id_with_zero_prefix = ('00' + id_as_string)[-3:]
            ServiceBuilder(self.organization).with_id(id_with_zero_prefix).create()

    def test_can_order_by_field(self):
        self.create_many_services(3)

        response = self.client.get('/v1/services/?sort_by=id')

        json = response.json()
        self.assertLess(json[0]['id'], json[1]['id'])
        self.assertLess(json[1]['id'], json[2]['id'])

    def test_can_order_by_translated_field(self):
        self.create_many_services(3)

        response = self.client.get('/v1/services/?sort_by=name')

        json = response.json()
        self.assertLess(json[0]['name'], json[1]['name'])
        self.assertLess(json[1]['name'], json[2]['name'])

    def test_can_reverse_ordering(self):
        self.create_many_services(3)

        response = self.client.get('/v1/services/?sort_by=-id')

        json = response.json()
        self.assertGreater(json[0]['id'], json[1]['id'])
        self.assertGreater(json[1]['id'], json[2]['id'])

    def test_can_reverse_ordering_on_translated_field(self):
        self.create_many_services(3)

        response = self.client.get('/v1/services/?sort_by=-name')

        json = response.json()
        self.assertGreater(json[0]['name'], json[1]['name'])
        self.assertGreater(json[1]['name'], json[2]['name'])

    def test_can_order_by_two_fields(self):
        ServiceBuilder(self.organization).with_description('bbb').create()
        ServiceBuilder(self.organization).with_description('bbb').create()
        ServiceBuilder(self.organization).with_description('bbb').create()

        ServiceBuilder(self.organization).with_description('ccc').create()
        ServiceBuilder(self.organization).with_description('aaa').create()

        url = '/v1/services/?sort_by=description+name'
        response = self.client.get(url)

        first, second, third, fourth, fifth = response.json()

        self.assertLess(first['description'], second['description'])
        self.assertEqual(second['description'], third['description'])
        self.assertEqual(third['description'], fourth['description'])
        self.assertLess(fourth['description'], fifth['description'])

        self.assertLess(second['name'], third['name'])
        self.assertLess(third['name'], fourth['name'])

    def test_can_reverse_order_by_one_of_two_fields(self):
        ServiceBuilder(self.organization).with_description('bbb').create()
        ServiceBuilder(self.organization).with_description('bbb').create()
        ServiceBuilder(self.organization).with_description('bbb').create()

        ServiceBuilder(self.organization).with_description('ccc').create()
        ServiceBuilder(self.organization).with_description('aaa').create()

        response = self.client.get('/v1/services/?sort_by=description+-name')

        first, second, third, fourth, fifth = response.json()

        self.assertLess(first['description'], second['description'])
        self.assertEqual(second['description'], third['description'])
        self.assertEqual(third['description'], fourth['description'])
        self.assertLess(fourth['description'], fifth['description'])

        self.assertGreater(second['name'], third['name'])
        self.assertGreater(third['name'], fourth['name'])

    def test_can_specify_page_size(self):
        self.create_many_services(6)
        response = self.client.get('/v1/services/?per_page=3')
        self.assertEqual(len(response.json()), 3)

    def test_can_specify_page_size_and_page_number(self):
        self.create_many_services(10)

        url = '/v1/services/?per_page=2&page=3'
        response = self.client.get(url)

        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['id'], '005')
        self.assertEqual(response.json()[1]['id'], '006')
