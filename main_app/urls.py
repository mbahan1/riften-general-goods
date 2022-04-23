
from django.urls import path, include
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.Home.as_view(), name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('product/<pk>/', views.Product_Detail.as_view(), name='product'),
    path('put-in-cart/<pk>/', views.put_in_cart, name='put-in-cart'),
    path('takeout-from-cart/<pk>/', views.takeout_from_cart, name='takeout-from-cart')
]
