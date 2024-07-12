from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tracker.models import Product  # Update this import
from .models import PriceAlert
from .forms import PriceAlertForm

@login_required
def add_price_alert(request, product_id):  # Change shoe_id to product_id
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already has an alert for this product
    existing_alert = PriceAlert.objects.filter(user=request.user, product=product, is_active=True).first()
    
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
                alert.product = product
                alert.save()
                messages.success(request, 'Price alert created successfully!')
            return redirect('/tracker')  # Update this URL to match your product list URL
    else:
        initial_price = existing_alert.target_price if existing_alert else product.current_price
        form = PriceAlertForm(initial={'target_price': initial_price})
    
    context = {
        'form': form,
        'product': product,
        'existing_alert': existing_alert
    }
    return render(request, 'notifications/add_price_alert.html', context)