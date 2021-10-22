from django.db import models
from django.contrib.auth.models import User
#class names should be capitalized while fields are in lowercase
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products', default= 'pox.jpg')
    
    def __str__(self):
        return self.title

    class Meta:
        db_table ='Category'
        managed = True
        verbose_name ='Category'
        verbose_name_plural ='Categories'

    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(upload_to='products', default='pix.jpg')
    description = models.TextField()
    featured = models.BooleanField()
    latest = models.BooleanField()
    available = models.BooleanField()
    min = models.IntegerField(default=1)
    max = models.IntegerField(default=20)

    def __str__(self):
        return self.name

class Carousel(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='products',default='pix.jpg')
    
    def __str__(self):
        return self.title



class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket_no = models.CharField(max_length=36)
    quantity = models.IntegerField()
    paid_order = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    basket_no = models.CharField(max_length=36)
    pay_code = models.CharField(max_length=36)
    paid_order = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    
