# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from scraper.models import Shoe
from .models import PriceAlert

@receiver(post_save, sender=Shoe)
def check_price_drop(sender, instance, **kwargs):
    alerts = PriceAlert.objects.filter(shoe=instance, is_active=True, target_price__gte=instance.price)
    for alert in alerts:
        send_price_drop_notification(alert)
        alert.is_active = False
        alert.save()

def send_price_drop_notification(alert):
    subject = f"Price Drop Alert: {alert.shoe.title}"
    message = f"The price of {alert.shoe.title} has dropped to ${alert.shoe.price}. " \
              f"Your target price was ${alert.target_price}."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [alert.user.email]
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Email sent to {alert.user.email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")