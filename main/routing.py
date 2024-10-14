from django.urls import path
from . import consumers  
websocket_urlpatterns = [
    path('ws/check-in/', consumers.CheckInConsumer.as_asgi()),
]