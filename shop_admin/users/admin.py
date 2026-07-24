from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Country


admin.site.register(CustomUser,UserAdmin)
admin.site.register(Country)
