from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category, Customer, Order, OrderItem
from .forms import ProductForm, CategoryForm, LoginForm, RegistrationForm, OrderForm, OrderItemForm
import time  # Para generar IDs de transacción

# Función para verificar si un usuario es administrador
def is_admin(user):
    """Verifica permisos de administrador."""
    return user.is_staff

# Vistas de autenticación
def login_view(request):
    """Procesa inicio de sesión y redirecciona según tipo de usuario."""
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
    """Procesa registro de nuevos usuarios."""
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
    """Cierra sesión y redirecciona a login."""
    logout(request)
    return redirect('login')

# Store main views
def store(request):
    """Muestra productos y categorías disponibles."""
    products = Product.objects.filter(is_available=True)  # Solo productos disponibles
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'store/store.html', context)

def customer_product_detail(request, pk):
    """Muestra detalle de producto y productos relacionados."""
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]  # Máximo 4 productos relacionados
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'store/customer_product_detail.html', context)

def customer_category_detail(request, pk):
    """Muestra categoría y sus productos disponibles."""
    category = get_object_or_404(Category, pk=pk)
    products = category.products.filter(is_available=True)  # Solo productos disponibles
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/customer_category_detail.html', context)

# Cart views
@login_required
def add_to_cart(request, product_id):
    """Añade producto al carrito o incrementa cantidad."""
    product = get_object_or_404(Product, id=product_id)
    
    # Obtener o crear un pedido en estado pendiente para el usuario
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, 
        complete=False,
        defaults={'status': 'pending'}
    )
    
    # Buscar si el producto ya está en el carrito
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 1}
    )
    
    # Si el producto ya estaba en el carrito, aumentar la cantidad
    if not created:
        order_item.quantity += 1
        order_item.save()
    
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('customer_product_detail', pk=product_id)

@login_required
def update_cart(request, product_id, action):
    """Actualiza cantidad de producto en carrito."""
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=False).first()
    
    if order:
        order_item = OrderItem.objects.filter(order=order, product=product).first()
        
        if order_item:
            if action == 'increase':
                order_item.quantity += 1
            elif action == 'decrease':
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                else:
                    order_item.delete()
                    messages.success(request, f"{product.name} removed from your cart.")
                    return redirect('cart')
            
            order_item.save()
            messages.success(request, "Cart updated successfully.")
    
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    """Elimina producto del carrito."""
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=False).first()
    
    if order:
        OrderItem.objects.filter(order=order, product=product).delete()
        messages.success(request, f"{product.name} removed from your cart.")
    
    return redirect('cart')

@login_required
def cart(request):
    """Muestra carrito de compras actual."""
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=False).first()
    
    if order:
        cart_items = order.orderitem_set.all()
        cart_total = order.get_cart_total
    else:
        cart_items = []
        cart_total = 0
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'store/cart.html', context)

@login_required
def checkout(request):
    """Procesa página de pago y finalización de pedido."""
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=False).first()
    
    if request.method == 'POST':
        # Procesar la orden cuando se envía el formulario
        if order:
            order.complete = True
            order.status = 'processing'
            order.transaction_id = f"TX-{int(time.time())}"  # Generar ID único basado en timestamp
            order.shipping_address = request.POST.get('shipping_address', '')
            order.save()
            
            messages.success(request, "Your order has been placed successfully!")
            return redirect('store')
    
    # Preparar datos para mostrar en la página de checkout
    if order:
        cart_items = order.orderitem_set.all()
        cart_total = order.get_cart_total
    else:
        cart_items = []
        cart_total = 0
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'store/checkout.html', context)

# Admin dashboard
@user_passes_test(is_admin)
def dashboard(request):
    """Dashboard administrativo con estadísticas."""
    # Contadores para las tarjetas de estadísticas
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    order_count = Order.objects.count()
    
    # Datos para las tablas de resumen
    products = Product.objects.all().order_by('-created_at')
    orders = Order.objects.all().order_by('-date_ordered')
    
    context = {
        'product_count': product_count,
        'category_count': category_count,
        'order_count': order_count,
        'products': products,
        'orders': orders
    }
    return render(request, 'store/dashboard/dashboard.html', context)

# Product CRUD operations
@user_passes_test(is_admin)
def product_list(request):
    """Lista productos para administración."""
    products = Product.objects.all()
    return render(request, 'store/dashboard/product_list.html', {'products': products})

