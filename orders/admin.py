from django.contrib import admin
from .models import Order, OrderItem, OrderProcessingLog


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


class OrderProcessingLogInline(admin.TabularInline):
    model = OrderProcessingLog
    extra = 0
    readonly_fields = ('timestamp',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_code',
        'customer_name',
        'customer_phone',
        'priority',
        'is_urgent',
        'status',
        'total_amount',
        'created_at'
    )
    list_filter = ('priority', 'is_urgent', 'status', 'created_at')
    search_fields = ('order_code', 'customer_name', 'customer_phone', 'customer_email')
    list_editable = ('status', 'priority', 'is_urgent')
    inlines = [OrderItemInline, OrderProcessingLogInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'subtotal')
    search_fields = ('order__order_code', 'product__name')


@admin.register(OrderProcessingLog)
class OrderProcessingLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'action', 'performed_by', 'timestamp')
    search_fields = ('order__order_code', 'action')
