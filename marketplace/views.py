from django.shortcuts import render, get_object_or_404, HttpResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    
    
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items= Cart.objects.filter(user=request.user)
    else:
        cart_items= None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        # Check if food item exists
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem =FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart= Cart.objects.get(user= request.user,fooditem=fooditem)
                    # Increase the card quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({"status":'Success','message':'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request) })
                except:
                    chkCart = Cart.objects.create(user= request.user,fooditem=fooditem ,quantity=1)
                    return JsonResponse({"status":'Success','message':'Added food to cart!', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request) })
 
                    
            except:
                return JsonResponse({"status":'Failed','message':'This food does not exist!'})
        else:
            return JsonResponse({"status":'Failed','message':'invalid request'})
    else:
    
        return JsonResponse({"status":'login_required','message':'Please Login to continue'})
    

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
    # Check if food item exists
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem =FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart= Cart.objects.get(user= request.user,fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # Decreased the card quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({"status":'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request) })
                except:
                    return JsonResponse({"status":'Failed','message':'You do not have this item in your card' })
 
            except:
                return JsonResponse({"status":'Failed','message':'This food does not exist!'})
        else:
            return JsonResponse({"status":'Failed','message':'invalid request'})
    else:
        
        return JsonResponse({"status":'login_required','message':'Please Login to continue'})



@login_required(login_url =  'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('create_at')

    context = {
        'cart_items': cart_items
        }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user= request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status":'Success','message':'Card item has been deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request) })
            except:
                return JsonResponse({"status":'Failed','message':'This cart item does not exist!'})
        else:
            return JsonResponse({"status":'Failed','message':'invalid request'})












