from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.forms import formset_factory
from django.contrib import messages
from item.models import Item
from .forms import DatesSelectionForm
from .models import (
    Proposal,
    Trade,
    ProposalStateMachine as ProposalState,
    TradeStateMachine as TradeState,
)


def index_trade(request):
    return render(request, "trades/index.html", {})


# TODO:  Hay que verificar que el usuario no le haya hecho una propuesta aun
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


# TODO: Hay que validar que las selecciones de rango no se superpongan ni sean inversas
@login_required
@require_POST
def dates_selection(request, requested_item_id):
    requested_item = Item.objects.filter(id=requested_item_id).first()
    offered_item = Item.objects.get(id=request.POST.get("offered_item"))
    DateSelectionFormSet = formset_factory(DatesSelectionForm, extra=3)
    context = {
        "formset": DateSelectionFormSet,
        "requested_item": requested_item,
        "offered_item": offered_item,
    }
    return render(request, "trades/snippets/dates_snippet.html", context)


@login_required
@require_POST
def proposal_creation(request, requested_item_id, offered_item_id):
    DateSelectionFormSet = formset_factory(DatesSelectionForm, extra=3)
    selected_dates = DateSelectionFormSet(request.POST)

    if selected_dates.is_valid():
        dates = [selection.save() for selection in selected_dates]
        requested_item = Item.objects.get(id=requested_item_id)
        offered_item = Item.objects.get(id=offered_item_id)
        requested_user = requested_item.user
        offering_user = offered_item.user
        branch = requested_item.branch
        proposal = Proposal.objects.create(
            requested_user=requested_user,
            offering_user=offering_user,
            requested_item=requested_item,
            offered_item=offered_item,
            branch=branch,
        )
        for date in dates:
            proposal.possible_dates.add(date)
        # TODO: Decidir si se envian notificaciones al crear la propuesta
        proposal.save()

        messages.warning(request, "Hasta aca llegué por ahora")
        response = HttpResponseRedirect("/trades")
        response["HX-Redirect"] = "/trades"

        return render(request, "trades/index.html", {})
    else:
        return JsonResponse(selected_dates.errors, safe=False)


def accept_proposal(request, proposal_id, settled_date):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    fsm = ProposalState(proposal)

    if fsm.is_pending():
        fsm.accept(settled_date=settled_date)
        return HttpResponse(f"Proposal {proposal_id} accepted and trade created.")
    return HttpResponse(f"Proposal {proposal_id} could not be accepted.")


def counteroffer_proposal(request, proposal_id, selected_item_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    counter_item = get_object_or_404(Item, id=selected_item_id)
    fsm = ProposalState(proposal)

    if fsm.is_pending():
        # TODO: Definir si al contra ofertar se vuelve a seleccionar las fechas
        fsm.counteroffer(item=counter_item)
        return HttpResponse(f"Proposal {proposal_id} counteroffered.")
    return HttpResponse(f"Proposal {proposal_id} could not be counteroffered.")
