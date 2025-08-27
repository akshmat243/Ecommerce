from django.contrib import admin
from .models import (
    ProductReview,
    ReviewComment,
    ProductQuestion,
    ProductAnswer,
    ContentEngagement,
)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "title",
        "is_verified_purchase",
        "is_approved",
        "likes",
        "dislikes",
        "created_at",
    )
    list_filter = ("is_verified_purchase", "is_approved", "rating", "created_at")
    search_fields = ("product__name", "user__email", "title", "content")
    readonly_fields = ("created_at", "updated_at", "likes", "dislikes")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ("review", "user", "content", "created_at")
    search_fields = ("review__product__name", "user__email", "content")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "question", "is_answered", "created_at")
    list_filter = ("is_answered", "created_at")
    search_fields = ("product__name", "user__email", "question")
    readonly_fields = ("created_at",)


@admin.register(ProductAnswer)
class ProductAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "user", "answer", "is_accepted", "created_at")
    list_filter = ("is_accepted", "created_at")
    search_fields = ("question__question", "user__email", "answer")
    readonly_fields = ("created_at",)


@admin.register(ContentEngagement)
class ContentEngagementAdmin(admin.ModelAdmin):
    list_display = ("user", "engagement_type", "review", "comment", "answer", "created_at")
    list_filter = ("engagement_type", "created_at")
    search_fields = ("user__email",)
    readonly_fields = ("created_at",)