@user_passes_test(is_admin)
def product_detail(request, pk):
    """Detalle de producto para administración."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/dashboard/product_detail.html', {'product': product})

@user_passes_test(is_admin)
def product_create(request):
    """Crea nuevo producto."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES para manejar la imagen
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
    """Actualiza producto existente."""
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
    """Elimina producto con confirmación."""
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
    """Lista categorías para administración."""
    categories = Category.objects.all()
    return render(request, 'store/dashboard/category_list.html', {'categories': categories})

@user_passes_test(is_admin)
def category_detail(request, pk):
    """Detalle de categoría y sus productos."""
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()  # Todos los productos de esta categoría
    return render(request, 'store/dashboard/category_detail.html', {
        'category': category,
        'products': products
    })

@user_passes_test(is_admin)
def category_create(request):
    """Crea nueva categoría."""
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
    """Actualiza categoría existente."""
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
    """Elimina categoría con confirmación."""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'store/dashboard/category_confirm_delete.html', {'category': category})

# Order CRUD operations
@user_passes_test(is_admin)
def order_list(request):
    """Lista órdenes para administración."""
    orders = Order.objects.all()
    return render(request, 'store/dashboard/order_list.html', {'orders': orders})

@user_passes_test(is_admin)
def order_detail(request, pk):
    """Detalle de orden y sus productos."""
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/dashboard/order_detail.html', {'order': order})

@user_passes_test(is_admin)
def order_update(request, pk):
    """Actualiza estado y dirección de orden."""
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order #{order.id} updated successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'store/dashboard/order_form.html', {
        'form': form,
        'order': order,
        'title': f'Edit Order #{order.id}'
    })

@user_passes_test(is_admin)
def order_delete(request, pk):
    """Elimina orden con confirmación."""
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        order_id = order.id
        order.delete()
        messages.success(request, f'Order #{order_id} deleted successfully!')
        return redirect('order_list')
    
    return render(request, 'store/dashboard/order_confirm_delete.html', {'order': order})

@user_passes_test(is_admin)
def add_order_item(request, pk):
    """Añade producto a una orden."""
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)  # No guardar inmediatamente
            item.order = order  # Asignar la orden al ítem
            item.save()  # Ahora guardar
            messages.success(request, 'Item added to the order successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderItemForm()
    
    return render(request, 'store/dashboard/order_item_form.html', {
        'form': form,
        'order': order,
        'title': f'Add Item to Order #{order.id}'
    })

@user_passes_test(is_admin)
def edit_order_item(request, pk):
    """Edita producto de una orden."""
    item = get_object_or_404(OrderItem, pk=pk)
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order item updated successfully!')
            return redirect('order_detail', pk=item.order.pk)
    else:
        form = OrderItemForm(instance=item)
    
    return render(request, 'store/dashboard/order_item_form.html', {
        'form': form,
        'item': item,
        'order': item.order,
        'title': f'Edit Item in Order #{item.order.id}'
    })

@user_passes_test(is_admin)
def delete_order_item(request, pk):
    """Elimina producto de una orden."""
    item = get_object_or_404(OrderItem, pk=pk)
    order = item.order
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Order item removed successfully!')
        return redirect('order_detail', pk=order.pk)
    
    return render(request, 'store/dashboard/order_item_confirm_delete.html', {
        'item': item,
        'order': order
    })

@login_required
def my_account(request):
    """Gestiona perfil del usuario."""
    customer = request.user.customer
    
    if request.method == 'POST':
        # Actualizar usuario
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        # Actualizar cliente
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.save()
        
        messages.success(request, "Your account information has been updated successfully!")
        return redirect('my_account')
    
    context = {
        'user': request.user,
        'customer': customer
    }
    return render(request, 'store/my_account.html', context)

@login_required
def my_orders(request):
    """Lista pedidos del usuario."""
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer).order_by('-date_ordered')
    
    context = {
        'orders': orders
    }
    return render(request, 'store/my_orders.html', context)

@login_required
def order_customer_detail(request, pk):
    """Detalle de pedido específico."""
    customer = request.user.customer
    order = get_object_or_404(Order, pk=pk, customer=customer)  # Asegurar que el pedido pertenece al cliente
    
    context = {
        'order': order
    }
    return render(request, 'store/order_customer_detail.html', context)