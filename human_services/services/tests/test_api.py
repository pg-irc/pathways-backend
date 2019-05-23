from common.testhelpers.random_test_values import a_string, a_float
from human_services.services.tests.helpers import ServiceBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from newcomers_guide.tests.helpers import create_tasks
from rest_framework import test as rest_test
from rest_framework import status
from search.models import TaskServiceSimilarityScore

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
        ServiceBuilder(self.organization).create()
        ServiceBuilder(self.organization).create()
        url = '/v1/services/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_service(self):
        service = ServiceBuilder(self.organization).create()
        url = '/v1/services/{0}/'.format(service.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], service.id)

    def test_cannot_post(self):
        url = '/v1/services/'
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put(self):
        service = ServiceBuilder(self.organization).create()
        url = '/v1/services/{0}/'.format(service.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete(self):
        service = ServiceBuilder(self.organization).create()
        url = '/v1/services/{0}/'.format(service.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_get_services_for_organization(self):
        ServiceBuilder(self.organization).create()
        ServiceBuilder(self.organization).create()
        url = '/v1/organizations/{0}/services/'.format(self.organization_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_can_get_one_service_for_organization(self):
        service = ServiceBuilder(self.organization).create()
        url = '/v1/organizations/{0}/services/{1}/'.format(self.organization_id, service.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], service.description)

    def test_cannot_post_to_organization(self):
        url = '/v1/organizations/{0}/services/'.format(self.organization_id)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_put_to_organization(self):
        service = ServiceBuilder(self.organization).create()
        url = '/v1/organizations/{0}/services/{1}/'.format(self.organization_id, service.pk)
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete_on_organization(self):
        service = ServiceBuilder(self.organization).create()
        url = '/v1/organizations/{0}/services/{1}/'.format(self.organization_id, service.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_get_topics_for_service(self):
        service_id = a_string()
        task_id = a_string()

        ServiceBuilder(self.organization).with_id(service_id).create()
        create_tasks([task_id])
        TaskServiceSimilarityScore.objects.create(
            task_id=task_id,
            service_id=service_id,
            similarity_score=a_float()
        )

        url = '/v1/services/{0}/related_topics/'.format(service_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_response_contains_attributes(self):
        service_id = a_string()
        task_id = a_string()

        ServiceBuilder(self.organization).with_id(service_id).create()
        create_tasks([task_id])

        similarity_score = a_float()
        TaskServiceSimilarityScore.objects.create(
            task_id=task_id,
            service_id=service_id,
            similarity_score=similarity_score
        )

        url = '/v1/services/{0}/related_topics/'.format(service_id)
        response = self.client.get(url)

        self.assertEqual(response.json()[0]['service_id'], service_id)
        self.assertEqual(response.json()[0]['task_id'], task_id)
        self.assertEqual(response.json()[0]['similarity_score'], similarity_score)
