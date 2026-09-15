from django.contrib import admin
from .models import Supplier, Stock, StockReceipt, StockReceiptItem


class StockReceiptItemInline(admin.TabularInline):
    model = StockReceiptItem
    extra = 1


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'contact_email', 'created_at')
    search_fields = ('name', 'phone', 'contact_email')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'min_threshold', 'updated_at')
    list_editable = ('quantity', 'min_threshold')
    search_fields = ('product__name', 'product__sku')


@admin.register(StockReceipt)
class StockReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_code', 'supplier', 'status', 'received_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('receipt_code', 'supplier__name')
    inlines = (StockReceiptItemInline,)
