from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    
    # Product CRUD URLs
    path('products/', views.product_list, name="product_list"),
    path('products/new/', views.product_create, name="product_create"),
    path('products/<int:pk>/', views.product_detail, name="product_detail"),
    path('products/<int:pk>/edit/', views.product_update, name="product_update"),
    path('products/<int:pk>/delete/', views.product_delete, name="product_delete"),
    
    # Category CRUD URLs
    path('categories/', views.category_list, name="category_list"),
    path('categories/new/', views.category_create, name="category_create"),
    path('categories/<int:pk>/', views.category_detail, name="category_detail"),
    path('categories/<int:pk>/edit/', views.category_update, name="category_update"),
    path('categories/<int:pk>/delete/', views.category_delete, name="category_delete"),
]