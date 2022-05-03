
from django.urls import path, include
from . import views
from django.views.generic import RedirectView

# app_name = 'main_app'

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.Home.as_view(), name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('inventory/', views.Product_List.as_view(), name="inventory"),
    path('product/<pk>/', views.Product_Detail.as_view(), name='product_detail'),
    path('put-in-cart/<pk>/', views.put_in_cart, name='put-in-cart'),
    path('takeout-from-cart/<pk>/', views.takeout_from_cart, name='takeout-from-cart'),
    # path('bag/', views.OrderItem_List.as_view(), name="bag"),
    path('subtract-item/<pk>/', views.subtract_item, name='subtract-item'),
    path('add-item/<pk>/', views.add_item, name='add-item'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('cart/', views.OrderSummaryView.as_view(), name="cart"),
    path('pickup', views.Pickup.as_view(), name='pickup'),
    path('inventory/Armor', views.Armor_List.as_view(), name="armor-list"),
    path('inventory/Books', views.Book_List.as_view(), name="books-list"),
    path('inventory/Food', views.Food_List.as_view(), name="food-list"),
    path('inventory/Jewelery', views.Jewelery_List.as_view(), name="jewelery-list"),
    path('inventory/Potions', views.Potions_List.as_view(), name="potions-list"),
    path('inventory/Weapons', views.Weapons_List.as_view(), name="weapons-list"),
]
