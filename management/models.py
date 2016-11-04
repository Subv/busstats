from __future__ import unicode_literals

from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField



class Company(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

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
    
    def __str__(self):
        return self.name


class RouteEndpoint(models.Model):
    name = models.CharField(max_length=255)
    position = GeopositionField()
    
    def __str__(self):
        return self.name


class BusRoute(models.Model):
    bus = models.ForeignKey(to=Bus)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    origin = models.ForeignKey(to=RouteEndpoint, related_name="as_origin")
    destination = models.ForeignKey(to=RouteEndpoint, related_name="as_destination")
    
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
        
    def __str__(self):
        return "%s - %s (%s)" % (self.origin, self.destination, self.departure_time)

    
class BusLocationPings(models.Model):
    position = GeopositionField()
    time = models.DateTimeField()
    route = models.ForeignKey(to=BusRoute, related_name="location_pings")
