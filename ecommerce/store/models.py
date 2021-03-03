from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)

    name = models.CharField( max_length=200,null=True)
    email = models.CharField( max_length=200,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital =  models.BooleanField(default=False,null=True,blank=True)
    #TODO:add image field
    image = models.ImageField(null=True,blank=True)

    @property
    def imageURL (self):
        try:
            url= self.image.url 
        except:
            url =  ''
        return url


    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=200,null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([order_item.get_total for order_item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.product.digital == False:
                shipping=True
        
        return shipping
            


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([order_item.quantity for order_item in orderitems])
        return total

    def __str__(self):
        return self.customer.name
        #return str(self.id)
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f"{self.quantity} of {self.product}"
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address
    
    


