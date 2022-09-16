from django.urls import path, include
from . import views

# user/urls.py
urlpatterns = [
    path('', views.greatview), # 기본
    path('list', views.list), #greatlist
    path('greatlist', views.get_greatlist), #great모든 목록 조회
    path('ai',views.airesult),
    path('models',views.addmodel)
]
