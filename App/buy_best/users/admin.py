from django.contrib import admin
from .models import CustomUser, Product, Order
from admin_views.admin import AdminAnalyticsView  # Import the custom admin view

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_customer', 'is_seller')
    list_filter = ('is_customer', 'is_seller')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'seller', 'created_at')
    search_fields = ('name', 'seller__username')

class OrderAdmin(AdminAnalyticsView):  # Use the custom admin view
    list_display = ('product', 'customer', 'quantity', 'order_date')
    search_fields = ('product__name', 'customer__username')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)