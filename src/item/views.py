from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item, Category
from .forms import createItemForm
from django.contrib import messages
import datetime

def itemList(request):
    items = Item.objects.all()
    return render(request, 'item/item_list.html', {'items': items})

def validFileExtension(value):
    value.lower()
    fileTypes = ['.png', '.jpg', '.jpeg', '.webp', '.avip']
    for typ in fileTypes:
        if value.endswith(typ):
            return True
    return False

def createItem(request):
    if request.method == 'GET':
        cats = Category.objects.all()
        return render(request, 'item/create_item.html', {'form': createItemForm(), 'categories': cats})
    else:
        print(request.FILES['image'].name)
        if validFileExtension(request.FILES['image'].name):
            Item.objects.create(name=request.POST['name'], description=request.POST['description'], creation_date=datetime.datetime.now(), category_id = request.POST['selected_category'], image = request.FILES['image'])
            messages.success(request, '¡Artículo cargado exitosamente!')
            return redirect('itemList')
        else:
            messages.error(request, 'Extensión del archivo no soportada')
            cats = Category.objects.all()
            return render(request, 'item/create_item.html', {'form': createItemForm(), 'categories': cats})

def deleteItem(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)#agregar desp como param user = request.user (solo acá)
        item.delete()
        messages.success(request, '¡Artículo eliminado exitosamente!')
    return redirect('itemList')

def item_detail(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=item_id)#agregar desp como param user = request.user (solo acá)
        form = createItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            item.category_id = request.POST['selected_category']
            item.save()
            messages.success(request, '¡Artículo modificado exitosamente!')
        return redirect('itemList')
    else:
        item = get_object_or_404(Item, pk=item_id)#agregar desp como param user = request.user (solo acá)
        form = createItemForm(instance=item)
        cats = Category.objects.all()
        return render(request, 'item/item_detail.html', {'form': form, 'item':item, 'categories': cats})

