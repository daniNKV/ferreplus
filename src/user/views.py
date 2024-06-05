from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.utils import timezone
from .models import Employee
from trades.models import (
    Trade,
    TradeStateMachine as TradeState,
)


@login_required
@has_role_decorator('employee')
def employee_panel(request):
    return render(request, "user/employee.html", {})


@login_required
@has_role_decorator('employee')
def scheduled_trades(request):
    employee_id = request.user.employee.id
    employee = Employee.objects.filter(id=employee_id).first()
    trades_branch = Trade.objects.filter(branch=employee.branch)
    trades = trades_branch.filter(state="PENDING")
    return render(request, "user/scheduled_trades.html", {"trades": trades})


@login_required
@has_role_decorator("employee")
def confirmed_trades(request):
    employee_id = request.user.employee.id
    employee = Employee.objects.filter(id=employee_id).first()
    employee_branch = employee.branch
    trades_branch = Trade.objects.filter(branch=employee_branch)
    trades = trades_branch.filter(state=TradeState.State.CONFIRMED)
    return render(request, "user/confirmed_trades.html", {"trades": trades})


@login_required
@has_role_decorator("employee")
def confirm_trade(request, trade_id):
    employee_id = request.user.employee.id
    trade = get_object_or_404(Trade, id=trade_id)
    employee = get_object_or_404(Employee, id=employee_id)
    is_offering = employee.user.id == trade.proposal.offering_user.id
    is_requested = employee.user.id == trade.proposal.offering_user.id
    if is_offering or is_requested:
        return HttpResponseNotAllowed("No te podes aceptar un trueque a vos mismo")
    fsm = TradeState(trade)
    if trade.state == TradeState.State.PENDING:
        trade.employee = employee
        trade.confirmed_at = timezone.now()
        trade.proposal.offered_item.was_traded = True
        trade.proposal.requested_item.was_traded = True
        trade.proposal.offered_item.save()
        trade.proposal.requested_item.save()
        messages.success('El trueque ha sido confirmado!')

        fsm.confirm(employee=employee)
    return redirect("scheduled_trades")


@login_required
@has_role_decorator("employee")
def expire_trade(request, trade_id):
    employee_id = request.user.employee.id
    trade = get_object_or_404(Trade, id=trade_id)
    employee = get_object_or_404(Employee, id=employee_id)
    fsm = TradeState(trade)
    if trade.state == TradeState.State.PENDING:
        trade.employee = employee
        trade.confirmed_at = timezone.now()
        messages.success('El trueque ha expirado')
        fsm.expire()
    return redirect("scheduled_trades")
