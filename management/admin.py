from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BusLocationPings, BusRoute, RouteEndpoint, Client, AccidentReport


@admin.register(BusLocationPings)
class BusLocationPingsAdmin(admin.ModelAdmin):
    pass


@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
    pass


@admin.register(RouteEndpoint)
class RouteEndpointAdmin(admin.ModelAdmin):
    pass


@admin.register(AccidentReport)
class AccidentReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'photo')}),
        (_('Company info'), {'fields': ('company',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'company', 'photo'),
        }),
    )

