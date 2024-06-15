from django.urls import path
from . import views

urlpatterns = [
    path('shoes/', views.show_shoes, name='show_shoes'),
]
