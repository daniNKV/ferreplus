from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# from rolepermissions.decorators import has_role_decorator
from item.models import Item
from .forms import ItemForm


def itemList(request):
    items = Item.objects.all()
    return render(request, "item/item_list.html", {"items": items})


@login_required
# @has_role_decorator('user')
def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            messages.success(request, "¡Artículo cargado exitosamente!")
            item.save()
            return redirect("profile_view", user_id=request.user.pk)
    else:
        form = ItemForm()
    return render(request, "item/create_item.html", {"form": form})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
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
        messages.success(request, "¡El articulo no es tuyo!")
        return redirect("profile_view", user_id=request.user.id)
    item.delete()
    messages.success(request, "¡Artículo eliminado exitosamente!")
    return redirect("profile_view", user_id=request.user.id)

def detail_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "item/detail_item.html", { "item": item })
