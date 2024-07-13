from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse 
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserPreferenceForm
from .models import UserPreference, CustomUser, Product, Order

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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
    return render(request, 'home.html')

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

@login_required
def view_preferences(request):
    try:
        preferences = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        preferences = None

    return render(request, 'view_preferences.html', {'preferences': preferences})

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