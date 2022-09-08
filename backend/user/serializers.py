from rest_framework import serializers
from .models import user


class UserSignupResponse(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['username']  # 프론트에주는 값


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'username', 'alias', 'password', 'email']


class AutoUpload(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['autosave']

