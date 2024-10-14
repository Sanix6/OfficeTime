from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'phone', 'first_name', 'last_name', 'user']
    list_display_links = ['id', 'phone', 'first_name', 'last_name']
    ordering = ['-id']
    fieldsets = (
        ('Основаная информация', {'fields': ('user', 'phone',  'summ', 'logo',  'first_name','last_name')}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Активация', {'fields': ('is_active', 'code')}))
