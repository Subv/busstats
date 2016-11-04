from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.utils import timezone

from models import BusRoute
from busstats import settings


def index(request):
    return render(request, "index.html")
    

def dashboard(request):
    # Get the latest location ping of routes that are currently on the way
    routes = BusRoute.objects.filter(departure_time__lt=timezone.now(), 
                                     arrival_time__gt=timezone.now())
                                     
    pings = []
    print(routes.count())
    for route in routes.all():
        if route.location_pings.count() > 0:
            pings.append({ "route": route, "ping": route.location_pings.latest("time") })

    context = {
        'username': request.user.username,
        'google_api_key': settings.GEOPOSITION_GOOGLE_MAPS_API_KEY,
        'route_pings': pings
    }
    return render(request, "dashboard.html", context)
    

def login(request):
    context = {}
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            django_login(request, user)
            return redirect('dashboard')
        else:
            context = {'login_error': True}

    return render(request, "login.html", context)