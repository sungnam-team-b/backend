from dataclasses import fields
from rest_framework import serializers
from .models import Great, Picture,Result

#Serializer는 요청한 값을 정제해서 보내주기 위해 사용합니다. 바로 user.username으로 사용 불가능! 
class GreatlistResponse(serializers.ModelSerializer):
    class Meta:
        model = Great
        fields = ['id', 'name','description','great_url']  # 프론트에주는 값



class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model =Picture
        fields =['id','picture_url','user_id']



class MyPageResponse(serializers.ModelSerializer):
    picture_id=PictureSerializer() #출처: https://www.hides.kr/846 [Hide:티스토리]
    class Meta:
        model = Result
        fields = ['id', 'similarity','picture_id']  