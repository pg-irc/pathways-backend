from rest_framework import serializers
from push_notifications import models


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PushNotificationToken
        fields = '__all__'
