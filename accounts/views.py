from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id
import requests


# Create your views here.
def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, phone_number=phone_number, password=password)
            user.save()
            messages.success(request, "Registration Successful.")
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, "accounts/register.html", context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    # find the current cart item list
                    curr_cart_item = CartItem.objects.filter(cart=cart)
                    # find the products associated with the current cart_item_list
                    curr_products = []
                    for item in curr_cart_item:
                        curr_products.append(item.product)
                    # find the user cart item list
                    user_cart_item = CartItem.objects.filter(user=user)
                    # find the products associated with the current cart_item_list
                    user_products = []
                    for item in user_cart_item:
                        user_products.append(item.product)
                    # check if the current_products exists in the user_products
                    for index, pr in enumerate(curr_products):
                        if pr in user_products:
                            # add the number of quantity
                            pr_index_in_user_cart = user_products.index(pr)
                            item_in_user_cart = user_cart_item[pr_index_in_user_cart]
                            item_in_curr_cart = curr_cart_item[index]
                            item_in_user_cart.quantity += item_in_curr_cart.quantity
                            item_in_user_cart.save()
                        else:
                            # assign the user to the cart item
                            item_in_curr_cart = curr_cart_item[index]
                            item_in_curr_cart.user = user
                            item_in_curr_cart.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')



