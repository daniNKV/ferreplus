from django.urls import path, include
from . import views
from item.views import itemList
from item.views import createItem

urlpatterns = [
    path("", include("allauth.urls")),
    path("", itemList, name="itemList"),
    path("subirArticulo/", createItem, name="createItem"),
]
