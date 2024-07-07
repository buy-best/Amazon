from django.db import models

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