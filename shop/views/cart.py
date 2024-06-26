from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from shop.models import Product
from shop.cart import Cart
from shop.forms import CartAddProductForm

# Create your views here.

@require_POST
def cart_add(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product=product, 
                quantity=cd['quantity'], 
                update_quantity=cd['update'])
        return redirect('cart_detail')
    except Exception as e:
        return HttpResponse("Error: {}".format(str(e)), status=500)


def cart_remove(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart_detail')
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)

def cart_detail(request):
    try:
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'], 
                        'update': True})
        return render(request, 'cart/detail.html', {'cart': cart})
    except Exception as e:
        return HttpResponse("Error: {}".format(str(e)), status=500)
