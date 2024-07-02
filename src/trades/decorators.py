from functools import wraps
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from trades.models import Proposal

def check_proposal(func):
    @wraps(func)
    def wrapper(request, proposal_id, *args, **kwargs):
        proposal = get_object_or_404(Proposal, id=proposal_id)
        if proposal.requested_user.id != request.user.id:
            return HttpResponseForbidden(f"Proposal {proposal_id} it's not for you")
        if proposal.all_dates_expired():
            return HttpResponseForbidden(f"Proposal {proposal_id} it's expired")
        return func(request, proposal_id, *args, **kwargs)
    return wrapper

def proposal_already_sent(func):
    @wraps(func)
    def wrapper(request, proposal_id, item_id, *args, **kwargs):
        proposal = get_object_or_404(Proposal, id=proposal_id)
        has_proposal_pending = Proposal.objects.filter(
        (Q(state="PENDING") |
        Q(state="COUNTEROFFERED")) &
        (Q(offering_user=request.user.id) & Q(requested_item=item_id))     
        ).exists()
        if has_proposal_pending:
            messages.error(request, "Ya enviaste una solicitud")
            return redirect("trades_home")

    return wrapper
