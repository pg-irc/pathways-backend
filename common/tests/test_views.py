from rest_framework import test as rest_test
from human_services.organizations.tests.helpers import OrganizationBuilder
from services.tests.helpers import ServiceBuilder
from common.testhelpers.random_test_values import an_integer

class TestPagination(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().create()

    def create_many_services(self, count):
        for i in range(0, count):
            one_based_id = i + 1
            id_as_string = str(one_based_id)
            id_with_zero_prefix = ('00' + id_as_string)[-3:]
            ServiceBuilder(self.organization).with_id(id_with_zero_prefix).create()

    def test_link_header_contains_links_to_pages(self):
        get_name_from_rel = lambda rel: rel.strip()[5:-1]
        strip_url = lambda url: url.strip()[1:-1]

        self.create_many_services(10)
        link_header = self.client.get('/v1/services/?per_page=2&page=3')['Link']

        links = link_header.split(',')
        urls_and_rels = [link.split(';') for link in links]
        link_map = {get_name_from_rel(rel): strip_url(url) for (url, rel) in urls_and_rels}

        self.assertNotRegex(link_map['first'], r'\bpage=')
        self.assertRegex(link_map['prev'], r'\bpage=2\b')
        self.assertRegex(link_map['next'], r'\bpage=4\b')
        self.assertRegex(link_map['last'], r'\bpage=5\b')

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

        self.assertRegex(relation.strip(), r'^rel="\w+"$')

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

    def test_can_specify_page_size(self):
        self.create_many_services(10)
        per_page = an_integer(min=1, max=10)

        response = self.client.get('/v1/services/?per_page={0}'.format(per_page))

        self.assertEqual(len(response.json()), per_page)

    def test_default_items_per_page_is_30(self):
        self.create_many_services(31)

        response = self.client.get('/v1/services/')

        self.assertEqual(len(response.json()), 30)

    def test_clamps_max_items_per_page_to_100(self):
        self.create_many_services(101)

        response = self.client.get('/v1/services/?per_page=101')

        self.assertEqual(len(response.json()), 100)

    def test_returns_records_from_the_specified_page(self):
        self.create_many_services(10)
        per_page = 2
        page_number = 4
        ids_on_the_fourth_page = ['007', '008']

        response = self.client.get('/v1/services/?per_page={0}&page={1}'.format(per_page, page_number))

        self.assertIn(response.json()[0]['id'], ids_on_the_fourth_page)
        self.assertIn(response.json()[1]['id'], ids_on_the_fourth_page)

    def test_by_default_returns_records_from_the_first_page(self):
        self.create_many_services(10)
        per_page = 2
        ids_on_the_first_page = ['001', '002']

        response = self.client.get('/v1/services/?per_page={0}'.format(per_page))

        self.assertIn(response.json()[0]['id'], ids_on_the_first_page)
        self.assertIn(response.json()[1]['id'], ids_on_the_first_page)

