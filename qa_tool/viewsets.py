from rest_framework import viewsets
from qa_tool import models, serializers


class RelevancyScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.RelevancyScore.objects.all()
    serializer_class = serializers.RelevancyScoreSerializer


class AlgorithmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Algorithm.objects.all()
    serializer_class = serializers.AlgorithmSerializer


class SearchLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.SearchLocation.objects.all()
    serializer_class = serializers.SearchLocationSerializer
