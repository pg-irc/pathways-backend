from rest_framework import test as rest_test
from rest_framework import status
from services.tests.helpers import ServiceBuilder
from organizations.tests.helpers import OrganizationBuilder
from common.testhelpers.random_test_values import a_string

class ServicesApiTests(rest_test.APITestCase):
    def setUp(self):
        self.organization_id = a_string()
        self.organization = OrganizationBuilder().with_id(self.organization_id).build()
        self.organization.save()
        self.data = {
            'id': a_string(),
            'name': a_string(),
            'organization_id': self.organization_id,
            'description': a_string()
        }

    def test_can_get_services(self):
        ServiceBuilder(self.organization).with_id(a_string()).create()
        ServiceBuilder(self.organization).with_id(a_string()).create()
        url = '/v1/services/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_service(self):
        service_id = a_string()
        service = ServiceBuilder(self.organization).with_id(service_id).build()
        service.save()
        url = '/v1/services/{0}/'.format(service_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], service_id)

    def test_cannot_post(self):
        url = '/v1/services/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put(self):
        service = ServiceBuilder(self.organization).build()
        service.save()
        url = '/v1/services/{0}/'.format(service.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete(self):
        service = ServiceBuilder(self.organization).build()
        service.save()
        url = '/v1/services/{0}/'.format(service.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_get_services_for_organization(self):
        ServiceBuilder(self.organization).with_id(a_string()).create()
        ServiceBuilder(self.organization).with_id(a_string()).create()
        url = '/v1/organizations/{0}/services/'.format(self.organization_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_service_for_organization(self):
        description = a_string()
        service = ServiceBuilder(self.organization).with_description(description).build()
        service.save()
        url = '/v1/organizations/{0}/services/{1}/'.format(self.organization_id, service.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], description)

    def test_cannot_post_to_organization(self):
        url = '/v1/organizations/{0}/services/'.format(self.organization_id)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put_to_organization(self):
        service = ServiceBuilder(self.organization).build()
        service.save()
        url = '/v1/organizations/{0}/services/{1}/'.format(self.organization_id, service.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete_on_organization(self):
        service = ServiceBuilder(self.organization).build()
        service.save()
        url = '/v1/organizations/{0}/services/{1}/'.format(self.organization_id, service.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
