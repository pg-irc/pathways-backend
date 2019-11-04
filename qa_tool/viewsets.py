from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from qa_tool import models, serializers
from django.utils import timezone


class RelevancyScoreViewSet(viewsets.ModelViewSet):
    queryset = models.RelevancyScore.objects.all()
    serializer_class = serializers.RelevancyScoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, algorithm_id=None, *args, **kwargs):
        rawdata = request.data.copy()
        if 'algorithm' not in rawdata and algorithm_id is not None:
            rawdata['algorithm'] = algorithm_id
        elif 'algorithm' not in rawdata and algorithm_id is None:
            return Response('Algorithm id missing in payload', status=status.HTTP_400_BAD_REQUEST)
        elif 'algorithm' in rawdata and algorithm_id is not None:
            return Response('Duplicate sources of algorithm id when there should only be 1', status=status.HTTP_400_BAD_REQUEST)
        rawdata['time_stamp'] = timezone.now()
        rawdata['user'] = request.user.id
        serializer = serializers.RelevancyScoreSerializer(data=rawdata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlgorithmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Algorithm.objects.all()
    serializer_class = serializers.AlgorithmSerializer


class SearchLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.SearchLocation.objects.all()
    serializer_class = serializers.SearchLocationSerializer
