
from django.urls import path, include
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.Home.as_view(), name="home"),
]
