from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils.http import urlencode
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Brand, SiteSetting, Order, OrderItem
from .forms import UserRegisterForm
from .utils import send_order_email

def get_cart_data(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    count = 0
    
    products = Product.objects.filter(id__in=cart.keys())
    product_map = {str(p.id): p for p in products}
    
    for product_id, item_data in cart.items():
        product = product_map.get(str(product_id))
        if product:
            quantity = item_data.get('quantity', 0)
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
            count += quantity
            
    return {
        'cart_items': cart_items,
        'total': total,
        'cart_count': count
    }

def get_common_context(request):
    cart_data = get_cart_data(request)
    return {
        'settings': {s.setting_key: s.setting_value for s in SiteSetting.objects.all()},
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'cart_count': cart_data['cart_count']
    }

def home(request):
    context = get_common_context(request)
    context.update({
        'featured_products': Product.objects.filter(is_featured=True, stock_status='in_stock')[:8],
    })
    return render(request, 'store/home.html', context)

def shop(request):
    products = Product.objects.all()
    
    # Filter by Category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Filter by Brand
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Filter by Stock Status
    stock_status = request.GET.get('stock')
    if stock_status:
        products = products.filter(stock_status=stock_status)
        
    # Filter by Price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
        
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Sorting
    sort = request.GET.get('sort')
    if sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at') # Default

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = get_common_context(request)
    context.update({
        'page_obj': page_obj,
        'current_category': category_slug,
        'current_brand': brand_slug,
    })
    return render(request, 'store/shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = get_common_context(request)
    context.update({
        'product': product,
        'related_products': related_products,
    })
    return render(request, 'store/product_detail.html', context)

def cart(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        
        if action == 'add':
            quantity = int(request.POST.get('quantity', 1))
            if product_id in cart:
                cart[product_id]['quantity'] += quantity
            else:
                cart[product_id] = {'quantity': quantity}
            messages.success(request, 'Product added to cart!')
            
        elif action == 'update':
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart[product_id] = {'quantity': quantity}
                messages.success(request, 'Cart updated')
            else:
                if product_id in cart:
                    del cart[product_id]
                    
        elif action == 'remove':
            if product_id in cart:
                del cart[product_id]
                messages.success(request, 'Item removed from cart')
        
        request.session['cart'] = cart
        return redirect('cart')

    cart_data = get_cart_data(request)
    context = get_common_context(request)
    context.update(cart_data)
    
    return render(request, 'store/cart.html', context)

def checkout(request):
    cart_data = get_cart_data(request)
    if not cart_data['cart_items']:
        messages.error(request, 'Your cart is empty')
        return redirect('cart')

    if request.method == 'POST':
        # Create Order
        import uuid
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            order_number=order_number,
            customer_name=request.POST.get('customer_name'),
            customer_phone=request.POST.get('phone'),
            customer_address=request.POST.get('location'),
            payment_method=request.POST.get('payment_method', 'whatsapp'),
            total_amount=cart_data['total'],
            notes=request.POST.get('notes'),
            status='pending'
        )
        
        # Create Order Items
        for item in cart_data['cart_items']:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                product_price=item['product'].price,
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )
            
        # Clear Cart
        request.session['cart'] = {}
        
        # Send Confirmation Email
        send_order_email(order)
        
        return redirect('order_confirmation', order_number=order_number)
        
    context = get_common_context(request)
    context.update(cart_data)
    return render(request, 'store/checkout.html', context)

def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    # Get WhatsApp Number
    whatsapp_setting = SiteSetting.objects.filter(setting_key='whatsapp_number').first()
    whatsapp_number = whatsapp_setting.setting_value if whatsapp_setting else '254701511606'
    
    context = get_common_context(request)
    context.update({
        'order': order,
        'whatsapp_number': whatsapp_number
    })
    return render(request, 'store/order_confirmation.html', context)

def about(request):
    context = get_common_context(request)
    return render(request, 'store/about.html', context)

def contact(request):
    context = get_common_context(request)
    # Get WhatsApp number for the template
    whatsapp_setting = SiteSetting.objects.filter(setting_key='whatsapp_number').first()
    context['whatsapp_number'] = whatsapp_setting.setting_value if whatsapp_setting else '254701511606'
    return render(request, 'store/contact.html', context)

def privacy(request):
    return render(request, 'store/privacy.html', get_common_context(request))

def terms(request):
    return render(request, 'store/terms.html', get_common_context(request))

def warranty(request):
    return render(request, 'store/warranty.html', get_common_context(request))

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    context = get_common_context(request)
    context['form'] = form
    return render(request, 'store/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    context = get_common_context(request)
    context['form'] = form
    return render(request, 'store/login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
