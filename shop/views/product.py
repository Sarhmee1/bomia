from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from shop.models import Category, Product
from shop.forms import CartAddProductForm, SearchForm
from django.contrib.postgres.search import SearchVector


def product_list(request, category_slug=None):
    try:
        category = None
        categories = Category.objects.all()
        product_l = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(
                Category, 
                slug=category_slug)
            product_l = product_l.filter(category=category)

        paginator = Paginator(product_l, 9)
        page_number = request.GET.get('page', 1)
        products = paginator.get_page(page_number)

        return render(request,
            'shop/product/list.html',
            {'category': category,
            'categories': categories,
            'products': products})
    except Exception as e:
        return HttpResponse("Error: {}".format(str(e)), status=500)

# def product_detail(request, id, slug):
#     try:
#         product = get_object_or_404(
#             Product,
#             id=id,
#             slug=slug,
#             available=True)
#         cart_product_form = CartAddProductForm()

#         return render(request,
#             'shop/product/detail.html',
#             {'product': product,
#             'cart_product_form': cart_product_form})
#     except Exception as e:
#         return HttpResponse("Error: {}".format(str(e)), status=500)

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

def product_detail(request, id, slug):
    try:
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        
        # Check if the product has a valid slug
        if not product.slug:
            # Log a warning or handle this case differently based on your requirements
            return HttpResponse("Product has an empty slug.", status=400)  

        cart_product_form = CartAddProductForm()
        return render(request, 'shop/product/detail.html', {
            'product': product,
            'cart_product_form': cart_product_form
        })
    except Product.DoesNotExist:
        return HttpResponse("Product not found.", status=404)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)



from django.shortcuts import render
from shop.forms import SearchForm
from shop.models import Product
from django.http import HttpResponse

def product_search(request):
    try:
        form = SearchForm()
        query = None
        results = []

        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                # Perform case-insensitive search on the 'name' field
                results = Product.objects.filter(name__icontains=query)

        return render(request,
                      'shop/product/search.html',
                      {'form': form,
                       'query': query,
                       'results': results})
    except Exception as e:
        return HttpResponse("Error: {}".format(str(e)), status=500)
