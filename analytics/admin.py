from django.contrib import admin
from .models import SearchQuery, UserActivity, Recommendation


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "result_count", "created_at")
    list_filter = ("created_at",)
    search_fields = ("query", "user__email")
    readonly_fields = ("slug", "created_at")
    ordering = ("-created_at",)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "action", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("user__email", "product__name", "action")
    readonly_fields = ("slug", "created_at")
    ordering = ("-created_at",)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "score", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "product__name")
    readonly_fields = ("slug", "created_at")
    ordering = ("-score", "-created_at")
