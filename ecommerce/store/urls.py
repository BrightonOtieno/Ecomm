from django.urls import path
from .views import cart,checkout,store,updateItem,processOrder
urlpatterns = [
    path('', store,name='store'),
    path('cart', cart,name='cart'),
    path('checkout', checkout,name='checkout'),
    path('update-item/', updateItem,name='update-item'),
    path('process-order/',processOrder,name='process-order'),
]