from django.urls import path, include
from . import views

# user/urls.py
urlpatterns = [
    path('', views.greatview), # 기본
    path('list/', views.list), #greatlist
    path('greatslist', views.greatlist),
    path('task_status', views.task_status)
    #/api/v1/greats/greatslist
    #/api/v1/greats/task_status
]
