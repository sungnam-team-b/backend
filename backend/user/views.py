from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import UserSignupResponse
from .userUtil import create_user, user_find_alias, user_find_email, user_find_id, user_find_name, user_ispassword, user_get_access_token, user_get_refresh_token

def test(request):
    return JsonResponse({"name" : "test"})


@api_view(['POST'])
def sign_up(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']
    alias = request.data['alias']

    new_user = create_user(username, email, password, alias)
    data = UserSignupResponse(new_user, many=False).data
    return JsonResponse(data, status=200)

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
                access_token = user_get_access_token(user_data)
                refresh_token = user_get_refresh_token(user_data)
            else: 
                return JsonResponse({"message": "wrong password"}, status=400)
        else:
            return JsonResponse({"message": "user not exist"}, status=400)

    data = {"access_token": access_token, "refresh_token": refresh_token}

    return JsonResponse(data, status=200)


class Auth(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', None)
        if token:
            return user_reaccess_token(request)
        else:
            return login(request)


def user_reaccess_token(request):
    token = request.headers.get('Authorization', None)
    payload = request.headers.get('Authorization')
    if payload:
        if payload.get('type') == 'refresh_token':
            access_token = token
            return JsonResponse({"access_token": access_token}, status=200)  # new access_token 반환
        else:
            return JsonResponse({"message": "it is not refresh_token"}, status=401)
    else:
        return JsonResponse({"message": payload}, status=401)