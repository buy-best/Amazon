from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserPreferenceForm
from .models import UserPreference
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