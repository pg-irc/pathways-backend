from rest_framework import serializers
from push_notifications import models


class PushNotificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PushNotificationToken
        fields = '__all__'
