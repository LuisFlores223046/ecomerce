from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'roast_level', 'format']
    list_filter = ['category', 'roast_level', 'format', 'is_available']
    search_fields = ['name', 'description', 'origin']
    list_editable = ['price', 'stock', 'is_available']