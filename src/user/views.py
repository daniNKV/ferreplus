from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator

@login_required
@has_role_decorator('employee')
def employee_panel(request):
    return render(request, "user/employee.html", {})
