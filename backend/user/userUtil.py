from .models import user 
import jwt
import bcrypt

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

def user_create_client(username, email, password, alias):
    hash_password, salt = user_hash_password(password)
    return user.objects.create(username=username, alias=alias, password=hash_password, salt=salt, email=email)

def user_ispassword(password, user_data):
    password = str(password).encode('utf-8')
    hash_password = bcrypt.hashpw(password, user_data.salt)
    return hash_password == user_data.password