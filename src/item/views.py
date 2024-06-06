from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
# from rolepermissions.decorators import has_role_decorator
from item.models import Item, Category
from trades.models import Trade, TradeStateMachine as TradeState, Proposal, ProposalStateMachine as ProposalState
from profiles.models import Profile
from .forms import ItemForm


def itemList(request):
    items = Item.objects.all()
    return render(request, "item/item_list.html", {"items": items})


@login_required
# @has_role_decorator('user')
def create_item(request, category_id=None):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            messages.success(request, "¡Artículo cargado exitosamente!")
            item.save()
            return redirect("profile_view", user_id=request.user.pk)
    else:
        category = None
        if (category_id):
            category = Category.objects.get(id=category_id) 
            
        form = ItemForm(initial={'category': category})
    return render(request, "item/create_item.html", {"form": form})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    exists_trade = Trade.objects.filter(
        Q(state=TradeState.State.PENDING) & (Q(proposal__offering_user=request.user.id) | Q(proposal__requested_user=request.user.id))
        )
    if exists_trade:
        messages.error(request, "¡No podes un articulo de trueque, cancelalo primero!")
        return redirect("profile_view", user_id=request.user.id)  

    if item.user != request.user:
        return redirect("profile_view", user_id=request.user.id)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            if "image" in request.FILES:
                item.image = request.FILES["image"]
            form.save()
            messages.success(request, "¡Artículo modificado exitosamente!")
            return redirect("profile_view", user_id=request.user.id)
    else:
        form = ItemForm(instance=item)
    return render(request, "item/edit_item.html", {"form": form})


@login_required
@require_POST
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.user != request.user:
        messages.error(request, "¡El articulo no es tuyo!")
        return redirect("profile_view", user_id=request.user.id)
    exists_trade = Trade.objects.filter(
        Q(state=TradeState.State.PENDING) & (Q(proposal__offering_user=request.user.id) | Q(proposal__requested_user=request.user.id))
    )
    
    exists_proposal = Proposal.objects.filter(
        Q(state=ProposalState.State.PENDING) & (Q(proposal__offering_user=request.user.id) | Q(proposal__requested_user=request.user.id))
    )

    if exists_trade or exists_proposal:
        messages.error(request, "¡No podes eliminar un articulo de trueque, cancela el trueque primero!")
        return redirect("profile_view", user_id=request.user.id) 
    item.is_visible = False
    item.save()
    messages.success(request, "¡Artículo eliminado exitosamente!")
    return redirect("profile_view", user_id=request.user.id)


def detail_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "item/detail_item.html", {"item": item})
