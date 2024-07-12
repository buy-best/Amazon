from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('start_scraping/', views.start_scraping, name='start_scraping'),
    path('clear_scrapes/', views.clear_scrapes, name='clear_scrapes'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
]