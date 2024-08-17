from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import OrderForm, CreateUserForm
from .models import *
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# View for user registration
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, "Account was created")
            return redirect('login')

    template = loader.get_template('accounts/register.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

# View for user login
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    template = loader.get_template('accounts/login.html')
    return HttpResponse(template.render(context, request))

# View for user logout
def logoutUser(request):
    logout(request)
    return redirect('login')

# Home page view with admin-only access
@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = Order.objects.filter(status="Delivered").count()
    pending = orders.filter(status='Pending').count()
    template = loader.get_template("accounts/dashboard.html")
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return HttpResponse(template.render(context, request))

# View for user profile page
def userPage(request):
    template = loader.get_template("accounts/user.html")
    return HttpResponse(template.render())

# View for account settings page
def accountSettings(request):
    template = loader.get_template("accounts/accountsettings.html")
    return HttpResponse(template.render())

# View for product listing with admin-only access
@login_required(login_url='login')
@admin_only
def products(request):
    products = Product.objects.all()
    template = loader.get_template("accounts/products.html")
    context = {"products": products}
    return HttpResponse(template.render(context, request))

# View for customer detail and filtering orders
@login_required(login_url='login')
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    template = loader.get_template("accounts/customer.html")
    context = {'customer': customer, 'orders': orders, 'myFilter': myFilter}
    return HttpResponse(template.render(context, request))

# View for creating orders with a formset
@login_required(login_url='login')
def createOrder(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=("product", "status"), extra=5)
    customer = Customer.objects.get(id=id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    template = loader.get_template("accounts/order_form.html")
    context = {'formset': formset}
    return HttpResponse(template.render(context, request))

# View for updating an existing order
@login_required(login_url='login')
def updateOrder(request, id):
    orders = Order.objects.get(id=id)
    form = OrderForm(instance=orders)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')

    template = loader.get_template('accounts/order_form.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

# View for deleting an existing order
@login_required(login_url='login')
def deleteOrder(request, id):
    orders = Order.objects.get(id=id)
    if request.method == 'POST':
        orders.delete()
        return redirect('/')
    template = loader.get_template('accounts/delete.html')
    context = {'orders': orders}
    return HttpResponse(template.render(context, request))
