from django.shortcuts import HttpResponseRedirect, render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .forms import DatesSelectionForm, ConfirmDateForm
from django.contrib import messages
from django.db.models import Q
from user.models import Employee
from item.models import Item
from .models import (
    Proposal,
    Trade,
    ProposalStateMachine as ProposalState,
    TradeStateMachine as TradeState,
)


@login_required
@require_GET
def index_trade(request):
    pending_proposals = Proposal.objects.filter(
        requested_user=request.user.id, state=ProposalState.State.PENDING
    )
    sent_proposals = Proposal.objects.filter(
        offering_user=request.user.id, state=ProposalState.State.PENDING
    )
    pending_trades = Trade.objects.filter(
        proposal__requested_user=request.user.id, state=ProposalState.State.PENDING
    )

    non_expired_proposals = [
        proposal for proposal in pending_proposals if not proposal.is_expired()
    ]
    context = {
        "proposals": {
            "pending": non_expired_proposals,
            "sent": sent_proposals,
        },
        "trades": pending_trades,
    }
    return render(request, "trades/index.html", context)


@login_required
@require_GET
def select_item_to_offer(request, requested_item_id):
    if Proposal.objects.filter(
        requested_item=requested_item_id, offering_user=request.user.id
    ).exists():
        messages.error(request, "Ya enviaste una solicitud")
        return redirect("trades_home")

    requested_item = Item.objects.filter(id=requested_item_id).first()
    items_to_offer = Item.objects.filter(
        user_id=request.user.pk, category=requested_item.category
    )
    context = {
        "requested_item": requested_item,
        "items_to_offer": items_to_offer,
    }
    return render(request, "trades/initiate_proposal.html", context)


# TODO: Hay que validar que las selecciones de rango no se superpongan ni sean inversas
@login_required
@require_POST
def select_possible_dates(request, requested_item_id):
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
def make_proposal(request, requested_item_id, offered_item_id):
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
            possible_branch=branch,
        )
        for date in dates:
            proposal.possible_dates.add(date)
        # TODO: Decidir si se envian notificaciones al crear la propuesta
        proposal.save()

        messages.success(request, "Solicitud enviada con exito!")
        response = HttpResponseRedirect("/trades/#sent-proposals")
        response["HX-Redirect"] = "/trades"
        return response
    else:
        return JsonResponse(selected_dates.errors, safe=True)


@login_required
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if proposal.requested_user.get_id() != request.user.id:
        return HttpResponseForbidden(f"Proposal {proposal_id} it's not for you")
    if proposal.is_expired():
        return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")
    context = {"proposal": proposal}
    if request.method == "POST":
        form = ConfirmDateForm(proposal, request.POST)
        if form.is_valid():
            proposal = get_object_or_404(Proposal, id=proposal_id)
            settled_date = form.cleaned_data
            fsm = ProposalState(proposal)
            if fsm.state == fsm.State.PENDING:
                proposal.confirmed_date = settled_date
                trade = Trade(
                    proposal=proposal,
                    agreed_date=settled_date,
                    branch=proposal.possible_branch,
                )
                trade.save()
                fsm.accept()
                messages.success(request, message="Propuesta aceptada!")
            return redirect("trades_home")
        else:
            return render(request, "trades/date_confirmation.html", {"form": form})
    else:
        form = ConfirmDateForm(proposal=proposal)
        context = {
            "date_confirmation_form": form,
            "proposal": proposal,
            "possible_dates": proposal.possible_dates.all(),
        }
        return render(request, "trades/date_confirmation.html", context)


@login_required
def detail_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if proposal.requested_user.id != request.user.id:
        return HttpResponseForbidden(f"Proposal {proposal_id} it's not for you")
    if proposal.all_dates_expired():
        return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")
    has_items = (
        Item.objects.filter(
            user=proposal.offering_user, category=proposal.offered_item.category
        )
        .exclude(id=proposal.offered_item.id)
        .exists()
    )
    is_counteroffer = proposal.counteroffer_to != None
    context = {
        "proposal": proposal,
        "can_counteroffer": has_items and not is_counteroffer,
    }
    return render(request, "trades/detail_proposal.html", context)


