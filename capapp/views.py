import uuid
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


from.models import Category, Product, Carousel, ShopCart, Payment
from . forms import SignupForm
#create your views here

def index(request):
    featured = Product.objects.filter(featured=True).filter(available=True)
    latest = Product.objects.filter(latest=True)
    available = Product.objects.filter(available=True)

    context = {
        'featured':featured,
        'latest':latest,
        'available':available,
    }

    return render(request, 'index.html', context)

def categories(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }
    return render(request, 'categories.html', context)


def single_category(request,id):
    category = Product.objects.filter(category_id=id)

    context={
        'category':category
    }

    return render(request, 'category.html', context)


def products(request):
    products = Product.objects.all().filter(available=True)

    context={
        'products':products
    }

    return render(request, 'products.html', context)

def single_product(request,id):
    details = Product.objects.get(pk=id)

    context={
        'details':details
    }

    return render(request, 'details.html', context)


def logoutt(request):
    logout(request)
    return redirect('loginform')

def loginform(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, 'You are now logged in as a user')
            return redirect('index')
        else:
            messages.info(request, 'Username/password incorrect')
            return redirect('loginform')

    return render(request, 'login.html')

def signupform(request):
    reg = SignupForm()
    if request.method=='POST':
        reg = SignupForm(request.POST)
        if reg.is_valid():
            reg.save()
            messages.success(request, 'Successfully!')
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect('signupform')
    
    context ={
        'reg':reg
    }

    return render(request, 'signup.html', context)

def password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Update Successful!')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('password')    

    context ={
        'form':form
    }
    return render(request, 'password.html', context)    

def addtocart(request):
    if request.method == 'POST':
        basket_num= str(uuid.uuid4())
        vol = int(request.POST['quantity'])
        pid = request.POST['itemid']
        item = Product.objects.get(pk=pid)
        cart = ShopCart.objects.filter(user__username= request.user.username, paid_order=False)
        if cart:
            basket = ShopCart.objects.filter(user__username=request.user.username, product_id=item.id).first()
            if basket:
                basket.quantity += vol # this runs when a product quantity is to be incremented
                basket.save()
                messages.success(request, 'Product added to Basket!')
                return redirect('products')
            else:
                newitem = ShopCart()  # this runs when a new item is added to the basket
                newitem.user = request.user
                newitem.product = item
                newitem.basket_no = cart[0].basket_no
                newitem.quantity = vol
                newitem.paid_order = False
                newitem.save()
                messages.success(request, 'Product added to Basket!')

        else:
            newbasket = ShopCart()  # this runs when a basket is to be created for the first time
            newbasket.user = request.user
            newbasket.product = item
            newbasket.basket_no = basket_num
            newbasket.quantity = vol
            newbasket.paid_order = False
            newbasket.save()
            messages.success(request, 'Product added to Basket!')
    return redirect('products')    

def cart(request):
    cart = ShopCart.objects.filter(user__username=request.user.username, paid_order=False)


    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.product.price * item.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total

    }
    return render(request, 'cart.html', context)

def checkout(request):
    cart = ShopCart.objects.filter(user__username=request.user.username, paid_order=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.product.price * item.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat

    context = {
        'cart':cart,
        'total':total,
        'cart_code':cart[0].basket_no
    }

    return render(request, 'checkout.html', context)

def placeorder(request):
    if request.method == 'POST':
        api_key = 'sk_test_55b070a7d173af2650b566ef4a1dc7194460ce5f'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://18.220.220.212/completed/'
        # cburl = 'http://localhost:8000/completed/'
        total = float(request.POST['total']) * 100
        cart_code = request.POST['cart_code']
        pay_code = str(uuid.uuid4())
        user = User.objects.get(username = request.user.username)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']

        # collect data that you will send to paystack
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':pay_code, 'email':user.email, 'amount': int(total), 'callback_url':cburl, 'order_number':cart_code}

        # make a call to paystack
        try:
            r= requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']

            paid = Payment()
            paid.user = user 
            paid.amount = total 
            paid.basket_no = cart_code
            paid.pay_code = pay_code
            paid.paid_order = True 
            paid.first_name = first_name
            paid.last_name = last_name
            paid.phone = phone 
            paid.address = address 
            paid.city = city 
            paid.state = state 
            paid.save()

            bag = ShopCart.objects.filter(user__username=request.user.username, paid_order=False)
            for item in bag:
                item.paid_order = True
                item.save()

                stock = Product.objects.get(pk=item.product.id)
                stock.max -= item.quantity
                stock.save()

            return redirect(rd_url)        
    return redirect('checkout')

def completed(request):
    user = User.objects.get(username= request.user.username)

    context={
        'user':user
    }
    return render(request, 'completed.html',context)

def deleteitem(request):
    itemid = request.POST['itemid']
    ShopCart.objects.filter(pk=itemid).delete()
    messages.success(request, 'Product deleted!')
    return redirect('cart')

def increase(request):
    itemval = request.POST['itemval']
    valid = request.POST['valid']
    update = ShopCart.objects.get(pk=valid)
    update.quantity = itemval
    update.save()
    messages.success(request, 'Product quantity updated successfully!')
    return redirect('cart')        
  