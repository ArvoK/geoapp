from django.urls import path
from . import views

urlpatterns = [
    path('', views.getStops),
    path('Haltestellen/', views.getHaltestellen)
]