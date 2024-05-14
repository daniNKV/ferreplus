from django.db import models
from django.forms import ModelForm
import os

class Category(models.Model):
    name = models.CharField(max_length=50)

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    creation_date = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to='item/images/', null=False, blank=False)
    wasTraded = models.BooleanField(default=False)
    #user = models.ForeignKey(
    #    User,
    #    on_delete=models.PROTECT,
    #    blank=True,
    #    null=True
    #)

    #branch = models.ForeignKey(
    #    Branch,
    #    on_delete=models.PROTECT,
    #    blank=True,
    #    null=True
    #)

