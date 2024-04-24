from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from shop.models import OrderItem, Order
from shop.forms import OrderForm
from shop.cart import Cart


# Create your views here.

def order_create(request):
    try:
        cart = Cart(request)
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'])
                cart.clear()
            return render(request,
                    'orders/created.html',
                    {'order': order})
        else:
            form = OrderForm()
        return render(request,
            'orders/create.html',
            {'cart': cart, 'form': form})
    except Exception as e:
        return HttpResponse("Error: {}".format(str(e)), status=500)
    

def orders_list(request):
    try:
        orders = Order.objects.all()
        return render(request, 'orders/list.html', {'orders' : orders})
    except Exception as e:
        return HttpResponse("Error: {}".format(str(e)), status=500)

def orders_detail(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        customer = order.customer
        user = get_object_or_404(User, id=customer.pk)
        order_items = OrderItem.objects.filter(order_id=order.id)
        return render(request, 'orders/detail.html', {'order' : order, 'user': user, 'order_items': order_items})
    except Exception as e:
            return HttpResponse("Error: {}".format(str(e)), status=500)