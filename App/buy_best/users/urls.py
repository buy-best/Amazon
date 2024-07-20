from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('tracked_items/', views.tracked_items, name='tracked_items'),
    path('add_balance/', views.add_balance, name='add_balance'),
    path('cancel_auto_buy/<int:auto_buy_id>/', views.cancel_auto_buy, name='cancel_auto_buy'),

]

