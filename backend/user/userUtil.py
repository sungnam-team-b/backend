from .models import user 
import bcrypt

def user_add(user_id,pw): 
    password, salt = hash_pw(pw)
    user.objects.create(name=user_id, password= password, salt = salt)
    return "success"

def user_all():
    result = user.objects.all()
    return result

def hash_pw(password):
    password = str(password).encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password, salt)
    return hash_password, salt

def user_find_id(user_id):
    return user.objects.filter(id=user_id)


def user_find_name(name):
    return user.objects.filter(name=name)


def user_find_alias(alias):
    return user.objects.filter(alias=alias)


def user_find_email(email):
    return user.objects.filter(email=email)