from django.urls import path, include
from . import views

# great/urls.py
urlpatterns = [
    path('/api/v1/greats/analysis/<user_id>', views.upload_picture)
]
