from django.db import models
from django.forms import ModelForm

class Category(abstractCategory):
    name = models.CharField(max_length=30)

class Item(AbstractItem):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    creation_date = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    # TODO: Instalar Pillow para manejo de imagenes. Implementar con el perfil del usuario.
    # image = models.ImageField(upload_to='items/', null=False, blank=Flase)

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "creation_date"]
