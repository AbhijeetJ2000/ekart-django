from django.shortcuts import render, redirect
from .models import Address, Order
from carts.models import CartItem
import datetime

# Create your views here.
def payments(request):
    return render(request, 'orders/payments.html')

def place_order(request, total=0, shipping_charge=0):
    current_user = request.user
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    total = 0
    shipping_charge = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
    total_amt = total + shipping_charge
    if request.method == 'POST':
        # Handle the address
        address = Address()
        address.user = current_user
        address.first_name = request.POST['first_name']
        address.last_name = request.POST['last_name']
        address.email = request.POST['email']
        address.contact_number = request.POST['contact_number']
        address.address_line_1 = request.POST['address_line_1']
        address.address_line_2 = request.POST['address_line_2']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.country = request.POST['country']
        address.zip_code = request.POST['zip_code']
        address.save()

        # Handle the order
        order = Order()
        order.user = current_user
        order.address = address
        order.total = total
        order.shipping_charge = shipping_charge
        order.save()
        # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.save()

        context = {
            'address': address,
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'shipping_charge': shipping_charge,
            'total_amt': total_amt,
        }
        return render(request, "orders/payments.html", context)
    return redirect('checkout')





