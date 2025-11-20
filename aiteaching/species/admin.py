from django.contrib import admin
from .models import Species


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['animal_name', 'status', 'trend', 'decline_rate', 'extinct_prob']
    list_filter = ['status', 'trend', 'fragmented']
    search_fields = ['animal_name', 'threats']
    ordering = ['animal_name']

