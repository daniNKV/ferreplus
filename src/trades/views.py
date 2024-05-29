from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from item.models import Item
from .forms import TradeForm

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
    form = TradeForm()
    context = {
        "form": form,
        "requested_item": requested_item,
        "offered_item": offered_item,
    }
    return render(request, "trades/snippets/dates_snippet.html", context)


@login_required
@require_POST
def proposal_creation(request, requested_item_id, offered_item_id):
    messages.warning(request, "Hasta aca llegué por ahora")
    response = HttpResponseRedirect("/")
    response["HX-Redirect"] = "/"
    return response
