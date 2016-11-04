from django.contrib import admin
from models import BusLocationPings, BusRoute, RouteEndpoint


@admin.register(BusLocationPings)
class BusLocationPingsAdmin(admin.ModelAdmin):
    pass


@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
    pass


@admin.register(RouteEndpoint)
class RouteEndpointAdmin(admin.ModelAdmin):
    pass
