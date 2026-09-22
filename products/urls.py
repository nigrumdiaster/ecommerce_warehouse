from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('recent/', views.recent_dashboard_view, name='recent_dashboard'),
    path('view/<int:product_id>/', views.product_detail_mock, name='product_detail'),
]