from django.shortcuts import render
from django.http import JsonResponse
from .models import Great, Picture, Result
from user.models import user
from .serializers import GreatlistResponse

from backend.settings import AWS_STORAGE_BUCKET_NAME
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from .utils import s3_connection, get_ai_result, s3_get_image_url, s3_put_object, get_animal_num
from .serializers import GreatlistResponse

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os, json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from dateutil.relativedelta import *

def greatview(request):
    return JsonResponse({"id" : "test"})

def great_list(request):
    greats = Great.objects.all()
    return JsonResponse({"greats" : "greats"})

@api_view(['GET'])
def get_greatlist(request):
    greatlist = Great.objects.all()
    serializer = GreatlistResponse(greatlist, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def airesult(request):
    #이미지 로컬에 저장
    picuuid = str(uuid4())
    file = request.FILES['filename']
    useruuid = request.POST['user_id'] #uuid로 모델에서 값 조회하는걸로 변경
    userquery = user.objects.filter(uuid = useruuid).values()
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
    #모델에 사진 넣기
    result = get_ai_result(f'{picuuid}.png')
    keys = list(result.keys())
    #picture_id 가져오기
    pictureid = Picture.objects.filter(uuid = picuuid).values('id')
    #ai 결과 db에 저장
    result1 = keys[0] # 첫번쨰 key값
    result2 = keys[1] # 두번째 key값
    result3 = keys[2] # 세번째 key값
    a = get_animal_num('abc')
    print('#########')
    print(int((pictureid[0])['id']))
    print(a)
    print('#########')
    data_convert = {k:float(v) for k,v in result.items()}
    
    ########
    # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
    #     great_id = Great.objects.get(id = ((get_animal_num(str(result1)))[0])['id']),\
    #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
    #             similarity = float(result[f'{str(result1)}']))
    # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
    #     great_id = Great.objects.get(id = ((get_animal_num(str(result2)))[0])['id']),\
    #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
    #             similarity = float(result[f'{str(result2)}']))
    # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
    #     great_id = Great.objects.get(id = ((get_animal_num(str(result3)))[0])['id']),\
    #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
    #             similarity = float(result[f'{str(result3)}']))
    ########
    Result.objects.create(user_id = user.objects.get(id = int(userid)),\
        great_id = Great.objects.get(id = ((get_animal_num('abc'))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float(result[f'{str(result1)}']))
    Result.objects.create(user_id = user.objects.get(id = int(userid)),\
        great_id = Great.objects.get(id = ((get_animal_num('BTS'))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float(result[f'{str(result2)}']))
    Result.objects.create(user_id = user.objects.get(id = int(userid)),\
        great_id = Great.objects.get(id = ((get_animal_num('name'))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float(result[f'{str(result3)}']))
    returnresult = {}
    returnresult['result'] = data_convert
    returnresult['userimage'] = retGet
    returnresult['animalimage'] = s3_get_image_url(s3, 'animal/' + str(result1) + '.png')

    return JsonResponse(returnresult)


@api_view(['GET'])
def addmodel(request):
    user.objects.create(id =1,uuid=1,username='a',alias='a',password=1,salt =1)
    Great.objects.create(name = 'name')

    return JsonResponse({'test':'succes'})
