from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name="home"),
    path('search/', views.all_items, name='all_items'),
    path('products/', views.all_products, name='all_products'),
]
