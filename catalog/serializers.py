from rest_framework import serializers
from .models import (
    Attribute, AttributeValue, ProductAttribute, 
    Variant, VariantAttribute, BundleItem, Product, Category, Brand
)


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="parent", write_only=True, required=False
    )

    class Meta:
        model = Category
        fields = [
            "id", "name", "slug", "description",
            "parent", "parent_id", "image",
            "is_active", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id", "name", "slug", "logo", "description",
            "website", "is_active", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


# ------------------ Attribute ------------------
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name', 'slug', 'type', 'is_variant_axis', 'is_filterable', 'ordering']
        read_only_fields = ['id', 'slug']

    def validate_name(self, value):
        qs = Attribute.objects.exclude(id=self.instance.id) if self.instance else Attribute.objects.all()
        if qs.filter(name=value).exists():
            raise serializers.ValidationError("An attribute with this name already exists.")
        return value


# ------------------ AttributeValue ------------------
class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    attribute_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = AttributeValue
        fields = ['id', 'value', 'slug', 'attribute', 'attribute_slug']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        slug = validated_data.pop('attribute_slug')
        try:
            attribute = Attribute.objects.get(slug=slug)
        except Attribute.DoesNotExist:
            raise serializers.ValidationError({'attribute_slug': 'Invalid attribute slug.'})
        validated_data['attribute'] = attribute
        return super().create(validated_data)

    def update(self, instance, validated_data):
        slug = validated_data.pop('attribute_slug', None)
        if slug:
            try:
                attribute = Attribute.objects.get(slug=slug)
                validated_data['attribute'] = attribute
            except Attribute.DoesNotExist:
                raise serializers.ValidationError({'attribute_slug': 'Invalid attribute slug.'})
        return super().update(instance, validated_data)


# ------------------ ProductAttribute ------------------
class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    attribute_slug = serializers.SlugField(write_only=True)
    product_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['id', 'product_slug', 'attribute', 'attribute_slug']
        read_only_fields = ['id']

    def create(self, validated_data):
        attr_slug = validated_data.pop('attribute_slug')
        prod_slug = validated_data.pop('product_slug')
        try:
            attribute = Attribute.objects.get(slug=attr_slug)
        except Attribute.DoesNotExist:
            raise serializers.ValidationError({'attribute_slug': 'Invalid attribute slug.'})

        try:
            product = Product.objects.get(slug=prod_slug)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})

        validated_data['attribute'] = attribute
        validated_data['product'] = product
        return super().create(validated_data)

    def update(self, instance, validated_data):
        attr_slug = validated_data.pop('attribute_slug', None)
        prod_slug = validated_data.pop('product_slug', None)

        if attr_slug:
            try:
                validated_data['attribute'] = Attribute.objects.get(slug=attr_slug)
            except Attribute.DoesNotExist:
                raise serializers.ValidationError({'attribute_slug': 'Invalid attribute slug.'})

        if prod_slug:
            try:
                validated_data['product'] = Product.objects.get(slug=prod_slug)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})

        return super().update(instance, validated_data)


# ------------------ Variant ------------------
class VariantSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Variant
        fields = ['id', 'name', 'slug', 'sku', 'price', 'product']
        read_only_fields = ['id', 'slug']


# ------------------ VariantAttribute ------------------
class VariantAttributeSerializer(serializers.ModelSerializer):
    variant = VariantSerializer(read_only=True)
    variant_slug = serializers.SlugField(write_only=True)

    attribute_value = AttributeValueSerializer(read_only=True)
    attribute_value_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = VariantAttribute
        fields = ['id', 'variant', 'variant_slug', 'attribute_value', 'attribute_value_slug']
        read_only_fields = ['id']

    def create(self, validated_data):
        variant_slug = validated_data.pop('variant_slug')
        attr_value_slug = validated_data.pop('attribute_value_slug')

        try:
            variant = Variant.objects.get(slug=variant_slug)
        except Variant.DoesNotExist:
            raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})

        try:
            attribute_value = AttributeValue.objects.get(slug=attr_value_slug)
        except AttributeValue.DoesNotExist:
            raise serializers.ValidationError({'attribute_value_slug': 'Invalid attribute value slug.'})

        validated_data['variant'] = variant
        validated_data['attribute_value'] = attribute_value
        return super().create(validated_data)

    def update(self, instance, validated_data):
        variant_slug = validated_data.pop('variant_slug', None)
        attr_value_slug = validated_data.pop('attribute_value_slug', None)

        if variant_slug:
            try:
                validated_data['variant'] = Variant.objects.get(slug=variant_slug)
            except Variant.DoesNotExist:
                raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})

        if attr_value_slug:
            try:
                validated_data['attribute_value'] = AttributeValue.objects.get(slug=attr_value_slug)
            except AttributeValue.DoesNotExist:
                raise serializers.ValidationError({'attribute_value_slug': 'Invalid attribute value slug.'})

        return super().update(instance, validated_data)


# ------------------ BundleItem ------------------
class BundleItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='slug')
    bundle = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='slug')

    class Meta:
        model = BundleItem
        fields = ['id', 'bundle', 'product', 'quantity']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True, required=False
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source="brand", write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "sku", "type",
            "category", "category_id", "brand", "brand_id",
            "short_description", "description", "status",
            "weight_grams", "dimensions", "country_of_origin",
            "is_returnable", "is_cod_allowed",
            "seo_title", "seo_description", "metadata",
            "is_active", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    # -------------------
    # Custom Validations
    # -------------------

    def validate_name(self, value):
        """Ensure product name length and no duplicates with same category"""
        if len(value) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        return value

    def validate_sku(self, value):
        """SKU should be unique and uppercase"""
        if value and not value.isupper():
            raise serializers.ValidationError("SKU must be uppercase.")
        return value

    def validate_weight_grams(self, value):
        if value and value <= 0:
            raise serializers.ValidationError("Weight must be a positive number.")
        return value

    def validate_country_of_origin(self, value):
        """ISO2 country code should be exactly 2 characters"""
        if value and len(value) != 2:
            raise serializers.ValidationError("Country code must be a 2-letter ISO2 code.")
        return value

    def validate(self, data):
        """Cross-field validation"""
        if data.get("status") == Product.STATUS_PUBLISHED and not data.get("category"):
            raise serializers.ValidationError("Published products must have a category assigned.")
        return data