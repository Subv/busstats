"""busstats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import logout_then_login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from management.views import index, dashboard, login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^login', login, name="login"),
    url(r'^logout/$', logout_then_login, name="logout"),
    url(r'^$', index)
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
