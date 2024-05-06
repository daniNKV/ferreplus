from django.shortcuts import render
from django.views.generic import CreateView
from owners.models import Branch, Employee

class BranchCreateView(CreateView):
    model = Branch
    fields = ['name', 'address', 'opening_hour', 'closing_hour']

class EmployeeCreateView(CreateView):
    model = Employee
    fields = ['name', 'email', 'birth_date', 'last_name', 'dni', 'branch_name']

    def form_valid(self, form):
        dni = form.cleaned_data['dni']
        if len(dni) != 8:
            form.add_error('dni', 'El DNI debe tener 8 caracteres')
            return self.form_invalid(form)
        return super().form_valid(form)