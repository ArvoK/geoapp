from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from .models import Haltestelle, routes
# Register your models here.
@admin.register(Haltestelle)

class NetworkAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')