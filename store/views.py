
from django.shortcuts import render, get_object_or_404
from .models import category, product  # Correct import names

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(category, slug=category_slug)
        products = product.objects.filter(category=categories, is_available=True)
        product_count = products.count()  # Count of filtered products

        context = {
            'products': products,
            'category': categories,
            'product_count': product_count
        }
    else:
        products = product.objects.filter(is_available=True)
        product_count=products.count()
        context = {
            'products': products,
            'product_count': product_count
           

        }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product=product.objects.get(category__slug=category_slug, slug=product_slug)
    
    except Exception as e:
        raise e
    
    context={

        'single_product':single_product


    }
    return render(request, 'store/product_detail.html', context)
   
