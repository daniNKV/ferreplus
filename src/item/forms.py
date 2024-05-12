from django import forms
from item.models import Item

class createItemForm(forms.Form):
    class Meta:
        model = Item
        fields = ['name', 'description', 'image']

    name = forms.CharField(max_length=50, label="Nombre del artículo")
    description = forms.CharField(widget=forms.Textarea, max_length=300, label="Descripción del artículo")
    image = forms.ImageField(label="Imagen del artículo (en jpg, jpeg, png, webp o avip)", required=True, widget=forms.FileInput(attrs={'class':'form-control'}))
