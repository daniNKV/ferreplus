from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.utils import timezone
from .models import Employee, User
from trades.models import (
    Trade,
    Proposal,
    Item,
    TradeStateMachine as TradeState,
)
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from django.utils.timezone import now, timedelta, datetime
from django.http import HttpResponse 
from item.models import Category
from owners.models import Product
from .forms import SaleForm

@login_required
@has_role_decorator('employee')
def employee_panel(request):
    return render(request, "user/employee.html", {})


@login_required
@has_role_decorator('employee')
def scheduled_trades(request):
    employee_id = request.user.employee.id
    employee = Employee.objects.filter(id=employee_id).first()
    trades_branch = Trade.objects.filter(branch=employee.branch)
    trades = trades_branch.filter(state="PENDING")
    return render(request, "user/scheduled_trades.html", {"trades": trades, "branch": employee.branch})


@login_required
@has_role_decorator("employee")
def confirmed_trades(request):
    employee_id = request.user.employee.id
    employee = Employee.objects.filter(id=employee_id).first()
    employee_branch = employee.branch
    trades_branch = Trade.objects.filter(branch=employee_branch)
    trades = trades_branch.filter(state=TradeState.State.CONFIRMED)
    return render(request, "user/confirmed_trades.html", {"trades": trades, "branch": employee_branch})


@login_required
@has_role_decorator("employee")
def confirm_trade(request, trade_id):
    employee_id = request.user.employee.id
    trade = get_object_or_404(Trade, id=trade_id)
    employee = get_object_or_404(Employee, id=employee_id)
    is_offering = employee.user.id == trade.proposal.offering_user.id
    is_requested = employee.user.id == trade.proposal.offering_user.id
    if is_offering or is_requested:
        return HttpResponseNotAllowed("No te podes aceptar un trueque a vos mismo")
    fsm = TradeState(trade)
    if trade.state == TradeState.State.PENDING:
        trade.employee = employee
        trade.confirmed_at = timezone.now()
        trade.proposal.offered_item.was_traded = True
        trade.proposal.requested_item.was_traded = True
        trade.proposal.offered_item.is_visible = False
        trade.proposal.requested_item.is_visible = False
        trade.proposal.offered_item.save()
        trade.proposal.requested_item.save()
        fsm.confirm(employee=employee)
        messages.success(request, 'El trueque ha sido confirmado!')
    return redirect("ask_to_upload_sale")


@login_required
@has_role_decorator("employee")
def expire_trade(request, trade_id):
    employee_id = request.user.employee.id
    trade = get_object_or_404(Trade, id=trade_id)
    employee = get_object_or_404(Employee, id=employee_id)
    fsm = TradeState(trade)
    if trade.state == TradeState.State.PENDING:
        trade.employee = employee
        trade.confirmed_at = timezone.now()
        trade.proposal.offered_item.is_visible = True
        trade.proposal.requested_item.is_visible = True
        trade.proposal.offered_item.save()
        trade.proposal.requested_item.save()
        fsm.expire()
        messages.success(request, 'El trueque ha expirado')
    return redirect("employee_panel")


@login_required
@has_role_decorator('employee')
def show_statistics(request):
    return render(request, "user/show_statistics.html", {})


def historical_states_trades(request):
    trades = Trade.objects.all().values()  
    trades_df = pd.DataFrame(trades) 
    
    if trades_df.empty:
        return HttpResponse("No se realizaron trueques.", content_type='text/plain')
    
    trades_for_state = trades_df['state'].value_counts()
    
    # Crear el gráfico
    plt.figure(figsize=(8, 8))
    trades_for_state.plot(kind='pie', autopct='%1.1f%%', subplots=True)
    plt.title('Distribución de trueques por estado')
    plt.ylabel('')  # Ocultar la etiqueta del eje Y

    # Guardar el gráfico en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Convertir la imagen a base64 para pasarla a la plantilla
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'user/historical_states_trades.html', {'graphic': graphic})


def weekly_states_trades(request):
    # Obtener la fecha y hora actuales
    current_time = now()
    # Calcular la fecha y hora hace una semana
    one_week_ago = current_time - timedelta(days=7)
    
    # Filtrar los trades de la última semana
    trades = Trade.objects.filter(agreed_date__gte=one_week_ago).values()
    
    # Convertir el QuerySet a un DataFrame de Pandas
    trades_df = pd.DataFrame(trades)
    
    if trades_df.empty:
        return HttpResponse("No hay trueques en la ultima semana.", content_type='text/plain')
    
    # Crear el gráfico
    plt.figure(figsize=(8, 8))
    trades_df.plot(kind='pie', autopct='%1.1f%%', subplots=True)
    plt.title('Distribución semanal de trueques por estado')
    plt.ylabel('')  # Ocultar la etiqueta del eje Y

    # Guardar el gráfico en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Convertir la imagen a base64 para pasarla a la plantilla
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'user/weekly_states_trades.html', {'graphic': graphic})


