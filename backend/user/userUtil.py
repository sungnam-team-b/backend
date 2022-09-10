from .models import user 
import jwt
import bcrypt
from backend.settings import ALGORITHM, JWT_SECRET_KEY
from datetime import datetime, timedelta

# password hashing
def user_hash_password(password):
    password = str(password).encode('utf-8') # 해시하기 전에 인코딩을 먼저 해야된다!!
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password, salt)
    return hash_password, salt

def user_find_id(user_id):
    return user.objects.filter(id=user_id)


def user_find_name(username):
    return user.objects.filter(username=username)


def user_find_alias(alias):
    return user.objects.filter(alias=alias)


def user_find_email(email):
    return user.objects.filter(email=email)

def create_user(username, email, password, alias):
    hash_password, salt = user_hash_password(password)
    return user.objects.create(username=username, alias=alias, password=hash_password, salt=salt, email=email)

def user_ispassword(password, user_data):
    password = str(password).encode('utf-8')
    hash_password = bcrypt.hashpw(password, user_data.salt)
    return hash_password == user_data.password

#tokens
def user_get_access_token(user_data):
    return jwt.encode(
        {'id': str(user_data.id), 'alias': user_data.alias, 'exp': datetime.utcnow() + timedelta(minutes=30),
         'type': 'access_token'},
        JWT_SECRET_KEY, ALGORITHM).decode('utf-8')


def user_get_refresh_token(user_data):
    return jwt.encode({'id': str(user_data.id), 'alias': user_data.alias, 'exp': datetime.utcnow() + timedelta(days=7),
                       'type': "refresh_token"},
                      JWT_SECRET_KEY, ALGORITHM).decode('utf-8')

                      class Auth(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', None)
        if token:
            return user_reissuance_access_token(request)
        else:
            return login(request)


def user_reissuance_access_token(request):
    token = request.headers.get('Authorization', None)
    payload = user_token_to_data(request.headers.get('Authorization', None))
    if payload:
        if payload.get('type') == 'refresh_token':
            access_token = user_refresh_to_access(token)
            return JsonResponse({"access_token": access_token}, status=200)  # new access_token 반환
        else:
            return JsonResponse({"message": "it is not refresh_token"}, status=401)
    else:
        return JsonResponse({"message": payload}, status=401)