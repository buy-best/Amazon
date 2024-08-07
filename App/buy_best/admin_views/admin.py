from django.contrib import admin
from django.shortcuts import render
from users.models import CustomUser, Product, Order

class AdminAnalyticsView(admin.ModelAdmin):
    change_list_template = "admin/analytics.html"

    def changelist_view(self, request, extra_context=None):
        customers_count = CustomUser.objects.filter(is_customer=True).count()
        sellers_count = CustomUser.objects.filter(is_seller=True).count()
        products_count = Product.objects.count()
        orders_count = Order.objects.count()
        
        extra_context = extra_context or {}
        extra_context['customers_count'] = customers_count
        extra_context['sellers_count'] = sellers_count
        extra_context['products_count'] = products_count
        extra_context['orders_count'] = orders_count
        
        return super().changelist_view(request, extra_context=extra_context)