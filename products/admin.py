from django.contrib import admin
from .models import Category, Product, ProductViewHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'cost_price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description')
    list_editable = ('price', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductViewHistory)
class ProductViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'session_key', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('product__name', 'user__username', 'session_key')
