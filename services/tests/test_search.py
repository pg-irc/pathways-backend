from rest_framework import test as rest_test
from rest_framework import status
from services.tests.helpers import ServiceBuilder
from organizations.tests.helpers import OrganizationBuilder
from taxonomies.tests.helpers import TaxonomyTermBuilder
from common.testhelpers.autofixtures import a_string

class ServicesTaxonomicSearchTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().build()
        self.organization.save()

    def test_search_with_taxonomic_argument_returns_service(self):
        taxonomy_term = TaxonomyTermBuilder().build()
        taxonomy_term.save()

        service = ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).build()
        service_id = service.id
        service.save()

        taxonomy_id = taxonomy_term.taxonomy_id
        name = taxonomy_term.name
        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_id, name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], service_id)
