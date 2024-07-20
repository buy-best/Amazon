from django.test import TestCase
from django.contrib.auth import get_user_model
from scraper.models import Shoe
from notifications.models import PriceAlert
from notifications.signals import check_price_drop, send_price_drop_notification
from decimal import Decimal
from django.core import mail
from django.core.mail import send_mail
from django.conf import settings



User = get_user_model()

class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='barsyayc@gmail.com', password='testpass')
        self.shoe = Shoe.objects.create(title='Test Shoe', price=Decimal('100.00'), image='http://example.com/shoe.jpg')
        self.alert = PriceAlert.objects.create(user=self.user, shoe=self.shoe, target_price=Decimal('90.00'))

    def test_price_drop_notification(self):
        self.shoe.update_price(Decimal('85.00'))
    
    def test_no_notification_for_higher_price(self):
        # Simulate a price increase
        self.shoe.update_price(Decimal('110.00'))
        
        # Check that no email was sent
        self.assertEqual(len(mail.outbox), 0)

    def test_alert_deactivation(self):
        self.shoe.update_price(Decimal('85.00'))
        
        # Check if the alert was deactivated
        self.alert.refresh_from_db()
        self.assertFalse(self.alert.is_active)

class EmailTestCase(TestCase):
    def test_send_email(self):
        try:
            send_mail(
                'Test Subject',
                'Test content',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print("Email sent successfully in test")
        except Exception as e:
            print(f"Failed to send email in test: {e}")

        self.assertEqual(len(mail.outbox), 1)
        print(f"mail.outbox contents: {mail.outbox}")

