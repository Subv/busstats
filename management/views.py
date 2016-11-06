import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as contrib_login, logout as contrib_logout
from django.utils import timezone

from .models import BusRoute, Bus, AccidentReport, RouteEndpoint
from busstats import settings


def index(request):
    return render(request, "index.html")
    

@login_required()
def dashboard(request):
    # Get the latest location ping of routes that are currently on the way
    routes = BusRoute.objects.filter(departure_time__lt=timezone.now(), 
                                     arrival_time__gt=timezone.now())
                                     
    pings = []
    for route in routes.all():
        if route.location_pings.count() > 0:
            pings.append({ "route": route, "ping": route.location_pings.latest("time") })

    today = datetime.datetime.today()
    today_routes = BusRoute.objects.filter(
        departure_time__year=today.year,
        departure_time__month=today.month,
        departure_time__day=today.day)

    today_routes_count = today_routes.count()

    most_used_bus = Bus.objects.annotate(count_routes=Count("routes")).order_by("-count_routes").first()

    accidents_today = AccidentReport.objects.filter(
        time__year=today.year,
        time__month=today.month,
        time__day=today.day)
    count_accidents = accidents_today.count()

    accidents_per_hour = count_accidents / (timezone.localtime(timezone.now()).hour + 1)

    count_passengers_travelling = routes.aggregate(count_passengers=Sum("passengers"))

    today_pending_routes = today_routes.filter(departure_time__gt=timezone.now())
    count_passengers_booked_today = today_pending_routes.aggregate(count_passengers=Sum("passengers"))

    endpoints = RouteEndpoint.objects.annotate(as_dest_count=Count("as_destination"),
                                               as_origin_count=Count("as_origin"))
    top_destinations = endpoints.order_by("-as_destination")[:5]
    top_origins = endpoints.order_by("-as_origin")[:5]

    context = {
        'user': request.user,
        'google_api_key': settings.GEOPOSITION_GOOGLE_MAPS_API_KEY,
        'route_pings': pings,
        'today_routes_count': today_routes_count,
        'most_used_bus': most_used_bus,
        'count_accidents': count_accidents,
        'accidents_per_hour': accidents_per_hour,
        'count_passengers': count_passengers_travelling["count_passengers"] or 0,
        'count_passengers_booked_today': count_passengers_booked_today["count_passengers"] or 0,
        'top_destinations': top_destinations,
        'top_origins': top_origins
    }
    return render(request, "gentelella/dashboard.html", context)
    

def login(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    context = {}
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active and hasattr(user, "client"):
            contrib_login(request, user)
            return redirect('dashboard')
        else:
            context = {'login_error': True}

    return render(request, "gentelella/login.html", context)

