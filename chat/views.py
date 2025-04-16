from django.http import JsonResponse
from chat.utils import get_available_conversations


def list_available_conversations(request):
    return JsonResponse({"conversations": get_available_conversations()})
