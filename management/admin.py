from django.contrib import admin
from models import BusLocationPings

@admin.register(BusLocationPings)
class BusLocationPingsAdmin(admin.ModelAdmin):
    pass