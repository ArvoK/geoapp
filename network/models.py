from django.contrib.gis.db import models

# Create your models here.
class Haltestelle(models.Model):
    hid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    location = models.GeometryField()
