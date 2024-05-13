from django.forms import ModelForm, ValidationError
from django.contrib import admin
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from .models import Employee, User

admin.site.site_header = "Panel de Administración de Ferreplus"
admin.site.site_title = "Admin"
admin.site.index_title = "Ferreplus"


class UserAdminForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "password",
        ]


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


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm


admin.site.register(User, UserAdmin)
admin.site.register(Employee, EmployeeAdmin)

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(Group)
