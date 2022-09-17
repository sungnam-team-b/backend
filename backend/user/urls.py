from django.urls import path, include
from . import views

# user/urls.py
urlpatterns = [
    path('', views.user),
    path('auth',views.Auth.as_view())
    # path('<str:userId>/mypage', views.mypage)
    #path('<uuid:userId>/mypage', views.mypage)
]
