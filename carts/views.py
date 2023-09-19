from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def _cart_id(request):
    cartId = request.session.session_key
    if not cartId:
        cartId = request.session.create()
    return cartId

def cart(request, total=0, shipping_charge = 70.0, cart_items=None):
    total_amt = 0
    try:
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

def checkout(request):
    return render(request, "cart/checkout.html")

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass            
    # Cart
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

    # CartItem
    # check if the item already exists in the cart
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        # if the item already exists in the cart 
        # check whether the item with the same variations exists or not
        # true -> increase the quantity of that item
        # false -> create a new cart item
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if product_variation in ex_var_list:
            # find the exact cart_item present in the cart with the same variation. For that we need the cart id. And increase the item quantity.
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variation)>0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()             
    return redirect('cart')

def decrement_cart_item_quantity(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    try:
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
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


