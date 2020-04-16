from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from push_notifications.models import PushNotificationToken
from push_notifications.serializers import PushNotificationTokenSerializer
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    methods=['PUT'],
    request_body=PushNotificationTokenSerializer,
    responses={
        200: PushNotificationTokenSerializer(many=False),
        400: 'Bad request',
    },
    operation_description='Save a push notification token of form "ExponentPushToken[xyz]"')
@api_view(['PUT'])
def create_or_update_push_notification_token(request, *args, **kwargs):
    data = request.data.copy()
    data['id'] = kwargs['token']
    api_key = data.get('api_key', None)

    serializer = get_serializer_for_create_or_update(data)
    if not serializer.is_valid() or not is_api_key_valid(api_key):
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data)


def is_api_key_valid(key):
    return key == settings.PATHWAYS_API_KEY

def get_serializer_for_create_or_update(data):
    the_id = data['id']
    create = not PushNotificationToken.objects.filter(pk=the_id).exists()

    if create:
        return PushNotificationTokenSerializer(data=data)

    existing_instance = PushNotificationToken.objects.get(pk=the_id)
    return PushNotificationTokenSerializer(existing_instance, data=data)
