from django.shortcuts import render
from django.models import Item


def itemList(request):
    items = Item.objects.all()
    return render(request, '../templates/item/item_list.html', {'items': objetos})
