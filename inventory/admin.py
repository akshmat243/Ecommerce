from django.contrib import admin
from .models import Warehouse, Stock, ProductPrice, StockTransaction

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'city', 'state', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'country', 'state']
    search_fields = ['name', 'city', 'state', 'country']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant', 'warehouse', 'quantity', 'reserved_quantity', 'min_quantity', 'max_quantity', 'slug', 'is_active']
    list_filter = ['warehouse', 'is_active']
    search_fields = ['product__name', 'variant__name', 'warehouse__name']
    ordering = ['product']
    readonly_fields = ['slug']

@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant', 'warehouse', 'price', 'compare_at_price', 'cost_price', 'currency', 'slug', 'is_active']
    list_filter = ['warehouse', 'currency', 'is_active']
    search_fields = ['product__name', 'variant__name', 'warehouse__name']
    ordering = ['product']
    readonly_fields = ['slug']

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['stock', 'type', 'quantity', 'reference', 'slug', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['stock__product__name', 'stock__variant__name', 'reference']
    ordering = ['-created_at']
    readonly_fields = ['slug']
