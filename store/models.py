# store/models.py
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])


class Product(models.Model):
    # Coffee product choices
    ROAST_CHOICES = [
        ('light', 'Light Roast'),
        ('medium', 'Medium Roast'),
        ('dark', 'Dark Roast'),
        ('espresso', 'Espresso Roast'),
    ]
    
    FORMAT_CHOICES = [
        ('whole_bean', 'Whole Bean'),
        ('ground', 'Ground'),
        ('capsule', 'Capsules'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    roast_level = models.CharField(max_length=20, choices=ROAST_CHOICES)
    origin = models.CharField(max_length=100)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    weight = models.IntegerField(help_text="Weight in grams")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])