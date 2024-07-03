from datetime import datetime
from allauth.account.forms import SignupForm
from django import forms
from . import models
from owners.models import Product


class UsersSignupForm(SignupForm):
    first_name = forms.CharField(
        required=True,
        max_length=30,
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "placeholder": ("Nombre"),
                "autocomplete": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        required=True,
        max_length=30,
        label="Apellido",
        widget=forms.TextInput(
            attrs={
                "placeholder": ("Apellido"),
                "autocomplete": "Last Name",
            }
        ),
    )
    birth_date = forms.DateField(
        required=True,
        label="Fecha de nacimiento",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": ("Fecha de nacimiento"),
                "autocomplete": "Date of Birth",
            }
        ),
    )

    def save(self, request):
        user = super(UsersSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.birth_date = self.cleaned_data["birth_date"]
        user.save()
        return user

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        today = datetime.now().date()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        if age < 18:
            raise forms.ValidationError(
                "Hay que ser mayor de 18 años para registrarse en la plataforma."
            )
        return birth_date


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
        }

class SaleForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["titulo", "sold"]

    sold = forms.IntegerField(
        label="Cantidad vendida",
        widget=forms.TextInput(
            attrs={"class": "textarea textarea-bordered w-full bg-neutral border-dark"}
        ),
    )

    titulo = forms.ModelChoiceField(
        label="Nombre del producto",
        queryset=Product.objects.all(),
        widget=forms.Select(
            attrs={"class": "select select-bordered w-full bg-neutral border-dark"}
        ),
    )
