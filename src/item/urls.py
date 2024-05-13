from django.urls import path, include
from . import views
from item import views

urlpatterns = [
    path("", include("allauth.urls")),
    path("", views.itemList, name="itemList"),
    path("subirArticulo/", views.createItem, name="createItem"),
    path("<int:item_id>/delete", views.deleteItem, name="deleteItem"),
]
