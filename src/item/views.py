from django.shortcuts import render
from item.models import Item, Category

def itemList(request):
    items = Item.objects.all()
    for item in items:
        print(item.creation_date)
    return render(request, 'item/item_list.html', {'items': items})
