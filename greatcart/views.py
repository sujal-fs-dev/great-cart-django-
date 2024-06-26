from django.shortcuts import render
from store.models import product  

def home(request):
    products = product.objects.filter(is_available=True)  # Correct field name

    context = {
        'products': products
    }
    return render(request, 'home.html', context)
