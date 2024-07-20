from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from tracker.models import Product
from tracker.forms import ProductFilterForm, ProductSortForm

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
def cancel_auto_buy(request, auto_buy_id):
    auto_buy = AutoBuy.objects.get(id=auto_buy_id, user=request.user)
    auto_buy.delete()

      
    return redirect('tracked_items')
