from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cartId = request.session.session_key
    if not cartId:
        cartId = request.session.create()
    return cartId

def cart(request, total=0, shipping_charge = 70.0, cart_items=None):
    total_amt = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
        if total>999.0:
            shipping_charge = 0.0
        total_amt = total + shipping_charge
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'shipping_charge': shipping_charge,
        'total_amt': total_amt,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, shipping_charge = 70.0, cart_items=None):
    total_amt = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
        if total>999.0:
            shipping_charge = 0.0
        total_amt = total + shipping_charge
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'shipping_charge': shipping_charge,
        'total_amt': total_amt,
        'cart_items': cart_items,
    }
    return render(request, "cart/checkout.html", context)


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=request.user).exists()
        if is_cart_item_exists:
            cartItem = CartItem.objects.get(product=product, user=request.user)
            cartItem.quantity += 1
            cartItem.save()
        else:
            # CartItem
            cartItem = CartItem.objects.create(product=product, user=request.user, quantity=1)
            cartItem.save()
        return redirect('cart')
    else:
        # cart
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cartItem = CartItem.objects.get(product=product, cart=cart)
            cartItem.quantity += 1
            cartItem.save()
        else:
            # CartItem
            cartItem = CartItem.objects.create(product=product, cart=cart, quantity=1)
            cartItem.save()
        return redirect('cart')
    

def decrement_cart_item_quantity(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity>1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')






