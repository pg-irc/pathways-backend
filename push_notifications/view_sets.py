from rest_framework import viewsets, status
from push_notifications import models, serializers
from rest_framework.response import Response


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PushNotificationToken.objects.all()
    serializer_class = serializers.TokenSerializer

    def create(self, request):
        serializer = serializers.TokenSerializer(data=request.data)

        new_id = request.data.copy()['id']
        already_exists = models.PushNotificationToken.objects.filter(id=new_id).exists()
        if already_exists:
            return Response([], status=status.HTTP_409_CONFLICT)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
