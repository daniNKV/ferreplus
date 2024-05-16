from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from item.models import Item
from .forms import ItemForm


def itemList(request):
    items = Item.objects.all()
    return render(request, "item/item_list.html", {"items": items})


@login_required
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
        return redirect('profile_view', user_id=request.user.id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            if 'image' in request.FILES:
                item.image = request.FILES['image']
            form.save()
            messages.success(request, "¡Artículo modificado exitosamente!")
            return redirect('profile_view', user_id=request.user.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'item/edit_item.html', {'form': form})

def delete_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(
            Item, pk=item_id
        )  # agregar desp como param user = request.user (solo acá)
        item.delete()
        messages.success(request, "¡Artículo eliminado exitosamente!")
    return redirect("itemList")


# def detail_item(request, item_id):
#     if request.method == "POST":
#         item = get_object_or_404(
#             Item, pk=item_id
#         )  # agregar desp como param user = request.user (solo acá)
#         form = ItemForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             item.category_id = request.POST["selected_category"]
#             item.image = request.FILES["image"]
#             item.save()
#             messages.success(request, "¡Artículo modificado exitosamente!")
#         return redirect("itemList")
#     else:
#         item = get_object_or_404(
#             Item, pk=item_id
#         )  # agregar desp como param user = request.user (solo acá)
#         form = ItemForm(instance=item)
#         cats = Category.objects.all()
#         return render(
#             request,
#             "item/item_detail.html",
#             {"form": form, "item": item, "categories": cats},
#         )
