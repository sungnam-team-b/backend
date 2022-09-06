from .models import user 
import jwt
import bcrypt

def user_add(username,password): 
    password, salt = user_hash_password(password)
    user.objects.create(username=username, password= password, salt = salt)  #id, pw, salt각각
    return "success"

def user_all():
    result = user.objects.all()
    return result

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

def user_create_client(username, email, password, alias):
    hash_password, salt = user_hash_password(password)
    return user.objects.create(username=username, alias=alias, password=hash_password, salt=salt, email=email)