from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from .models import Employee
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from trades.models import (

    Trade,
    TradeStateMachine as TradeState,
)

@login_required
@has_role_decorator('employee')
def employee_panel(request):
    return render(request, "user/employee.html", {})

def scheduled_trades(request):
    employee_id = request.user.id
    employee = Employee.objects.filter(id=employee_id).first()
    employee_branch = employee.branch
    trades_branch = Trade.objects.filter(branch = employee_branch)
    trades = trades_branch.filter(state = 'PENDING')
    return render(request, "user/scheduled_trades.html", {'trades' : trades})

def confirmed_trades(request):
    employee_id = request.user.id
    employee = Employee.objects.filter(id=employee_id).first()
    employee_branch = employee.branch
    trades_branch = Trade.objects.filter(branch = employee_branch)
    trades = trades_branch.filter(state = TradeState.State.CONFIRMED)
    return render(request, "user/confirmed_trades.html", {'trades' : trades})

def confirm_trade(request, trade_id, employee_id):
    # TODO: Validar que los usuarios involucrados no sean el empleado que confirma
    trade = get_object_or_404(Trade, id=trade_id)
    employee = get_object_or_404(Employee, id=employee_id)
    fsm = TradeState(trade)
    if trade.state == TradeState.State.PENDING:
        trade.employee = employee
        trade.confirmed_at = datetime.now
        fsm.confirm(employee=employee)
    return redirect("scheduled_trades")

def expire_trade(request, trade_id, employee_id):
    # TODO: Validar que los usuarios involucrados no sean el empleado que confirma
    trade = get_object_or_404(Trade, id=trade_id)
    employee = get_object_or_404(Employee, id=employee_id)
    fsm = TradeState(trade)
    if trade.state == TradeState.State.PENDING:
        trade.employee = employee
        trade.confirmed_at = datetime.now
        fsm.expire()
    return redirect("scheduled_trades")