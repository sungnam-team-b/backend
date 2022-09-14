from django.contrib import admin
from .models import Great

@admin.register(Great)
class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'name','description','great_url']
