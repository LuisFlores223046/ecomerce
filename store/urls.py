from django.urls import path
from . import views

# URLs para autenticación
auth_urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]

# URLs para clientes
customer_urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/<int:pk>/', views.customer_product_detail, name="customer_product_detail"),
    path('category/<int:pk>/', views.customer_category_detail, name="customer_category_detail"),
]

# URLs para el panel de administración
admin_urlpatterns = [
    path('admin-dashboard/', views.dashboard, name="dashboard"),
    path('admin-dashboard/products/', views.product_list, name="product_list"),
    path('admin-dashboard/products/new/', views.product_create, name="product_create"),
    path('admin-dashboard/products/<int:pk>/', views.product_detail, name="product_detail"),
    path('admin-dashboard/products/<int:pk>/edit/', views.product_update, name="product_update"),
    path('admin-dashboard/products/<int:pk>/delete/', views.product_delete, name="product_delete"),
    
    path('admin-dashboard/categories/', views.category_list, name="category_list"),
    path('admin-dashboard/categories/new/', views.category_create, name="category_create"),
    path('admin-dashboard/categories/<int:pk>/', views.category_detail, name="category_detail"),
    path('admin-dashboard/categories/<int:pk>/edit/', views.category_update, name="category_update"),
    path('admin-dashboard/categories/<int:pk>/delete/', views.category_delete, name="category_delete"),
]

# Combinar todas las URLs
urlpatterns = auth_urlpatterns + customer_urlpatterns + admin_urlpatterns