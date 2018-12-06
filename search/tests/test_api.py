from django.utils import translation
from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string, a_float
from search.models import Task, TaskSimilarityScore, TaskServiceSimilarityScore
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder


class RelatedTasksApiTests(rest_test.APITestCase):
    def setUp(self):
        translation.activate('en')
        self.first_task_id = a_string()

        self.second_task_id = a_string()
        self.second_task_name = a_string()
        self.second_task_description = a_string()

        self.first_task = Task(id=self.first_task_id, name=a_string(), description=a_string())
        self.first_task.save()

        self.second_task = Task(id=self.second_task_id, name=self.second_task_name,
                                description=self.second_task_description)
        self.second_task.save()

        self.similarity_score = a_float()
        TaskSimilarityScore(first_task=self.first_task, second_task=self.second_task,
                            similarity_score=self.similarity_score).save()

    def test_can_get_response(self):
        url = '/v1/tasks/{}/related_tasks/'.format(self.first_task_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_the_task_id(self):
        url = '/v1/tasks/{}/related_tasks/'.format(self.first_task_id)
        response = self.client.get(url)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['first_task_id'], self.first_task_id)

    def test_can_get_related_task_id(self):
        url = '/v1/tasks/{}/related_tasks/'.format(self.first_task_id)
        response = self.client.get(url)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['second_task_id'], self.second_task_id)

    def test_can_get_related_task_name(self):
        url = '/v1/tasks/{}/related_tasks/'.format(self.first_task_id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['name'], self.second_task_name)

    def test_can_get_related_task_description(self):
        url = '/v1/tasks/{}/related_tasks/'.format(self.first_task_id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['description'], self.second_task_description)

    def test_can_get_similarity_score(self):
        url = '/v1/tasks/{}/related_tasks/'.format(self.first_task_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.json()[0]['similarity_score'], self.similarity_score)

    def test_returns_tasks_ordered_by_score(self):
        the_task = Task(id=a_string(), name=a_string(), description=a_string())
        more_related_task = Task(id=a_string(), name=a_string(), description=a_string())
        less_related_task = Task(id=a_string(), name=a_string(), description=a_string())

        the_task.save()
        more_related_task.save()
        less_related_task.save()

        high_score = 0.9
        low_score = 0.1

        TaskSimilarityScore(first_task=the_task, second_task=more_related_task,
                            similarity_score=high_score).save()

        TaskSimilarityScore(first_task=the_task, second_task=less_related_task,
                            similarity_score=low_score).save()

        url = '/v1/tasks/{}/related_tasks/'.format(the_task.id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['second_task_id'], more_related_task.id)
        self.assertEqual(response.json()[1]['second_task_id'], less_related_task.id)


class RelatesServicesApiTests(rest_test.APITestCase):
    def setUp(self):
        translation.activate('en')
        self.task_id = a_string()

        self.task = Task(id=self.task_id, name=a_string(), description=a_string())
        self.task.save()

        organization = OrganizationBuilder().create()
        self.service = ServiceBuilder(organization).create()

        self.similarity_score = a_float()
        TaskServiceSimilarityScore(task=self.task, service=self.service,
                                   similarity_score=self.similarity_score).save()

    def test_can_get_response(self):
        url = '/v1/tasks/{}/related_services/'.format(self.task_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_can_get_task_id(self):
        url = '/v1/tasks/{}/related_services/'.format(self.task_id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['task_id'], self.task_id)

    def test_can_get_related_service_id(self):
        url = '/v1/tasks/{}/related_services/'.format(self.task_id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['service_id'], self.service.id)

    def test_can_get_related_service_name(self):
        url = '/v1/tasks/{}/related_services/'.format(self.task_id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['name'], self.service.name)

    def test_can_get_related_service_description(self):
        url = '/v1/tasks/{}/related_services/'.format(self.task_id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['description'], self.service.description)

    def test_can_get_related_service_similarity_score(self):
        url = '/v1/tasks/{}/related_services/'.format(self.task_id)
        response = self.client.get(url)
        self.assertEqual(response.json()[0]['similarity_score'], self.similarity_score)

    def test_returns_services_ordered_by_score(self):
        task_id = a_string()
        task = Task(id=task_id, name=a_string(), description=a_string())
        task.save()

        organization = OrganizationBuilder().create()
        more_related_service = ServiceBuilder(organization).create()
        less_related_service = ServiceBuilder(organization).create()

        higher_score = 0.9
        lower_score = 0.1
        TaskServiceSimilarityScore(task=task, service=more_related_service,
                                   similarity_score=higher_score).save()

        TaskServiceSimilarityScore(task=task, service=less_related_service,
                                   similarity_score=lower_score).save()

        url = '/v1/tasks/{}/related_services/'.format(task_id)
        response = self.client.get(url)

        self.assertEqual(response.json()[0]['service_id'], more_related_service.id)
        self.assertEqual(response.json()[1]['service_id'], less_related_service.id)
