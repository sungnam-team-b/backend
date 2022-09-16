from django.db import models
import uuid 

class user(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=200, null=True, blank=True)
    alias = models.CharField(unique=True, max_length=200)
    password = models.BinaryField(max_length=60)
    salt = models.BinaryField(max_length=30)
    email = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Meta:
    db_table = 'member'
