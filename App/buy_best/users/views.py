from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse 
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserPreferenceForm
from .models import UserPreference, CustomUser, Product, Order
from django.shortcuts import render
from tracker.models import Product
from tracker.forms import ProductFilterForm, ProductSortForm
from django.db.models import Avg, Count

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            
            if user_type == 'customer':
                user.is_customer = True
            elif user_type == 'seller':
                user.is_seller = True
            
            user.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    products = Product.objects.all()
    filter_form = ProductFilterForm(request.GET)
    sort_form = ProductSortForm(request.GET)

    if filter_form.is_valid():
        brand = filter_form.cleaned_data.get('brand')
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        rating = filter_form.cleaned_data.get('rating')
        search = filter_form.cleaned_data.get('search')

        if brand:
            products = products.filter(brand=brand)
        if min_price is not None:
            products = products.filter(current_price__gte=min_price)
        if max_price is not None:
            products = products.filter(current_price__lte=max_price)
        if rating:
            products = products.filter(rating__startswith=rating)
        if search:
            products = products.filter(Q(name__icontains=search) | Q(brand__icontains=search))

    if sort_form.is_valid():
        sort_by = sort_form.cleaned_data.get('sort_by')
        if sort_by:
            products = products.order_by(sort_by)

    context = {
        'products': products,
        'filter_form': filter_form,
        'sort_form': sort_form,
    }
    return render(request, 'home.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

from tracker.models import AutoBuy

@login_required
def tracked_items(request):
    tracked_items = AutoBuy.objects.filter(user=request.user)
    return render(request, 'tracked_items.html', {'tracked_items': tracked_items})

from .forms import BalanceForm

@login_required
def add_balance(request):
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.balance += amount
            request.user.save()
            return redirect('profile')
    else:
        form = BalanceForm()
    return render(request, 'add_balance.html', {'form': form})

@login_required
def edit_preferences(request):
    try:
        preferences = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        preferences = None

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preferences)
        if form.is_valid():
            data = form.cleaned_data
            if preferences:
                preferences.price_min = data.get('price_min')
                preferences.price_max = data.get('price_max')
                preferences.product_type = data.get('product_type')
                preferences.brand = data.get('brand')
                preferences.keywords = data.get('keywords')
                preferences.save()
            else:
                UserPreference.objects.create(
                    user=request.user,
                    price_min=data.get('price_min'),
                    price_max=data.get('price_max'),
                    product_type=data.get('product_type'),
                    brand=data.get('brand'),
                    keywords=data.get('keywords')
                )
            return redirect('view_preferences')
    else:
        form = UserPreferenceForm(instance=preferences)
    return render(request, 'edit_preferences.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
    
    customers_count = CustomUser.objects.filter(is_customer=True).count()
    sellers_count = CustomUser.objects.filter(is_seller=True).count()
    products_count = Product.objects.count()
    orders_count = Order.objects.count()
    
    context = {
        'customers_count': customers_count,
        'sellers_count': sellers_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def get_customer_seller_trend(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    customers_count = CustomUser.objects.filter(is_customer=True).count()
    sellers_count = CustomUser.objects.filter(is_seller=True).count()
    
    data = {
        'customers_count': customers_count,
        'sellers_count': sellers_count,
    }
    
    return JsonResponse(data)

@login_required
def manage_products(request):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
    
    if request.method == 'POST':
        # Handle product addition or deletion
        pass
    
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'manage_products.html', context)

@login_required
def manage_users(request):
    if not request.user.is_staff:
        return render(request, '403.html', status=403)
    
    customers = CustomUser.objects.filter(is_customer=True)
    sellers = CustomUser.objects.filter(is_seller=True)
    
    context = {
        'customers': customers,
        'sellers': sellers,
    }
    return render(request, 'manage_users.html', context)

@login_required
def cancel_auto_buy(request, auto_buy_id):
    auto_buy = AutoBuy.objects.get(id=auto_buy_id, user=request.user)
    auto_buy.delete()

      
    return redirect('tracked_items')


@login_required
def view_preferences(request):
    try:
        preferences = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        preferences = None

    context = {
        'preferences': preferences,
    }
    return render(request, 'view_preferences.html', context)


@login_required
def product_reports(request):
    if not request.user.is_seller:
        return redirect('home')  # Redirect non-sellers away from this page

    # Fetch all AutoBuy orders
    autobuy_orders = AutoBuy.objects.all()

    # Calculate average target prices and count of customers for each product
    product_aggregates = AutoBuy.objects.values('product__name', 'product__id').annotate(
        avg_target_price=Avg('target_price'),
        customer_count=Count('user', distinct=True)
    )

    context = {
        'autobuy_orders': autobuy_orders,
        'product_aggregates': product_aggregates
    }

    return render(request, 'product_reports.html', context)
