from django.http import JsonResponse
from rest_framework.decorators import api_view
import jwt

from .userUtil import user_add, user_all

def test(request):
    return JsonResponse({"name" : "test"})

@api_view(['GET'])
def get_data(request):
    input_value = request.GET.get('input')
    return JsonResponse({"response":input_value})

@api_view(['POST'])
def post_data(request):
    input_value = request.data['input']
    return JsonResponse({"response":input_value})

def jwtfuc(request):
    token = jwt.encode(payload={},key='asdf123',algorithm='HS256').decode('utf-8')
    return JsonResponse({"jwt": token})


@api_view(['POST'])
def login(request):
    input_name = request.data['name']
    input_password = request.data['password']
    token = jwt.encode(payload={"name":input_name},key='asd123',algorithm='HS256').decode('utf-8')
    data = {"token" : token, "ID" : input_name}
    return JsonResponse({"data":data})

@api_view(['POST'])
def sign_up(request):
    user_id = request.data['id']
    pw = request.data['pw']
    result = user_add(user_id= user_id, pw = pw) # 얘를 나중에 묶어서 하나로 만들자!
    return JsonResponse({"response":result})

@api_view(['GET'])
def get_all_mem(request):
    respon = user_all().first() # 오브젝트의 꾸러미가 올때 제일 앞에만 가져온다!!
    result = {
        "name" : respon.name,
        "pw" : str(respon.password)
    }
    return JsonResponse(result)