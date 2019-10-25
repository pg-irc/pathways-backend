from rest_framework import serializers
from qa_tool import models


class AlgorithmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Algorithm
        fields = ('id', 'url', 'name', 'notes')


class SearchLocationSerializer(serializers.HyperlinkedModelSerializer):
    latitude = serializers.ReadOnlyField(source='point.y')
    longitude = serializers.ReadOnlyField(source='point.x')

    class Meta:
        model = models.SearchLocation
        fields = ('id', 'name', 'latitude', 'longitude')


class RelevancyScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RelevancyScore
        fields = ('id', 'value', 'time_stamp', 'algorithm',
                  'search_location', 'user', 'service_at_location', 'topic')
