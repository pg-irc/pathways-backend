from rest_framework import serializers
from search import models


class RelatedTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TaskSimilarityScore
        fields = ('id', 'first_task_id', 'second_task_id', 'name', 'description', 'similarity_score')

    name = serializers.SerializerMethodField('related_task_name')
    description = serializers.SerializerMethodField('related_task_description')

    def related_task_name(self, record):
        return record.second_task.name

    def related_task_description(self, record):
        return record.second_task.description
