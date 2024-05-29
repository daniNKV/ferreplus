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
    pass


class PendingTrade(State):
    def accept(self):
        pass

    def decline(self):
        pass

    def counteroffer(self):
        pass


class AcceptedTrade(State):
    def confirm(self):
        pass

    def cancel(self):
        pass

    def expire(self):
        pass


class DateTuple(models.Model):
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return str(self.start_time) + str(self.end_time)


class TradeDateTuple(models.Model):
    trade = models.ForeignKey("trades.Trade", on_delete=models.CASCADE)
    date_tuple = models.ForeignKey(DateTuple, on_delete=models.CASCADE)


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
        DateTuple,
        through=TradeDateTuple,
        verbose_name="Fechas seleccionadas",
    )
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True)
    replied_at = models.DateField()
