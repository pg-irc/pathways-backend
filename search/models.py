from common.models import ValidateOnSaveMixin, RequiredCharField
from django.core import validators
from django.db import models


class TaskSimilarityScores(ValidateOnSaveMixin, models.Model):
    first_task_id = RequiredCharField(max_length=200, validators=[validators.validate_slug])
    second_task_id = RequiredCharField(max_length=200, validators=[validators.validate_slug])
    similarity_score = models.FloatField()

    class Meta:
        unique_together = ('first_task_id', 'second_task_id')
