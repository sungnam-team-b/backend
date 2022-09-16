from django.shortcuts import render
from django.http import JsonResponse
from .models import Great, Picture, Result
from user.models import user
from .serializers import GreatlistResponse

from backend.settings import AWS_STORAGE_BUCKET_NAME
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from .utils import s3_connection, get_ai_result, s3_get_image_url, s3_put_object
from .serializers import GreatlistResponse

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from pathlib import Path
from uuid import uuid4

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

@api_view(['POST'])
def airesult(request):
    #이미지 로컬에 저장
    picuuid = str(uuid4())
    file = request.FILES['filename']
    userid = request.data['user_id']
    fs = FileSystemStorage(location='media', base_url='media')
    filename = fs.save(picuuid+'.png', file)
    uploaded_file_url = fs.url(filename)
    #s3 버킷에 업로드
    s3 = s3_connection()
    retPut = s3_put_object(
        s3, AWS_STORAGE_BUCKET_NAME, '/app/media/' + str(picuuid) + '.png', 'image/' + str(picuuid) + '.png')
    retGet = s3_get_image_url(s3, 'image/' + str(picuuid) + '.png') #s3 이미지 url
    #db에 저장
    Picture.objects.create(id = id, user_id = userid, picture_url = retGet, uuid = picuuid )
    #모델에 사진 넣기
    result = get_ai_result(f'{picuuid}.png')
    print('##############')
    print(retGet)
    print(result)
    print('##############')

    return JsonResponse({'test':'succes'})

@api_view(['GET'])
def addmodel(request):
    user.objects.create(id =1,uuid=1,username='a',alias='a',password=1,salt =1)

    return JsonResponse({'test':'succes'})
