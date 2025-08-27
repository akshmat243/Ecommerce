from django.contrib import admin
from .models import Coupon, GiftCard, Promotion


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code", "discount_type", "discount_value", 
        "min_order_value", "max_discount_amount",
        "start_date", "end_date", "is_active", "used_count"
    )
    list_filter = ("discount_type", "is_active", "start_date", "end_date")
    search_fields = ("code",)
    prepopulated_fields = {"slug": ("code",)}
    ordering = ("-created_at",)


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = (
        "code", "initial_balance", "balance", "issued_to",
        "status", "expiry_date", "created_at"
    )
    list_filter = ("status", "expiry_date", "created_at")
    search_fields = ("code", "issued_to__email", "issued_to__username")
    prepopulated_fields = {"slug": ("code",)}
    ordering = ("-created_at",)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "name", "discount_type", "discount_value",
        "start_date", "end_date", "is_active", "created_at"
    )
    list_filter = ("discount_type", "is_active", "start_date", "end_date")
    search_fields = ("name", "description")
    filter_horizontal = ("products",)  # Nice UI for selecting products
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
