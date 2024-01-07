from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, CustomUser, Cart, CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserRegisterForm, CustomUserForm, AddProductForm
from django.db import transaction
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, "home.html")


def products(request):
    prods = Product.objects.all()
    p = Paginator(prods, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {'page_obj': page_obj}
    # context = {"products": prods}
    return render(request, "products.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        c_form = CustomUserForm(request.POST)
        if form.is_valid() and c_form.is_valid():
            with transaction.atomic():
                user = form.save()  # Save the User instance
                custom_user = c_form.save(commit=False)  # Create CustomUser instance but don't save yet
                custom_user.user = user  # Set the User instance for the CustomUser
                custom_user.save()  # Save the CustomUser instance with the user relationship
            return redirect('login')
    else:
        form = UserRegisterForm(initial=request.POST)  # Use request.POST to pre-fill the form
        c_form = CustomUserForm(initial=request.POST)
    return render(request, 'register.html', {'form': form, 'c_form': c_form})


def is_not_staff_user(user):
    return user.is_authenticated and not user.is_staff


@user_passes_test(is_not_staff_user)
def account(request):
    custom_user = CustomUser.objects.get(user=request.user)
    return render(request, "account.html", {'custom_user': custom_user})


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user)
def addproduct(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # product.photo = form.cleaned_data['photo']
            # product.save()
            return redirect('products')
    else:
        form = AddProductForm()
    return render(request, 'admin_account.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'products'))


@user_passes_test(is_staff_user)
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('products')


@user_passes_test(is_not_staff_user)
def cart(request):
    user_cart = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in user_cart)
    custom_user = CustomUser.objects.get(user=request.user)

    return render(request, 'cart.html', {'cart_items': user_cart, 'total_price': total_price, 'custom_user': custom_user})


@login_required
def update_cart(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(cart__user=request.user)
        for item in cart_items:
            new_quantity = int(request.POST.get(f'quantity_{item.id}', 0))
            if new_quantity > 0:
                item.quantity = new_quantity
                item.save()
    return redirect('cart')


@login_required
def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


def delivery(request):
    user_cart = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in user_cart)
    custom_user = CustomUser.objects.get(user=request.user)

    return render(request, "delivery_information.html",
                  {'cart_items': user_cart, 'total_price': total_price, 'custom_user': custom_user})


def confirmation(request):
    user_cart = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in user_cart)
    custom_user = CustomUser.objects.get(user=request.user)

    return render(request, "confirmation_information.html",
                  {'cart_items': user_cart, 'total_price': total_price, 'custom_user': custom_user})


def ordered(request):
    user_cart = CartItem.objects.filter(cart__user=request.user)
    user_cart.delete()
    return render(request, "order_confirmed.html")


def favicon_view(request):
    return HttpResponse(status=404)
