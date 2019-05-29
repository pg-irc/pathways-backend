from rest_framework import serializers
from search import models


class RelatedTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TaskSimilarityScore
        fields = ('task_id', 'similarity_score', 'name', 'description')

    task_id = serializers.SerializerMethodField('related_task_id')
    name = serializers.SerializerMethodField('related_task_name')
    description = serializers.SerializerMethodField('related_task_description')

    def related_task_id(self, record):
        return record.second_task.id

    def related_task_name(self, record):
        return record.second_task.name

    def related_task_description(self, record):
        return record.second_task.description


class RelatedServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TaskServiceSimilarityScore
        fields = ('service_id', 'similarity_score', 'name', 'description')

    name = serializers.SerializerMethodField('related_service_name')
    description = serializers.SerializerMethodField('related_service_description')

    def related_service_name(self, record):
        return record.service.name

    def related_service_description(self, record):
        return record.service.description


class RelatedTopicsForGivenServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TaskServiceSimilarityScore
        fields = ('service_id', 'task_id', 'similarity_score')
