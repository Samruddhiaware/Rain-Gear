from django.db import models
from django.db.models import Manager 


# Create your models here.
class Custommanager(models.Manager):     
    def filterdata(self, a):
        return super().get_queryset().filter(location=a)

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=500)    
    usertype = models.CharField(max_length=50) 
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50, default='area')
    city = models.CharField(max_length=50, default='city')
    state = models.CharField(max_length=50, default='state')
    pincode = models.BigIntegerField()
    contact = models.BigIntegerField()

    class Meta:
        db_table = 'user'

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media")
    features = models.CharField(max_length=250)
    category = models.CharField(max_length=50)
    seller = models.CharField(max_length=50)    
    price = models.FloatField()    
    status = models.CharField(max_length=50, default='pending')
    rating = models.FloatField(default='3.5')
    review = models.CharField(max_length=100, default='review')
    additional_info = models.CharField(max_length=300, default='additional info')

    productobj = Custommanager()
    objects = Manager()

    class Meta:
        db_table = 'product'

class cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalamount = models.FloatField()

    class Meta:
        db_table='cart'

class Order(models.Model):
    ordernumber = models.CharField(max_length=100)
    orderdate = models.DateField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phonenumber = models.BigIntegerField()
    pincode = models.BigIntegerField()
    orderstatus = models.CharField(max_length=50)

    class Meta:
        db_table = 'order'

class Payment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    paymentmode = models.CharField(max_length=100, default='paypal')
    paymentstatus = models.CharField(max_length=100, default='pending')
    transaction_id = models.CharField(max_length=200)    

    class Meta:
        db_table = 'payment'

class Orderdetail(models.Model):    
    ordernumber = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)   
    totalprice = models.IntegerField()
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'orderdetail'



