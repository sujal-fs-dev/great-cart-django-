from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from category.models import category
# Create your models here.
class product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug        =models.SlugField(max_length=200,unique=True)
    description =models.TextField(max_length=200,blank=True)
    price       =models.IntegerField()
    image       =models.ImageField(upload_to='photoes/products')
    stock       =models.IntegerField()
    is_available=models.BooleanField()
    category    =models.ForeignKey(category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug,self.slug])

    def __self__(self):

        return self.product_name
VARIATION_CATEGORY_CHOICES=(
        ('color', 'color'),
        ('size', 'size')
    )
class Variation(models.Model):
      product             =models.ForeignKey(product, on_delete=models.CASCADE)
      variation_category  =models.CharField(max_length=200, choices= VARIATION_CATEGORY_CHOICES) 
      variation_value     =models.CharField(max_length=100)
      is_active           =models.BooleanField(default=True)
      created_date        =models.DateField(auto_now=True)
      
      def __str__(self):
          return self.product
      
      


        
        
      