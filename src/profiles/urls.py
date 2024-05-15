from django.urls import path
from .views import profile_view

urlpatterns = [
    path('<int:user_id>/', profile_view, name='profile_view'),
]