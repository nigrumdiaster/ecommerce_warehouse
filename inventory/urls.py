from django.urls import path
from . import views

urlpatterns = [
    path('low-stock/', views.low_stock_view, name='low_stock'),
]