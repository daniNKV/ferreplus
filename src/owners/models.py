from django.db import models


class Branch(models.Model):
    class Meta:
        verbose_name = "Sucursal"

    name = models.CharField(verbose_name="nombre", max_length=100)
    address = models.CharField(verbose_name="direccion", max_length=100)
    opening_hour = models.TimeField(verbose_name="hora de apertura")
    closing_hour = models.TimeField(verbose_name="hora de cierre")
    
    def __str__(self):
        return self.name
