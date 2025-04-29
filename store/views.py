from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category, Customer
from .forms import ProductForm, CategoryForm, LoginForm, RegistrationForm

# Función para verificar si un usuario es administrador
def is_admin(user):
    return user.is_staff

# Vistas de autenticación
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigir al dashboard si es admin, a la tienda si es cliente
                if user.is_staff:
                    return redirect('dashboard')
                else:
                    return redirect('store')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Por defecto, los usuarios registrados son clientes, no staff
            user.is_staff = False
            user.save()
            login(request, user)
            return redirect('store')
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Store main views
def store(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def customer_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'store/customer_product_detail.html', context)

def customer_category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.filter(is_available=True)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/customer_category_detail.html', context)

# Admin dashboard
@user_passes_test(is_admin)
def dashboard(request):
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    products = Product.objects.all().order_by('-created_at')
    
    context = {
        'product_count': product_count,
        'category_count': category_count,
        'products': products
    }
    return render(request, 'store/dashboard/dashboard.html', context)

# Product CRUD operations
@user_passes_test(is_admin)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/dashboard/product_list.html', {'products': products})

@user_passes_test(is_admin)
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/dashboard/product_detail.html', {'product': product})

@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'store/dashboard/product_form.html', {
        'form': form,
        'title': 'New Coffee Product'
    })

@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'store/dashboard/product_form.html', {
        'form': form,
        'product': product,
        'title': f'Edit {product.name}'
    })

@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'store/dashboard/product_confirm_delete.html', {'product': product})

# Category CRUD operations
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/dashboard/category_list.html', {'categories': categories})

@user_passes_test(is_admin)
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    return render(request, 'store/dashboard/category_detail.html', {
        'category': category,
        'products': products
    })

@user_passes_test(is_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()
    
    return render(request, 'store/dashboard/category_form.html', {
        'form': form,
        'title': 'New Category'
    })

@user_passes_test(is_admin)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'store/dashboard/category_form.html', {
        'form': form,
        'category': category,
        'title': f'Edit {category.name}'
    })

@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'store/dashboard/category_confirm_delete.html', {'category': category})