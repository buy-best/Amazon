# report/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('list/', views.complaint_list, name='complaint_list'),
    path('resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path('product/<int:product_id>/', views.product_complaints, name='product_complaints'),
]