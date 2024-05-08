from django import forms


class ItemForm(forms.Form):
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=200)
    creation_date = forms.DateField(required=False)
