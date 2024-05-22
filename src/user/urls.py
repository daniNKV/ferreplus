from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("allauth.urls")),
    path("employee/", views.employee_panel, name="employee_panel"),
]
