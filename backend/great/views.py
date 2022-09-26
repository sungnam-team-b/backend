from django.shortcuts import render
from django.http import JsonResponse
from .models import Great, Picture, Result
from user.models import user
from user.serializers import UUIDSerializer

from backend.settings import AWS_STORAGE_BUCKET_NAME
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from .utils import s3_connection, get_ai_result, s3_get_image_url, s3_put_object, get_animal_num
from .serializers import GreatlistResponse

from rest_framework import status, viewsets
from .serializers import GreatlistResponse, MyPageResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from user.userUtil import user_token_to_data

# redis 
import time
import logging
from django.core.cache import cache


import os, json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from dateutil.relativedelta import *
from .tasks import ai_task
from celery.result import AsyncResult
from PIL import Image, ImageOps
import numpy as np


logger = logging.getLogger(__name__)

def greatview(request):
    return JsonResponse({"id" : "test"})

#전체 great 조회 
@api_view(['GET'])
def get_greatlist(request):
    greatlist = cache.get_or_set('Great', Great.objects.all())
    #greatlist = Great.objects.all()
    serializer = GreatlistResponse(greatlist, many=True)
    logger.debug("********************************걸린 시간:")
    return Response(serializer.data)

@api_view(['POST'])
def get_task_id(request,user_id):
    picuuid = str(uuid4())
    file = request.FILES['filename']
    userquery = user.objects.filter(uuid = user_id).values()
    userid = (userquery[0])['id']
    fs = FileSystemStorage(location='media', base_url='media')
    filename = fs.save(picuuid+'.png', file)
    uploaded_file_url = fs.url(filename)
    #s3 버킷에 업로드
    s3 = s3_connection()
    retPut = s3_put_object(
        s3, AWS_STORAGE_BUCKET_NAME, '/app/media/' + str(picuuid) + '.png', 'image/' + str(picuuid) + '.png')
    retGet = s3_get_image_url(s3, 'image/' + str(picuuid) + '.png') #s3 이미지 url
    #picture 정보 db에 저장
    Picture.objects.create(user_id = user.objects.get(id=userid), picture_url = retGet, uuid = picuuid )
    task = ai_task.delay(filename)
    returndata = {"task_id":task.id, "picuuid":picuuid}
    # task = ai_task.delay()
    return JsonResponse(returndata)

@api_view(['POST'])
def get_task_result(request, user_id, task_id):
    userid = user_id 
    task = AsyncResult(task_id)
    if not task.ready(): #작업이 완료되지 않았을 경우 
        return JsonResponse({'ai_result': 'notyet'})
    ai_results = task.get("ai_result")
    if ai_results['ai_result'] == 0:
        return JsonResponse({"ai_result": "false"})    
    keys = list((ai_results['ai_result']).keys())
    picuuid = request.POST['picuuid']
    ret_user_id = user.objects.filter(uuid = user_id ).values('id')
    pictureid = Picture.objects.filter(uuid = picuuid).values('id')
    #ai 결과 db에 저장
    result1 = keys[0] # 첫번쨰 key값
    result2 = keys[1] # 두번째 key값
    result3 = keys[2] # 세번째 key값
    data_convert = {k:float(v) for k,v in ai_results['ai_result'].items()}
    print(float((ai_results['ai_result'])[f'{result3}']))    

    Result.objects.create(user_id = user.objects.get(id = (ret_user_id[0])['id']),\
        great_id = Great.objects.get(id = ((get_animal_num(result1))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float((ai_results['ai_result'])[f'{result1}']))            
    Result.objects.create(user_id = user.objects.get(id = (ret_user_id[0])['id']),\
        great_id = Great.objects.get(id = ((get_animal_num(result2))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float((ai_results['ai_result'])[f'{result2}']))
    Result.objects.create(user_id = user.objects.get(id = (ret_user_id[0])['id']),\
        great_id = Great.objects.get(id = ((get_animal_num(result3))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float((ai_results['ai_result'])[f'{result3}']))

    s3 = s3_connection()
    retGet = s3_get_image_url(s3, 'image/' + str(picuuid) + '.png')
    returnresult = {}
    returnresult['result'] = data_convert
    returnresult['userimage'] = retGet
    returnresult['animalimage'] = s3_get_image_url(s3, 'animal/' + str(result1) + '.png')
    print(returnresult)
    os.remove(f'/app/media/{picuuid}.png')

    return JsonResponse(returnresult, status = 201)
    

@api_view(['Get'])
def ranking(request):
    alist = []
    blist = []
    clist = []
    returnrank = {}
    today = datetime.today()
    start_date = datetime(today.year, today.month, 1)
    end_date = start_date + relativedelta(months = 1)
    x = Result.objects.filter(created_at__range=(start_date, end_date)).order_by('-similarity')\
        .values_list('great_id','user_id','similarity')
    x = list(x[0:10])
    a = Great.objects.get(id = x[0][0]).name
    for i in range(0,len(x)):
        alist.append(Great.objects.get(id = x[i][0]).name) #alias
        blist.append(user.objects.get(id = x[i][1]).alias) #animalname
        clist.append(x[i][2]) #similarity
    for i in range(len(x)):
        returnrank[i] = {}
        returnrank[i]['alias'] = blist[i]
        returnrank[i]['name'] = alist[i]
        returnrank[i]['similarity'] = clist[i]
        returnrank[i]['rank'] = i
    print(returnrank)
    return JsonResponse(returnrank, status = 201)


#마이페이지 
@api_view(['GET'])
def mypage(request, user_id):
    userId = user.objects.get(uuid = user_id).id
    payload = user_token_to_data(request.headers.get('Authorization', None))
    if (payload.get('id') == str(userId)):
        if not Result.objects.filter(user_id=userId).exists():
            return JsonResponse({userId: 'PRODUCT_DOES_NOT_EXIST'}, status=404)
        
        resultByUser = Result.objects.all().filter(user_id=userId)
        #resultByUser = Result.objects.select_related('picture_id').select_related('great_id').filter(user_id=user.objects.get(id=userId))
        #resultByUser = Result.objects.select_related('picture_id').filter(user_id=userId)
        serializer = MyPageResponse(resultByUser, many=True)
        return Response(serializer.data)
    else:
        return JsonResponse({"message": "Token Error"}, status=401)
    
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
    

