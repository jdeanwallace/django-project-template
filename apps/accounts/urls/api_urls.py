from django.urls import path

from .. import views


app_name = 'accounts-api'
urlpatterns = [
    path('auth/token/', views.AuthTokenView.as_view(), name='auth-token'),
]
