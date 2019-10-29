from rest_framework import viewsets, permissions
from qa_tool import models, serializers


class RelevancyScoreViewSet(viewsets.ModelViewSet):
    queryset = models.RelevancyScore.objects.all()
    serializer_class = serializers.RelevancyScoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AlgorithmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Algorithm.objects.all()
    serializer_class = serializers.AlgorithmSerializer


class SearchLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.SearchLocation.objects.all()
    serializer_class = serializers.SearchLocationSerializer
