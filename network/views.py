from django.shortcuts import render
from django.views.generic import ListView
from .models import Haltestelle
from django.core.serializers import serialize
from django.db.models.expressions import RawSQL
from django.db import connection
import re

def haltestelle(request):
    Line1 = Haltestelle.objects.raw\
        ("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle WHERE hid LIKE '%%521%%'")
    Line2 = Haltestelle.objects.raw\
        ("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle WHERE hid LIKE '%%520%%'")
    Caseritz = Haltestelle.objects.raw\
        ("SELECT ST_X(location) as xvalue, ST_Y(location) as yvalue, name as info, hid as id FROM network_haltestelle WHERE hid LIKE '%%111%%'")


# Create your views here.
    context = {'Line1': Line1, 'Line2': Line2 , 'Caseritz': Caseritz}
    return render(request, 'index.html', context)
