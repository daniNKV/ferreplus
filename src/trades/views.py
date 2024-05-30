from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from item.models import Item
from .models import Trade, Appointment, State, AcceptedTrade, CanceledTrade, PendingTrade
from .forms import DatesForm

# Create your views here.


def index_trade(request):
    return render(request, "trades/index.html", {})


@login_required
@require_GET
def item_selection(request, requested_item_id):
    requested_item = Item.objects.filter(id=requested_item_id).first()
    items_to_offer = Item.objects.filter(
        user_id=request.user.pk, category=requested_item.category
    )
    context = {
        "requested_item": requested_item,
        "items_to_offer": items_to_offer,
    }
    return render(request, "trades/select_item.html", context)


@login_required
@require_POST
def dates_selection(request, requested_item_id):
    requested_item = Item.objects.filter(id=requested_item_id).first()
    offered_item = Item.objects.get(id=request.POST.get("offered_item"))
    form = DatesForm()
    context = {
        "form": form,
        "requested_item": requested_item,
        "offered_item": offered_item,
    }
    return render(request, "trades/snippets/dates_snippet.html", context)


@login_required
@require_POST
def trade_creation(request, requested_item_id, offered_item_id):
    form = DatesForm(request.POST)
    if form.is_valid():
        date1 = form.cleaned_data['date1']
        time1 = form.cleaned_data['time1']
        date2 = form.cleaned_data['date2']
        time2 = form.cleaned_data['time2']
        date3 = form.cleaned_data['date3']
        time3 = form.cleaned_data['time3']
        dates = [date1, date2, date3]
        times = [time1, time2, time3]
        appointments = [Appointment.objects.create(date=date, time=time) for date, time in zip(dates, times)]
        
        requested_item = Item.objects.get(id=requested_item_id)
        offered_item = Item.objects.get(id=offered_item_id)
        requested_user = requested_item.user
        offering_user = offered_item.user
        branch = requested_item.branch
        state = PendingTrade.load()
        trade = Trade.objects.create(
            requested_user=requested_user,
            offering_user=offering_user,
            requested_item=requested_item,
            offered_item=offered_item,
            branch=branch,
            state=state,
        )
        for appointment in appointments:
            trade.selected_dates.add(appointment)
            
        trade.save()
        messages.warning(request, "Hasta aca llegué por ahora")
        messages.warning(request, "Las fechas no estan siendo validadas")
        response = HttpResponseRedirect("/trades")
        response["HX-Redirect"] = "/trades"
        
        return render(request, "trades/index.html", {})
    else:
        # Handle the case where the form is not valid
        return JsonResponse(form.errors, safe=False)