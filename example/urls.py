"""
URL configuration for example project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


api_urls = [
    path("accounts/", include("apps.accounts.urls.api_urls")),
]

# Preserve that fresh new Django project smell :D
if settings.DEBUG:
    from django.views.debug import default_urlconf

    default_view = default_urlconf
else:
    from django.views.generic import RedirectView

    default_view = RedirectView.as_view(url="v1/")

urlpatterns = [
    path("", default_view),
    path("admin/", admin.site.urls),
    path("v1/", include(api_urls)),
]

if settings.DEBUG:
    # Let Django serve up static files while in debug mode
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
