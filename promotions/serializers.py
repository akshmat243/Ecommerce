from rest_framework import serializers
from .models import Coupon, GiftCard, Promotion
from catalog.serializers import ProductSerializer


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("id", "slug", "used_count", "created_at", "updated_at")

    def validate(self, data):
        """ Ensure coupon validity """
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("End date must be after start date.")
        if data.get("usage_limit") is not None and data["usage_limit"] < data["used_count"]:
            raise serializers.ValidationError("Usage limit cannot be less than used count.")
        return data


class GiftCardSerializer(serializers.ModelSerializer):
    issued_to_email = serializers.EmailField(source="issued_to.email", read_only=True)

    class Meta:
        model = GiftCard
        fields = "__all__"
        read_only_fields = ("id", "slug", "balance", "created_at", "updated_at")

    def validate(self, data):
        """ Ensure gift card validity """
        if data.get("expiry_date") and data["expiry_date"] <= data["created_at"]:
            raise serializers.ValidationError("Expiry date must be in the future.")
        if data.get("balance") is not None and data["balance"] < 0:
            raise serializers.ValidationError("Balance cannot be negative.")
        return data


class PromotionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def validate(self, data):
        """ Ensure promotion validity """
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("End date must be after start date.")
        return data
