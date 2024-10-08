from django.shortcuts import render
from item.models import Item, Category
from owners.models import Branch, Product

def branches(request):
    branches = Branch.objects.all()
    return render(request, 'index/all_items.html', {'branches': branches})

def home_view(request):
    items_shown = 10
    items = Item.objects.filter(was_traded=False, is_visible=True).order_by('?')[:items_shown]  # Get 10 random items
    products = Product.objects.all()[:items_shown]
    return render(request, 'index.html', {'items': items, 'products': products})

def all_items(request):
    text = request.GET.get('text')
    category_query = request.GET.get('category')
    branch_query = request.GET.get('branch')
    if (text):
        resultados = Item.objects.filter(name__icontains=text)
    else:
        resultados = Item.objects.all()
    if (category_query):
        category_name = Category.objects.filter(name__icontains=category_query).first()
        resultados = resultados.filter(category = category_name)
    if (branch_query):
        branch_name = Branch.objects.filter(id=branch_query).first()
        resultados = resultados.filter(branch = branch_name)
    
    branches = Branch.objects.all()  # Obtener todas las sucursales
    categories = Category.objects.all()
    return render(request, 'index/all_items.html', {'resultados': resultados, 'branches': branches, 'categories': categories})

def all_products(request):
    products = Product.objects.all()
    return render(request, 'index/all_products.html', {'products': products})