from django.urls import path
from . import views

urlpatterns = [
    path('add-price-alert/<int:shoe_id>/', views.add_price_alert, name='add_price_alert'),
]