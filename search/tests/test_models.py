from django.test import TestCase
from common.testhelpers.database import validate_save_and_reload
from common.testhelpers.random_test_values import a_string, a_float
from search.models import TaskSimilarityScores


class TestTaskSimilarityScores(TestCase):
    def test_can_create_row(self):
        first_id = a_string()
        second_id = a_string()
        score = a_float()

        score = TaskSimilarityScores(first_task_id=first_id,
                                     second_task_id=second_id,
                                     similarity_score=score)
        score_from_db = validate_save_and_reload(score)

        self.assertEqual(score_from_db.first_task_id, first_id)
        self.assertEqual(score_from_db.second_task_id, second_id)
        self.assertEqual(score_from_db.similarity_score, score)
