from django.http import JsonResponse
import jwt

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import UserSignupResponse, AutoUpload
from .userUtil import user_create_client, user_find_alias, user_find_email, user_find_id,user_find_name, user_ispassword

def test(request):
    return JsonResponse({"name" : "test"})

def jwtfuc(request):
    token = jwt.encode(payload={},key='asdf123',algorithm='HS256').decode('utf-8')
    return JsonResponse({"jwt": token})


@api_view(['POST'])
def sign_up(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']
    alias = request.data['alias']

    new_user = user_create_client(username, email, password, alias)
    data = UserSignupResponse(new_user, many=False).data
    return Response(data, status=200)

@api_view(['POST']) #로그인 구현
def login(request):
    input_name = request.data['username']
    input_password = request.data['password']
    access_token = None
    refresh_token = None

    if input_password and input_name: #코드에 if문이 세 개... 프론트랑 얘기해서 이건 프론트에서 처리하도록!
        user_data = user_find_name(input_name).first()
        if user_data:
            if user_ispassword(input_password, user_data):
                newdata = str(input_name)
            else: 
                return JsonResponse({"message": "wrong password"}, status=400)
        else:
            return JsonResponse({"message": "user not exist"}, status=400)

    data = {"message":newdata}

    return JsonResponse(data, status=200)