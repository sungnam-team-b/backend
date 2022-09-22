from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.greatview), # 기본
    path('animallist', views.get_greatlist), 
    path('<user_uuid>/mypage', views.mypage),
    #path('<uuid:userId>/mypage', views.mypage)
    # path('user/<user_id>',views.airesult),
    # path('user',views.airesult),
    path('user/<user_id>',views.get_task_id),
    path('user/<user_id>/tasks/<task_id>',views.get_task_result),
    path('models',views.addmodel), #test용 user 모델 추가
    path('<int:userId>/mypage', views.mypage),
    path('rank',views.ranking)
]
