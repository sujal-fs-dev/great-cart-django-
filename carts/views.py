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
    product_instance = get_object_or_404(product, id=product_id)
    product_variation = []

    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product_instance,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    try:
        cart_instance = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_instance = Cart.objects.create(cart_id=_cart_id(request))
        cart_instance.save()
    is_cart_item_exists=CartItem.objects.filter(product=product_instance, cart=cart_instance).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product_instance,  cart=cart_instance)

        ex_var_list=[]
        id=[]
        for item in cart_item:
            existing_var_list=item.variation.all()
            ex_var_list.append(list(existing_var_list))
            id.append(item.id)

        print(ex_var_list)

        if product_variation in ex_var_list:
           #increase queantity
           index=existing_var_list.index(product_variation)
           item_id=id[index]
           item=CartItem.objects.get(product=product_instance, id=item_id)
           item.quantity +=1
           item.save()

        
        else:

         if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        #cart_item.quantity += 1
        cart_item.save()
    else :
        cart_item = CartItem.objects.create(
            product=product_instance,
            quantity=1,
            cart=cart_instance,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
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
