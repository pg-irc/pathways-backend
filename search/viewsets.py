from rest_framework import viewsets
from search import models, serializers


# pylint: disable=too-many-ancestors
class RelatedTasksViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return models.TaskSimilarityScore.objects.filter(first_task=task_id).order_by('second_task__id')

    serializer_class = serializers.RelatedTaskSerializer
