from .models import user #.models에서 user을 가져옴
import bcrypt # bcrypt import

def user_add(user_id,pw): 
    # user.objects -> 유저가 테이블이면, 테이블의 object들을 전부 불러옴. 만질 수 있는 객체를 불러옴.
    password, salt = hash_pw(pw) #pw을 해시 한번 해줌. 리턴값이 두개여서 두개 받게 해줌.
    user.objects.create(name=user_id, password= password, salt = salt)  #id, pw, salt각각
    return "success"

def user_all():
    result = user.objects.all()
    return result

def hash_pw(password):
    password = str(password).encode('utf-8') # 해시하기 전에 인코딩을 먼저 해야된다!!
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password, salt)
    return hash_password, salt