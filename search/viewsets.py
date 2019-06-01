from rest_framework import viewsets
from django.utils.decorators import method_decorator
from search import models, serializers, documentation


@method_decorator(name='list', decorator=documentation.get_related_topics_schema())
class RelatedTopicsViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return models.TaskSimilarityScore.objects.filter(first_task=topic_id).order_by('-similarity_score')

    serializer_class = serializers.RelatedTaskSerializer


@method_decorator(name='list', decorator=documentation.get_related_services_schema())
class RelatedServicesViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return models.TaskServiceSimilarityScore.objects.filter(task=topic_id).order_by('-similarity_score')

    serializer_class = serializers.RelatedServiceSerializer
