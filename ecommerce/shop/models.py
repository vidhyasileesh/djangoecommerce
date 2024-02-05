from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to="images/category",null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    image = models.ImageField(upload_to="images/product", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)

    def __str__(self):
        return self.name



