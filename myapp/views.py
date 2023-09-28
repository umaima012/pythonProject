from urllib import request

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from django.urls import reverse_lazy

from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.views import LoginView
from .forms import ProductSearchForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import RegistrationForm

def login_view(request):
    if request.method == 'POST':
        breakpoint()
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            # user = form.get_user()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            auth_login(request, user)
            return redirect('page')  # Redirect to a success page after login
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            # login(request, user)
            customer = Customer(user=user)
            customer.save()
            return redirect('page')  # Redirect to the page
    else:
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})




def page(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'myapp/page.html', context)

def form(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'myapp/form.html', context)

def categories(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'categories': categories, 'cartItems': cartItems}
    return render(request, 'myapp/categories.html', context)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'myapp/store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'myapp/cart.html', context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'myapp/checkout.html', context)

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'myapp/contact.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Orders.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = (Orders.objects.get_or_create(customer=customer, complete=False))

    else:
        customer, order = guestOrder(request, data)


    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
            email=email,
                )
    customer.name = name
    customer.save()

    order = Orders.objects.create(
            customer=customer,
            complete=False,
            )

    for item in items:
            product = Product.objects.get(id=item['id'])
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        Shipping.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)



def product_search(request):
    if request.method == 'GET':
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.filter(name__icontains=query)
        else:
            products = []
    else:
        form = ProductSearchForm()
        products = []

    context = {
        'form': form,
        'products': products,
    }
    return render(request, 'myapp/search.html', context)



def product_detail(request, product_slug):
    # Retrieve the product from the database using get_object_or_404
    product = get_object_or_404(Product, slug=product_slug)
    context = {
        'product': product,
    }

    return render(request, 'myapp/product_detail.html', context)
