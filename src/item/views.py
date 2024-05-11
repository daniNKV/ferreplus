from django.shortcuts import render, redirect
from item.models import Item, Category
from .forms import createItemForm
import datetime

def itemList(request):
    items = Item.objects.all()
    for item in items:
        print(item.creation_date)
    return render(request, 'item/item_list.html', {'items': items})

def createItem(request):
    if request.method == 'GET':
        cats = Category.objects.all()
        return render(request, 'item/create_item.html', {'form': createItemForm(), 'categories': cats})
    else:
        Item.objects.create(name=request.POST['name'], description=request.POST['description'], creation_date=datetime.datetime.now(), category_id = request.POST['selected_category'], image = request.FILES['image'])
    return redirect('itemList')
