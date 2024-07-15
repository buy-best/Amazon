from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
import json

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard view
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'buyer/enterBuyer.html')

def register_view(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'buyer/registerBuyer.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'buyer/registerBuyer.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'buyer/registerBuyer.html')

        if Profile.objects.filter(phone_number=phone_number).exists():  # Check for existing phone number
            messages.error(request, 'Telephone number already registered')
            return render(request, 'buyer/registerBuyer.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)
        return redirect('dashboard')  # Redirect to the dashboard view

    return render(request, 'buyer/registerBuyer.html')

@login_required  # Ensure the user is logged in to access the dashboard
def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'buyer/dashboard.html', {'profile': profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if request.user.check_password(current_password):
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Incorrect current password.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})
