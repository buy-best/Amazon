import os
import django
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buy_best.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core import mail
from scraper.models import Shoe
from notifications.models import PriceAlert

User = get_user_model()

def run_tests():
    # Setup
    user = User.objects.create_user(username='testuser', email='barsyayc@gmail.com', password='testpass')
    shoe = Shoe.objects.create(title='Test Shoe', price=Decimal('100.00'), image='http://example.com/shoe.jpg')
    alert = PriceAlert.objects.create(user=user, shoe=shoe, target_price=Decimal('90.00'))

    # Test price drop notification
    print("Testing price drop notification...")
    shoe.update_price(Decimal('85.00'))


    # Test no notification for higher price
    print("\nTesting no notification for higher price...")
    shoe.update_price(Decimal('110.00'))


    # Test alert deactivation
    print("\nTesting alert deactivation...")
    shoe.update_price(Decimal('85.00'))
    alert.refresh_from_db()
    if alert.is_active:
        print("Alert is still active, which is unexpected")
    else:
        print("Alert was deactivated as expected")

    # Cleanup
    user.delete()
    shoe.delete()
    alert.delete()

if __name__ == "__main__":
    run_tests()