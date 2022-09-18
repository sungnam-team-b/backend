from django.contrib import admin
from .models import user

@admin.register(user)
class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'uuid', 'username', 'alias', 'password', 'salt', 'email','active']
