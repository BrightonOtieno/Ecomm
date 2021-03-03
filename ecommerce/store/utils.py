import json
from .models import *


# Deals with guest user logic
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}


    print('cart:',cart)
    order_items = []
    order = {
        'get_cart_total':0,
        'get_total_items':0
        }
    cartItems = order['get_total_items']

    # i is the productId
    for i in  cart:
        try:
            cartItems += cart[i]['quantity']

            # building the order
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_total_items'] += cart[i]['quantity']

            order_item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }

            order_items.append(order_item)

            # take care of shipping status
            if product.digital == False:
                order["shipping"] = True

        except:
            # if there is an error in the db query-> pass it shouldn't break the code // bcz id is still in cart but it was removed from db   
            pass

    return {'cartItems':cartItems,'order':order,'order_items':order_items}

# handles the  type of users if .....else ....
def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        #order = Order.objects.get(customer=customer,complete=False)
        # get all orderitems associated with that order
        # orderitem has -> individual item/product and its quantity
        order_items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        # if user is not logged in  
        # pass in empty order_items and order
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        order_items = cookieData['order_items']
                
    return {'cartItems':cartItems,'order':order,'order_items':order_items}



# handled guest orders from checkout
def guestOrder(request,data):
    print('User is not logged in')
    print('COOKIES:',request.COOKIES)
    # data -> all data from checkout Form they filled
    name = data['form']['name']
    email = data['form']['email']
    # cookieCart -> gives a dictionary representation of order,orderitems..
    cookieData = cookieCart(request)
    order_items = cookieData['order_items']
    #
    customer,created =  Customer.objects.get_or_create(
        email = email
    )
    customer.name = name # they might change name through the form
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete = False # will be True when paypal processes payment successfully
    )

    # loop through the fabricated order_items and save them to db
    # individual  order_item has product and order its accossiated with

    for order_item in order_items:
        product = Product.objects.get(id=order_item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=order_item['quantity']
        )
    
    return customer,order