from re import X
from django.shortcuts import render
from django.http import JsonResponse
from .models import Great, Picture, Result
from user.models import user

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


from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os, json
from pathlib import Path
from uuid import uuid4
from datetime import datetime
# from dateutil.relativedelta import *
from .tasks import ai_task
from celery.result import AsyncResult
from PIL import Image, ImageOps
import numpy as np

def greatview(request):
    return JsonResponse({"id" : "test"})

def great_list(request):
    greats = Great.objects.all()
    return JsonResponse({"greats" : "greats"})

#전체 great 조회 
@api_view(['GET'])
def get_greatlist(request):
    greatlist = Great.objects.all()
    serializer = GreatlistResponse(greatlist, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# def airesult(request):
#     #이미지 로컬에 저장
#     picuuid = str(uuid4())
#     file = request.FILES['filename']
#     useruuid = request.POST['user_id'] #uuid로 모델에서 값 조회하는걸로 변경
#     userquery = user.objects.filter(uuid = useruuid).values()
#     userid = (userquery[0])['id']
#     fs = FileSystemStorage(location='media', base_url='media')
#     filename = fs.save(picuuid+'.png', file)
#     uploaded_file_url = fs.url(filename)
#     #s3 버킷에 업로드
#     s3 = s3_connection()
#     retPut = s3_put_object(
#         s3, AWS_STORAGE_BUCKET_NAME, '/app/media/' + str(picuuid) + '.png', 'image/' + str(picuuid) + '.png')
#     retGet = s3_get_image_url(s3, 'image/' + str(picuuid) + '.png') #s3 이미지 url
#     #picture 정보 db에 저장
#     Picture.objects.create(user_id = user.objects.get(id=userid), picture_url = retGet, uuid = picuuid )
#     #모델에 사진 넣기
#     ##################################################################################################################
#     result = get_ai_result(f'{picuuid}.png')
#     keys = list(result.keys())
#     #picture_id 가져오기
#     pictureid = Picture.objects.filter(uuid = picuuid).values('id')
#     #ai 결과 db에 저장
#     result1 = keys[0] # 첫번쨰 key값
#     result2 = keys[1] # 두번째 key값
#     result3 = keys[2] # 세번째 key값
#     a = get_animal_num('abc')
#     print('#########')
#     print(int((pictureid[0])['id']))
#     print(a)
#     print('#########')
#     data_convert = {k:float(v) for k,v in result.items()}
    
#     ########
#     # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
#     #     great_id = Great.objects.get(id = ((get_animal_num(str(result1)))[0])['id']),\
#     #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
#     #             similarity = float(result[f'{str(result1)}']))
#     # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
#     #     great_id = Great.objects.get(id = ((get_animal_num(str(result2)))[0])['id']),\
#     #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
#     #             similarity = float(result[f'{str(result2)}']))
#     # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
#     #     great_id = Great.objects.get(id = ((get_animal_num(str(result3)))[0])['id']),\
#     #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
#     #             similarity = float(result[f'{str(result3)}']))
#     ################################
#     # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
#     #     great_id = Great.objects.get(id = 123),\
#     #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
#     #             similarity = float(result[f'{str(result1)}']))
#     ################################
#     Result.objects.create(user_id = user.objects.get(id = int(userid)),\
#         great_id = Great.objects.get(id = ((get_animal_num('abc'))[0])['id']),\
#             picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
#                 similarity = float(result[f'{str(result1)}']))            
#     Result.objects.create(user_id = user.objects.get(id = int(userid)),\
#         great_id = Great.objects.get(id = ((get_animal_num('BTS'))[0])['id']),\
#             picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
#                 similarity = float(result[f'{str(result2)}']))
#     Result.objects.create(user_id = user.objects.get(id = int(userid)),\
#         great_id = Great.objects.get(id = ((get_animal_num('name'))[0])['id']),\
#             picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
#                 similarity = float(result[f'{str(result3)}']))
#     returnresult = {}
#     returnresult['result'] = data_convert
#     returnresult['userimage'] = retGet
#     returnresult['animalimage'] = s3_get_image_url(s3, 'animal/' + str(result1) + '.png')
#     os.remove(f'/app/media/{picuuid}.png')
#     return JsonResponse(returnresult, status = 201)

@api_view(['POST'])
def get_task_id(request,user_id):
    picuuid = str(uuid4())
    file = request.FILES['filename']
    # useruuid = request.POST['user_id'] #uuid로 모델에서 값 조회하는걸로 변경
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
    # data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # image = Image.open(f'app/media/{filename}')
    print('##############')
    print(picuuid)
    print('##############')
    picuuid = str(picuuid)
    # image = Image.open(f'/app/media/{picuuid}.png').convert('RGB')
    # size = (224, 224)
    # image = ImageOps.fit(image, size, Image.ANTIALIAS)
    # image_array = np.asarray(image)
    # normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # data[0] = normalized_image_array
    image = Image.open(f'/app/media/{picuuid}.png').convert('RGB')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    img_instance = {'a':normalized_image_array}
    task = ai_task.delay(img_instance)
    returndata = {"task_id":task.id, "picuuid":picuuid}
    # task = ai_task.delay()
    return JsonResponse(returndata)

@api_view(['GET'])
def get_task_result(request, user_id, task_id):
    userid = user_id 
    task = AsyncResult(task_id)
    if not task.ready(): #작업이 완료되지 않았을 경우 
        return JsonResponse({'ai_result': 'notyet'})

    ai_results = task.get("ai_result")

    if ai_results['ai_result'] == 0:
        return JsonResponse({"ai_result": "false"})    

    keys = list((ai_results['ai_result']).keys())
    print('####################')
    print(keys)
    print(ai_results)
    print('####################')
    # picuuid = user.objects.get(uuid = user.objects.get(id=userid)).uuid
    picuuid = userid
    # pictureid = Picture.objects.filter(uuid = picuuid).values('id')
    ret_user_id = user.objects.filter(uuid = user_id ).values('id')
    pictureid = Picture.objects.filter(user_id = ret_user_id).values('id')
    #ai 결과 db에 저장
    result1 = keys[0] # 첫번쨰 key값
    result2 = keys[1] # 두번째 key값
    result3 = keys[2] # 세번째 key값
    a = get_animal_num('abc')
    print('#########')
    print(pictureid[0])
    print(result1)
    print(result2)
    print(result3)
    print('#########')
    data_convert = {k:float(v) for k,v in ai_results['ai_result'].items()}
    
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
    ################################
    # Result.objects.create(user_id = user.objects.get(id = int(userid)),\
    #     great_id = Great.objects.get(id = 123),\
    #         picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
    #             similarity = float(result[f'{str(result1)}']))
    ################################
    Result.objects.create(user_id = user.objects.get(id = int(userid)),\
        great_id = Great.objects.get(id = ((get_animal_num('abc'))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float(ai_results[f'{str(result1)}']))            
    Result.objects.create(user_id = user.objects.get(id = int(userid)),\
        great_id = Great.objects.get(id = ((get_animal_num('BTS'))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float(ai_results[f'{str(result2)}']))
    Result.objects.create(user_id = user.objects.get(id = int(userid)),\
        great_id = Great.objects.get(id = ((get_animal_num('name'))[0])['id']),\
            picture_id = Picture.objects.get(id = int((pictureid[0])['id'])),\
                similarity = float(ai_results[f'{str(result3)}']))
    s3 = s3_connection()
    retGet = s3_get_image_url(s3, 'image/' + str(picuuid) + '.png')
    returnresult = {}
    returnresult['result'] = data_convert
    returnresult['userimage'] = retGet
    returnresult['animalimage'] = s3_get_image_url(s3, 'animal/' + str(result1) + '.png')
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
    for i in range(0,10):
        alist.append(Great.objects.get(id = x[i][0]).name) #alias
        blist.append(user.objects.get(id = x[i][1]).alias) #animalname
        clist.append(x[i][2]) #similarity
    for i in range(10):
        returnrank[i] = {}
        returnrank[i]['alias'] = alist[i]
        returnrank[i]['name'] = blist[i]
        returnrank[i]['similarity'] = clist[i]
    print(returnrank)
    return JsonResponse(returnrank, status = 201)

@api_view(['GET'])
def addmodel(request):
    user.objects.create(id =1,uuid=1,username='a',alias='a',password=1,salt =1)
    Great.objects.create(name = 'name')

    return JsonResponse({'test':'succes'})


#마이페이지 
@api_view(['GET'])
def mypage(request, userId):
    
    if not Result.objects.filter(user_id=userId).exists():
        return JsonResponse({userId: 'PRODUCT_DOES_NOT_EXIST'}, status=404)
    

    resultByUser = Result.objects.select_related('picture_id').filter(user_id=user.objects.get(id=userId))
    #resultByUser = Result.objects.select_related('picture_id').filter(user_id=userId)
    
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
    


