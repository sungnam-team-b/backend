from rest_framework import serializers
from .models import user

#Serializer는 요청한 값을 정제해서 보내주기 위해 사용합니다. 바로 user.username으로 사용 불가능! 
class UserSignupResponse(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['username']  # 프론트에주는 값


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['uuid_id', 'username', 'alias', 'password', 'email']
