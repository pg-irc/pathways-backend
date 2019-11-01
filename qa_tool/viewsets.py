from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from qa_tool import models, serializers
from django.utils import timezone


class RelevancyScoreViewSet(viewsets.ModelViewSet):
    queryset = models.RelevancyScore.objects.all()
    serializer_class = serializers.RelevancyScoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, algorithm_id=None, *args, **kwargs):
        rawdata = request.data.copy()
        if 'algorithm' not in rawdata:
            rawdata['algorithm'] = algorithm_id
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


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})
