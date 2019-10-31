from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
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


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})