@login_required
def counteroffer_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if proposal.requested_user.id != request.user.id:
        return HttpResponseForbidden(f"Proposal {proposal_id} it's not for you")
    if proposal.all_dates_expired():
        return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")
    if request.method == "POST":
        proposal = get_object_or_404(Proposal, id=proposal_id)
        fsm = ProposalState(proposal)
        if fsm.state == fsm.State.PENDING:
            fsm.counteroffer()
        return redirect("trades_home")
    else:
        items = Item.objects.filter(
            user=proposal.offering_user, category=proposal.offered_item.category
        ).exclude(id=proposal.offered_item.id)
        context = {
            "proposal": proposal,
            "items_to_choose": items,
        }
        return render(request, "trades/counteroffer_proposal.html", context)


def decline_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    fsm = ProposalState(proposal)
    if proposal.requested_user.get_id() != request.user.id:
        return HttpResponseForbidden(f"Proposal {proposal_id} it's not for you")
    if proposal.is_expired():
        return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")

    if proposal.state in [
        ProposalState.State.PENDING,
        ProposalState.State.COUNTEROFFERED,
    ]:
        fsm.decline()
        messages.success(
            request,
            f"Solicitud rechazada! Le avisaremos a {proposal.offering_user.first_name}",
        )
        return redirect("trades_home")
    return HttpResponse(f"Proposal {proposal_id} could not be declined.")


def confirm_trade(request, trade_id, employee_id):
    # TODO: Validar que los usuarios involucrados no sean el empleado que confirma
    trade = get_object_or_404(Trade, id=trade_id)
    employee = get_object_or_404(Employee, id=employee_id)
    fsm = TradeState(trade)

    if trade.state == TradeState.PENDING:
        fsm.confirm(employee=employee)
        return HttpResponse(f"Trade {trade_id} confirmed.")
    return HttpResponse(f"Trade {trade_id} could not be confirmed.", status=400)


def cancel_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    fsm = TradeState(trade)

    if trade.state == TradeState.PENDING:
        fsm.cancel()
        return HttpResponse(f"Trade {trade_id} canceled.")
    return HttpResponse(f"Trade {trade_id} could not be canceled.", status=400)


@login_required
@require_GET
def show_history(request):
    return render(request, "trades/event_history.html", {})


@login_required
@require_GET
def show_concreted_history(request):
    trades = Trade.objects.filter(
        Q(state=TradeState.State.CONFIRMED) & Q(proposal__requested_user=request.user)
        | Q(proposal__offering_user=request.user)
    )

    return render(request, "trades/snippets/trade_history.html", {"trades": trades})


@login_required
@require_GET
def show_canceled_history(request):
    trades = Trade.objects.filter(
        Q(state=TradeState.State.CANCELED)
        & (
            Q(proposal__requested_user=request.user)
            | Q(proposal__offering_user=request.user)
        )
    )
    proposals = Proposal.objects.filter(
        Q(state=ProposalState.State.CANCELED)
        & (Q(requested_user=request.user) | Q(offering_user=request.user))
    )

    return render(
        request,
        "trades/snippets/history_snippet.html",
        {"proposals": proposals, "trades": trades},
    )


@login_required
@require_GET
def show_expired_history(request):
    trades = Trade.objects.filter(
        Q(state=TradeState.State.EXPIRED)
        & (
            Q(proposal__requested_user=request.user)
            | Q(proposal__offering_user=request.user)
        )
    )
    proposals = Proposal.objects.filter(
        Q(state=ProposalState.State.EXPIRED)
        & (Q(requested_user=request.user) | Q(offering_user=request.user))
    )

    return render(
        request,
        "trades/snippets/history_snippet.html",
        {"proposals": proposals, "trades": trades},
    )


@login_required
@require_GET
def show_declined_history(request):
    proposals = Proposal.objects.filter(
        Q(state=ProposalState.State.DECLINED)
        & (
            Q(proposal__requested_user=request.user)
            | Q(proposal__offering_user=request.user)
        )
    )

    return render(
        request, "trades/snippets/proposal_snippet.html", {"proposals": proposals}
    )
