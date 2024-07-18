from django.db import models
from django.conf import settings
from tracker.models import Product  # Update this import

class PriceAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)  # Add null=True
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Product"
        return f"Alert for {product_name} - Target: {self.target_price}"  # Note the closing parenthesis here
