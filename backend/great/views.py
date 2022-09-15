from unittest import result
from django.db.models import Count
from django.http import JsonResponse
import uuid
from PIL import Image

from backend.backend.settings import AWS_STORAGE_BUCKET_NAME, IMAGE_URL

from .models import picture, great, result
from user.models import user
from .utils import s3_connection, s3_put_object, s3_get_image_url

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

# 여기에 serializer 씀
from .serializers import
#date 타임 객체 생성시 사용 
from datatime import datetime, timedelta 




@api_view(['GET'])
def upload_picture(request, user_id):
    s3 = s3_connection()
    try:
        file = request.FILES.getitem('file')
        user_id = request.GET.get('user_id')
        key = "%s" %(user_id)
        uuid = uuid.uuid4()
        file._set_name(str(uuid))
        s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object( Key=key+'/%s'%(file), Body=file, ContentType='jpg')
        Image.object.create(
            image_url = IMAGE_URL + "%s/%s"%(user_id, file),
            user_id = user_id
        )
        b = picture(user_id = user_id, uuid = uuid, picture_url = image_url)
        b.save()
        return JsonResponse({"MESSGE" : "SUCCESS"}, status=200)        

    except Exception as e:
        return JsonResponse({"ERROR" : e.massage})

# @api_view(['GET'])
# def get ai result(request, user_id):
#     file = request.FILES.getitem('')
    
