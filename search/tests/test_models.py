from django.test import TestCase
from common.testhelpers.database import validate_save_and_reload
from common.testhelpers.random_test_values import a_string, a_float
from search.models import Task, TaskSimilarityScore, TaskServiceSimilarityScore
from human_services.services.tests.helpers import ServiceBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from search.tests.helpers import create_tasks


class TestTaskSimilarityScores(TestCase):
    def test_can_create_row(self):
        first_id = a_string()
        second_id = a_string()
        score = a_float()
        create_tasks([first_id, second_id])
        score_record = TaskSimilarityScore(first_task_id=first_id,
                                           second_task_id=second_id,
                                           similarity_score=score)
        score_record_from_db = validate_save_and_reload(score_record)

        self.assertEqual(score_record_from_db.first_task_id, first_id)
        self.assertEqual(score_record_from_db.second_task_id, second_id)
        self.assertAlmostEqual(score_record_from_db.similarity_score, score)


class TestTaskServiceSimilarityScores(TestCase):
    def test_can_create_row(self):
        organization = OrganizationBuilder().create()
        service = ServiceBuilder(organization).create()
        task_id = a_string()
        score = a_float()

        create_tasks([task_id])
        score_record = TaskServiceSimilarityScore(task_id=task_id,
                                                  service=service,
                                                  similarity_score=score)
        score_record_from_db = validate_save_and_reload(score_record)

        self.assertEqual(score_record_from_db.task_id, task_id)
        self.assertEqual(score_record_from_db.service_id, service.id)
        self.assertAlmostEqual(score_record_from_db.similarity_score, score)
