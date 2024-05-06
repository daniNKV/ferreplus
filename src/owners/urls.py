from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from owners.views import BranchCreateView


urlpatterns = [ 
    path('create_branch/', BranchCreateView.as_view(), name='create')
]