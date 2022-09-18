from unittest import result
from rest_framework import serializers
from .models import Great

#Serializer는 요청한 값을 정제해서 보내주기 위해 사용합니다. 바로 user.username으로 사용 불가능! 
class GreatlistResponse(serializers.ModelSerializer):
    class Meta:
        model = Great
        fields = ['id', 'name','description','great_url']  # 프론트에주는 값

# class RanklistSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = result
#         fields = 