from django.contrib import admin
from .models import CustomUser,UserPreference
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserPreference)