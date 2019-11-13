from rest_framework import viewsets, status
from rest_framework.response import Response
from push_notifications import models, serializers
from rest_framework.decorators import api_view


@api_view(['PUT'])
def hello_world(request):
    return Response({"message": "Got some data!", "data": request.data})


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PushNotificationToken.objects.all()
    serializer_class = serializers.TokenSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return self.bad_request(serializer.errors)
        serializer.save()
        return self.success(serializer.data)

    def bad_request(self, errors):
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def success(self, data):
        return Response(data, status=status.HTTP_201_CREATED)
