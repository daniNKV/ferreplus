from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from .models import Employee, User

admin.site.site_header = "Panel de Administración de Ferreplus"
admin.site.site_title = "Admin"
admin.site.index_title = "Ferreplus"


class UserAdmin(admin.ModelAdmin):
    fields = ("first_name", "last_name", "email", "birth_date", "password")

    def save_model(self, request, obj, form, change):
        if not change:  # only for new objects
            password = form.cleaned_data.get("password")
            obj.set_password(password)
        obj.save()

class EmployeeAdminForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            "user",
            "dni",
            "branch",
        ]

    def clean_(self):
        cleaned_data = super().clean()
        if not cleaned_data.name:
            raise ValidationError("This field is required.")
        if not cleaned_data.email:
            raise ValidationError("This field is required.")

    def clean_dni(self):
        dni = self.cleaned_data.get("dni")
        if len(dni) >= 7:
            return dni
        raise ValidationError("El DNI debe tener 7 o 8 caracteres")



class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm
    fields = ("user", "dni", "branch")

admin.site.register(User, UserAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(Group)
