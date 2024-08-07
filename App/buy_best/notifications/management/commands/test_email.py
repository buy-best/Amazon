# notifications/management/commands/test_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Test email functionality'

    def handle(self, *args, **options):
        send_mail(
            'Test Email',
            'This is a test email from Django.',
            'barsyayc@gmail.com',
            ['barsyayc@gmail.com'],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Test email sent successfully'))