from django.urls import path
from game import consumers

websocket_urlpatterns = [
    path("ws/game1/", consumers.Game1.as_asgi()),
]
