from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Great
from .serializers import GreatlistResponse
from rest_framework.response import Response

def greatview(request):
    return JsonResponse({"id" : "test"})

def list(request):
    greats = Great.objects.all()
    return JsonResponse({"greats" : "greats"})

@api_view(['GET'])
def get_greatlist(request):
    greatlist = Great.objects.all()
    serializer = GreatlistResponse(greatlist, many=True)
    return Response(serializer.data)