from django.utils.decorators import method_decorator
from rest_framework import viewsets
from content import models, serializers, documentation

# pylint: disable=too-many-ancestors
@method_decorator(name='list', decorator=documentation.get_alerts_list_schema())
class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.AlertSerializer

    def get_queryset(self):
        locale = self.kwargs['locale']
        return models.Alert.objects.language(locale).all()