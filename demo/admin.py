from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'math_performance', 'reading_writing_performance', 'eligible_for_support']
    list_filter = ['eligible_for_support']
    search_fields = ['name']

