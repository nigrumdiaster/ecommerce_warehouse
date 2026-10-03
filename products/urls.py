from django.urls import path
from . import views

urlpatterns = [
    # Danh sách sản phẩm
    path('', views.product_list, name='product_list'),

    # Sản phẩm vừa nhập kho / vừa xem
    path(
        'recent/',
        views.recent_dashboard_view,
        name='recent_dashboard'
    ),

    # Chi tiết sản phẩm
    path(
        'view/<int:product_id>/',
        views.product_detail_mock,
        name='product_detail'
    ),

    # Autocomplete tìm kiếm bằng Trie
    path(
        'autocomplete/',
        views.autocomplete_view,
        name='product_autocomplete'
    ),
]