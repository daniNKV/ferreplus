from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from owners.views import BranchCreateView, EmployeeCreateView, employeeList, branchList, employeeDelete, branchDelete, branchUpdate


urlpatterns = [ 
    path('create_branch/', BranchCreateView.as_view(), name='create_branch'),
    path('create_employee/', EmployeeCreateView.as_view(), name='create_employee'),
    path('employee_list/', employeeList, name='employee_list'),
    path('branch_list/', views.branchList, name='branch_list'),
    path('employee_delete/<str:employee_email>/', employeeDelete, name='employee_delete'),
    path('branch_delete/<int:branch_id>/', branchDelete, name='branch_delete'),
    path('branch_update/<int:branch_id>/', views.branchUpdate, name='branch_update'),
]


