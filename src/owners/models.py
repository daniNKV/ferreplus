from django.db import models
from core.jobs import UploadToPathAndRename


class Branch(models.Model):
    class Meta:
        verbose_name = "Sucursal"

    name = models.CharField(verbose_name="nombre", max_length=100)
    address = models.CharField(verbose_name="direccion", max_length=100)
    opening_hour = models.TimeField(verbose_name="hora de apertura")
    closing_hour = models.TimeField(verbose_name="hora de cierre")

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    class Meta:
        verbose_name = "Producto"

    title = models.CharField(verbose_name="titulo", max_length=100)
    image = models.ImageField(
        upload_to=UploadToPathAndRename("product/images/"), null=False, blank=False
    )

    def __str__(self):
        return str(self.title)