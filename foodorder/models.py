from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(max_length=30,widget=forms.PasswordInput)
    date=forms.DateField()

class Category(models.Model):
    category_name=models.CharField(max_length=100)
    category_discription=models.TextField(max_length=100)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    product_discription=models.CharField(max_length=200)
    product_price=models.IntegerField()
    image=models.ImageField(null=True)
    product_m=models.CharField(max_length=10,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    stock=models.IntegerField(default=100)

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

class cloth(models.Model):
    name=models.CharField(max_length=30)
    amount=models.CharField(max_length=30)
    payment_id=models.CharField(max_length=100)
    paid=models.BooleanField(default=False)
    
    class Meta:
        db_table='cloth'
