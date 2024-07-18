# reports/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .services import ComplaintService
from .forms import ComplaintForm
from tracker.models import Product
from .models import Complaint


def submit_complaint(request):
    initial_data = {}
    if 'product' in request.GET:
        try:
            product = Product.objects.get(id=request.GET['product'])
            initial_data['product'] = product
        except Product.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save()
            return redirect('/tracker')
    else:
        form = ComplaintForm(initial=initial_data)

    return render(request, 'report/submit_complaint.html', {'form': form})


@staff_member_required
def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'report/complaint_list.html', {'complaints': complaints})

@staff_member_required
def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.resolved = True
        complaint.save()
    return redirect('complaint_list')

@staff_member_required
def product_complaints(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    complaints = Complaint.objects.filter(product=product)
    return render(request, 'report/product_complaints.html', {'product': product, 'complaints': complaints})

