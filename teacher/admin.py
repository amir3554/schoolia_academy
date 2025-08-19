from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherModelAdmin(admin.ModelAdmin):
    list_per_page = 10

