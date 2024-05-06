from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from owners.views import BranchCreateView, EmployeeCreateView


urlpatterns = [ 
    path('create_branch/', BranchCreateView.as_view(), name='create_branch'),
    path('create_employee/', EmployeeCreateView.as_view(), name='create_employee')
]