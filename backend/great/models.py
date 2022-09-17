# Create your models here.
from pyexpat import model
from django.db import models
from user.models import user
import uuid 

class Great(models.Model):
    name = models.CharField(unique=True, max_length=30, null=True, blank=True)  #erd랑 다름
    description = models.CharField(max_length=200,default="")   #erd랑 다름
    great_url = models.CharField(max_length=200,default="")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'great'
        ordering = ['id']
        ordering = ['name']
        ordering = ['description']
        ordering = ['great_url']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.name+ ' ' +  self.description+ ' ' +  self.great_url+ ' ' +  self.created_at+ ' ' + self.updated_at

class Picture(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column = 'user_id')
    picture_url = models.CharField(max_length=200,default="")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'picture'
        ordering = ['id']
        ordering = ['user_id']
        ordering = ['picture_url']
        ordering = ['uuid']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.user_id+ ' ' + self.picture_url + ' ' +self.uuid + ' ' + self.created_at+ ' ' + self.updated_at


class Result(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column = 'user_id')
    great_id = models.ForeignKey(Great, on_delete=models.CASCADE, db_column ='great_id')
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE, db_column ='picture_id')
    similarity = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    

    class Meta:
        db_table = 'result'
        ordering = ['id']
        ordering = ['user_id']
        ordering = ['great_id']
        ordering = ['picture_id']
        ordering = ['similarity']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.user_id+ ' ' + self.great_id + ' ' + self.picture_id + ' ' + self.similarity + ' ' + self.created_at+ ' ' + self.updated_at
