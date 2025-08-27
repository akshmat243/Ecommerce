from rest_framework import serializers
from .models import SearchQuery, UserActivity, Recommendation


class SearchQuerySerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email", default=None)

    class Meta:
        model = SearchQuery
        fields = [
            "id", "slug", "query", "user", "user_email",
            "result_count", "created_at"
        ]
        read_only_fields = ("slug", "created_at")

    def validate_query(self, value):
        if not value.strip():
            raise serializers.ValidationError("Query cannot be empty.")
        return value


class UserActivitySerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email", default=None)
    product_name = serializers.ReadOnlyField(source="product.name", default=None)

    class Meta:
        model = UserActivity
        fields = [
            "id", "slug", "user", "user_email", "product", "product_name",
            "action", "created_at"
        ]
        read_only_fields = ("slug", "created_at")

    def validate_action(self, value):
        valid_actions = dict(UserActivity.ACTION_CHOICES).keys()
        if value not in valid_actions:
            raise serializers.ValidationError(f"Invalid action. Must be one of {valid_actions}.")
        return value


class RecommendationSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email", default=None)
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = Recommendation
        fields = [
            "id", "slug", "user", "user_email", "product", "product_name",
            "score", "created_at"
        ]
        read_only_fields = ("slug", "created_at")

    def validate_score(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError("Score must be between 0.0 and 1.0")
        return value
