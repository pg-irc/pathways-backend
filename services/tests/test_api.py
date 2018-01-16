from rest_framework import test as rest_test
from rest_framework import status
from services.tests.helpers import ServiceBuilder
from organizations.tests.helpers import OrganizationBuilder

class ServicesApiTests(rest_test.APITestCase):
    def setUp(self):
        self.organization_id = 'the_organization_id'
        self.organization = OrganizationBuilder().with_id(self.organization_id).build()
        self.organization.save()
        self.data = {
            'id': 'the_service_id',
            'name': 'the name',
            'organization_id': self.organization_id,
            'description': 'the description'
        }

    def test_can_get_services(self):
        ServiceBuilder(self.organization).with_id('First').build().save()
        ServiceBuilder(self.organization).with_id('Second').build().save()
        url = '/v1/services/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_service(self):
        service_id = 'the_service_id'
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
        ServiceBuilder(self.organization).with_id('First').build().save()
        ServiceBuilder(self.organization).with_id('Second').build().save()
        url = '/v1/organizations/{0}/services/'.format(self.organization_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_service_for_organization(self):
        service = ServiceBuilder(self.organization).with_description('The description').build()
        service.save()
        url = '/v1/organizations/{0}/services/{1}/'.format(self.organization_id, service.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], 'The description')

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
