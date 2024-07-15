from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Default route for login
    path('loginBuyer/', views.login_view, name='loginBuyer'),
    path('registerBuyer/', views.register_view, name='registerBuyer'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Add this line for the dashboard view
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Add this line for logout
    path('change-password/', views.change_password, name='change_password'),
]
