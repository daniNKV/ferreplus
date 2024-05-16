from django.shortcuts import render
from item.models import Item

def home_view(request):
    items = Item.objects.order_by('?')[:10]  # Get 10 random items
    return render(request, 'index.html', {'items': items})