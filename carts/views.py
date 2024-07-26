from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from carts.models import CartItem, Cart
from store.models import product,Variation
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key  # Fetch the session key again after creation
    return cart_id



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
    
    
        

   
    
   
   
     try:
        cart_instance = Cart.objects.get(cart_id=_cart_id(request))
     except Cart.DoesNotExist:
        cart_instance = Cart.objects.create(cart_id=_cart_id(request))
        cart_instance.save()
    
     try:
        cart_item = CartItem.objects.get(product=product_instance, cart=cart_instance)
        cart_item.quantity += 1
        cart_item.save()
     except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product_instance,
            quantity=1,
            cart=cart_instance,
        )
        cart_item.save()
   
    
     return redirect('cart')

def remove_cart_item(request, product_id):
    from store.models import product
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def remove_cart(request, product_id):
    from store.models import product
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(product, id=product_id)  # Corrected to 'Product'
    cart_item = CartItem.objects.get(product=product, cart=cart)
   
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

def cart(request, total=0, quantity=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity
    except  ObjectDoesNotExist:
        pass    #type ignore

    tax=(2*total/100)
    grand_total=total+tax
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
        
    }



    return render(request, 'store/cart.html', context)
