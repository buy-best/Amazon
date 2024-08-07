# report/models.py

from django.db import models
from tracker.models import Product

class Complaint(models.Model):
    COMPLAINT_TYPES = [
        ('quality', 'Quality Issue'),
        ('pricing', 'Pricing Issue'),
        ('delivery', 'Delivery Problem'),
        ('description', 'Incorrect Description'),
        ('other', 'Other'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Complaint for {self.product.name} - {self.get_complaint_type_display()}"