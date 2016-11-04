from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField



class Company(models.Model):
    name = models.CharField(max_length=255)
    

class Client(User):
    company = models.ForeignKey(to=Company, on_delete=models.PROTECT)


class Bus(models.Model):
    identifier = models.CharField(max_length=50)
    capacity = models.IntegerField()
    chasis_number = models.CharField(max_length=255)


class DriverContract(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    contract_number = models.CharField(max_length=255)
    eps = models.CharField(max_length=255)


class Driver(models.Model):
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=50)
    age = models.IntegerField()
    contract_number = models.OneToOneField(to=DriverContract, on_delete=models.PROTECT)


class BusRoute(models.Model):
    bus = models.ForeignKey(to=Bus)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    origin = models.CharField(max_length=255)
    destiny = models.CharField(max_length=255)

    
class BusLocationPings(models.Model):
    position = GeopositionField()
    time = models.DateTimeField()
    route = models.ForeignKey(to=BusRoute, related_name="location_pings")
