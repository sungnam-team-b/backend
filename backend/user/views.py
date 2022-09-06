from django.http import JsonResponse
from rest_framework.decorators import api_view
import jwt

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import UserSignupResponse, AutoUpload

from .userUtil import user_add, user_all, user_create_client, user_find_alias, user_find_email, user_find_id,user_find_name

def test(request):
    return JsonResponse({"name" : "test"})

def jwtfuc(request):
    token = jwt.encode(payload={},key='asdf123',algorithm='HS256').decode('utf-8')
    return JsonResponse({"jwt": token})


@api_view(['POST']) #로그인 구현
def login(request):
    input_name = request.data['username']
    input_password = request.data['password']
    if input_name and input_password:
        user_data = user_find_name(input_name).first()
    token = jwt.encode(payload={"username":input_name},key='asd123',algorithm='HS256').decode('utf-8')
    data = {"token" : token, "your ID" : input_name}
    return JsonResponse({"data":data})

@api_view(['POST'])
def sign_up(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']
    alias = request.data['alias']

    new_user = user_create_client(username, email, password, alias)
    data = UserSignupResponse(new_user, many=False).data
    return Response(data, status=200)


@api_view(['GET'])
def get_all_mem(request):
    respon = user_all().first() # 오브젝트의 꾸러미가 올때 제일 앞에만 가져온다!!
    result = {
        "name" : respon.username,
        "pw" : str(respon.password)
    }
    return JsonResponse(result)
