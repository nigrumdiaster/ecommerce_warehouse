from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('autocomplete/', views.autocomplete_view, name='product_autocomplete'),]
