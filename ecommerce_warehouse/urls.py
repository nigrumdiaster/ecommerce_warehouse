"""
URL configuration for ecommerce_warehouse project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from products.views import recent_dashboard_view

urlpatterns = [
    # Dashboard Trang chủ
    path('', recent_dashboard_view, name='home_dashboard'),

    path('admin/', admin.site.urls),

    # Product
    path('product/', include('products.urls')),

    # Inventory
    path('inventory/', include('inventory.urls')),

    # Orders (Hàng đợi ưu tiên MC2)
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )