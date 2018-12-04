from common.models import ValidateOnSaveMixin, RequiredCharField
from human_services.services.models import Service
from django.core import validators
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Task(ValidateOnSaveMixin, TranslatableModel):
    id = RequiredCharField(primary_key=True,
                           max_length=200,
                           validators=[validators.validate_slug])
    translations = TranslatedFields(
        name=models.CharField(blank=False, max_length=200),
        description=models.TextField(blank=True)
    )


class TaskSimilarityScore(ValidateOnSaveMixin, models.Model):
    first_task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name='first_task')
    second_task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name='second_task')
    similarity_score = models.FloatField()

    class Meta:
        unique_together = ('first_task', 'second_task')


class TaskServiceSimilarityScore(ValidateOnSaveMixin, models.Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    similarity_score = models.FloatField()

    class Meta:
        unique_together = ('task', 'service')
