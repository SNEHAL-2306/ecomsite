from django.shortcuts import render, get_object_or_404,redirect,render
from .models import Product, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST




@login_required(login_url='login')
def product_list(request):
    print("User is:", request.user)

    category_id = request.GET.get('category')
    if category_id:
        products   = Product.objects.filter(category_id=category_id)
    else:
        products   = Product.objects.all()
    categories  = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_cat': category_id
    })



def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request,'store/product_detail.html',{'product': product})




def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'quantity': 1}

    request.session['cart'] = cart

    messages.success(request, "Product added to cart!")

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id_str, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))
        quantity = item.get('quantity', 1)
        item_total = product.price * quantity
        total_price += item_total

        # ✅ Append only one entry per product
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,  # ✅ changed from 'products'
        'total_price': total_price
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    
    return redirect('cart')

def clear_cart(request):
    request.session['cart'] = {}  # Set to empty dict
    return redirect('cart')

@require_POST
def custom_logout_view(request):
    logout(request)
    return redirect('goodbye')


def goodbye_view(request):
    return render(request, 'store/goodbye.html')