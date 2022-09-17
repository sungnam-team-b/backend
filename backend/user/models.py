from django.db import models
import uuid 

class user(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=20, null=True, blank=True)
    alias = models.CharField(unique=True, max_length=20)
    password = models.BinaryField(max_length=60)
    salt = models.BinaryField(max_length=29)
    email = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class Meta:
    db_table = 'member'
