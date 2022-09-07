from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('v1/api/admin/', admin.site.urls),
    path('v1/api/user/',include("user.urls"))
]
