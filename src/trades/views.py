from django.shortcuts import HttpResponseRedirect, render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .forms import DatesSelectionForm, ConfirmDateForm
from django.forms import formset_factory
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .decorators import check_proposal
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
        proposal__requested_user=request.user.id, state=ProposalState.State.PENDING or ProposalState.State.COUNTEROFFERED
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
    has_proposal_pending = Proposal.objects.filter(
        (Q(state=ProposalState.State.PENDING) |
        Q(state=ProposalState.State.COUNTEROFFERED)) &
        (Q(offering_user=request.user.id) & Q(requested_item=requested_item_id))     
    ).exists()
    if has_proposal_pending:
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
    
    
@require_POST
def handle_post_accept_proposal(request, proposal):
    if proposal.confirmed_date == None:
        form = ConfirmDateForm(proposal, request.POST)
        if form.is_valid():
            proposal.confirmed_date = form.cleaned_data
        else:
            return render(request, "trades/accept_proposal.html", {"form": form})
    fsm = ProposalState(proposal)
    if fsm.state == fsm.State.PENDING:
        trade = Trade(
            proposal=proposal,
            agreed_date=proposal.confirmed_date,
            branch=proposal.possible_branch,
        )
        requested_item = proposal.requested_item
        offered_item = proposal.offered_item
        proposal.replied_at = timezone.now()
        requested_item.is_visible = False
        offered_item.is_visible = False
        requested_item.save()
        offered_item.save()
        trade.save()
        fsm.accept()
        messages.success(request, message="Propuesta aceptada!")

    return redirect("trades_home")


@require_GET
def handle_get_accept_proposal(request, proposal):
    if (proposal.confirmed_date == None):
        form = ConfirmDateForm(proposal=proposal)
        context = {
            "date_confirmation_form": form,
            "proposal": proposal,
            "possible_dates": proposal.possible_dates.all(),
            "is_confirmed": False
        }
    else: 
        context = { 
            "proposal": proposal,
            "is_confirmed": True,
        }

    return render(request, "trades/accept_proposal.html", context)


@login_required
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if proposal.requested_user.get_id() != request.user.id:
        return HttpResponseForbidden(f"Proposal {proposal_id} it's not for you")
    if proposal.is_expired():
        return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")

    if request.method == "POST":
        return handle_post_accept_proposal(request, proposal)
    else:
        return handle_get_accept_proposal(request, proposal)


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
@require_GET
def select_item_to_request(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if proposal.requested_user.id != request.user.id:
        return HttpResponseForbidden(f"Proposal {proposal_id} it's not for you")
    if proposal.all_dates_expired():
        return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")
    items = Item.objects.filter(
        user=proposal.offering_user, category=proposal.offered_item.category
    ).exclude(id=proposal.offered_item.id, is_visible=False)
    context = {
        "proposal": proposal,
        "items_to_choose": items,
    }
    return render(request, "trades/counteroffer_proposal.html", context)

@login_required
@require_POST
def confirm_date(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    requested_item = Item.objects.get(id=request.POST.get("selected_item"))
    form = ConfirmDateForm(proposal=proposal)
    context = {
        "date_confirmation_form": form,
        "proposal": proposal,
        "possible_dates": proposal.possible_dates.all(),
        "selected_item": requested_item
    }
    return render(request, "trades/snippets/confirm_date_form.html", context)


@login_required
@require_POST
def make_counteroffer(request, proposal_id, selected_item_id):
    has_proposal_pending = Proposal.objects.filter(
        (Q(state=ProposalState.State.PENDING) |
        Q(state=ProposalState.State.COUNTEROFFERED)) &
        (Q(offering_user=request.user.id) & Q(requested_item=selected_item_id))     
    ).exists()
    if has_proposal_pending:
        messages.error(request, "Ya enviaste una solicitud")
        return redirect("trades_home")

    proposal = get_object_or_404(Proposal, id=proposal_id)
    form = ConfirmDateForm(proposal, request.POST)
    if form.is_valid():
        item = get_object_or_404(Item, id=selected_item_id)
        settled_date = form.cleaned_data
        fsm = ProposalState(proposal)
        if fsm.state == fsm.State.PENDING:
            proposal.replied_at = timezone.now()
            messages.success(request, message="Contraoferta enviada!")
            fsm.counteroffer(item=item, date=settled_date)
        response = HttpResponseRedirect("/trades")
        response["HX-Redirect"] = "/trades"
        return response
    else:
        return JsonResponse(form.errors, safe=True)


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



def cancel_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    user_involved = trade.proposal.requested_user.id == request.user.id or trade.proposal.offering_user.id == request.user.id
    if not user_involved:
        return HttpResponseForbidden(f"Proposal {trade_id} it's not for you")
    if trade.state == TradeState.State.EXPIRED:
        return HttpResponseForbidden(f"Proposal {trade_id} it's expired")
    fsm = TradeState(trade)
    if (trade.state == fsm.State.PENDING):
        messages.success(request, message='Trueque cancelado! Le avisaremos del inconveniente')
        requested_item = get_object_or_404(Item, id=trade.proposal.requested_item)
        offered_item = get_object_or_404(Item, id=trade.proposal.offered_item)
        requested_item.is_visible = True
        offered_item.is_visible = True
        requested_item.save()
        offered_item.save()
        fsm.cancel()
    
    return redirect('trades_home')


def cancel_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    user_involved = proposal.requested_user.id == request.user.id or proposal.offering_user.id == request.user.id
    if not user_involved:
        return HttpResponseForbidden(f"Proposal {proposal_id} it's not yours'")
    if proposal.is_expired():
        return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")

    fsm = ProposalState(proposal)
    if (proposal.state == fsm.State.PENDING):
        messages.success(request, message='Hemos retirado tu propuesta!')
        fsm.cancel()
    
    return redirect('trades_home')

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
