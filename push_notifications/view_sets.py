from rest_framework import viewsets
from push_notifications import models
from rest_framework import serializers


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PushNotificationToken
        fields = '__all__'


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PushNotificationToken.objects.all()
    serializer_class = TokenSerializer
