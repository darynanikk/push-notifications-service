from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from notifications.seriailizers import SubscriptionSerializer, UserSubscriptionSerializer
from django.views.decorators.http import require_GET
from webpush.utils import send_to_subscription
from django.conf import settings
from notifications.models import UserSubscription
import json


@require_GET
def home(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    return render(request, 'home.html', {user: user, 'vapid_key': vapid_key})


@api_view(['POST'])
@csrf_exempt
def send_push(request):
    data = request.data

    if 'head' not in data or 'body' not in data or 'rule' not in data:
        return Response({"message": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

    rule = data['rule']

    payload = {'head': data['head'], 'body': data['body']}

    try:
        user_subscription = UserSubscription.objects.values_list('subscription', flat=True).get(rule=rule)
    except UserSubscription.DoesNotExist:
        return Response({"message": "Invalid data"}, status=status.HTTP_404_NOT_FOUND)
    serializer = SubscriptionSerializer(data=json.loads(user_subscription))
    if serializer.is_valid():
        subscription = serializer.save()
        send_to_subscription(subscription, json.dumps(payload))
        return Response({"message": "Web push successful"}, status=status.HTTP_200_OK)
    return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def subscribe(request):
    serializer = UserSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)