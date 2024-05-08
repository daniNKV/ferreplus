from django.shortcuts import render
from django.views.generic import CreateView
from owners.models import Branch, Employee
from django.contrib import messages
from django.shortcuts import redirect


class BranchCreateView(CreateView):
    model = Branch
    fields = ['name', 'address', 'opening_hour', 'closing_hour']

class EmployeeCreateView(CreateView):
    model = Employee
    fields = ['name', 'email', 'birth_date', 'last_name', 'dni']
    success_url = '/'  # Redirige a la misma página para crear otro empleado

    def form_valid(self, form):
        dni = form.cleaned_data['dni']
        email = form.cleaned_data['email']
        if not Employee.objects.filter(email=email).exists():
            if len(dni) >= 7 and len(dni) <= 8:
                messages.success(self.request, '¡Empleado creado exitosamente!')
                return super().form_valid(form)
            form.add_error('dni', 'El DNI debe tener 7 o 8 caracteres')
        form.add_error('email', 'El email ingresado ya se encuentra registrado')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_saved'] = self.request.GET.get('employee_saved', False)
        return context


def employeeList(request):
    objetos = Employee.objects.all()
    return render(request, 'C:/Users/nicol/OneDrive/Desktop/Informatica/IS2/ferreplus/src/templates/owners/employee_list.html', {'objetos': objetos})

def branchList(request):
    objetos = Employee.objects.all()
    return render(request, 'C:/Users/nicol/OneDrive/Desktop/Informatica/IS2/ferreplus/src/templates/owners/branch_list.html', {'objetos': objetos})

def employeeDelete(request, employee_email):
    Employee.objects.filter(email=employee_email).delete()
    return redirect('employee_list')
