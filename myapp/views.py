from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.forms import PayPalPaymentsForm
import uuid

from .models import Product, Category, Cart, CartItem, Wishlist, ShippingAddress
from .forms import RegistrationForm, SearchForm, WishlistForm, ShippingAddressForm

def home(request):
    """View to display home page with all products."""
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def about(request):
    """View to display the about page."""
    return render(request, 'about.html')

def product_detail(request, pk):
    """View to display details of a specific product."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_page.html', {'product': product})

def category_view(request, food):
    """View to display products in a specific category."""
    food = food.replace('-', ' ')
    try:
        category = Category.objects.get(name=food)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category': category, 'products': products})
    except Category.DoesNotExist:
        messages.error(request, 'That category does not exist.')
        return redirect('home')

def register(request):
    """View to handle user registration."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """View to handle user login."""
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    """View to handle user logout."""
    logout(request)
    return redirect('user_login')

def search_view(request):
    """View to handle product search."""
    form = SearchForm()
    query = None
    results = []
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(name__icontains=query)
    return render(request, 'search.html', {'form': form, 'query': query, 'results': results})

@login_required
def add_shipping_address(request):
    """View to add a new shipping address."""
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('shipping_address_list')
    else:
        form = ShippingAddressForm()
    return render(request, 'add_shipping_address.html', {'form': form})

@login_required
def shipping_address_list(request):
    """View to display list of shipping addresses for a user."""
    addresses = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'shipping_address_list.html', {'addresses': addresses})

@login_required
def wishlist_view(request):
    """View to display and edit the wishlist."""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist)
        if form.is_valid():
            form.save()
            return redirect('wishlist')
    else:
        form = WishlistForm(instance=wishlist)
    return render(request, 'wishlist.html', {'form': form, 'wishlist': wishlist})

@login_required
def remove_from_wishlist(request, product_id):
    """View to remove a product from the wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')

@csrf_exempt
def paypal_ipn(request):
    """Endpoint to handle PayPal IPN."""
    return HttpResponse("PayPal IPN endpoint")

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    """Handle PayPal payment notifications."""
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            return
        try:
            cart = Cart.objects.get(user=request.user)
            cart.is_paid = True
            cart.save()
        except Cart.DoesNotExist:
            pass

def payment_success(request):
    """View to display payment success."""
    return render(request, 'payment_success.html')

def payment_failed(request):
    """View to display payment failure."""
    return render(request, 'payment_failed.html')


@login_required
def checkout(request, product_id):
    """View to handle checkout process."""
    product = get_object_or_404(Product, id=product_id)
    host = request.get_host()

    total_price = request.GET.get('total_price', product.price)  # Get the total_price from the query params or use product price

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_price,
        'item_name': product.name,
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success')}",
        'cancel_url': f"http://{host}{reverse('payment-failed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'product': product,
        'total_price': total_price,
        'paypal': paypal_payment
    }

    return render(request, 'saviourj.html', context)











from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')  # Redirect to cart detail view or any desired page

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'saviour.html', context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item.quantity = max(1, quantity)
        cart_item.save()
    return redirect('cart_detail')
