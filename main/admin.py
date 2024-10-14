from django.contrib import admin
from .models import *


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'salary', 'type', 'date']