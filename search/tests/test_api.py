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

    def test_can_get_multiple_responses(self):

        first_task_id = a_string()
        second_task_id = a_string()
        third_task_id = a_string()

        first_task = Task(id=first_task_id, name=a_string(), description=a_string())
        second_task = Task(id=second_task_id, name=a_string(), description=a_string())
        third_task = Task(id=third_task_id, name=a_string(), description=a_string())

        first_task.save()
        second_task.save()
        third_task.save()

        TaskSimilarityScore(first_task=first_task, second_task=second_task,
                            similarity_score=a_float()).save()
        TaskSimilarityScore(first_task=first_task, second_task=third_task,
                            similarity_score=a_float()).save()

        url = '/v1/tasks/{}/related_tasks/'.format(first_task_id)
        response = self.client.get(url)
        self.assertEqual(len(response.json()), 2)


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
