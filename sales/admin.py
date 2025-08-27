from django.contrib import admin
from .models import Customer, SalesOrder, SalesOrderItem, Payment, Shipment, Invoice


# ---------------- Customer ----------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "city", "country", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone", "city", "country")
    list_filter = ("country", "city", "created_at")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("first_name", "last_name", "email")}


# ---------------- SalesOrder ----------------
class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total_amount", "order_date", "created_by")
    search_fields = ("id", "customer__first_name", "customer__last_name", "customer__email")
    list_filter = ("status", "order_date")
    ordering = ("-order_date",)
    prepopulated_fields = {"slug": ("id",)}
    inlines = [SalesOrderItemInline]


# ---------------- SalesOrderItem ----------------
@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "subtotal")
    search_fields = ("order__id", "product__name")
    list_filter = ("order__status",)
    ordering = ("-order__order_date",)


# ---------------- Payment ----------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "order", "amount", "method", "payment_date")
    search_fields = ("transaction_id", "order__id", "order__customer__email")
    list_filter = ("method", "payment_date")
    ordering = ("-payment_date",)
    prepopulated_fields = {"slug": ("transaction_id",)}


# ---------------- Shipment ----------------
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("tracking_number", "order", "warehouse", "carrier", "status", "shipped_date", "delivered_date")
    search_fields = ("tracking_number", "order__id", "carrier")
    list_filter = ("status", "warehouse", "carrier")
    ordering = ("-shipped_date",)


# ---------------- Invoice ----------------
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("order", "invoice_date", "total_amount", "due_date", "is_paid")
    search_fields = ("order__id", "order__customer__email")
    list_filter = ("is_paid", "invoice_date")
    ordering = ("-invoice_date",)
    prepopulated_fields = {"slug": ("order",)}
