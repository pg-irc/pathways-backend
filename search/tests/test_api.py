from rest_framework import status
from rest_framework import test as rest_test

from organizations.tests.helpers import OrganizationBuilder
from urllib.parse import urljoin

SEARCH_URL = '/v1/search/'

ORGANIZATION_ID_1 = 'test_organization_1'
ORGANIZATION_NAME_1 = 'the_name_1'

ORGANIZATION_ID_2 = 'test_organization_2'
ORGANIZATION_NAME_2 = 'the_name_2'

class SearchApiTests(rest_test.APITestCase):
    def setUp(self):
        organization1 = OrganizationBuilder().with_id(ORGANIZATION_ID_1).build()
        organization1.name = ORGANIZATION_NAME_1
        organization1.save()

        organization2 = OrganizationBuilder().with_id(ORGANIZATION_ID_2).build()
        organization2.name = ORGANIZATION_NAME_2
        organization2.save()

    def test_can_get(self):
        response = self.client.get(SEARCH_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_post(self):
        response = self.client.post(SEARCH_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_lists_types(self):
        response_json = self.client.get(SEARCH_URL).json()
        self.assertIn('organizations', response_json)
        self.assertIn('locations', response_json)
        self.assertIn('services', response_json)

    def test_get_lists_organizations(self):
        response_json = self.client.get(SEARCH_URL).json()
        self.assertEqual(len(response_json['organizations']), 2)
        self.assertEqual(response_json['organizations'][0]['name'], ORGANIZATION_NAME_1)
        self.assertEqual(response_json['organizations'][1]['name'], ORGANIZATION_NAME_2)

    def test_cannot_get_one_entity(self):
        url = urljoin(SEARCH_URL, ORGANIZATION_ID_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_put(self):
        url = urljoin(SEARCH_URL, ORGANIZATION_ID_1)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete(self):
        url = urljoin(SEARCH_URL, ORGANIZATION_ID_1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
