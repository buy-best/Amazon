from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Shoe(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()

    def __str__(self):
        return self.title

    def update_price(self, new_price):
        if self.price != new_price:
            old_price = self.price
            self.price = new_price
            self.save()
            return old_price
        return None

