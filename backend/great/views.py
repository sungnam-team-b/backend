from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import jwt

def userview(request):
    return JsonResponse({"id" : "test"})
# Create your views here.
