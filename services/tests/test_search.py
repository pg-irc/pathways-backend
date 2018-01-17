from rest_framework import test as rest_test
from rest_framework import status
from services.tests.helpers import ServiceBuilder
from organizations.tests.helpers import OrganizationBuilder
from taxonomies.tests.helpers import TaxonomyTermBuilder
from common.testhelpers.random_test_values import a_string

class ServicesTaxonomicSearchTests(rest_test.APITestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().build()
        self.organization.save()

    def test_search_with_taxonomic_argument_returns_service(self):
        taxonomy_term = TaxonomyTermBuilder().build()
        taxonomy_term.save()
        service = ServiceBuilder(self.organization).with_taxonomy_terms([taxonomy_term]).build()
        service.save()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_term.taxonomy_id,
                                                           taxonomy_term.name)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], service.id)

    def test_search_with_wrong_taxonomic_argument_returns_404(self):
        taxonomy_term = TaxonomyTermBuilder().build()
        taxonomy_term.save()
        second_taxonomy_term = TaxonomyTermBuilder().build()
        second_taxonomy_term.save()
        ServiceBuilder(self.organization).with_taxonomy_terms([second_taxonomy_term]).build().save()

        url = '/v1/services/?taxonomy_term={0}:{1}'.format(taxonomy_term.taxonomy_id,
                                                           taxonomy_term.name)
        response = self.client.get(url)

        #TODO this should throw 404, need middleware for that
        self.assertEqual(len(response.json()), 0)

    def test_taxonomic_argument_with_wrong_separator_returns_400(self):
        url_with_plus_instead_of_colon = '/v1/services/?taxonomy_term=foo+bar'
        response = self.client.get(url_with_plus_instead_of_colon)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_taxonomic_argument_with_missing_taxonomy_id_returns_400(self):
        url_with_missing_taxonomy_id = '/v1/services/?taxonomy_term=:bar'
        response = self.client.get(url_with_missing_taxonomy_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_taxonomic_argument_with_missing_taxonomy_term_returns_400(self):
        url_with_missing_taxonomy_term = '/v1/services/?taxonomy_term=foo:'
        response = self.client.get(url_with_missing_taxonomy_term)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
