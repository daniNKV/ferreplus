from django.urls import path, include
from . import views
from item.views import itemList

urlpatterns = [
    path("", include("allauth.urls")),
    path("", itemList, name="itemList"),
]
