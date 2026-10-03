from django.urls import path
from . import views

urlpatterns = [
    # Giao diện hàng đợi ưu tiên
    path('', views.order_queue_view, name='order_queue'),

    # Bốc đơn hàng tiếp theo (pop_max)
    path('process-next/', views.process_next_order_view, name='process_next_order'),

    # Tạo đơn hàng test
    path('create-mock/', views.create_mock_order_view, name='create_mock_order'),

    # Đồng bộ lại Heap từ DB
    path('reload-queue/', views.reload_queue_view, name='reload_order_queue'),
]
