from pyexpat import model
from django.db import models
import uuid 

class Great(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=20, null=True, blank=True)  #erd랑 다름
    description = models.CharField(max_length=100,default="")   #erd랑 다름
    great_url = models.CharField(max_length=200,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        ordering = ['name']
        ordering = ['description']
        ordering = ['great_url']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.id,  self.name,  self.description,  self.great_url,  self.created_at, self.updated_at

class Picture(models.Model):
    id = models.IntegerField(primary_key=True)
    picture_url = models.CharField(max_length=200,default="")
    #UUID = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        ordering = ['similarity']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.id,  self.similarity, self.created_at, self.updated_at


class Result(models.Model):
    id = models.IntegerField(primary_key=True)
    similarity =models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    greats = models.ManyToManyField(Great)#다대다 with great
    picture = models.OneToOneField(Picture, on_delete=models.CASCADE) #일대일 with result


    class Meta:
        ordering = ['id']
        ordering = ['similarity']
        ordering = ['created_at']
        ordering = ['updated_at']

    def __str__(self):
        return self.id,  self.similarity, self.created_at, self.updated_at



# class great(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(unique=True, max_length=20, null=True, blank=True)
#     alias = models.CharField(unique=True, max_length=20)
#     # password = models.CharField(unique=True, max_length=20)
#     password = models.BinaryField(max_length=60)
#     salt = models.BinaryField(max_length=29)
#     email = models.CharField(max_length=50)
#     active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)