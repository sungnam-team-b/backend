from django.urls import path, include
from . import views

# user/urls.py
urlpatterns = [
    path('', views.test),
    path('login',views.login),
    path('signup',views.sign_up),
    #09-18 merged
    #path('auth',views.Auth.as_view())
]
