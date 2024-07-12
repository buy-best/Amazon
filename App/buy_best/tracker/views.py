from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, PriceHistory
from .scraper import update_prices
from .forms import ProductForm
from .scraper import scrape_amazon_shoes
from django.shortcuts import render
from django.db.models import Q
from .models import Product
from .forms import ProductFilterForm, ProductSortForm

def product_list(request):
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
    return render(request, 'tracker/product_list.html', context)

def start_scraping(request):
    if request.method == 'POST':
        update_prices()
        messages.success(request, 'Scraping completed successfully!')
    return redirect('product_list')

def clear_scrapes(request):
    if request.method == 'POST':
        Product.objects.all().delete()
        PriceHistory.objects.all().delete()
        messages.success(request, 'All scrape data has been cleared!')
    return redirect('product_list')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    price_history = product.price_history.all()
    return render(request, 'tracker/product_detail.html', {'product': product, 'price_history': price_history})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            # Scrape initial data
            shoes = scrape_amazon_shoes()
            for shoe in shoes:
                if shoe['url'] == product.url:
                    product.current_price = Decimal(shoe['price'].replace('$', '').replace(',', ''))
                    product.image_url = shoe['image']
                    product.brand = shoe['brand']
                    product.color = shoe['color']
                    product.rating = shoe['rating']
                    product.review_count = shoe['review_count']
                    break
            else:
                # If the product is not found in the scrape results, set default values
                product.current_price = Decimal('0.00')
                product.brand = 'Unknown'
                product.color = 'Various'
                product.rating = 'N/A'
                product.review_count = 'N/A'
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'tracker/add_product.html', {'form': form})

