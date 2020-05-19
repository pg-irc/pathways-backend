from rest_framework import serializers
from content import models

class AlertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Alert
        fields = ('id', 'heading', 'content')
