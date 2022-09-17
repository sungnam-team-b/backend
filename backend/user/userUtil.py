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

class UserDuplicateCheck:
    @staticmethod
    def alias(alias):
        if user_find_alias(alias):
            return False
        return True

    @staticmethod
    def email(email):
        if user_find_email(email):
            return False
        return True

    @staticmethod
    def username(username):
        if user_find_name(username):
            return False
        return True

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

def user_token_to_data(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    except jwt.exceptions.ExpiredSignatureError: #토큰이 날짜가 만료되었을 때
        return "Expired_Token"
    except jwt.exceptions.DecodeError: # 토큰 디코딩 오류 생겼을 때
        return "Invalid_Token"
    return payload


def user_refresh_get_access(refresh_token):
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        access_token = jwt.encode(
            {'id': payload.get('id'), 'username': payload.get('username'), 'alias': payload.get('alias'),
             'email': payload.get('email'), 'type': "access_token",
             'exp': datetime.utcnow() + timedelta(minutes=5)}, JWT_SECRET_KEY, ALGORITHM).decode('utf-8')
    except jwt.exceptions.ExpiredSignatureError or jwt.exceptions.DecodeError:
        return False
    return access_token
    