from rest_framework import serializers
from search import models


class RelatedTaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.TaskSimilarityScore
        fields = ('id', 'first_task_id', 'second_task_id', 'similarity_score')
