from datetime import datetime
from allauth.account.forms import SignupForm
from django import forms


class UsersSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": ("First Name"),
                "autocomplete": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": ("Last Name"),
                "autocomplete": "Last Name",
            }
        ),
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": ("Date of Birth"),
                "autocomplete": "Date of Birth",
            }
        ),
    )

    def signup(self, request, user):
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
