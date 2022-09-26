from django.urls import path, include
from . import views

urlpatterns = [
    path('animallist', views.get_greatlist), 
    path('user/<user_id>/mypage', views.mypage),
    path('user/<user_id>',views.get_task_id),
    path('user/<user_id>/tasks/<task_id>',views.get_task_result),
    path('rank',views.ranking)
]
