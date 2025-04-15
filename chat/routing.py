# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat/visitor/(?P<conversation_id>[^/]+)/$",
        consumers.VisitorConsumer.as_asgi(),
    ),
    re_path(
        r"ws/chat/agent/(?P<conversation_id>[^/]+)/$",
        consumers.AgentConsumer.as_asgi(),
    ),
]
