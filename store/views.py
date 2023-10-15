from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from carts.models import Cart, CartItem
from carts.views import _cart_id

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, "store/store.html", context)

def product_detail(request, category_slug, product_slug):
    single_product = Product.objects.get(slug=product_slug, category__slug=category_slug)
    if request.user.is_authenticated:
        is_cart_item_exits = CartItem.objects.filter(product=single_product, user=request.user).exists()
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        is_cart_item_exits = CartItem.objects.filter(product=single_product, cart=cart).exists()
    print(is_cart_item_exits)
    context = {
        'single_product': single_product,
        'is_cart_item_exits': is_cart_item_exits,
    }
    return render(request, "store/product_detail.html", context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
        else:
            products = None
            product_count = 0
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)





