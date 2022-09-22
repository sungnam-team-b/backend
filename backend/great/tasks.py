from __future__ import absolute_import,unicode_literals
from backend.celery import app
from django.http import JsonResponse
from .utils import get_ai_result

@app.task
def ai_task(request):
    r = get_ai_result(request)
    return r 
    