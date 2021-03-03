from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData,guestOrder
# Create your views here.
def store(request): 

    data = cartData(request)
    cartItems = data['cartItems']


    products = Product.objects.all()
    context ={
        'products':products,
        'cartItems':cartItems,
        'shipping':False
    }
    
    
    return render(request,'store/store.html',context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    order_items = data['order_items']



    context ={
        'order_items':order_items,
        'order':order,
        'cartItems':cartItems,
        'shipping':False
    }
    return render(request,'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    order_items = data['order_items']

    context ={
        'order_items':order_items,
        'order':order,
        'cartItems':cartItems,
        'shipping':False
    }
    
    return render(request,'store/checkout.html',context)


def updateItem(request):
    #print(request.body)
    data = json.loads(request.body)
    #print(data) 
    productId = data['productId']
    action = data['action']
    
    print('Action',action)
    print('productId',productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    #order = Order.objects.get(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action =="remove":
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item added',safe=False)
    



def processOrder(request):
    #print('Data',request.body)
    # use timestamp for transaction ID
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # for LOGGED-IN users
    if request.user.is_authenticated:
        customer = request.user.customer
        #TODO: get or create or get ord 404
        order,created = Order.objects.get_or_create(customer=customer,complete = False)
        #order = Order.objects.get(customer=customer,complete = False)
        

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address= data['shippingInfo']['address'],
                city = data['shippingInfo']['city'],
                state = data['shippingInfo']['state'],
                zipcode = data['shippingInfo']['zipcode'],

            )

            #ShippingAddress.save()

    # if user is not logged in (GUEST)
    else:
        customer,order = guestOrder(request,data)

    # regardless of who is checking out (logged in user or guest) 
    # we can still access this values
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

        # put a measure in place (don't acceptmanipulated total) 

    if total == float(order.get_cart_total):
        order.complete =True
        #order.save()
    # regardless we save order  whether complete or not

    order.save()
    return JsonResponse('payment submitted successfully',safe=False)
