from django.db import models
import uuid

from great.models import Picture, Result 

class user(models.Model):
    uuid_id = models.UUIDField(unique=True,default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=20, null=True, blank=True)
    alias = models.CharField(unique=True, max_length=20, null=True)
    #09-18 merged
    #null-Ture
    password = models.BinaryField(max_length=60, null=True)
    salt = models.BinaryField(max_length=29, null=True)
    email = models.CharField(max_length=50, null=True)
    active = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Meta:
    db_table = 'member'
