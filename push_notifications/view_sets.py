from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from push_notifications import models, serializers
from rest_framework.decorators import api_view, action
from push_notifications.models import PushNotificationToken
from django.db.utils import DataError


@api_view(['PUT'])
def create_or_update_push_notification_token(request, *args, **kwargs):
    the_id = kwargs['theid']

    the_data = request.data.copy()
    the_data['id'] = the_id
    serializer = get_serializer(the_id, the_data)

    if not serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data)


def get_serializer(the_id, the_data):
    exists = PushNotificationToken.objects.filter(pk=the_id).exists()

    if not exists:
        return serializers.TokenSerializer(data=the_data)

    instance = PushNotificationToken.objects.get(pk=the_id)
    return serializers.TokenSerializer(instance, data=the_data)
