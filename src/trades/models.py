from datetime import time
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from user.models import User, Employee
from item.models import Item
from owners.models import Branch


class State(models.Model):
    name = models.CharField(max_length=20, verbose_name="Estado")
    


class CanceledTrade(State):
    def save(self, *args, **kwargs):
        self.pk = 1
        super(CanceledTrade, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class PendingTrade(State):
    def accept(self):
        pass

    def decline(self):
        pass

    def counteroffer(self):
        pass

    def expire(self):
        pass
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super(PendingTrade, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class AcceptedTrade(State):
    def confirm(self):
        pass

    def cancel(self):
        pass

    def expire(self):
        pass

    def save(self, *args, **kwargs):
        self.pk = 1
        super(AcceptedTrade, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
       
    


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.date) + str(self.time)


class Trade(models.Model):
    requested_user = models.ForeignKey(
        User,
        verbose_name="Usuario solicitado",
        related_name="requested_user",
        on_delete=models.PROTECT,
    )
    offering_user = models.ForeignKey(
        User,
        verbose_name="Usuario solicitante",
        related_name="requesting_user",
        on_delete=models.PROTECT,
    )
    requested_item = models.ForeignKey(
        Item,
        verbose_name="Articulo solicitado",
        related_name="requested_item",
        on_delete=models.PROTECT,
    )
    offered_item = models.ForeignKey(
        Item,
        verbose_name="Articulo ofrecido",
        related_name="offered_item",
        on_delete=models.PROTECT,
    )
    branch = models.ForeignKey(
        Branch, verbose_name="Sucursal elegida", on_delete=models.PROTECT
    )
    selected_dates = models.ManyToManyField(
        Appointment,
        verbose_name="Fechas seleccionadas",
        related_name="agreed_date",
    )
    agreed_date = models.DateTimeField(verbose_name="Cita consensuada", null=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.PROTECT)
    replied_at = models.DateTimeField(null=True)
