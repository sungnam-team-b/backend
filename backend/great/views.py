from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Great,Result
from .serializers import GreatlistResponse, MyPageResponse
from rest_framework.response import Response
from django.core.cache import cache

def greatview(request):
    return JsonResponse({"id" : "test"})

def list(request):
    greats = Great.objects.all()
    return JsonResponse({"greats" : "greats"})

#전체 great 조회 
@api_view(['GET'])
def get_greatlist(request):
    greatlist = Great.objects.all()
    serializer = GreatlistResponse(greatlist, many=True)
    return Response(serializer.data)

#마이페이지 
@api_view(['GET'])
def mypage(request,userId):
    print('userId:'+ str(userId) )
    resultByUser = Result.objects.filter(user=userId)
    serializer = MyPageResponse(resultByUser, many=True)
    return Response(serializer.data)
    # if cache.get("logindata"):
    #     logindata = cache.get("logindata")

    #     # access 토큰 확인?

    #     #userId에 해당하는 result 데이터 조회
    #     resultByUser = Result.objects.filter(userId=userId)
    #     serializer = MyPageResponse(resultByUser, many=True)
    #     return Response(serializer.data)

        
    # else:
    #     return JsonResponse({"message": "access denined"}, status=401)
    #     #로그인 데이터가 없다면
    #     #로그인 페이지로 이동하도록
    