from rest_framework import test as rest_test
from rest_framework import status
from common.testhelpers.random_test_values import a_string, a_float
from search.models import Task, TaskSimilarityScore


class TaskApiTests(rest_test.APITestCase):
    def setUp(self):
        self.first_task_id = a_string()
        self.second_task_id = a_string()
        self.second_task_name = a_string()
        self.first_task = Task(id=self.first_task_id, name=a_string(), description=a_string())
        self.first_task.save()
        self.second_task = Task(id=self.second_task_id, name=self.second_task_name, description=a_string())
        self.second_task.save()
        self.similarity_score = a_float()
        TaskSimilarityScore(first_task=self.first_task, second_task=self.second_task,
                            similarity_score=self.similarity_score).save()

    def test_can_get_related_tasks_to_a_given_task(self):
        url = '/v1/tasks/{}/related_tasks/'.format(self.first_task_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['first_task_id'], self.first_task_id)
        self.assertEqual(response.json()[0]['second_task_id'], self.second_task_id)
        self.assertAlmostEqual(response.json()[0]['similarity_score'], self.similarity_score)
