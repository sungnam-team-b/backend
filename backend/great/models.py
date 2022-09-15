from django.db import models
from user.models import user
import uuid


class picture(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column = 'user_id')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'picture'

class great(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'great'

class result(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column = 'user_id')
    picture_id = models.ForeignKey(picture, on_delete=models.CASCADE, db_colume ='picture_id')
    great_id = models.ForeignKey(great, on_delete=models.CASCADE, db_colume ='great_id')
    similarity = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'result'

