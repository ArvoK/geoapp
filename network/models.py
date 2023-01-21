from django.contrib.gis.db import models

# Create your models here.
class Haltestelle(models.Model):
    hid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    location = models.GeometryField()

class networkgraph(models.Model):
    ogc_fid = models.IntegerField()
    towards = models.CharField(max_length=20)
    back = models.CharField(max_length=20)
    weight =models.CharField(max_length=20)

class routes(models.Model):
    routing_id = models.AutoField(primary_key=True)
    start = models.CharField(max_length=100)
    stop = models.CharField(max_length=100)
    last = models.DateTimeField(auto_now_add=True)