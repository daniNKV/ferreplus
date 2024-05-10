from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from owners.models import Branch, Employee
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView

class BranchCreateView(CreateView):
    model = Branch
    fields = ['name', 'address', 'opening_hour', 'closing_hour']

    def form_valid(self, form):
        messages.success(self.request, '¡Sucursal creada exitosamente!')
        return super().form_valid(form) 

    def get_success_url(self):
        return reverse_lazy('branch_list') # Redirige a la lista de sucursales después de crear una sucursal

class EmployeeCreateView(CreateView):
    model = Employee
    fields = ['name', 'email', 'birth_date', 'last_name', 'dni', 'password', 'branch']
    success_url = '/'  # Redirige a la misma página principal

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
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['branch'].queryset = Branch.objects.all()
        return form
    

def employeeList(request):
    objetos = Employee.objects.all()
    return render(request, 'owners/employee_list.html', {'objetos': objetos})

def branchList(request):
    objetos = Branch.objects.all()
    return render(request, 'owners/branch_list.html', {'objetos': objetos})

def employeeDelete(request, employee_email):
    Employee.objects.filter(email=employee_email).delete()
    return redirect('employee_list')

def branchDelete(request, branch_id):
    Branch.objects.filter(id=branch_id).delete()
    return redirect('branch_list')

class BranchUpdateView(UpdateView):
    model = Branch
    fields = ['name', 'address', 'opening_hour', 'closing_hour']
    template_name = 'owners/branch_update.html'

    def get_success_url(self):
        return reverse_lazy('branch_update', kwargs={'pk': self.object.pk})

def branchList(request):
    objetos = Branch.objects.all()
    return render(request, 'owners/branch_list.html', {'objetos': objetos})

def branchUpdate(request, branch_id):
    branch = Branch.objects.get(id=branch_id)
    if request.method == 'POST':
        # Obtener los datos del formulario enviado
        name = request.POST.get('name')
        address = request.POST.get('address')
        opening_hour = request.POST.get('opening_hour')
        closing_hour = request.POST.get('closing_hour')

        # Actualizar los campos de la sucursal
        branch.name = name
        branch.address = address
        branch.opening_hour = opening_hour
        branch.closing_hour = closing_hour
        branch.save()

        # Redirigir a la lista de sucursales o a una página de confirmación
        return redirect('branch_list')
    else:
        return render(request, 'owners/branch_update.html', {'objeto': branch})