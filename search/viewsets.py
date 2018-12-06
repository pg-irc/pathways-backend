from rest_framework import viewsets
from search import models, serializers


class RelatedTasksViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return models.TaskSimilarityScore.objects.filter(first_task=task_id).order_by('-similarity_score')

    serializer_class = serializers.RelatedTaskSerializer


class RelatedServicesViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return models.TaskServiceSimilarityScore.objects.filter(task=task_id).order_by('-similarity_score')

    serializer_class = serializers.RelatedServiceSerializer
