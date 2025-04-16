from django.urls import path
from . import views

urlpatterns = [path("chat/available/", views.list_available_conversations)]
