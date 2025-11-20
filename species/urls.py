from django.urls import path
from . import views

app_name = 'species'

urlpatterns = [
    path('', views.network_visualization, name='network_visualization'),
    path('predict/<int:species_id>/', views.predict_species, name='predict_species'),
]
