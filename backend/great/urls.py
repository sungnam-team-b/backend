from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.greatview), # 기본
    path('greatlist', views.get_greatlist), #great모든 목록 조회
    path('<userId>/mypage', views.mypage)
    #path('<uuid:userId>/mypage', views.mypage)
]
