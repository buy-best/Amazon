from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from scraper.models import Shoe
from .models import PriceAlert
from .forms import PriceAlertForm

@login_required
def add_price_alert(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    
    # Check if user already has an alert for this shoe
    existing_alert = PriceAlert.objects.filter(user=request.user, shoe=shoe, is_active=True).first()
    
    if request.method == 'POST':
        form = PriceAlertForm(request.POST)
        if form.is_valid():
            if existing_alert:
                # Update existing alert
                existing_alert.target_price = form.cleaned_data['target_price']
                existing_alert.is_active = True
                existing_alert.save()
                messages.success(request, 'Price alert updated successfully!')
            else:
                # Create new alert
                alert = form.save(commit=False)
                alert.user = request.user
                alert.shoe = shoe
                alert.save()
                messages.success(request, 'Price alert created successfully!')
            return redirect('/scraper/shoes/')
    else:
        initial_price = existing_alert.target_price if existing_alert else shoe.price
        form = PriceAlertForm(initial={'target_price': initial_price})
    
    context = {
        'form': form,
        'shoe': shoe,
        'existing_alert': existing_alert
    }
    return render(request, 'notifications/add_price_alert.html', context)