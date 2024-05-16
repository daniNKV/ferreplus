from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from item.models import Item, Category
from .forms import ItemCreateForm


def itemList(request):
    items = Item.objects.all()
    return render(request, "item/item_list.html", {"items": items})


@login_required
def create_item(request):
    if request.method == "POST":
        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            messages.success(request, "¡Artículo cargado exitosamente!")
            item.save()
            return redirect("profile_view", user_id=request.user.pk)
    else:
        form = ItemCreateForm()
    return render(request, "item/create_item.html", {"form": form})


def delete_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(
            Item, pk=item_id
        )  # agregar desp como param user = request.user (solo acá)
        item.delete()
        messages.success(request, "¡Artículo eliminado exitosamente!")
    return redirect("itemList")


def detail_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(
            Item, pk=item_id
        )  # agregar desp como param user = request.user (solo acá)
        form = ItemCreateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            item.category_id = request.POST["selected_category"]
            item.image = request.FILES["image"]
            item.save()
            messages.success(request, "¡Artículo modificado exitosamente!")
        return redirect("itemList")
    else:
        item = get_object_or_404(
            Item, pk=item_id
        )  # agregar desp como param user = request.user (solo acá)
        form = ItemCreateForm(instance=item)
        cats = Category.objects.all()
        return render(
            request,
            "item/item_detail.html",
            {"form": form, "item": item, "categories": cats},
        )
