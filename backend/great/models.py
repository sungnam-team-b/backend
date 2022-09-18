# Create your models here.
from pyexpat import model
from django.db import models
#from user.models import user
import uuid 

class Great(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=200, null=True, blank=True)  #erd랑 다름
    description = models.CharField(max_length=200,default="")   #erd랑 다름
    great_url = models.CharField(max_length=200,default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['id']
        ordering = ['name']
        ordering = ['description']
        ordering = ['great_url']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.id+ ' ' + self.name+ ' ' +  self.description+ ' ' +  self.great_url+ ' ' +  self.created_at+ ' ' + self.updated_at

class Picture(models.Model):
    id = models.IntegerField(primary_key=True)
    picture_url = models.CharField(max_length=200,default="")
    #UUID = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    #results = models.ForeignKey(Result, on_delete=models.CASCADE, db_column='result_id', null=True)#1:N
    #user_id = models.ForeignKey( "user.user", on_delete=models.CASCADE, db_column='user_id', null=True)

    class Meta:
        ordering = ['id']
        ordering = ['similarity']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.id + ' ' +  self.similarity+ ' ' + self.created_at+ ' ' + self.updated_at

class Result(models.Model):
    id = models.IntegerField(primary_key=True)
    similarity =models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    great = models.OneToOneField(Great, on_delete=models.CASCADE)
    user_id = models.ForeignKey( "user.user", on_delete=models.CASCADE, db_column='user_id', null=True)
    picture_id = models.ForeignKey( Picture, on_delete=models.CASCADE, db_column='picture_id', null=True)
    #set user model foreignKey 
    #user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column='user_id')
    

    class Meta:
        ordering = ['id']
        ordering = ['similarity']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.id + ' ' + self.similarity + ' ' + self.created_at+ ' ' + self.updated_at




