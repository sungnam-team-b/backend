from django.urls import path, include
from . import views

# user/urls.py
urlpatterns = [
    path('', views.greatview), # 기본
    path('list', views.great_list), #greatlist
    path('greatlist', views.get_greatlist), #great모든 목록 조회
    # path('user/<user_id>',views.airesult),
    path('user',views.airesult),
    path('models',views.addmodel) #test용 user 모델 추가
]

