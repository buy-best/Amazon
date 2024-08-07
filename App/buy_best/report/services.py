# reports/services.py

from .models import Complaint
from tracker.models import Product
from django.utils import timezone

class ComplaintService:
    @staticmethod
    def create_complaint(product_id, complaint_type, description):
        product = Product.objects.get(id=product_id)
        complaint = Complaint.objects.create(
            product=product,
            complaint_type=complaint_type,
            description=description
        )
        return complaint

    @staticmethod
    def get_complaint(complaint_id):
        return Complaint.objects.get(id=complaint_id)

    @staticmethod
    def get_complaints_for_product(product_id):
        return Complaint.objects.filter(product_id=product_id)

    @staticmethod
    def get_all_complaints():
        return Complaint.objects.all()

    @staticmethod
    def resolve_complaint(complaint_id):
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.resolved = True
        complaint.resolution_date = timezone.now()
        complaint.save()
        return complaint

    @staticmethod
    def get_unresolved_complaints():
        return Complaint.objects.filter(resolved=False)