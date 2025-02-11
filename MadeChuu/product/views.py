from django.shortcuts import render
from main.models import *
from .filters import ProductFilter, ShopFilter
from .forms import CartForm
from django.shortcuts import render , redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt


def product(request):
    categories = Category.objects.all()

    shop_filter = ShopFilter(request.GET, queryset=Shop.objects.all())
    
    # Combine the filtered results
    if shop_filter.qs.exists():
        selected_shops = shop_filter.qs
        product_filter = ProductFilter(request.GET, queryset=Product.objects.filter(shop__in=selected_shops))
        categories = Category.objects.filter(product__shop__in=selected_shops).distinct()
    else:
        product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
    filtered_products = product_filter.qs
    
    context = {
        'categories': categories,
        'filtered_products': filtered_products,
        'product_filter': product_filter,
        'shop_filter': shop_filter,
    }
    
    return render(request, 'product.html', context)

def add_cart(request , product_id):
    # test user session
    request.session['user_id'] = 17
    ## end test user session
    product = get_object_or_404(Product, product_id=product_id)
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect ('login')
    
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user_id=user_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product , quantity=quantity)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    cart.save()
    
    return redirect('product')