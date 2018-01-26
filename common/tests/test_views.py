from rest_framework import test as rest_test
from organizations.tests.helpers import OrganizationBuilder
from services.tests.helpers import ServiceBuilder

class TestPagination(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()

    def create_many_services(self, count):
        for i in range(0, count):
            one_based_id = i + 1
            id_as_string = str(one_based_id)
            id_with_zero_prefix = ('00' + id_as_string)[-3:]
            ServiceBuilder(self.organization).with_id(id_with_zero_prefix).create()

    def test_link_header_elements_are_separated_by_comma(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=2')['Link']
        links = link_header.split(',')

        self.assertEqual(len(links), 4)

    def test_url_and_relation_are_separated_by_semicolon(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=2')['Link']
        one_link = link_header.split(',')[0]
        parts = one_link.split(';')

        self.assertEqual(len(parts), 2)
        self.assertIn('http', parts[0])
        self.assertIn('rel=', parts[1])

    def test_url_is_surrounded_by_angle_brackets(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=2')['Link']
        one_link = link_header.split(',')[0]
        link = one_link.split(';')[0]

        self.assertRegex(link.strip(), r'^<http.+>$')

    def test_relation_element_formatting(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=2')['Link']
        one_link = link_header.split(',')[0]
        relation = one_link.split(';')[1]

        self.assertRegex(relation.strip(), r'rel="\w+"')

    def test_includes_previous_link_in_link_header(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=2')['Link']

        self.assertIn('rel="prev"', link_header)

    def test_includes_no_previous_link_for_first_page(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2')['Link']

        self.assertNotIn('rel="prev"', link_header)

    def test_includes_next_link_in_link_header(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=2')['Link']

        self.assertIn('rel="next"', link_header)

    def test_includes_no_next_link_for_last_page(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=5')['Link']

        self.assertNotIn('rel="next"', link_header)

    def test_includes_first_link_in_link_header(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=3')['Link']

        self.assertIn('rel="first"', link_header)

    def test_includes_no_first_link_for_first_page(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2')['Link']

        self.assertNotIn('rel="first"', link_header)

    def test_includes_last_link_in_link_header(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=3')['Link']

        self.assertIn('rel="last"', link_header)

    def test_includes_no_last_link_for_last_page(self):
        self.create_many_services(10)

        link_header = self.client.get('/v1/services/?per_page=2&page=5')['Link']

        self.assertNotIn('rel="last"', link_header)

    def test_includes_no_Link_header_for_only_page(self):
        self.create_many_services(2)

        response = self.client.get('/v1/services/?per_page=2')

        self.assertNotContains(response, 'Link')

    def test_includes_total_element_count_in_link_header(self):
        self.create_many_services(10)

        response = self.client.get('/v1/services/?per_page=2&page=2')

        self.assertEqual(response['Count'], '10')
    def test_default_items_per_page_is_30(self):
        self.create_many_services(31)

        response = self.client.get('/v1/services/')

        self.assertEqual(len(response.json()), 30)

    def test_clamps_max_items_per_page_to_100(self):
        self.create_many_services(101)

        response = self.client.get('/v1/services/?per_page=101')

        self.assertEqual(len(response.json()), 100)

    def test_page_number_defaults_to_one(self):
        self.create_many_services(10)

        response = self.client.get('/v1/services/?per_page=3')

        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]['id'], '001')
        self.assertEqual(response.json()[1]['id'], '002')
        self.assertEqual(response.json()[2]['id'], '003')
