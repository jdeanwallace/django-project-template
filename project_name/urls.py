"""{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from apps.accounts import views as account_views


api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register('auth', account_views.AuthViewSet, base_name='auth')

api_urls = [
    path('v1/', include(api_router.urls)),
]

# Preserve that fresh new Django project smell :D
if settings.DEBUG:
    from django.views.debug import default_urlconf
    default_view = default_urlconf
else:
    from django.views.generic import RedirectView
    default_view = RedirectView.as_view(url='v1/')

urlpatterns = [
    path('', default_view),
    path('admin/', admin.site.urls),
] + api_urls
