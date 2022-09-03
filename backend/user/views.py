from django.http import JsonResponse
from rest_framework.decorators import api_view
import jwt

def test(request):
    return JsonResponse({"name" : "test"})