from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name="home"),
    path('all_items/', views.all_items, name='all_items')
]
