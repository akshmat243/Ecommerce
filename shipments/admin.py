from django.contrib import admin
from .models import ShippingMethod, Shipment, ShippingAddress


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "base_cost", "additional_cost_per_kg", "estimated_delivery_days", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("estimated_delivery_days", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("order", "shipping_method", "tracking_number", "status", "shipped_at", "delivered_at", "created_at")
    list_filter = ("status", "shipping_method", "created_at")
    search_fields = ("tracking_number", "order__id")
    ordering = ("-created_at",)
    autocomplete_fields = ("order", "shipping_method")


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "city", "state", "country", "postal_code", "is_default", "created_at")
    search_fields = ("full_name", "user__email", "city", "state", "country")
    list_filter = ("country", "state", "is_default", "created_at")
    ordering = ("-created_at",)
    autocomplete_fields = ("user",)
