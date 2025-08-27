from django.contrib import admin
from .models import Wishlist, WishlistItem, CompareList, CompareItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 1
    autocomplete_fields = ["product"]
    readonly_fields = ("added_at",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "is_public", "created_at", "updated_at")
    search_fields = ("name", "user__email")
    list_filter = ("is_public", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [WishlistItemInline]


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("wishlist", "product", "added_at")
    search_fields = ("wishlist__name", "wishlist__user__email", "product__name")
    list_filter = ("added_at",)


class CompareItemInline(admin.TabularInline):
    model = CompareItem
    extra = 1
    autocomplete_fields = ["product"]
    readonly_fields = ("added_at",)


@admin.register(CompareList)
class CompareListAdmin(admin.ModelAdmin):
    list_display = ("user", "slug", "created_at")
    search_fields = ("user__email",)
    inlines = [CompareItemInline]


@admin.register(CompareItem)
class CompareItemAdmin(admin.ModelAdmin):
    list_display = ("compare_list", "product", "added_at")
    search_fields = ("compare_list__user__email", "product__name")
    list_filter = ("added_at",)
