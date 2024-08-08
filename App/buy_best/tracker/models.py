from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, default='Unknown')
    url = models.URLField(unique=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    rating = models.CharField(max_length=10, default='N/A')
    review_count = models.CharField(max_length=20, default='N/A')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

class AutoBuy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='auto_buys')
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    bought = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line for timestamps
    def __str__(self):
        return f'{self.user.username} - {self.product.name} - ${self.target_price}'