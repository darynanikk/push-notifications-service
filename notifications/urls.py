from django.urls import path, include
from notifications.views import subscribe, send_push, home


urlpatterns = [
    path('', home),
    path('send_push', send_push),
    path('subscribe', subscribe),
]
