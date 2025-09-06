from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Payment, Refund, OrderInvoice


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "user", "session_key", "is_active", "created_at", "updated_at")
    search_fields = ("slug", "user__email", "session_key")
    list_filter = ("is_active", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "cart", "product", "variant", "quantity", "price", "total_price", "created_at")
    search_fields = ("slug", "product__name", "cart__slug")
    list_filter = ("created_at", "product")
    readonly_fields = ("total_price", "created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "slug", "user", "status", "total_amount", "discount_amount", "final_amount",
        "payment_status", "payment_method", "tracking_number", "created_at", "updated_at"
    )
    search_fields = ("slug", "user__email", "tracking_number")
    list_filter = ("status", "payment_status", "payment_method", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "order", "product", "quantity", "price", "subtotal", "created_at")
    search_fields = ("slug", "order__slug", "product__name")
    list_filter = ("created_at", "product")
    readonly_fields = ("subtotal", "created_at")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "slug", "order", "user", "amount", "currency", "method", "status",
        "transaction_id", "created_at", "updated_at"
    )
    search_fields = ("slug", "order__slug", "user__email", "transaction_id")
    list_filter = ("method", "status", "currency", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "payment", "amount", "status", "created_at", "updated_at")
    search_fields = ("slug", "payment__order__slug")
    list_filter = ("status", "created_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(OrderInvoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "invoice_number", "order", "amount", "issued_date", "due_date", "created_at")
    search_fields = ("slug", "invoice_number", "order__slug")
    list_filter = ("issued_date", "due_date")
    readonly_fields = ("created_at", "issued_date")
