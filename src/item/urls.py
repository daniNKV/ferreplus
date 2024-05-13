from django.urls import path, include
from . import views
from item import views

urlpatterns = [
    path("", include("allauth.urls")),
    path("", views.itemList, name="itemList"),
    path("subirArticulo/", views.createItem, name="createItem"),
    path("<int:item_id>/delete", views.deleteItem, name="deleteItem"),
    path("<int:item_id>/detail", views.item_detail, name="item_detail"),
]
