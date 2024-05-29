from django.urls import path
from . import views

urlpatterns = [
    path("", views.itemList, name="item_list"),
    path("make/", views.create_item, name="item_create"),
    path('make/<int:category_id>/', views.create_item, name='item_create_for_trade'),
    path("edit/<int:item_id>/", views.edit_item, name="item_edit"),
    path("delete/<int:item_id>/", views.delete_item, name="item_delete"),
    path("detail/<int:item_id>/", views.detail_item, name="item_detail"),
]
