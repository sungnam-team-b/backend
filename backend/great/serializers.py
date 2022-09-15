from rest_framework import serializers
from .models import picture, great, result

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = picture
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = result
        fields = '__all__'

class GreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = great
        fields = '__all__'