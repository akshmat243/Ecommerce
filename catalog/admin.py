from django.contrib import admin
from .models import (
    Category, Brand, Attribute, AttributeValue,
    Product, ProductAttribute, Variant, VariantAttribute,
    ProductMedia, BundleItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_active", "created_at")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "website", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("is_active",)
    ordering = ("name",)


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "type", "is_variant_axis", "is_filterable", "ordering")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AttributeValueInline]


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value", "numeric_value", "bool_value", "hex_code", "ordering")
    list_filter = ("attribute",)
    search_fields = ("value", "hex_code")


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class VariantAttributeInline(admin.TabularInline):
    model = VariantAttribute
    extra = 1


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1


class BundleItemInline(admin.TabularInline):
    model = BundleItem
    fk_name = "bundle"
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sku", "type", "status", "category", "brand", "is_active", "created_at")
    search_fields = ("name", "slug", "sku")
    list_filter = ("status", "type", "category", "brand", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductAttributeInline, VariantInline, ProductMediaInline, BundleItemInline]


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "name", "price", "stock_status", "is_active", "created_at")
    search_fields = ("sku", "product__name", "name")
    list_filter = ("is_active",)
    inlines = [VariantAttributeInline]

    def stock_status(self, obj):
        return "Active" if obj.is_active else "Inactive"


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_primary", "position", "created_at")
    list_filter = ("is_primary",)
    search_fields = ("alt_text",)


@admin.register(BundleItem)
class BundleItemAdmin(admin.ModelAdmin):
    list_display = ("bundle", "child_product", "quantity")
    list_filter = ("bundle", "child_product")
