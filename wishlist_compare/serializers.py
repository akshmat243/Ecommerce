from rest_framework import serializers
from .models import Wishlist, WishlistItem, CompareList, CompareItem
from catalog.models import Product


class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = WishlistItem
        fields = ["id", "product", "product_name", "added_at"]
        read_only_fields = ["id", "added_at"]

    def validate(self, attrs):
        wishlist = self.context["wishlist"]
        product = attrs.get("product")
        if WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
            raise serializers.ValidationError("This product is already in the wishlist.")
        return attrs


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "name", "slug", "is_public", "created_at", "updated_at", "items"]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Wishlist.objects.create(user=user, **validated_data)


class CompareItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = CompareItem
        fields = ["id", "product", "product_name", "added_at"]
        read_only_fields = ["id", "added_at"]

    def validate(self, attrs):
        compare_list = self.context["compare_list"]
        product = attrs.get("product")
        if CompareItem.objects.filter(compare_list=compare_list, product=product).exists():
            raise serializers.ValidationError("This product is already in the compare list.")
        return attrs


class CompareListSerializer(serializers.ModelSerializer):
    items = CompareItemSerializer(many=True, read_only=True)

    class Meta:
        model = CompareList
        fields = ["id", "slug", "created_at", "items"]
        read_only_fields = ["id", "slug", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        # Ensure each user has only one CompareList
        compare_list, _ = CompareList.objects.get_or_create(user=user)
        return compare_list
