from rest_framework import viewsets
from django.utils.decorators import method_decorator
from search import models, serializers, documentation


@method_decorator(name='list', decorator=documentation.get_related_tasks_schema())
class RelatedTasksViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return models.TaskSimilarityScore.objects.filter(first_task=task_id).order_by('-similarity_score')

    serializer_class = serializers.RelatedTaskSerializer


@method_decorator(name='list', decorator=documentation.get_related_services_schema())
class RelatedServicesViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return models.TaskServiceSimilarityScore.objects.filter(task=task_id).order_by('-similarity_score')

    serializer_class = serializers.RelatedServiceSerializer
