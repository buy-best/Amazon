from django.shortcuts import render
from .models import Shoe
from .scraper import scrape_amazon_shoes

def show_shoes(request):
    if not Shoe.objects.exists():
        shoe_data = scrape_amazon_shoes()
        for shoe in shoe_data:
            Shoe.objects.create(title=shoe['title'], price=shoe['price'], image=shoe['image'])
    shoes = Shoe.objects.all()
    return render(request, 'scraper/shoes.html', {'shoes': shoes})