def category_trades(request):
    # Obtener los datos de las tablas
    trade_data = Trade.objects.all().values()
    proposals_data = Proposal.objects.all().values()
    items_data = Item.objects.all().values()
    categories_data = Category.objects.all().values()

    # Crear DataFrames de Pandas con los datos obtenidos
    trades_df = pd.DataFrame(trade_data)
    proposals_df = pd.DataFrame(proposals_data)
    items_df = pd.DataFrame(items_data)
    categories_df = pd.DataFrame(categories_data)

    # Fusionar los DataFrames
    merged_df = pd.merge(trades_df, proposals_df, left_on='proposal_id', right_on='id', suffixes=('_trades', '_proposals'))
    merged_df = pd.merge(merged_df, items_df, left_on='requested_item_id', right_on='id', suffixes=('_merged', '_items'))
    merged_df = pd.merge(merged_df, categories_df, left_on='category_id', right_on='id', suffixes=('_merged', '_categories'))
    
    # Realizar el conteo de valores en la columna deseada
    category_counts = merged_df['name_categories'].value_counts()

     # Obtener todas las categorías posibles
    all_categories = categories_df['name'].tolist()

    # Crear un DataFrame con todas las categorías y establecer el conteo en cero para aquellas que no estén presentes
    all_categories_counts = pd.Series({category: category_counts.get(category, 0) for category in all_categories})

    # Crear el gráfico de barras
    plt.figure(figsize=(15, 10))
    all_categories_counts.plot(kind='bar')
    plt.title('Distribución de trueques por categoría')
    plt.xlabel('Categoría')
    plt.ylabel('Cantidad de Trueques')

    plt.yticks(range(int(all_categories_counts.max()) + 1))

    plt.xticks(rotation=25, ha='right')

    # Guardar el gráfico en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Convertir la imagen a base64 para pasarla a la plantilla
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'user/category_trades.html', {'graphic': graphic})


def users_ages(request):
    # Obtener los datos de las tablas
    users = User.objects.all().values()
    users_df = pd.DataFrame(users)

    # Calcular las edades a partir de las fechas de nacimiento
    current_date = datetime.now()
    users_df['birth_date'] = pd.to_datetime(users_df['birth_date'])
    users_df['age'] = current_date.year - users_df['birth_date'].dt.year - \
                      (current_date.month < users_df['birth_date'].dt.month) - \
                      ((current_date.month == users_df['birth_date'].dt.month) & \
                       (current_date.day < users_df['birth_date'].dt.day))

    # Calcular los bordes de los bins
    min_age = users_df['age'].min()
    max_age = users_df['age'].max()
    bin_edges = list(range(min_age, max_age + 6, 5))  # Incremento de 5 años

    # Crear el gráfico de barras de la distribución de edades
    plt.figure(figsize=(10, 6))
    plt.hist(users_df['age'], bins=bin_edges, edgecolor='black')
    plt.title('Distribución de edades de los usuarios')
    plt.xlabel('Edad')
    plt.ylabel('Cantidad de Usuarios')

    plt.yticks(range(int(users_df.count().max()) + 1))

    # Establecer los límites del eje X para comenzar desde la edad mínima
    plt.xlim(min_age, max_age + 1)

    # Establecer las marcas del eje X manualmente
    plt.xticks([18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])

    # Guardar el gráfico en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen a base64 para pasarla a la plantilla
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'user/users_ages.html', {'graphic': graphic})


def sold_products(request):
    # Obtener los datos de las tablas
    products_data = Product.objects.all().values()
    products_df = pd.DataFrame(products_data)
    
     # Realizar el conteo de valores en la columna sold
    products_counts = products_df.groupby('title')['sold'].sum()

     # Obtener todos los productos posibles
    all_products = products_df['title'].tolist()

    # Crear un DataFrame con todos los productos y establecer el conteo en cero para aquellas que no estén presentes
    all_products_counts = pd.Series({product: products_counts.get(product, 0) for product in all_products})

    # Crear el gráfico de barras
    plt.figure(figsize=(15, 10))
    all_products_counts.plot(kind='bar')
    plt.title('Productos vendidos en los trueques')
    plt.xlabel('Productos')
    plt.ylabel('Cantidad vendidos')

    plt.yticks(range(int(all_products_counts.max()) + 1))

    plt.xticks(rotation=25, ha='right')

    # Guardar el gráfico en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Convertir la imagen a base64 para pasarla a la plantilla
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'user/sold_products.html', {'graphic': graphic})


def upload_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            selected_product = form.cleaned_data['titulo']
            selected_product.sold += int(request.POST['sold'])
            selected_product.save()
            return redirect('ask_to_upload_sale')
    else:
        form = SaleForm()
    return render(request, 'user/upload_sale.html', {'form': form})

def ask_to_upload_sale(request):
    return render(request, 'user/ask_to_upload_sale.html', {})