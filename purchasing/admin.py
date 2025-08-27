from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseOrderItem, GoodsReceipt

# ---------------- Supplier ----------------
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'country', 'city')
    search_fields = ('name', 'contact_person', 'email', 'phone')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)


# ---------------- Purchase Order ----------------
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'warehouse', 'status', 'order_date', 'expected_delivery_date', 'total_amount')
    list_filter = ('status', 'warehouse', 'supplier', 'order_date')
    search_fields = ('order_number', 'supplier__name', 'warehouse__name')
    prepopulated_fields = {'slug': ('order_number',)}
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    ordering = ('-order_date',)


# ---------------- Purchase Order Item ----------------
@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'product', 'variant', 'quantity', 'unit_price', 'total_price')
    list_filter = ('purchase_order', 'product')
    search_fields = ('product__name', 'variant__sku', 'purchase_order__order_number')
    readonly_fields = ('total_price',)
    ordering = ('purchase_order',)


@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "purchase_order",
        "receipt_date",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "receipt_date", "created_at")
    search_fields = ("slug", "purchase_order__id", "remarks")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("slug", "purchase_order", "receipt_date", "status", "remarks")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
