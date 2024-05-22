from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>/", views.profile_view, name="profile_view"),
    path("edit/<int:user_id>/", views.profile_edit, name="profile_edit"),
]
