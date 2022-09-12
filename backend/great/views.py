from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import jwt
from .models import Great

def greatview(request):
    return JsonResponse({"id" : "test"})
# Create your views here.

# CRUD 
# https://woolbro.tistory.com/98

def list(request):
    greats = Great.objects.all()
    return JsonResponse({"greats" : "greats"})
    #return JsonResponse({"greats" : greats}) error 발생
    #return render(request, )
