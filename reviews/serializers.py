from rest_framework import serializers
from .models import (
    ProductReview,
    ReviewComment,
    ProductQuestion,
    ProductAnswer,
    ContentEngagement,
)


class ProductReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = ProductReview
        fields = "__all__"
        read_only_fields = ("slug", "created_at", "updated_at", "likes", "dislikes")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        # Ensure unique review per product by user
        user = data.get("user")
        product = data.get("product")
        if self.instance is None and ProductReview.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        return data


class ReviewCommentSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = ReviewComment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ProductQuestionSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = ProductQuestion
        fields = "__all__"
        read_only_fields = ("created_at",)


class ProductAnswerSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = ProductAnswer
        fields = "__all__"
        read_only_fields = ("created_at",)


class ContentEngagementSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = ContentEngagement
        fields = "__all__"
        read_only_fields = ("created_at",)

    def validate(self, data):
        # Ensure engagement is linked to only one object at a time
        targets = [data.get("review"), data.get("comment"), data.get("answer")]
        if sum(1 for t in targets if t) != 1:
            raise serializers.ValidationError("Engagement must be linked to exactly one target (review, comment, or answer).")
        return data
